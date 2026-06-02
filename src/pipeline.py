import logging

from extract import extract
from transform import transform
from load import load

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO
)

def run_pipeline():

    logging.info("Extraction Started")

    df = extract("data/raw/sales.csv")

    logging.info("Transformation Started")

    df = transform(df)

    logging.info("Loading Started")

    load(df)

    logging.info("Pipeline Completed")

if __name__ == "__main__":
    run_pipeline()