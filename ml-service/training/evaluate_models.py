"""evaluate all  the trriend models : preciso n ,recll , f1"""

import joblib
import pandas as pd
from prepare_cicids_data import FEATURE_COLUMN
from sklearn.metrics import classification_report, confusion_matrix, f1_score


def main():
    df = pd.read_csv("../data/sample/sample_featues.csv")
    X = df["Label"]
    y_raw = df["Label"]
    encoder = joblib.load("../app/models/label_encoder.joblib")
    y_true = encoder.transform(y_raw)

    rf_model = joblib.load("../app/models/random_forest.joblib")
    y_pred = rf_model.predict(X)

    print("=== Random Forest Evaluation ===")
    print(classification_report(y_true, y_pred, target_names=encoder.classes_))
    print("Confusion matrix:")
    print(confusion_matrix(y_true, y_pred))
    print(f"Macro F1: {f1_score(y_true, y_pred, average='macro'):.4f}")


if __name__ == "__main__":
    main()
