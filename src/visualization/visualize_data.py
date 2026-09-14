

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_data(input_path: str, output_path: str):
    """
    Visualize the data and save the plot to the specified path.
    """
    try:
        data = pd.read_csv(input_path)
        plt.figure(figsize=(10, 6))
        sns.histplot(data['target'], bins=30, kde=True)
        plt.title('Target Distribution')
        plt.xlabel('Target')
        plt.ylabel('Frequency')
        plt.savefig(output_path)
        print(f"Plot saved to {output_path}")
    except Exception as e:
        print(f"Error visualizing data: {e}")

if __name__ == "__main__":
    input_path = "./data/processed/preprocessed_data.csv"
    output_path = "./reports/figures/histogram.png"
    visualize_data(input_path, output_path)



