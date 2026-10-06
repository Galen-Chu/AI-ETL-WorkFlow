import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def extract(source_path: str | Path, encoding: str = "utf-8-sig") -> pd.DataFrame:
    """Read raw tabular data (CSV) from source_path into a DataFrame.

    utf-8-sig handles the BOM that Excel writes into exported CSVs.
    """
    df = pd.read_csv(source_path, encoding=encoding)
    logger.debug("columns: %s", list(df.columns))
    return df
