

import os
import pandas as pd

def download_data(url: str, output_path: str):
    """
    Download data from a URL and save it to the specified path.
    """
    try:
        data = pd.read_csv(url)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        data.to_csv(output_path, index=False)
        print(f"Data downloaded and saved to {output_path}")
    except Exception as e:
        print(f"Error downloading data: {e}")

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/DebmalyaRay9989/Load_Balancer/main/dataset.csv"
    output_path = "./data/raw/dataset.csv"
    download_data(url, output_path)



