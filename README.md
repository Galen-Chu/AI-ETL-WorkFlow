# AI-ETL-WorkFlow

Data / ETL pipeline scaffold.

```
[Raw data] -> Extract -> Transform -> Load -> [Clean data / DB]
```

## Structure

- `src/extract.py` — reads raw data (CSV) into a DataFrame
- `src/transform.py` — cleans and normalizes the data
- `src/load.py` — writes the result to its destination
- `src/pipeline.py` — orchestrates extract -> transform -> load, CLI entrypoint
- `data/raw/` — input data (git-ignored, folder tracked via `.gitkeep`)
- `data/processed/` — output data (git-ignored, folder tracked via `.gitkeep`)
- `tests/` — pytest test suite
- `.github/workflows/ci.yml` — lint + test pipeline

## Local development

```bash
pip install -r requirements-dev.txt
flake8 src tests
pytest -v
python -m src.pipeline --source data/raw/input.csv --dest data/processed/output.csv
```

## Note on data storage

Raw and processed data files are intentionally excluded from git (see
`.gitignore`). Large or sensitive datasets (e.g. genomic data) should live in
external storage (S3/GCS/a database) or be version-controlled with a tool like
DVC — not committed directly to this repository.
