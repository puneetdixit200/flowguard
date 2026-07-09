"""
UPDATED: Now splits data into train/test BEFORE fitting, and saves the test
set separately so evaluate_models.py can score on truly unseen data. This is
the fix for the "always split before preprocessing" rule that prevents
data leakage. [web:51][web:56]
"""
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder

from prepare_cicids_data import FEATURE_COLUMNS

def main():
    df = pd.read_csv("../data/sample/sample_features.csv")

    X = df[FEATURE_COLUMNS]
    y_raw = df["Label"]

    encoder = LabelEncoder()
    y = encoder.fit_transform(y_raw)

    # THE FIX: split into train (80%) and test (20%) BEFORE any fitting happens.
    # stratify=y keeps class proportions consistent in both splits, which matters
    # because attack classes are much rarer than normal traffic. [web:56]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    # Cross-validation now runs ONLY on the training split, never touching test data.
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=skf, scoring="f1_macro")
    print(f"Cross-val F1-macro scores (train split only): {scores}")
    print(f"Mean F1-macro: {scores.mean():.4f}")

    # Fit the FINAL model only on the training split — never on test data.
    model.fit(X_train, y_train)

    importances = sorted(zip(FEATURE_COLUMNS, model.feature_importances_), key=lambda x: -x[1])
    print("Feature importances:")
    for name, score in importances:
        print(f"  {name}: {score:.4f}")

    # Save the model + encoder as before.
    joblib.dump(model, "../app/models/random_forest.joblib")
    joblib.dump(encoder, "../app/models/label_encoder.joblib")

    # NEW: save the held-out test set to disk so evaluate_models.py can score
    # on data the model has genuinely never seen.
    X_test.assign(Label=encoder.inverse_transform(y_test)).to_csv(
        "../data/sample/test_holdout.csv", index=False
    )
    print(f"Saved {len(X_test)} held-out test rows -> ../data/sample/test_holdout.csv")
    print("Random Forest + label encoder saved.")

if __name__ == "__main__":
    main()
