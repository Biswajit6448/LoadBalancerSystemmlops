

import os
import pandas as pd
import joblib

def predict_model(model_path: str, input_path: str, output_path: str):
    """
    Make predictions using the trained model and save the results to the specified path.
    """
    try:
        model = joblib.load(model_path)
        data = pd.read_csv(input_path)
        X = data.drop('target', axis=1)

        predictions = model.predict(X)
        data['prediction'] = predictions
        data.to_csv(output_path, index=False)
        print(f"Predictions saved to {output_path}")
    except Exception as e:
        print(f"Error making predictions: {e}")

if __name__ == "__main__":
    model_path = "../../models/model_v1.pkl"
    input_path = "../../data/processed/preprocessed_data.csv"
    output_path = "../../data/processed/predictions.csv"
    predict_model(model_path, input_path, output_path)




