import json, pytest
from combination_studio.models.character_set import CharacterSetSpec, dedupe_preserve_order
from combination_studio.generation.cartesian_generator import generate_fixed, generate_range
from combination_studio.generation.index_converter import index_to_combination
from combination_studio.generation.pattern_generator import parse_position_pattern, generate_pattern
from combination_studio.generation.counter_generator import generate_counter
from combination_studio.generation.estimator import estimate_uniform, estimate_range, estimate_positions
from combination_studio.generation.filters import OutputFilter
from combination_studio.generation.random_generator import generate_random_unique
from combination_studio.models.generation_settings import GenerationSettings, OutputSettings, FilterSettings
from combination_studio.models.enums import GenerationMode
from combination_studio.jobs.worker import GenerationWorker
from combination_studio.jobs.recovery import save_state, load_state, can_resume

def test_five_digit_numeric_generation():
    vals=list(generate_fixed('0123456789',5)); assert len(vals)==100000; assert vals[0][1]=='00000'; assert vals[-1][1]=='99999'
def test_charset_custom_dedupe_exclude(): assert dedupe_preserve_order('abca')=='abc' and CharacterSetSpec(['digits'],'001A','0').build()=='123456789A'
def test_estimations(): assert estimate_uniform(10,5).total==100000; assert estimate_range(2,2,3).total==12; assert estimate_positions(['AB','01','x']).total==4
def test_index_and_range(): assert index_to_combination(0,'01',3)=='000'; assert index_to_combination(7,'01',3)=='111'; assert list(generate_fixed('01',3,2,3))==[(2,'010'),(3,'011')]
def test_range_generation(): assert [v for _,v in generate_range('ab',1,2)]==['a','b','aa','ab','ba','bb']
def test_patterns(): assert parse_position_pattern('[A-Z][0-9]')[0].startswith('A'); assert [v for _,v in generate_pattern(['AB','01'])]==['A0','A1','B0','B1']
def test_counter(): assert [v for _,v in generate_counter(1,3,1,3,'X','Z')]==['X001Z','X002Z','X003Z']
def test_filters_invalid_regex():
    with pytest.raises(Exception): OutputFilter(FilterSettings(regex='['))
def test_filters_match(): assert OutputFilter(FilterSettings(min_digits=2, disallow_adjacent_repeats=True)).match('A12')
def test_random_unique_validation():
    with pytest.raises(ValueError): list(generate_random_unique('01',2,5))
def test_file_splitting_manifest_utf8_resume(tmp_path):
    s=GenerationSettings(mode=GenerationMode.FIXED, charset=CharacterSetSpec(custom='abç'), exact_length=2, max_records=5, output=OutputSettings(directory=tmp_path, max_records_per_file=2))
    r=GenerationWorker(s).run(); assert r['records']==5; assert len(r['files'])==3
    m=json.loads((tmp_path/'generation_manifest.json').read_text(encoding='utf-8')); assert m['records_written']==5; assert all(f['sha256'] for f in m['output_files'])
    st=tmp_path/'state.json'; save_state(st,s,4,str(r['files'][-1]),5,10); assert load_state(st)['records_written']==5; assert can_resume(st,s)
def test_empty_charset_rejection():
    with pytest.raises(ValueError): estimate_uniform(0,2)
def test_insufficient_disk_rejection(monkeypatch,tmp_path):
    import combination_studio.utils.disk_space as ds
    monkeypatch.setattr(ds,'available_bytes',lambda p:1)
    with pytest.raises(RuntimeError): ds.ensure_space(tmp_path,100,0)
