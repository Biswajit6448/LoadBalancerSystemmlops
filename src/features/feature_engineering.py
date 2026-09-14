

import os
import pandas as pd

def feature_engineering(input_path: str, output_path: str):
    """
    Perform feature engineering on the preprocessed data and save it to the specified path.
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Load data
        data = pd.read_csv(input_path)
        print("Columns in the dataset:", list(data.columns))

        # Check if 'existing_feature' exists, or create dummy one
        if 'existing_feature' not in data.columns:
            print("Column 'existing_feature' not found. Adding dummy column for testing.")
            data['existing_feature'] = 1  # Replace with appropriate logic if needed

        # Feature engineering logic
        data['new_feature'] = data['existing_feature'] * 2

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save processed data
        data.to_csv(output_path, index=False)
        print(f"Feature engineering completed and saved to {output_path}")

    except Exception as e:
        print(f"Error performing feature engineering: {e}")

if __name__ == "__main__":
    input_path = "./data/interim/cleaned_data.csv"
    output_path = "./data/processed/preprocessed_data.csv"
    feature_engineering(input_path, output_path)



