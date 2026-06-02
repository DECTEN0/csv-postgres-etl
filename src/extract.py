import pandas as pd

def extract(csv_path):
    df = pd.read_csv(csv_path)
    return df