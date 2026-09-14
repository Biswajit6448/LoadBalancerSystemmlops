

import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_model(input_path: str, model_output_path: str):
    """
    Train the model and save it to the specified path.
    """
    try:
        data = pd.read_csv(input_path)
        X = data.drop('target', axis=1)
        y = data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy}")

        joblib.dump(model, model_output_path)
        print(f"Model saved to {model_output_path}")
    except Exception as e:
        print(f"Error training model: {e}")

if __name__ == "__main__":
    input_path = "../../data/processed/preprocessed_data.csv"
    model_output_path = "../../models/model_v1.pkl"
    train_model(input_path, model_output_path)



