import pandas as pd

from src.transform import transform
from src.load import load
from src.pipeline import run_pipeline


def test_transform_normalizes_columns_and_drops_duplicates():
    df = pd.DataFrame(
        {"Full Name": ["Alice", "Alice", "Bob"], " Age ": [30, 30, 25]}
    )
    result = transform(df)
    assert list(result.columns) == ["full_name", "age"]
    assert len(result) == 2


def test_load_writes_csv(tmp_path):
    df = pd.DataFrame({"a": [1, 2]})
    dest = tmp_path / "out.csv"
    load(df, dest)
    assert dest.exists()
    assert pd.read_csv(dest).equals(df)


def test_run_pipeline_end_to_end(tmp_path):
    source = tmp_path / "input.csv"
    dest = tmp_path / "output.csv"
    pd.DataFrame({"Name": ["Alice", "Bob"], "Score": [90, 85]}).to_csv(
        source, index=False
    )

    run_pipeline(str(source), str(dest))

    result = pd.read_csv(dest)
    assert list(result.columns) == ["name", "score"]
    assert len(result) == 2
