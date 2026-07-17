# FlowGuard Real-PCAP Case Study

## Dataset

A 24 MB PCAP containing network traffic from an infected Android device was
processed through the complete FlowGuard pipeline.

## Pipeline

1. C++ and libpcap parsed the raw packet capture.
2. Packets were grouped into bidirectional network flows.
3. Flow statistics were written to JSONL.
4. The FastAPI service normalized each flow.
5. Isolation Forest, Random Forest and Autoencoder predictions were combined
   using a 2-of-3 voting rule.
6. Generated alerts were persisted in PostgreSQL.

## Results

- Raw PCAP size: approximately 24 MB
- Extracted flows: 799
- Model-generated alerts: 723
- Alert rate: 90.5%
- Low-severity alerts: 655
- Critical-severity alerts: 68
- Random Forest PortScan classifications: 69
- Random Forest BENIGN classifications among alerts: 654
- Threat-intelligence matches: 0

## Interpretation

The high alert rate must not be treated as detection accuracy because this PCAP
does not provide a ground-truth label for every individual flow.

Most low-severity alerts occurred when Isolation Forest and the Autoencoder
marked traffic as unusual while Random Forest classified it as BENIGN. This
indicates model disagreement and possible dataset distribution shift.

The CICIDS2017 external evaluation further showed that models trained primarily
on synthetic data do not generalize reliably to real traffic. The next phase is
to retrain and calibrate the models using CICIDS2017 training, validation and
held-out test partitions.
