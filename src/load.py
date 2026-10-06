import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load(df: pd.DataFrame, dest_path: str | Path) -> None:
    """Write the transformed DataFrame to dest_path as CSV, creating parent dirs."""
    Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(dest_path, index=False)
    logger.info("load: wrote %d rows to %s", len(df), dest_path)
