# ML Models

This document reflects the saved model artifacts and evaluation verified on
Friday, July 17, 2026.

## Ensemble Design

FlowGuard scores each flow with three models:

| Model | Type | Role |
|---|---|---|
| Isolation Forest | Unsupervised | Detect statistical outliers |
| Random Forest | Supervised multi-class | Predict `BENIGN`, `DDoS`, or `PortScan` |
| Autoencoder | Deep learning anomaly detector | Flag flows with high reconstruction error |

Alert rule:

- raise an alert when at least `2 of 3` models vote anomalous

## Saved Artifacts

Saved under `ml-service/app/models/`:

- `scaler.joblib`
- `isolation_forest.joblib`
- `random_forest.joblib`
- `label_encoder.joblib`
- `autoencoder.pt`
- `autoencoder_meta.joblib`
- `gnn_graphsage.pt`
- `gnn_meta.pt`

## Held-Out Evaluation

Evaluation dataset:

- file: `ml-service/data/sample/test_holdout.csv`
- rows: `940`
- benign: `830`
- attacks: `110`

### Isolation Forest

- Accuracy: `0.9511`
- Precision: `0.7254`
- Recall: `0.9364`
- F1: `0.8175`
- Confusion matrix:

```text
[[791  39]
 [  7 103]]
```

### Random Forest

- Accuracy: `0.9521`

Per-class results:

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| BENIGN | 1.00 | 1.00 | 1.00 | 830 |
| DDoS | 0.47 | 0.50 | 0.48 | 40 |
| PortScan | 0.69 | 0.64 | 0.67 | 70 |

Confusion matrix:

```text
[[830   0   0]
 [  0  20  20]
 [  2  23  45]]
```

### Autoencoder

- Threshold: `0.727320`
- Accuracy: `0.9415`
- Precision: `0.7068`
- Recall: `0.8545`
- F1: `0.7737`
- Confusion matrix:

```text
[[791  39]
 [ 16  94]]
```

### Ensemble

- Accuracy: `0.9894`
- Precision: `0.9630`
- Recall: `0.9455`
- F1: `0.9541`
- False positives: `4`
- False negatives: `6`

Confusion matrix:

```text
[[826   4]
 [  6 104]]
```

## Interpretation

- The ensemble is much stronger than any single anomaly detector on the held-out
  dataset.
- Isolation Forest contributes strong recall but also most of the noise.
- Random Forest is best for attack type labeling, but its minority-class results
  are materially weaker than its overall accuracy suggests.
- The ensemble meaningfully reduces false positives without sacrificing much
  recall.
