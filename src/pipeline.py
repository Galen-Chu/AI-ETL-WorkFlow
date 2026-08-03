import argparse

from src.extract import extract
from src.transform import transform
from src.load import load


def run_pipeline(source_path: str, dest_path: str) -> None:
    raw_df = extract(source_path)
    clean_df = transform(raw_df)
    load(clean_df, dest_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ETL pipeline")
    parser.add_argument("--source", default="data/raw/input.csv")
    parser.add_argument("--dest", default="data/processed/output.csv")
    args = parser.parse_args()
    run_pipeline(args.source, args.dest)


if __name__ == "__main__":
    main()
