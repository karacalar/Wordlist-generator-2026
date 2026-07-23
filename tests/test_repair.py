import json, threading, time, pytest
from combination_studio.models.character_set import CharacterSetSpec
from combination_studio.models.generation_settings import GenerationSettings, OutputSettings, FilterSettings
from combination_studio.models.enums import GenerationMode
from combination_studio.generation.estimator import estimate_uniform, estimate_positions
from combination_studio.generation.index_converter import index_to_combination
from combination_studio.generation.preview import preview_values, theoretical_total
from combination_studio.jobs.worker import GenerationWorker

def test_digits_length5_exact_sequence_and_total():
    assert estimate_uniform(10,5).total == 100000
    assert index_to_combination(0,'0123456789',5) == '00000'
    assert index_to_combination(1,'0123456789',5) == '00001'
    assert index_to_combination(99999,'0123456789',5) == '99999'

def test_digits_plus_hex_lower_dedup_and_count():
    cs=CharacterSetSpec(['digits','hex_lower']).build()
    assert cs == '0123456789abcdef'
    assert estimate_uniform(len(cs),5).total == 1048576

def test_prefix_suffix_two_digit_output(tmp_path):
    s=GenerationSettings(mode=GenerationMode.PREFIX_SUFFIX,charset=CharacterSetSpec(['digits']),exact_length=2,prefixes=['TEST-'],suffixes=['-TR'],max_records=100,output=OutputSettings(directory=tmp_path,base_name='pref'))
    r=GenerationWorker(s).run(); lines=(tmp_path/'pref_0001.txt').read_text().splitlines()
    assert lines[0]=='TEST-00-TR'; assert lines[-1]=='TEST-99-TR'; assert r['records']==100

def test_position_pattern_count_first_final():
    sets=['ABCDEFGHIJKLMNOPQRSTUVWXYZ','ABCDEFGHIJKLMNOPQRSTUVWXYZ','0123456789','0123456789']
    assert estimate_positions(sets).total == 26*26*10*10
    assert index_to_combination(0, sets[0], 2) == 'AA'
    vals=preview_values(GenerationSettings(mode=GenerationMode.PATTERN,position_sets=sets),limit=1,final=True)
    assert vals == ['ZZ99']

def test_preview_is_limited():
    s=GenerationSettings(mode=GenerationMode.FIXED,charset=CharacterSetSpec(['digits']),exact_length=5)
    vals=preview_values(s,limit=100)
    assert len(vals)==100 and vals[:4]==['00000','00001','00002','00003']

def test_stop_creates_valid_partial_output(tmp_path):
    s=GenerationSettings(mode=GenerationMode.FIXED,charset=CharacterSetSpec(['digits']),exact_length=5,max_records=100000,output=OutputSettings(directory=tmp_path,base_name='stop'))
    w=GenerationWorker(s); seen=[]; w.stopped.connect(lambda r: seen.append(r)); t=threading.Thread(target=lambda: (time.sleep(.01), w.stop())); t.start(); result=w.run(); t.join()
    assert result['status'] in {'interrupted','completed_limit','completed'}; assert (tmp_path/'generation_manifest.json').exists(); assert (tmp_path/'stop_0001.txt').exists()

def test_pause_resume_continue(tmp_path):
    s=GenerationSettings(mode=GenerationMode.FIXED,charset=CharacterSetSpec(['digits']),exact_length=3,max_records=20,output=OutputSettings(directory=tmp_path,base_name='pause'))
    w=GenerationWorker(s); w.pause(); res=[]
    th=threading.Thread(target=lambda: res.append(w.run())); th.start(); time.sleep(.05); assert th.is_alive(); w.resume(); th.join(5)
    assert res and res[0]['records']==20; assert (tmp_path/'pause_0001.txt').read_text().splitlines()[0]=='000'

def test_invalid_regex_prevents_worker_start(tmp_path):
    s=GenerationSettings(mode=GenerationMode.FIXED,charset=CharacterSetSpec(['digits']),exact_length=1,filters=FilterSettings(regex='['),output=OutputSettings(directory=tmp_path))
    w=GenerationWorker(s); errors=[]; w.failed.connect(errors.append)
    with pytest.raises(Exception): w.run()
    assert errors

def test_file_splitting_record_counts(tmp_path):
    s=GenerationSettings(mode=GenerationMode.FIXED,charset=CharacterSetSpec(['digits']),exact_length=1,max_records=10,output=OutputSettings(directory=tmp_path,base_name='split',max_records_per_file=3))
    r=GenerationWorker(s).run(); counts=[len(p.read_text().splitlines()) for p in r['files']]
    assert counts == [3,3,3,1]

def test_invalid_output_directory_error(tmp_path):
    bad=tmp_path/'file'; bad.write_text('x')
    s=GenerationSettings(output=OutputSettings(directory=bad))
    w=GenerationWorker(s); errors=[]; w.failed.connect(errors.append)
    with pytest.raises(Exception): w.run()
    assert errors
