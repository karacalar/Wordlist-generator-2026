# Combination Studio

Combination Studio is a professional Windows desktop application for generating bounded local character combinations for software testing, QA fixtures, serial-number test data, coupon-code datasets, and identifier/PIN tests on systems you own or are authorized to test.

## Responsible use

This application generates local test datasets and identifier combinations. It does not test accounts, passwords, hashes, networks, websites, archives, or remote systems. Use generated data only in systems and environments you own or are authorized to test.

It intentionally contains no networking, login automation, hash processing, credential checking, or integrations with cracking tools.

## Installation

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Running from source

```powershell
python main.py
```

## Building the Windows executable

```powershell
build_windows.bat
```

This uses PyInstaller and `combination_studio.spec`.

## Generator modes

- Fixed Length: enumerate a uniform character set at one exact length, preserving leading zeroes.
- Length Range: enumerate each selected length in deterministic order.
- Prefix/Suffix: combine generated sections with one or more local prefix/suffix values.
- Position Pattern: each position has a different set, e.g. `[A-Z][A-Z][0-9][0-9][0-9][0-9]`.
- Template: tokens such as `{UPPER}{UPPER}-{DIGIT}{DIGIT}{DIGIT}{DIGIT}` and `{CUSTOM:name}`.
- Counter: sequential zero-padded identifiers with prefix, suffix, start, end, and step.
- Random Unique: bounded unique random identifiers; secure mode uses Python `secrets`.

## Examples

- All five-digit numeric values: digits, fixed length 5 generates `00000` through `99999` (100,000 records).
- Hexadecimal identifiers: hexadecimal lowercase with fixed length such as 8.
- Two letters followed by four digits: `[A-Z][A-Z][0-9][0-9][0-9][0-9]`.
- Fixed prefix plus padded counter: prefix `TEST-`, counter 1 to 9999, padding 4.
- Selected index range: set start index and end index; uniform sets use base-N index conversion and do not iterate skipped values.

## Character sets

Built-in groups include digits, ASCII lower/upper, letters plus digits, safe symbols, lowercase/uppercase hexadecimal, binary, Turkish lowercase, Turkish uppercase, and custom text. Duplicates are removed while preserving order. Exclusion characters such as `0O1Il` can improve readability.

## Count estimation and large spaces

Combination Studio calculates theoretical counts and estimated output size before generation. Uniform fixed length uses `charset_size ** length`; ranges sum each length; position patterns multiply each position count. Extremely large spaces may take years and require impractical storage.

## Output and splitting

Output formats are TXT, CSV, and JSON Lines. TXT supports UTF-8, UTF-8 BOM, LF, and CRLF. Large outputs can be split by maximum records or bytes. A `generation_manifest.json` records settings, theoretical count, index range, record count, output files, SHA-256 checksums, and completion/interruption status.

## Pause, resume, and recovery

Workers stream data through bounded buffers and save resumable state with atomic writes where practical. Stop requests flush and close the active file, preserve completed output, and mark interrupted manifests.

## Disk-space protections

The application estimates output size, checks available disk space, reserves a safety margin, and rejects jobs that cannot fit. A default maximum of 10,000,000 records avoids accidental huge jobs.

## Known limitations

Multiprocessing is not enabled by default because disk speed is often the bottleneck. GUI pages are intentionally lightweight but expose the requested workflow. Random-unique mode stores selected indexes to enforce uniqueness, so requests must remain bounded.
