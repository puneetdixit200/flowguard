"""
Trains an unsupervised Isolation Forest for anomaly detection.

Purpose:
- Learn mostly normal/benign network traffic.
- Later detect traffic that looks different from normal.
"""

import joblib
import pandas as pd
from prepare_cicids_data import FEATURE_COLUMN
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def main():
    df = pd.read_csv("../data/sample/sample_features.csv")
    normal_df = df[df["Label"].str.upper() == "BENIGN"]
    X_train = normal_df[FEATURE_COLUMN]

 # Scale features so no single feature

    scaler= StandardScaler()
    X_scaled = scaler.fit_transform(X_train)


    # contamination = expected proportion of anomalies in a typical batch.

    model= IsolationForest(
     n_estimators=200,
     contamination= 0.05
     random_state = 42,
     n_jobs=-1
    )

    model.fit(X_scaled)

    joblib.dump(model , "../app/models/isolation_forest.joblib")

    joblib.dump(scaler , "../app/models/scaler.joblib")

    print("Isolation Forest + Scaler Saved")


if __name__=="__main__":
    main()
