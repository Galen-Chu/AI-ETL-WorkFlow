import argparse
import logging
import sys
from pathlib import Path

from pandas.errors import EmptyDataError

from src.extract import extract
from src.transform import transform
from src.load import load

logger = logging.getLogger(__name__)


def run_pipeline(source_path: str | Path, dest_path: str | Path) -> None:
    raw_df = extract(source_path)
    logger.info("extract: read %d rows from %s", len(raw_df), source_path)

    clean_df = transform(raw_df)
    load(clean_df, dest_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ETL pipeline")
    parser.add_argument("--source", default="data/raw/input.csv")
    parser.add_argument("--dest", default="data/processed/output.csv")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    try:
        run_pipeline(args.source, args.dest)
    except FileNotFoundError:
        logger.error("Source file not found: %s", args.source)
        sys.exit(1)
    except EmptyDataError:
        logger.error("Source file is empty (no columns to parse): %s", args.source)
        sys.exit(1)


if __name__ == "__main__":
    main()
