import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from data_preprocessing import DataPreprocessor

class PredictiveMaintenanceModel:
    def __init__(self):
        self.preprocessor = DataPreprocessor()
        self.model = None
        self.anomaly = None

    def train(self):
        if not os.path.exists("data/manufacturing_data.csv"):
            df = self.preprocessor.load_data("data/manufacturing_data.csv")
        else:
            df = pd.read_csv("data/manufacturing_data.csv")

        X, y, _ = self.preprocessor.preprocess(df)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.model = RandomForestClassifier(n_estimators=150, random_state=42)
        self.model.fit(X_train, y_train)

        self.anomaly = IsolationForest(contamination=0.05, random_state=42)
        self.anomaly.fit(X_train)

        pred = self.model.predict(X_test)
        print("Training completed. Classification Report:")
        print(classification_report(y_test, pred))

        os.makedirs("models", exist_ok=True)
        joblib.dump(self.model, "models/predictive_model.pkl")
        joblib.dump(self.anomaly, "models/anomaly.pkl")
        self.preprocessor.save_preprocessors("models/preprocessors.pkl")
        print("Models saved successfully.")

    def load_model(self):
        if not os.path.exists("models/predictive_model.pkl"):
            print("Model files not found! Training model dynamically...")
            self.train()
            
        self.model = joblib.load("models/predictive_model.pkl")
        self.anomaly = joblib.load("models/anomaly.pkl")
        self.preprocessor.load_preprocessors("models/preprocessors.pkl")

    def predict(self, df):
        X_num = df[self.preprocessor.numerical_features]
        X_scaled = self.preprocessor.scaler.transform(X_num)
        
        X_scaled = pd.DataFrame(
            X_scaled,
            columns=self.preprocessor.numerical_features
        )

        le = self.preprocessor.label_encoders["machine_id"]
        # Convert unseen labels to known just in case, but assume correct ID
        X_scaled["machine_id"] = le.transform(df["machine_id"])

        failure = self.model.predict(X_scaled)
        prob = self.model.predict_proba(X_scaled)[:, 1]
        anomaly = self.anomaly.predict(X_scaled)

        return failure, prob, anomaly
