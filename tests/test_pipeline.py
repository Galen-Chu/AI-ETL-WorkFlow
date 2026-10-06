import logging
import sys

import pandas as pd
import pytest

from src.extract import extract
from src.transform import transform
from src.load import load
from src.pipeline import main, run_pipeline


def test_transform_normalizes_columns_and_drops_duplicates():
    df = pd.DataFrame(
        {"Full Name": ["Alice", "Alice", "Bob"], " Age ": [30, 30, 25]}
    )
    result = transform(df)
    assert list(result.columns) == ["full_name", "age"]
    assert len(result) == 2


def test_transform_drops_fully_empty_rows():
    df = pd.DataFrame({"name": ["Alice", None, "Bob"], "age": [30, None, 25]})
    result = transform(df)
    assert len(result) == 2
    assert list(result["name"]) == ["Alice", "Bob"]


def test_transform_handles_empty_dataframe():
    df = pd.DataFrame(columns=["Full Name", " Age "])
    result = transform(df)
    assert list(result.columns) == ["full_name", "age"]
    assert len(result) == 0


def test_transform_logs_row_counts(caplog):
    df = pd.DataFrame({"a": [1, 1, None], "b": [1, 1, None]})
    with caplog.at_level(logging.INFO, logger="src.transform"):
        transform(df)
    assert "3 rows in -> 2 after empty-row drop -> 1 after dedupe" in caplog.text


def test_extract_reads_csv_with_bom(tmp_path):
    source = tmp_path / "bom.csv"
    source.write_text("name,score\nAlice,90\n", encoding="utf-8-sig")
    result = extract(source)
    assert list(result.columns) == ["name", "score"]
    assert len(result) == 1


def test_extract_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract(tmp_path / "missing.csv")


def test_load_writes_csv(tmp_path):
    df = pd.DataFrame({"a": [1, 2]})
    dest = tmp_path / "out.csv"
    load(df, dest)
    assert dest.exists()
    assert pd.read_csv(dest).equals(df)


def test_load_creates_missing_parent_dirs(tmp_path):
    df = pd.DataFrame({"a": [1, 2]})
    dest = tmp_path / "nested" / "dir" / "out.csv"
    load(df, dest)
    assert dest.exists()
    assert pd.read_csv(dest).equals(df)


def test_run_pipeline_end_to_end(tmp_path):
    source = tmp_path / "input.csv"
    dest = tmp_path / "output.csv"
    pd.DataFrame({"Name": ["Alice", "Bob"], "Score": [90, 85]}).to_csv(
        source, index=False
    )

    run_pipeline(source, dest)

    result = pd.read_csv(dest)
    assert list(result.columns) == ["name", "score"]
    assert len(result) == 2


def test_main_exits_with_error_when_source_missing(tmp_path, monkeypatch, caplog):
    monkeypatch.setattr(
        sys, "argv", ["pipeline", "--source", str(tmp_path / "missing.csv")]
    )
    with caplog.at_level(logging.ERROR):
        with pytest.raises(SystemExit) as excinfo:
            main()
    assert excinfo.value.code == 1
    assert "not found" in caplog.text


def test_main_exits_with_error_when_source_empty(tmp_path, monkeypatch, caplog):
    source = tmp_path / "empty.csv"
    source.write_text("", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["pipeline", "--source", str(source)])
    with caplog.at_level(logging.ERROR):
        with pytest.raises(SystemExit) as excinfo:
            main()
    assert excinfo.value.code == 1
    assert "empty" in caplog.text
