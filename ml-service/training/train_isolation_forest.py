import os
import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from prepare_cicids_data import FEATURE_COLUMNS

def main():
    df = pd.read_csv("../data/sample/sample_features.csv")

    normal_df = df[df["Label"].str.upper() == "BENIGN"]
    X_train = normal_df[FEATURE_COLUMNS]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)

    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_scaled)

    os.makedirs("../app/models", exist_ok=True)

    joblib.dump(model, "../app/models/isolation_forest.joblib")
    joblib.dump(scaler, "../app/models/scaler.joblib")

    print("Isolation Forest + scaler saved.")

if __name__ == "__main__":
    main()
