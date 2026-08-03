import pandas as pd


def load(df: pd.DataFrame, dest_path: str) -> None:
    """Write the transformed DataFrame to dest_path as CSV."""
    df.to_csv(dest_path, index=False)
