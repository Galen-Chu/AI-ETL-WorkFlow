import pandas as pd


def extract(source_path: str) -> pd.DataFrame:
    """Read raw tabular data (CSV) from source_path into a DataFrame."""
    return pd.read_csv(source_path)
