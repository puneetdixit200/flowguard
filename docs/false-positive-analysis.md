# False Positive Analysis

This note summarizes the held-out ensemble errors verified on Friday, July 17,
2026.

## Held-Out Error Counts

From `docs/evaluation_report.txt`:

- false positives: `4`
- false negatives: `6`

Confusion matrix:

```text
[[826   4]
 [  6 104]]
```

## What This Means

- Only `4` benign flows were incorrectly flagged as attacks on the held-out set.
- `6` true attacks were missed by the ensemble.
- The remaining errors are small enough that the ensemble is credible, but not
  small enough to claim perfect detection.

## Practical Read

- Isolation Forest improves recall but contributes some false positives.
- Autoencoder adds another anomaly signal, but it is also noisier than the full
  ensemble.
- The `2 of 3` vote rule is doing the important work here: it reduces single-model
  noise while keeping recall high.

## Honest Limitation

These numbers come from the saved held-out dataset, not from a large,
long-running production traffic capture. They are useful and defensible for a
project report, but they are still lab results.
