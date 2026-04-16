import os
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.numerical_features = []
        self.categorical_features = []

    def load_data(self, filepath="data/manufacturing_data.csv"):
        np.random.seed(42)
        n = 5000

        os.makedirs("data", exist_ok=True)

        df = pd.DataFrame({
            "machine_id": np.random.choice(
                ["M001", "M002", "M003", "M004"], n
            ),
            "temperature": np.random.normal(70, 10, n),
            "vibration": np.random.normal(2, 1, n),
            "pressure": np.random.normal(100, 15, n),
            "rpm": np.random.normal(1500, 200, n),
            "power_consumption": np.random.normal(50, 8, n),
            "cycle_count": np.random.randint(0, 10000, n),
            "operating_hours": np.random.randint(0, 5000, n)
        })

        # Failure condition derived logically 
        df["failure"] = (
            (df["temperature"] > 85) |
            (df["vibration"] > 4) |
            (df["pressure"] > 125) |
            (df["cycle_count"] > 8500)
        ).astype(int)

        df.to_csv(filepath, index=False)
        return df

    def preprocess(self, df):
        self.numerical_features = [
            "temperature",
            "vibration",
            "pressure",
            "rpm",
            "power_consumption",
            "cycle_count",
            "operating_hours"
        ]

        X = df[self.numerical_features].copy()

        le = LabelEncoder()
        df_copy = df.copy()
        df_copy["machine_id"] = le.fit_transform(df_copy["machine_id"])

        self.label_encoders["machine_id"] = le
        self.categorical_features = ["machine_id"]

        X_scaled = self.scaler.fit_transform(X)

        X_scaled = pd.DataFrame(
            X_scaled,
            columns=self.numerical_features
        )

        X_final = pd.concat(
            [X_scaled, df_copy[self.categorical_features]],
            axis=1
        )

        y = df["failure"]

        return X_final, y, df

    def save_preprocessors(self, path):
        os.makedirs("models", exist_ok=True)
        joblib.dump({
            "scaler": self.scaler,
            "label_encoders": self.label_encoders,
            "numerical_features": self.numerical_features,
            "categorical_features": self.categorical_features
        }, path)

    def load_preprocessors(self, path):
        if not os.path.exists(path):
            return False
            
        obj = joblib.load(path)
        self.scaler = obj["scaler"]
        self.label_encoders = obj["label_encoders"]
        self.numerical_features = obj["numerical_features"]
        self.categorical_features = obj["categorical_features"]
        return True
