# 🔄 AI-ETL-WorkFlow

> Data / ETL pipeline scaffold.

---

## 🏗️ Pipeline · 管線

```
[Raw data] → Extract → Transform → Load → [Clean data / DB]
```

---

## 📁 Structure · 結構

| Path | Purpose |
|------|---------|
| `src/extract.py` | Reads raw data (CSV) into a DataFrame |
| `src/transform.py` | Cleans and normalizes the data |
| `src/load.py` | Writes the result to its destination |
| `src/pipeline.py` | Orchestrates E→T→L, CLI entrypoint |
| `data/raw/` | Input data (git-ignored, `.gitkeep` placeholder) |
| `data/processed/` | Output data (git-ignored, `.gitkeep` placeholder) |
| `tests/` | pytest test suite |
| `.github/workflows/ci.yml` | Lint + test pipeline |

---

## 🚀 Local Development · 本地開發

```bash
pip install -r requirements-dev.txt
flake8 src tests
pytest -v
python -m src.pipeline --source data/raw/input.csv --dest data/processed/output.csv
```

---

## 💾 Data Storage · 資料儲存

Raw and processed data files are intentionally excluded from git (see
`.gitignore`). Large or sensitive datasets (e.g. genomic data) should live in
external storage (S3/GCS/a database) or be version-controlled with a tool like
DVC — not committed directly to this repository.

---

## 📄 License

MIT — see [LICENSE](LICENSE).
