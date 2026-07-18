# ml-service/training/evaluate_imbalanced.py
"""
Your held-out set is 830 benign / 110 attack (~7:1). Real traffic is far more
skewed — often 1000:1 or worse. A model can look great on a mild imbalance and
fall apart on a realistic one, because precision is extremely sensitive to the
benign:attack ratio. This script builds a naturally-skewed test set by
undersampling attacks (not oversampling benign) to simulate real conditions.
"""
import pandas as pd
import joblib
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from prepare_cicids_data import load_and_filter, FEATURE_COLUMNS

df = load_and_filter("../data/raw/cicids2017_sample.csv")

benign = df[df["Label"] == "BENIGN"]
attacks = df[df["Label"] != "BENIGN"]

# Simulate a realistic 200:1 imbalance instead of the lab-friendly ~7:1.
TARGET_RATIO = 200
n_attacks = min(len(attacks), max(1, len(benign) // TARGET_RATIO))
attacks_sampled = attacks.sample(n=n_attacks, random_state=42)

realistic_df = pd.concat([benign, attacks_sampled]).sample(frac=1, random_state=42)
print(f"Realistic test set: {len(benign)} benign, {len(attacks_sampled)} attack "
      f"(ratio ~{len(benign)//max(1,len(attacks_sampled))}:1)")

scaler = joblib.load("../app/models/scaler.joblib")
rf = joblib.load("../app/models/random_forest.joblib")
le = joblib.load("../app/models/label_encoder.joblib")

X = scaler.transform(realistic_df[FEATURE_COLUMNS])
y_true = (realistic_df["Label"] != "BENIGN").astype(int)

preds = rf.predict(X)
pred_labels = le.inverse_transform(preds)
y_pred = (pred_labels != "BENIGN").astype(int)

print("\n===== RANDOM FOREST ON REALISTIC IMBALANCE =====")
print(f"Precision: {precision_score(y_true, y_pred, zero_division=0):.4f}")
print(f"Recall:    {recall_score(y_true, y_pred, zero_division=0):.4f}")
print(f"F1:        {f1_score(y_true, y_pred, zero_division=0):.4f}")
print(f"Confusion matrix:\n{confusion_matrix(y_true, y_pred)}")
print("\nNOTE: precision typically drops sharply here even if recall holds — "
      "this is the honest, realistic number, not the lab number.")
