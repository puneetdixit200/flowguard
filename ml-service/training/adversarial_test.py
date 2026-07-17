"""
Tests how much each model's accuracy DEGRADES under a simple evasion
attack (slow-drip scan: same attack pattern but spread across more time
with smaller packets, mimicking normal traffic). This produces the single
most impressive resume number: "GNN degraded only X% under adversarial
conditions vs Y% for flat models" — directly mirrors published research. [web:100]
"""
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import accuracy_score
from prepare_cicids_data import FEATURE_COLUMNS

def craft_evasive_samples(df, fraction=0.3):
    """
    Takes real attack rows and perturbs them to look more like normal
    traffic — slower rate, smaller bytes — simulating an attacker who
    knows how detection works and adapts.
    """
    attack_rows = df[df["Label"] != "BENIGN"].copy()
    n_evasive = int(len(attack_rows) * fraction)
    evasive = attack_rows.sample(n=n_evasive, random_state=1).copy()

    # Shrink the "loud" signals that make attacks obvious.
    evasive["packets_per_sec"] *= 0.15
    evasive["bytes_per_sec"] *= 0.2
    evasive["syn_ack_ratio"] *= 0.4

    return evasive

def main():
    df = pd.read_csv("../data/sample/test_holdout.csv")
    evasive = craft_evasive_samples(df)

    scaler = joblib.load("../app/models/scaler.joblib")
    rf_model = joblib.load("../app/models/random_forest.joblib")
    encoder = joblib.load("../app/models/label_encoder.joblib")

    X_normal = df[df["Label"] != "BENIGN"][FEATURE_COLUMNS]
    y_normal = np.ones(len(X_normal))

    X_evasive = evasive[FEATURE_COLUMNS]
    y_evasive = np.ones(len(X_evasive))

    normal_preds = (encoder.inverse_transform(rf_model.predict(X_normal)) != "BENIGN").astype(int)
    evasive_preds = (encoder.inverse_transform(rf_model.predict(X_evasive)) != "BENIGN").astype(int)

    normal_acc = accuracy_score(y_normal, normal_preds)
    evasive_acc = accuracy_score(y_evasive, evasive_preds)
    degradation = ((normal_acc - evasive_acc) / normal_acc) * 100

    print("===== ADVERSARIAL ROBUSTNESS TEST (Random Forest) =====")
    print(f"Accuracy on normal attacks:  {normal_acc:.4f}")
    print(f"Accuracy on evasive attacks: {evasive_acc:.4f}")
    print(f"Accuracy degradation:        {degradation:.1f}%")
    print("\nRepeat this same test swapping in GNN predictions to compare robustness.")

if __name__ == "__main__":
    main()
