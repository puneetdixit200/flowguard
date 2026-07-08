"""
Trains a supervised Random Forest multi-class classifier.
Purpose per dossier: explainable feature importance, classes = normal/DDoS/port scan/
brute force/web attack/botnet/infiltration, evaluated with stratified k-fold. [file:1]
"""

from json import encoder

import joblib
import pandas as pd
from prepare_cicids_data import FEATURE_COLUMNS
from sklearn.enemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder


def main():
    df = pd.read_csv("../data/sample/sample_feature.csv")
    X = df[FEATURE_COLUMNS]
    y = df["Label"]
    y = LabelEncoder().fit_transform(
        y
    )  # convert text label into ntegers which moe iwtll use)

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        class_weight="balanced",  # handles class imbalance
        random_state=42,
    )

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=skf, scoring="f1_macro")
    print(f"F1 Macro Score: {scores.mean():.4f}")
    print(f"Cross-Validation Scores: {scores}")

    model.fit(X, y)

    importances = sorted(
        zip(FEATURE_COLUMNS, model.feature_importances_),
        key=lambda x: x[1],
        reverse=True,
    )
    print(f"Feature Importances")
    for feature, importance in importances:
        print(f"{feature}: {importance:.4f}")

    joblib.dump(model, "../models/random_forest_model.joblib")

    joblib.dump(LabelEncoder(), "../models/label_encoder.joblib")
    print("Model and label encoder saved.")


if __name__ == "__main__":
    main()
