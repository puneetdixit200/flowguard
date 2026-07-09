# ML Models

| Model | Type | Purpose | Threshold Rule |
|---|---|---|---|
| Isolation Forest | Unsupervised | Catch unknown attacks | contamination=0.05 |
| Random Forest | Supervised multi-class | Explainable classification | class_weight=balanced |
| Autoencoder | Deep learning | Reconstruction-error anomaly | 95th percentile error |

Ensemble rule: if 2 of 3 models vote anomaly, raise an alert.
Severity: 50-70%=low, 70-85%=medium, 85-95%=high, 95%+=critical.
