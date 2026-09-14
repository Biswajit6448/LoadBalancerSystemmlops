

import os
import pandas as pd

def preprocess_data(input_path: str, output_path: str):
    """
    Preprocess the raw data and save it to the specified path.
    """
    try:
        data = pd.read_csv(input_path)
        # Add preprocessing steps here
        data.dropna(inplace=True)
        data.to_csv(output_path, index=False)
        print(f"Data preprocessed and saved to {output_path}")
    except Exception as e:
        print(f"Error preprocessing data: {e}")

if __name__ == "__main__":
    input_path = "./data/raw/dataset.csv"
    output_path = "./data/interim/cleaned_data.csv"
    preprocess_data(input_path, output_path)



