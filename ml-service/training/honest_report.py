"""
Generates an honest performance report including false positives and false
negatives — not just accuracy. This file becomes docs/false-positive-analysis.md
content directly. Real portfolios show failures, not just clean numbers. [web:69]
"""
import pandas as pd
import joblib
from sklearn.metrics import confusion_matrix
from prepare_cicids_data import FEATURE_COLUMNS

def main():
    df = pd.read_csv("../data/sample/test_holdout.csv")
    X = df[FEATURE_COLUMNS]
    y_true_raw = df["Label"]

    encoder = joblib.load("../app/models/label_encoder.joblib")
    rf_model = joblib.load("../app/models/random_forest.joblib")

    y_true = encoder.transform(y_true_raw)
    y_pred = rf_model.predict(X)

    # Find actual misclassified rows — these are your "real" false positives/negatives.
    df["true_label"] = y_true_raw.values
    df["predicted_label"] = encoder.inverse_transform(y_pred)
    mistakes = df[df["true_label"] != df["predicted_label"]]

    false_positives = mistakes[mistakes["true_label"] == "BENIGN"]
    false_negatives = mistakes[mistakes["true_label"] != "BENIGN"]

    print(f"Total test rows: {len(df)}")
    print(f"Total mistakes: {len(mistakes)} ({len(mistakes)/len(df)*100:.2f}%)")
    print(f"False positives (normal flagged as attack): {len(false_positives)}")
    print(f"False negatives (attack missed as normal): {len(false_negatives)}")

    if len(false_positives) > 0:
        print("\nSample false positive (normal traffic wrongly flagged):")
        print(false_positives[FEATURE_COLUMNS + ["true_label", "predicted_label"]].head(1).to_string())

    if len(false_negatives) > 0:
        print("\nSample false negative (attack that slipped through):")
        print(false_negatives[FEATURE_COLUMNS + ["true_label", "predicted_label"]].head(1).to_string())

    # Save full mistake log for the docs/false-positive-analysis.md writeup.
    mistakes.to_csv("../data/sample/misclassified_rows.csv", index=False)
    print("\nFull mistake log saved -> ../data/sample/misclassified_rows.csv")

if __name__ == "__main__":
    main()
