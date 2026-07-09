"""
UPDATED: Now evaluates on test_holdout.csv (data the model never saw during
training) instead of the original training file. This is the actual fix for
the 100% accuracy problem — you were grading the model on its own homework. [web:54]
"""
import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix, f1_score, accuracy_score

from prepare_cicids_data import FEATURE_COLUMNS

def main():
    # THE FIX: load the held-out test set, NOT sample_features.csv.
    df = pd.read_csv("../data/sample/test_holdout.csv")
    X = df[FEATURE_COLUMNS]
    y_raw = df["Label"]

    encoder = joblib.load("../app/models/label_encoder.joblib")
    y_true = encoder.transform(y_raw)

    rf_model = joblib.load("../app/models/random_forest.joblib")
    y_pred = rf_model.predict(X)

    print("=== Random Forest Evaluation (on UNSEEN test data) ===")
    print(f"Test set size: {len(df)} rows")
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
    print(classification_report(y_true, y_pred, target_names=encoder.classes_))
    print("Confusion matrix:")
    print(confusion_matrix(y_true, y_pred))
    print(f"Macro F1: {f1_score(y_true, y_pred, average='macro'):.4f}")

if __name__ == "__main__":
    main()
