import logging

import pandas as pd

logger = logging.getLogger(__name__)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize raw data: drop empty rows, trim column names."""
    rows_in = len(df)
    df = df.dropna(how="all")
    rows_after_empty = len(df)
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    df = df.drop_duplicates()
    logger.info(
        "transform: %d rows in -> %d after empty-row drop -> %d after dedupe",
        rows_in,
        rows_after_empty,
        len(df),
    )
    return df.reset_index(drop=True)
