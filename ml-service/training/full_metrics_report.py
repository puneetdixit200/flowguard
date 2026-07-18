# ml-service/training/full_metrics_report.py
"""
Generates the complete metrics package: FPR, FNR, precision-recall curve
(saved as PNG), and per-attack-family breakdown. This replaces "one accuracy
number" with the full picture reviewers/interviewers will ask for.
"""
import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, confusion_matrix, classification_report
from prepare_cicids_data import FEATURE_COLUMNS

df = pd.read_csv("../data/sample/test_holdout.csv")
scaler = joblib.load("../app/models/scaler.joblib")
rf = joblib.load("../app/models/random_forest.joblib")
le = joblib.load("../app/models/label_encoder.joblib")

X = scaler.transform(df[FEATURE_COLUMNS])
y_true_binary = (df["Label"] != "BENIGN").astype(int)

proba = rf.predict_proba(X)
benign_idx = list(le.classes_).index("BENIGN")
attack_proba = 1 - proba[:, benign_idx]

preds = (attack_proba >= 0.5).astype(int)
cm = confusion_matrix(y_true_binary, preds)
tn, fp, fn, tp = cm.ravel()

fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
fnr = fn / (fn + tp) if (fn + tp) > 0 else 0

print("===== FALSE POSITIVE / NEGATIVE RATES =====")
print(f"False Positive Rate (FPR): {fpr:.4f}  ({fp} / {fp+tn} benign flows wrongly flagged)")
print(f"False Negative Rate (FNR): {fnr:.4f}  ({fn} / {fn+tp} attacks missed)")

# ---- Precision-Recall curve ----
precisions, recalls, thresholds = precision_recall_curve(y_true_binary, attack_proba)
plt.figure(figsize=(7, 5))
plt.plot(recalls, precisions, color="#01696f", linewidth=2)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Random Forest — Precision-Recall Curve")
plt.grid(alpha=0.3)
plt.savefig("../../docs/pr_curve.png", dpi=150, bbox_inches="tight")
print("Saved PR curve -> docs/pr_curve.png")

# ---- Per-attack-family report ----
print("\n===== PER-ATTACK-FAMILY METRICS =====")
y_true_multiclass = df["Label"]
pred_labels = le.inverse_transform(rf.predict(X))
print(classification_report(y_true_multiclass, pred_labels, zero_division=0))

with open("../../docs/full_metrics_report.txt", "w") as f:
    f.write(f"FPR: {fpr:.4f}\nFNR: {fnr:.4f}\n\n")
    f.write(classification_report(y_true_multiclass, pred_labels, zero_division=0))
print("\nSaved -> docs/full_metrics_report.txt")
