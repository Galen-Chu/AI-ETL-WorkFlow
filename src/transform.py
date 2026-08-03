import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize raw data: drop empty rows, trim column names."""
    df = df.dropna(how="all")
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    df = df.drop_duplicates()
    return df.reset_index(drop=True)
