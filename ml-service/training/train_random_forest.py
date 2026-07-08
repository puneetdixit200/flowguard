import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder

from prepare_cicids_data import FEATURE_COLUMNS

def main():
    df = pd.read_csv("../data/sample/sample_features.csv")

    X = df[FEATURE_COLUMNS]
    y_raw = df["Label"]

    encoder = LabelEncoder()
    y = encoder.fit_transform(y_raw)

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    scores = cross_val_score(
        model,
        X,
        y,
        cv=skf,
        scoring="f1_macro"
    )

    print(f"Cross-val F1-macro scores: {scores}")
    print(f"Mean F1-macro: {scores.mean():.4f}")

    model.fit(X, y)

    importances = sorted(
        zip(FEATURE_COLUMNS, model.feature_importances_),
        key=lambda x: -x[1]
    )

    print("Feature importances:")
    for name, score in importances:
        print(f"  {name}: {score:.4f}")

    os.makedirs("../app/models", exist_ok=True)

    joblib.dump(model, "../app/models/random_forest.joblib")
    joblib.dump(encoder, "../app/models/label_encoder.joblib")

    print("Random Forest + label encoder saved.")

if __name__ == "__main__":
    main()
