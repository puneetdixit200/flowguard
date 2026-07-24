Tue, Jun 30 at 11:16 PM
flowguard.md
File
IM GOING OT BUILD THTA TJUST UNDERSTAND IT , AND WELL CONTINUE , IF YOU UNSERSTTOOD JSUT SAY YES


flowguard main  ❯ cd capture-cpp/build
cmake .. && make
./flowguard_capture
zoxide: no match found
Error: Directory not found
CMake Warning:
  Ignoring extra path from command line:

   ".."


CMake Error: The source directory "/home/pd/Downloads" does not appear to contain CMakeLists.txt.
Specify --help for usage, or press the help button on the CMake GUI.
bash: ./flowguard_capture: No such file or directory

flowguard main  ✗?

Sat, Jul 4 at 11:23 PM
?

out of 3

Total Test time (real) =   0.11 sec

…/capture-cpp/build main  ? ❯ cd ml-service
pip install pytest httpx
pytest tests/ -v
󱞩 /home/pd/Downloads/flowguard/ml-service
Collecting pytest
  Downloading pytest-9.1.1-py3-none-any.whl.metadata (7.6 kB)
Collecting httpx
  Downloading httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting iniconfig>=1.0.1 (from pytest)
  Downloading iniconfig-2.3.0-py3-none-any.whl.metadata (2.5 kB)
Requirement already satisfied: packaging>=22 in /home/pd/.local/lib/python3.12/site-packages (from pytest) (26.2)
Collecting pluggy<2,>=1.5 (from pytest)
  Downloading pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
Requirement already satisfied: pygments>=2.7.2 in /home/pd/.local/lib/python3.12/site-packages (from pytest) (2.20.0)
Requirement already satisfied: anyio in /home/pd/.local/share/mise/installs/python/3.12.13/lib/python3.12/site-packages (from httpx) (4.14.1)
Collecting certifi (from httpx)
  Downloading certifi-2026.6.17-py3-none-any.whl.metadata (2.5 kB)
Collecting httpcore==1.* (from httpx)
  Downloading httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
Requirement already satisfied: idna in /home/pd/.local/share/mise/installs/python/3.12.13/lib/python3.12/site-packages (from httpx) (3.18)
Requirement already satisfied: h11>=0.16 in /home/pd/.local/share/mise/installs/python/3.12.13/lib/python3.12/site-packages (from httpcore==1.*->httpx) (0.16.0)
Requirement already satisfied: typing_extensions>=4.5 in /home/pd/.local/lib/python3.12/site-packages (from anyio->httpx) (4.15.0)
Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)
Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
Downloading certifi-2026.6.17-py3-none-any.whl (133 kB)
Installing collected packages: pluggy, iniconfig, certifi, pytest, httpcore, httpx
Successfully installed certifi-2026.6.17 httpcore-1.0.9 httpx-0.28.1 iniconfig-2.3.0 pluggy-1.6.0 pytest-9.1.1
============================================================== test session starts ===============================================================
platform linux -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0 -- /home/pd/.local/share/mise/installs/python/3.12.13/bin/python3.12
cachedir: .pytest_cache
rootdir: /home/pd/Downloads/flowguard/ml-service
plugins: anyio-4.14.1
collected 2 items / 2 errors

===================================================================== ERRORS =====================================================================
_______________________________________________ ERROR collecting tests/test_feature_normalizer.py ________________________________________________
ImportError while importing test module '/home/pd/Downloads/flowguard/ml-service/tests/test_feature_normalizer.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/home/pd/.local/share/mise/installs/python/3.12.13/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_feature_normalizer.py:11: in <module>
    from app.services.feature_normalizer import normalize_flow
app/services/feature_normalizer.py:3: in <module>
    from app.services.feature_normalizer import normalize_flow
E   ImportError: cannot import name 'normalize_flow' from partially initialized module 'app.services.feature_normalizer' (most likely due to a circular import) (/home/pd/Downloads/flowguard/ml-service/tests/../app/services/feature_normalizer.py)
__________________________________________________ ERROR collecting tests/test_inference_api.py __________________________________________________
ImportError while importing test module '/home/pd/Downloads/flowguard/ml-service/tests/test_inference_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/home/pd/.local/share/mise/installs/python/3.12.13/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_inference_api.py:11: in <module>
    from app.main import app
app/main.py:3: in <module>
    from app.services.feature_normalizer import normalize_flow
app/services/feature_normalizer.py:3: in <module>
    from app.services.feature_normalizer import normalize_flow
E   ImportError: cannot import name 'normalize_flow' from partially initialized module 'app.services.feature_normalizer' (most likely due to a circular import) (/home/pd/Downloads/flowguard/ml-service/tests/../app/services/feature_normalizer.py)
============================================================ short test summary info =============================================================
ERROR tests/test_feature_normalizer.py
ERROR tests/test_inference_api.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
=============================================================== 2 errors in 1.64s ================================================================

flowguard/ml-service main  ? ✗
flowguard/ml-service main  ? ✗ builtin cd ~/Downloads/flowguard/ml-service

cat > app/services/feature_normalizer.py <<'PY'
def normalize_flow(flow: dict) -> dict:
    """
    Convert a raw flow dictionary into numeric ML features.

    Input example:
    {
        "packet_count": 10,
        "total_bytes": 5000,
        "duration_seconds": 2.0,
        "syn_count": 3,
        "ack_count": 5,
        "fin_count": 1,
        "rst_count": 0
    }
    """

    duration = max(float(flow.get("duration_seconds", 0.0001)), 0.0001)
    packets = int(flow.get("packet_count", 0))
    total_bytes = int(flow.get("total_bytes", 0))

    syn_count = int(flow.get("syn_count", 0))
    ack_count = int(flow.get("ack_count", 0))
    fin_count = int(flow.get("fin_count", 0))
    rst_count = int(flow.get("rst_count", 0))

    return {
        "duration_seconds": duration,
        "packet_count": packets,
        "total_bytes": total_bytes,
        "bytes_per_sec": total_bytes / duration,
        "packets_per_sec": packets / duration,
        "syn_count": syn_count,
        "ack_count": ack_count,
        "fin_count": fin_count,
        "rst_count": rst_count,
        "syn_ack_ratio": syn_count / max(ack_count, 1),
        "rst_ratio": rst_count / max(packets, 1),
    }
PY

flowguard/ml-service main  ? ❯ touch app/__init__.py
touch app/services/__init__.py
touch app/ml/__init__.py

flowguard/ml-service main  ? ❯ builtin cd ~/Downloads/flowguard/ml-service
python -m pytest -v
============================================================== test session starts ===============================================================
platform linux -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0 -- /home/pd/.local/share/mise/installs/python/3.12/bin/python
cachedir: .pytest_cache
rootdir: /home/pd/Downloads/flowguard/ml-service
plugins: anyio-4.14.1
collected 4 items / 1 error

===================================================================== ERRORS =====================================================================
__________________________________________________ ERROR collecting tests/test_inference_api.py __________________________________________________
ImportError while importing test module '/home/pd/Downloads/flowguard/ml-service/tests/test_inference_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/home/pd/.local/share/mise/installs/python/3.12.13/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_inference_api.py:11: in <module>
    from app.main import app
app/main.py:7: in <module>
    from prepare_cicids_data import FEATURE_COLUMNS  # same order used in training
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ModuleNotFoundError: No module named 'prepare_cicids_data'
============================================================ short test summary info =============================================================
ERROR tests/test_inference_api.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
================================================================ 1 error in 1.82s ================================================================

flowguard/ml-service main  ? ✗ builtin cd ~/Downloads/flowguard/ml-service

cp training/prepare_cicids_data.py prepare_cicids_data.py

flowguard/ml-service main  ? ❯ builtin cd ~/Downloads/flowguard/ml-service
cp training/prepare_cicids_data.py prepare_cicids_data.py
python -m pytest -v
============================================================== test session starts ===============================================================
platform linux -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0 -- /home/pd/.local/share/mise/installs/python/3.12/bin/python
cachedir: .pytest_cache
rootdir: /home/pd/Downloads/flowguard/ml-service
plugins: anyio-4.14.1
collected 4 items / 1 error

===================================================================== ERRORS =====================================================================
__________________________________________________ ERROR collecting tests/test_inference_api.py __________________________________________________
tests/test_inference_api.py:11: in <module>
    from app.main import app
app/main.py:19: in <module>
    detector = EnsembleDetector()
               ^^^^^^^^^^^^^^^^^^
app/ml/ensemble.py:24: in __init__
    self.iso_forest = joblib.load(os.path.join(MODEL_DIR, "iso_forest.joblib"))
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/home/pd/.local/share/mise/installs/python/3.12.13/lib/python3.12/site-packages/joblib/numpy_pickle.py:735: in load
    with open(filename, "rb") as f:
         ^^^^^^^^^^^^^^^^^^^^
E   FileNotFoundError: [Errno 2] No such file or directory: '/home/pd/Downloads/flowguard/ml-service/tests/../app/ml/../models/iso_forest.joblib'
============================================================ short test summary info =============================================================
ERROR tests/test_inference_api.py - FileNotFoundError: [Errno 2] No such file or directory: '/home/pd/Downloads/flowguard/ml-service/tests/../app/ml/../models/iso_forest.joblib'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
================================================================ 1 error in 1.71s ================================================================

flowguard/ml-service main  ? ✗

 what are these erros?

 now help me run 

 any change to be made?

tell em what to write in docker file for this frontend

?

Great — the eBPF object compiled successfully.

Now compile the userspace loader:

gcc \
  -O2 \
  -g \
  loader.c \
  -o loader \
  $(pkg-config --cflags --libs libbpf)

Then verify:

file loader

Next, find your active interface:

ip route | awk '/default/ {print $5; exit}'

Then run:

sudo ./loader "$(ip route | awk '/default/ {print $5; exit}')"

You should see something like:

XDP program attached to wlan0.
Press Ctrl+C to stop.

Then network events should start printing.

Press Ctrl+C to detach safely.

done thne?

Then your eBPF capture layer is working.

Next steps:

    Keep the loader running and confirm events appear.

    Press Ctrl+C and check that it says the XDP program detached.

    Then connect the loader output to FlowGuard by writing each event as JSONL into:

/home/pd/Downloads/flowguard/data/flows_output.jsonl

After that, start the FastAPI service and dashboard.

For now, run:

sudo ./loader "$(ip route | awk '/default/ {print $5; exit}')"

Generate some traffic in another terminal:

ping -c 4 8.8.8.8

or:

curl https://example.com

You should see packet lines in the loader terminal.

done move forward tella coring to this Let's get this fully running end to end, capture the real metrics, and then write a resume-ready README. I'll break this into 6 clean phases you run in order.

## Phase 1: Install everything (one-time)

bash
sudo pacman -Syu
sudo pacman -S base-devel cmake gcc libpcap postgresql redis python python-pip nodejs npm clang llvm libbpf bpftool linux-headers git

# Initialize and start Postgres
sudo -u postgres initdb --locale en_US.UTF-8 -D /var/lib/postgres/data
sudo systemctl enable --now postgresql
sudo systemctl status postgresql

# Start Redis
sudo systemctl enable --now redis
sudo systemctl status redis



Create the database:

bash
sudo -u postgres psql -c "CREATE DATABASE flowguard; CREATE USER flowguard_user WITH PASSWORD 'flowguard_pass'; GRANT ALL PRIVILEGES ON DATABASE flowguard TO flowguard_user;"



If both 
systemctl status commands show active (running), you're clear to move on — this two-service setup (Postgres + Redis) matches the standard Arch install flow. [medium](https://medium.com/@rigenskylouisz/setting-up-postgresql-step-by-step-arch-linux-4b8d9fc7602b)

## Phase 2: Build the C++ capture layer

bash
cd ~/flowguard/capture-cpp
mkdir -p build && cd build
cmake ..
make
./flowguard_capture



Expected output: a printed 
FLOW SUMMARY block. If it errors on pcap_open_offline, confirm data/sample/small_sample.pcap exists at the relative path in main.cpp.

## Phase 3: Set up the ML/API service

bash
cd ~/flowguard/ml-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install prisma redis networkx torch-geometric

# Set up Prisma + Postgres tables
prisma generate
prisma migrate dev --name init



Generate the harder synthetic dataset and train all 4 models:

bash
cd training
python generate_sample_dataset.py
python train_isolation_forest.py
python train_random_forest.py
python train_autoencoder.py
python train_gnn.py



Now start the API:

bash
cd ..
uvicorn app.main:app --reload



Visit 
http://127.0.0.1:8000/health — you should see {"status":"ok"}.

## Phase 4: Run the honest 4-model evaluation and save the numbers

bash
cd ~/flowguard/ml-service/training
python evaluate_models.py > ../../docs/evaluation_report.txt
cat ../../docs/evaluation_report.txt



You have completed package installation, PostgreSQL, Valkey, and the eBPF build. Continue from database creation, using your actual project path.
Phase 1B: Create the FlowGuard database

Run these separately:

sudo -iu postgres psql -c "CREATE USER flowguard_user WITH PASSWORD 'flowguard_pass';"

sudo -iu postgres psql -c "CREATE DATABASE flowguard OWNER flowguard_user;"

Test the connection:

PGPASSWORD=flowguard_pass psql \
  -h 127.0.0.1 \
  -U flowguard_user \
  -d flowguard \
  -c "SELECT current_database(), current_user;"

Expected:

current_database | current_user
flowguard         | flowguard_user

If it says the user or database already exists, that is fine. Continue.
Phase 2: Build and run the C++ capture layer

builtin cd /home/pd/Downloads/flowguard/capture-cpp

mkdir -p build
builtin cd build

cmake ..

cmake --build . -j"$(nproc)"

Run the existing capture program:

./flowguard_capture

Check that the output file contains flows:

wc -l /home/pd/Downloads/flowguard/data/flows_output.jsonl

head -n 2 /home/pd/Downloads/flowguard/data/flows_output.jsonl

Since your eBPF loader is also working, you currently have:

Offline PCAP capture → capture-cpp
Live packet capture  → capture-ebpf

Phase 3: Set up the Python ML service

Enter the service folder:

builtin cd /home/pd/Downloads/flowguard/ml-service

Create the virtual environment only if it does not already exist:

python -m venv .venv

Activate it:

source .venv/bin/activate

Upgrade installation tools:

python -m pip install --upgrade pip setuptools wheel

Install project dependencies:

pip install -r requirements.txt

Install the additional dependencies:

pip install prisma redis networkx torch torch-geometric

Verify imports:

python -c "
import fastapi
import redis
import networkx
import torch
import torch_geometric
print('All Python dependencies imported successfully')
"

Configure PostgreSQL and Valkey

Check whether the project already has an environment file:

ls -la

Create or edit .env:

nano .env

Put this inside:

DATABASE_URL="postgresql://flowguard_user:flowguard_pass@127.0.0.1:5432/flowguard"
REDIS_URL="redis://127.0.0.1:6379/0"

Valkey supports the Redis protocol, so the Python redis package and redis:// address are correct.

Save in Nano:

Ctrl+O
Enter
Ctrl+X

Prisma setup

First verify that a Prisma schema exists:

find . -name "schema.prisma" -print

If it prints a path such as:

./prisma/schema.prisma

run:

prisma generate

Then:

prisma migrate dev --name init

If no schema.prisma file is found, skip Prisma for now rather than running migration commands blindly.
Train the four models

builtin cd /home/pd/Downloads/flowguard/ml-service/training

First inspect the available scripts:

ls

Run the dataset generator:

python generate_sample_dataset.py

Train Isolation Forest:

python train_isolation_forest.py

Train Random Forest:

python train_random_forest.py

Train Autoencoder:

python train_autoencoder.py

Train the Graph Neural Network:

python train_gnn.py

After training, find the generated model files:

find .. -type f \( \
  -name "*.pkl" -o \
  -name "*.joblib" -o \
  -name "*.pt" -o \
  -name "*.pth" \
\) -print

Start the FastAPI service

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

Start it without reload first:

uvicorn app.main:app --host 127.0.0.1 --port 8000

Keep that terminal open.

In a second terminal, test:

curl http://127.0.0.1:8000/health

Expected:

{"status":"ok"}

Test recent flows:

curl "http://127.0.0.1:8000/flows/recent?limit=5"

Run analysis:

curl -X POST http://127.0.0.1:8000/analyze

View alerts:

curl http://127.0.0.1:8000/alerts

Phase 4: Run the evaluation

With the virtual environment active:

builtin cd /home/pd/Downloads/flowguard/ml-service/training

Ensure the documentation directory exists:

mkdir -p /home/pd/Downloads/flowguard/docs

Run evaluation and save the output:

python evaluate_models.py \
  | tee /home/pd/Downloads/flowguard/docs/evaluation_report.txt

Check the saved report:

cat /home/pd/Downloads/flowguard/docs/evaluation_report.txt

Start now with the two PostgreSQL creation commands, then proceed to the C++ build. Stop only at the first actual error.

Today 8:18 PM
Straight answer: **no, not fully** — and it's worth being precise about exactly what's tested and what isn't, because this gap matters a lot for your resume honesty.

## What IS actually tested (3 of 4 models)

| Model | Accuracy/F1 tested? | Where |
|---|---|---|
| Isolation Forest | Yes — held-out F1 0.8175, real CICIDS2017 F1 0.3232 | evaluation_report.txt, real_data_evaluation.txt |
| Random Forest | Yes — held-out 95.21%, real CICIDS2017 collapsed to 0% recall | Same files |
| Autoencoder | Yes — held-out F1 0.7737 | evaluation_report.txt |
| **GraphSAGE GNN (4th ensemble member)** | **No — never evaluated** | Trained (gnn_graphsage.pt exists) but no accuracy/F1/precision/recall numbers anywhere in your logs |

The case-study.md follow-up work section says this explicitly: "either wire the saved GNN into the live API path or explicitly treat it as offline-only" — meaning as of your last verified run, the GNN is trained but sitting unused, not scored, and not part of the ensemble vote. Every ensemble metric you have (98.94% accuracy, 0.9541 F1) is from **3 models**, not 4.

## What IS tested for kernel-layer speed (also incomplete)

Looking at your logs, capture-ebpf/loader and xdp_filter.o exist as **built artifacts**, but none of your attached logs (benchmark_output.txt, real_pcap_capture.log, real_pcap_persist.log) contain any timing comparison between the libpcap path and the eBPF/XDP path. There's no packets/sec, no latency-per-packet, no side-by-side number showing kernel-space filtering was actually faster than userspace libpcap. The eBPF component compiled successfully, but it was never benchmarked against libpcap.

## What this means for your resume right now

You currently have real, defensible numbers for:
- 3-model ensemble accuracy/precision/recall/F1 (held-out AND real CICIDS2017)
- C++ flow aggregation working end-to-end on a real 24MB infected-Android pcap (799 flows extracted)

You do **not yet have** real numbers for:
- GNN accuracy/precision/recall/F1 (untested)
- eBPF/XDP vs libpcap speed comparison (unbenchmarked)

Claiming either of these on a resume right now would be the exact overclaiming your false-positive-analysis.md explicitly tries to avoid.

## Fix it — two scripts to close both gaps

### 1. Evaluate the GNN

python
# ml-service/training/evaluate_gnn.py
"""
Scores the trained GraphSAGE GNN on the same held-out test set used for
the other 3 models, so we get a real, comparable accuracy/F1 number
instead of leaving the GNN untested.
"""
import pandas as pd
import torch
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from app.ml.graph_builder import build_ip_graph, graph_to_pyg_data
from app.ml.gnn_model import FlowGraphSAGE

df = pd.read_csv("../data/sample/test_holdout.csv")
flows = df.to_dict("records")

# Build the same IP graph structure used at training time.
G = build_ip_graph(flows)
data, node_list = graph_to_pyg_data(G)

meta = torch.load("../app/models/gnn_meta.pt")
model = FlowGraphSAGE(in_channels=data.x.shape [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/31875035/7a728a34-2b6c-44e1-bb85-9fc883434b83/app-tree.md?AWSAccessKeyId=ASIA2F3EMEYE3WFSRZU7&Signature=JxX0gJqF56i1srGOWfCnuaWuZsI%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEK%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQC3SCRUOFfsvkZelLe7p7jQ8aVh02irjNyK2klFGWo6IgIhAKzuqhWqt5TMcgsT2Bjv3dl%2BEGT4lXbG%2B9IiirvJopMoKvMECHcQARoMNjk5NzUzMzA5NzA1Igylyz3yEHDycR11PzIq0AS03PQkvmd5t6o43tlJGDfHR1JEaFwsNYiFcupbPpDAi2CMTW65UzOTQ%2BcqhmwHfXzQVHXM0cp%2FfDqDvmNkwr1jYm7Vwz%2FFQaPKQHSPSiO%2FyPiLMlVQmXUtFDwH0HfdZ2obm9qWzKlQ0WT1lqiGzDQTLm1YCa%2B55AXP5ymRNZceSoRxnaArcx1j3D11mg8HSBsoVBc2zLGzPehFzqfYst9QncU9DCdaspycrY4QnfGCD1kXfhGLMu0NQLTinXg0YSW%2B3GglLLwbbnbbCZI3VQLdtLr1oioeqJBz3MQg8umCh7%2B9T6bxGiVAmjenJe7eqUBTibNUtXxQRytQr7LdkLZJYcs42VnAoW46FRa4ZDCmA0f9l2zEbv7NBoLgmIdYCxzV2M%2FulHVFyYNpWUQAB1Ug0k67n3DFW07T9qXTXeiqKtnqLJHR28aDBwLJPtVagerOVbISKabSwWXazrnpQIeKwuOxMhGeyh8ipsjLu9X4Pu58NMl63qM6nxndiRsFQ5ELJQoqCGBT1Dk%2F1lwinALHm3flVIlmxdfcjR3dE3T4Wk%2BrPI3%2Fa6eul7cA1gMo2b8GIkyrCRIIyi9VPVV8CHo%2FjmJSfFTtvjJYz%2Fn88xDZvkBCFyDHZg4r1ZE938KTGYHXikd0cFYftp5%2B63wZzBamvo0sJHBIgWLUNADCcfEQymObG%2BkqZtgjNqSE3fwMjTKkdN1UIUu04hX3i6%2Bx3pdluNsF%2B%2B0xpW5fTkGhz1z8RzB4sZJIE%2B1fZwQl%2FM2plUeoMC82PiS0l%2BVBCqLuvuFFMNuR7tIGOpcB9fm%2F6Er4Gql%2BgWhMqFlU3e67vmIZAL4fpcrWNLYbM7LL6pErdD%2BNwYqHs%2BjbjflfWy9emCZajJC39q%2FVT5yEg2CMDnT29%2F2HPYaJG6MNWBzAvkbsYrr2EST%2FeitIZyhfQ9%2BtyC893RwRvkau0MP%2FuEIYIDptkeh81xAuJ4GBNmuxG1%2FdGVgUYDmzBI8NDmrXW2VK4fgwwA%3D%3D&Expires=1784387246))
model.load_state_dict(torch.load("../app/models/gnn_graphsage.pt"))
model.eval()

with torch.no_grad():
    logits = model(data.x, data.edge_index)
    preds = logits.argmax(dim=1).numpy()

# Map node-level predictions back to flow-level ground truth so this is
# comparable to the other 3 models' flow-level scores.
node_to_label = {}
for f in flows:
    is_attack = 1 if f["Label"] != "BENIGN" else 0
    node_to_label[f["src_ip"]] = max(node_to_label.get(f["src_ip"], 0), is_attack)

y_true = [node_to_label.get(ip, 0) for ip in node_list]
y_pred = [1 if p == 1 else 0 for p in preds]

print("===== GNN (GraphSAGE) EVALUATION =====")
print(f"Accuracy:  {accuracy_score(y_true, y_pred):.4f}")
print(f"Precision: {precision_score(y_true, y_pred, zero_division=0):.4f}")
print(f"Recall:    {recall_score(y_true, y_pred, zero_division=0):.4f}")
print(f"F1:        {f1_score(y_true, y_pred, zero_division=0):.4f}")
print(f"Confusion matrix:\n{confusion_matrix(y_true, y_pred)}")



bash
cd ~/flowguard/ml-service/training
python evaluate_gnn.py | tee ../../docs/gnn_evaluation.txt



### 2. Benchmark eBPF/XDP vs libpcap

bash
# libpcap path — time it directly
cd ~/flowguard/capture-cpp/build
time ./flowguard_capture ../../data/attack_samples/*.pcap > /tmp/libpcap_run.log 2>&1

# eBPF/XDP path — needs a live interface, run for a fixed window
cd ~/flowguard/capture-ebpf
sudo timeout 15 ./loader lo 2>&1 | tee /tmp/ebpf_run.log
# count events captured in that fixed 15-second window
wc -l /tmp/ebpf_run.log



Save both outputs into 
docs/kernel_speed_comparison.md with real wall-clock time and packet/event counts side by side — that's the only way to get a legitimate "X% faster" number instead of a guess.

Once you run both of these and get real output, paste the results here and I'll add them into your resume keywords doc as verified numbers — and update the "what NOT to say" section to correctly caveat whichever one still isn't fully wired in. i hav todo this , 


flowguard/ml-service main ? ❯ source .venv/bin/activate

flowguard/ml-service main ? ❯ python evaluate_gnn.py | tee ../../docs/gnn_evaluation.txt
tee: ../../docs/gnn_evaluation.txt: No such file or directory
python: can't open file '/home/pd/Downloads/flowguard/ml-service/evaluate_gnn.py': [Errno 2] No such file or directory

flowguard/ml-service main ? ✗ ls
Permissions Size User Date Modified Name
drwxr-xr-x     - pd   17 Jul 16:15   __pycache__
drwxr-xr-x     - pd   17 Jul 16:20   app
drwxr-xr-x     - pd   18 Jul 17:14   data
drwxr-xr-x     - pd   17 Jul 15:48   prisma
drwxr-xr-x     - pd   17 Jul 19:42   scripts
drwxr-xr-x     - pd    9 Jul 07:52   tests
drwxr-xr-x     - pd   18 Jul 20:15   training
.rw-r--r--   459 pd   17 Jul 16:52   docker-entrypoint.sh
.rw-r--r--   914 pd   17 Jul 16:54   Dockerfile
.rw-r--r--   373 pd    9 Jul 08:54   prepare_cicids_data.py
.rw-r--r--   107 pd   12 Jul 12:32   requirements.txt

flowguard/ml-service main ? ❯ cd training

…/ml-service/training main ? ❯ python evaluate_gnn.py | tee ../../docs/gnn_evaluation.txt
Traceback (most recent call last):
  File "/home/pd/Downloads/flowguard/ml-service/training/evaluate_gnn.py", line 11, in <module>
    from app.ml.graph_builder import build_ip_graph, graph_to_pyg_data
ModuleNotFoundError: No module named 'app'

…/ml-service/training main ? ❯ # libpcap path — time it directly
cd ~/flowguard/capture-cpp/build
time ./flowguard_capture ../../data/attack_samples/*.pcap > /tmp/libpcap_run.log 2>&1

# eBPF/XDP path — needs a live interface, run for a fixed window
cd ~/flowguard/capture-ebpf
sudo timeout 15 ./loader lo 2>&1 | tee /tmp/ebpf_run.log
# count events captured in that fixed 15-second window
wc -l /tmp/ebpf_run.log
zoxide: no match found
Error: Directory not found

real	0m0.001s
user	0m0.000s
sys	0m0.001s
zoxide: no match found
Error: Directory not found
[sudo] password for pd:
timeout: failed to run command ‘./loader’: No such file or directory
1 /tmp/ebpf_run.log

…/ml-service/training main ? ❯

flowguard/ml-service main ? ❯ source .venv/bin/activate

flowguard/ml-service main ? ❯ python evaluate_gnn.py | tee ../../docs/gnn_evaluation.txt
tee: ../../docs/gnn_evaluation.txt: No such file or directory
python: can't open file '/home/pd/Downloads/flowguard/ml-service/evaluate_gnn.py': [Errno 2] No such file or directory

flowguard/ml-service main ? ✗ ls
Permissions Size User Date Modified Name
drwxr-xr-x     - pd   17 Jul 16:15   __pycache__
drwxr-xr-x     - pd   17 Jul 16:20   app
drwxr-xr-x     - pd   18 Jul 17:14   data
drwxr-xr-x     - pd   17 Jul 15:48   prisma
drwxr-xr-x     - pd   17 Jul 19:42   scripts
drwxr-xr-x     - pd    9 Jul 07:52   tests
drwxr-xr-x     - pd   18 Jul 20:15   training
.rw-r--r--   459 pd   17 Jul 16:52   docker-entrypoint.sh
.rw-r--r--   914 pd   17 Jul 16:54   Dockerfile
.rw-r--r--   373 pd    9 Jul 08:54   prepare_cicids_data.py
.rw-r--r--   107 pd   12 Jul 12:32   requirements.txt

flowguard/ml-service main ? ❯ cd training

…/ml-service/training main ? ❯ python evaluate_gnn.py | tee ../../docs/gnn_evaluation.txt
Traceback (most recent call last):
  File "/home/pd/Downloads/flowguard/ml-service/training/evaluate_gnn.py", line 11, in <module>
    from app.ml.graph_builder import build_ip_graph, graph_to_pyg_data
ModuleNotFoundError: No module named 'app'

…/ml-service/training main ? ❯ # libpcap path — time it directly
cd ~/flowguard/capture-cpp/build
time ./flowguard_capture ../../data/attack_samples/*.pcap > /tmp/libpcap_run.log 2>&1

# eBPF/XDP path — needs a live interface, run for a fixed window
cd ~/flowguard/capture-ebpf
sudo timeout 15 ./loader lo 2>&1 | tee /tmp/ebpf_run.log
# count events captured in that fixed 15-second window
wc -l /tmp/ebpf_run.log
zoxide: no match found
Error: Directory not found

real	0m0.001s
user	0m0.000s
sys	0m0.001s
zoxide: no match found
Error: Directory not found
[sudo] password for pd:
timeout: failed to run command ‘./loader’: No such file or directory
1 /tmp/ebpf_run.log

…/ml-service/training main ? ❯ help me

Your commands failed for three simple reasons:

    Your project is in /home/pd/Downloads/flowguard, not ~/flowguard.

    Python cannot find app because ml-service is not in PYTHONPATH.

    The benchmark never ran—the cd failed, so both commands executed from training.

The 0.001s and 1 /tmp/ebpf_run.log results are invalid and must not be used.
Step 1: Run the GNN evaluation correctly

Run exactly this:

builtin cd /home/pd/Downloads/flowguard/ml-service/training

source ../.venv/bin/activate

mkdir -p /home/pd/Downloads/flowguard/docs

PYTHONPATH=/home/pd/Downloads/flowguard/ml-service \
python evaluate_gnn.py \
| tee /home/pd/Downloads/flowguard/docs/gnn_evaluation.txt

The important part is:

PYTHONPATH=/home/pd/Downloads/flowguard/ml-service

It tells Python:

Search for the app package inside ml-service/

Your directory structure is:

flowguard/
├── docs/
└── ml-service/
    ├── app/
    └── training/
        └── evaluate_gnn.py

Without PYTHONPATH, Python starts searching from training/ and cannot see its sibling directory app/.
Permanent fix for evaluate_gnn.py

Add this near the top of the file, before importing anything from app:

from pathlib import Path
import sys

# ml-service/
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Allow imports such as: from app.ml...
sys.path.insert(0, str(PROJECT_ROOT))

Then these imports will work without manually setting PYTHONPATH:

from app.ml.graph_builder import build_ip_graph, graph_to_pyg_data
from app.ml.gnn_model import FlowGraphSAGE

For now, use the shell command first.
Step 2: Verify the files used by the GNN script

Before evaluating, you can inspect the actual paths:

builtin cd /home/pd/Downloads/flowguard/ml-service/training

find ../app/models -maxdepth 2 -type f -print | sort

You should find files resembling:

../app/models/gnn_graphsage.pt
../app/models/gnn_meta.pt

Check datasets:

find ../data -type f -print | sort

Check the graph code:

find ../app/ml -maxdepth 2 -type f -print | sort

You should find files resembling:

../app/ml/graph_builder.py
../app/ml/gnn_model.py

If test_holdout.csv is not at:

ml-service/data/sample/test_holdout.csv

locate it with:

find /home/pd/Downloads/flowguard \
  -type f \
  -name "test_holdout.csv" \
  -print

Step 3: Confirm the eBPF loader exists

Use the correct absolute path:

builtin cd /home/pd/Downloads/flowguard/capture-ebpf

Check files:

pwd
ls -lh loader loader.c xdp_filter.o xdp_filter.c

If loader does not exist, compile it:

gcc \
  -O2 \
  -g \
  loader.c \
  -o loader \
  $(pkg-config --cflags --libs libbpf)

Verify:

file loader

It should report an executable such as:

ELF 64-bit LSB pie executable, x86-64

Step 4: Run an eBPF functionality test

Find your active network interface:

INTERFACE="$(ip route | awk '/default/ {print $5; exit}')"
echo "$INTERFACE"

It may print something such as:

wlan0

or:

wlp2s0

Start traffic generation in the background:

(
  sleep 2
  ping -c 20 1.1.1.1 >/dev/null
  curl -s https://example.com >/dev/null
) &

Run the loader for 15 seconds:

sudo timeout --signal=INT 15 \
  ./loader "$INTERFACE" \
  2>&1 | tee /tmp/ebpf_run.log

Inspect the result:

cat /tmp/ebpf_run.log

Count all output lines:

wc -l /tmp/ebpf_run.log

This confirms that the eBPF/XDP path works, but it is not yet a fair speed benchmark.
Step 5: Run the C++ libpcap path correctly

Use the real path:

builtin cd /home/pd/Downloads/flowguard/capture-cpp/build

Verify the executable:

ls -lh ./flowguard_capture

Run and time it:

{
  time ./flowguard_capture
} > /tmp/libpcap_run.log 2> /tmp/libpcap_time.log

View its output:

cat /tmp/libpcap_run.log

View timing:

cat /tmp/libpcap_time.log

Check the flows generated:

wc -l /home/pd/Downloads/flowguard/data/flows_output.jsonl

Do not use this command yet:

./flowguard_capture ../../data/attack_samples/*.pcap

Your current C++ program may not accept command-line PCAP paths. The wildcard could also pass several files even when the program expects only one.

Check whether it accepts arguments:

grep -RIn "argc\|argv\|pcap_open_offline" \
  /home/pd/Downloads/flowguard/capture-cpp/src \
  /home/pd/Downloads/flowguard/capture-cpp/include

Important: this is not yet a fair XDP-versus-libpcap benchmark

These two workloads are different:

libpcap → reads a saved PCAP file as quickly as possible
eBPF/XDP → waits for live packets arriving over 15 seconds

Therefore, you cannot calculate:

XDP is X% faster

from those results.

A legitimate comparison requires:

                    Same PCAP
                       │
            ┌──────────┴──────────┐
            ▼                     ▼
     libpcap offline       replay through interface
            │                     │
            ▼                     ▼
      C++ processing          XDP processing
            │                     │
            └──── same packet count ────┘

It also requires disabling per-packet printing because terminal output is much slower than packet processing and would distort the eBPF result.

For now, run the GNN evaluation command first:

builtin cd /home/pd/Downloads/flowguard/ml-service/training

PYTHONPATH=/home/pd/Downloads/flowguard/ml-service \
python evaluate_gnn.py \
| tee /home/pd/Downloads/flowguard/docs/gnn_evaluation.txt

Stop at the first new traceback and paste that full traceback.



…/ml-service/training main ? ❯ builtin cd /home/pd/Downloads/flowguard/ml-service/training

source ../.venv/bin/activate

mkdir -p /home/pd/Downloads/flowguard/docs

PYTHONPATH=/home/pd/Downloads/flowguard/ml-service \
python evaluate_gnn.py \
| tee /home/pd/Downloads/flowguard/docs/gnn_evaluation.txt
Traceback (most recent call last):
  File "/home/pd/Downloads/flowguard/ml-service/training/evaluate_gnn.py", line 18, in <module>
    G = build_ip_graph(flows)
  File "/home/pd/Downloads/flowguard/ml-service/app/ml/graph_builder.py", line 17, in build_ip_graph
    src, dst = flow["src_ip"], flow["dst_ip"]
               ~~~~^^^^^^^^^^
KeyError: 'src_ip'

…/ml-service/training main ? ❯ from pathlib import Path
import sys

# ml-service/
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Allow imports such as: from app.ml...
sys.path.insert(0, str(PROJECT_ROOT))
bash: command not found: from
from app.ml.graph_builder import build_ip_graph, graph_to_pyg_data
from app.ml.gnn_model import FlowGraphSAGE  , # ml-service/training/evaluate_gnn.py
"""
Scores the trained GraphSAGE GNN on the same held-out test set used for
the other 3 models, so we get a real, comparable accuracy/F1 number
instead of leaving the GNN untested.
"""
import pandas as pd
import torch
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from app.ml.graph_builder import build_ip_graph, graph_to_pyg_data
from app.ml.gnn_model import FlowGraphSAGE

df = pd.read_csv("../data/sample/test_holdout.csv")
flows = df.to_dict("records")

# Build the same IP graph structure used at training time.
G = build_ip_graph(flows)
data, node_list = graph_to_pyg_data(G)

meta = torch.load("../app/models/gnn_meta.pt")
model = FlowGraphSAGE(in_channels=data.x.shape[1])
model.load_state_dict(torch.load("../app/models/gnn_graphsage.pt"))
model.eval()

with torch.no_grad():
    logits = model(data.x, data.edge_index)
    preds = logits.argmax(dim=1).numpy()

# Map node-level predictions back to flow-level ground truth so this is
# comparable to the other 3 models' flow-level scores.
node_to_label = {}
for f in flows:
    is_attack = 1 if f["Label"] != "BENIGN" else 0
    node_to_label[f["src_ip"]] = max(node_to_label.get(f["src_ip"], 0), is_attack)

y_true = [node_to_label.get(ip, 0) for ip in node_list]
y_pred = [1 if p == 1 else 0 for p in preds]

print("===== GNN (GraphSAGE) EVALUATION =====")
print(f"Accuracy:  {accuracy_score(y_true, y_pred):.4f}")
print(f"Precision: {precision_score(y_true, y_pred, zero_division=0):.4f}")
print(f"Recall:    {recall_score(y_true, y_pred, zero_division=0):.4f}")
print(f"F1:        {f1_score(y_true, y_pred, zero_division=0):.4f}")
print(f"Confusion matrix:\n{confusion_matrix(y_true, y_pred)}")
 , telll one liners to to fix and work

Your import issue is fixed. The new problem is that test_holdout.csv does not contain src_ip and dst_ip.

Run these one at a time.
1. Show the dataset columns

python -c "import pandas as pd; print(pd.read_csv('../data/sample/test_holdout.csv', nrows=1).columns.tolist())"

2. Find a CSV that actually contains src_ip and dst_ip

python -c "import glob,pandas as pd; [print(f) for f in glob.glob('../data/**/*.csv',recursive=True) if {'src_ip','dst_ip'}.issubset(set(pd.read_csv(f,nrows=1).columns))]"

3. Check which dataset train_gnn.py originally used

grep -nE "read_csv|src_ip|dst_ip|build_ip_graph" train_gnn.py

4. Do not paste Python imports directly into Bash

To add the Python path fix automatically:

sed -i '1i from pathlib import Path\nimport sys\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n' evaluate_gnn.py

5. Run again after replacing the incorrect CSV path

PYTHONPATH=/home/pd/Downloads/flowguard/ml-service python evaluate_gnn.py | tee /home/pd/Downloads/flowguard/docs/gnn_evaluation.txt

The important point: do not rename random feature columns to src_ip and dst_ip. A Graph Neural Network requires the original IP relationships. Paste the output of commands 1–3, and the correct dataset path can be substituted exactly.


flowguard main ? ✗ builtin cd /home/pd/Downloads/flowguard/ml-service/training

source ../.venv/bin/activate

…/ml-service/training main ? ❯ python -c "import pandas as pd; print(pd.read_csv('../data/sample/test_holdout.csv', nrows=1).columns.tolist())"
['duration_seconds', 'packet_count', 'total_bytes', 'bytes_per_sec', 'packets_per_sec', 'syn_count', 'ack_count', 'fin_count', 'rst_count', 'syn_ack_ratio', 'rst_ratio', 'Label']

…/ml-service/training main ? ❯ python -c "import glob,pandas as pd; [print(f) for f in glob.glob('../data/**/*.csv',recursive=True) if {'src_ip','dst_ip'}.issubset(set(pd.read_csv(f,nrows=1).columns))]"

…/ml-service/training main ? ❯ grep -nE "read_csv|src_ip|dst_ip|build_ip_graph" train_gnn.py
47:                "src_ip": ip, "dst_ip": peer, "protocol": "TCP",
58:                "src_ip": ip, "dst_ip": peer, "protocol": "TCP",
75:    from app.ml.graph_builder import build_ip_graph
76:    G = build_ip_graph(flows)

…/ml-service/training main ? ❯ sed -i '1i from pathlib import Path\nimport sys\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n' evaluate_gnn.py

…/ml-service/training main ? ❯ PYTHONPATH=/home/pd/Downloads/flowguard/ml-service python evaluate_gnn.py | tee /home/pd/Downloads/flowguard/docs/gnn_evaluation.txt
Traceback (most recent call last):
  File "/home/pd/Downloads/flowguard/ml-service/training/evaluate_gnn.py", line 22, in <module>
    G = build_ip_graph(flows)
  File "/home/pd/Downloads/flowguard/ml-service/app/ml/graph_builder.py", line 17, in build_ip_graph
    src, dst = flow["src_ip"], flow["dst_ip"]
               ~~~~^^^^^^^^^^
KeyError: 'src_ip'

…/ml-service/training main ? ❯ ^C

The evaluator cannot use test_holdout.csv because that file has no IP addresses. Your train_gnn.py creates synthetic src_ip and dst_ip values internally.

Run this one command so I can give you the exact working replacement without guessing function names:

nl -ba train_gnn.py | sed -n '1,180p'

Paste its output here. Do not rerun evaluate_gnn.py yet; it will keep producing the same KeyError: 'src_ip'.



…/ml-service/training main ? ✗ nl -ba train_gnn.py | sed -n '1,180p'
     1	"""
     2	Trains the GraphSAGE model. Since we don't have real labeled multi-host
     3	attack graphs, this trains on synthetic graphs: some IPs behave normally,
     4	others simulate scanning behavior (many peers, low bytes each).
     5	Swap this data generator for real flow logs once you have them.
     6	
     7	Train the GraphSAGE model using synthetic network traffic.
     8	
     9	Because we currently do not have enough labelled multi-host attack graphs,
    10	we create fake normal hosts, scanner hosts, and target hosts.
    11	
    12	Normal hosts:
    13	    Contact only a few targets
    14	    Transfer a reasonable amount of data
    15	
    16	Scanner hosts:
    17	    Contact many different targets
    18	    Transfer very few bytes per connection
    19	
    20	Later, this synthetic generator should be replaced with real labelled flows.
    21	"""
    22	
    23	import torch
    24	import torch.nn.functional as F
    25	import networkx as nx
    26	import random
    27	from app.ml.gnn_model import FlowGraphSAGE
    28	from app.ml.graph_builder import graph_to_pyg_data
    29	
    30	
    31	def generate_synthetic_flow_graph(n_normal_hosts=40, n_scanners=5, n_targets=60):
    32	    """
    33	    Builds a synthetic network: normal hosts talk to a few peers with
    34	    real byte volume; scanner hosts touch MANY targets with near-zero bytes
    35	    """
    36	    flows = []
    37	
    38	    normal_ips = [f"10.0.0.{i}" for i in range(n_normal_hosts)]
    39	    scanner_ips = [f"10.0.1.{i}" for i in range(n_scanners)]
    40	    target_ips = [f"10.0.2.{i}" for i in range(n_targets)]
    41	
    42	    # Normal traffic: each normal host talks to 2-5 random targets with real bytes.
    43	    for ip in normal_ips:
    44	        peers = random.sample(target_ips, k=random.randint(2, 5))
    45	        for peer in peers:
    46	            flows.append({
    47	                "src_ip": ip, "dst_ip": peer, "protocol": "TCP",
    48	                "packet_count": random.randint(10, 200),
    49	                "total_bytes": random.randint(2000, 50000),
    50	                "syn_count": random.randint(1, 3),
    51	            })
    52	
    53	    # Scanner traffic: each scanner touches MANY targets, each with tiny bytes.
    54	    for ip in scanner_ips:
    55	        peers = random.sample(target_ips, k=random.randint(30, 60))
    56	        for peer in peers:
    57	            flows.append({
    58	                "src_ip": ip, "dst_ip": peer, "protocol": "TCP",
    59	                "packet_count": random.randint(1, 3),
    60	                "total_bytes": random.randint(40, 120),   # tiny — just a SYN probe
    61	                "syn_count": 1,
    62	            })
    63	
    64	    labels = {}
    65	    for ip in normal_ips + target_ips:
    66	        labels[ip] = 0  # normal
    67	    for ip in scanner_ips:
    68	        labels[ip] = 1  # anomalous (scanner)
    69	
    70	    return flows, labels
    71	
    72	def main():
    73	    flows, labels = generate_synthetic_flow_graph()
    74	    G = nx.DiGraph()
    75	    from app.ml.graph_builder import build_ip_graph
    76	    G = build_ip_graph(flows)
    77	    data ,node_list =graph_to_pyg_data(G)
    78	    #map string labels dict to a tensor alignes with node_list order
    79	    y = torch.tensor([labels.get(ip, 0) for ip in node_list],dtype=torch.long)
    80	    model=FlowGraphSAGE(in_channels=data.x.shape[1],hidden_channels=32,out_channels=2)
    81	    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    82	    model.train()
    83	
    84	    for epoch in range(1,101):
    85	        optimizer.zero_grad()
    86	        out = model(data.x, data.edge_index)
    87	        loss = F.cross_entropy(out, y)
    88	        loss.backward()
    89	        optimizer.step()
    90	        if epoch % 20 == 0:
    91	            pred = out.argmax(dim=1)
    92	            acc = (pred == y).float().mean().item()
    93	            print(f'Epoch {epoch:03d}, Loss: {loss.item():.4f}, Train Accuracy: {acc:.4f}')
    94	
    95	    torch.save(model.state_dict(), "app/models/gnn_graphsage.pt")
    96	    torch.save({"in_channels": data.x.shape[1]}, "app/models/gnn_meta.pt")
    97	    print("GNN model saved -> ../app/models/gnn_graphsage.pt")
    98	
    99	if __name__ == "__main__":
   100	    main()

…/ml-service/training main ? ❯

Your GNN was trained on synthetic IP graphs, so test_holdout.csv cannot evaluate it. Replace evaluate_gnn.py with an evaluation on separate unseen synthetic graphs.

Run this entire block:

cat > /home/pd/Downloads/flowguard/ml-service/training/evaluate_gnn.py <<'PY'
"""
Evaluate the trained GraphSAGE model on unseen synthetic network graphs.

Important:
- This is a node-level synthetic evaluation.
- It is not a real CICIDS2017 evaluation.
- It is not directly comparable to flow-level Random Forest metrics.
"""

from pathlib import Path
import random
import sys

import torch
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

# ml-service/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.ml.gnn_model import FlowGraphSAGE
from app.ml.graph_builder import build_ip_graph, graph_to_pyg_data
from train_gnn import generate_synthetic_flow_graph


MODEL_DIRECTORY = PROJECT_ROOT / "app" / "models"
MODEL_PATH = MODEL_DIRECTORY / "gnn_graphsage.pt"
META_PATH = MODEL_DIRECTORY / "gnn_meta.pt"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"GNN model not found: {MODEL_PATH}")

if not META_PATH.exists():
    raise FileNotFoundError(f"GNN metadata not found: {META_PATH}")


# Load the architecture information saved during training.
metadata = torch.load(META_PATH, map_location="cpu")

model = FlowGraphSAGE(
    in_channels=int(metadata["in_channels"]),
    hidden_channels=32,
    out_channels=2,
)

model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

all_true_labels = []
all_predictions = []

# Evaluate on 20 independently generated graphs that were not used to train.
for test_seed in range(1000, 1020):
    random.seed(test_seed)
    torch.manual_seed(test_seed)

    flows, labels = generate_synthetic_flow_graph(
        n_normal_hosts=80,
        n_scanners=10,
        n_targets=120,
    )

    graph = build_ip_graph(flows)
    data, node_list = graph_to_pyg_data(graph)

    true_labels = torch.tensor(
        [labels.get(ip_address, 0) for ip_address in node_list],
        dtype=torch.long,
    )

    with torch.no_grad():
        logits = model(data.x, data.edge_index)
        predictions = logits.argmax(dim=1)

    all_true_labels.extend(true_labels.tolist())
    all_predictions.extend(predictions.tolist())


print("===== GRAPHSAGE SYNTHETIC EVALUATION =====")
print(f"Graphs evaluated: 20")
print(f"Nodes evaluated:  {len(all_true_labels)}")
print(f"Accuracy:          {accuracy_score(all_true_labels, all_predictions):.4f}")
print(
    f"Precision:         "
    f"{precision_score(all_true_labels, all_predictions, zero_division=0):.4f}"
)
print(
    f"Recall:            "
    f"{recall_score(all_true_labels, all_predictions, zero_division=0):.4f}"
)
print(
    f"F1:                "
    f"{f1_score(all_true_labels, all_predictions, zero_division=0):.4f}"
)
print("Confusion matrix:")
print(confusion_matrix(all_true_labels, all_predictions))
PY

Then run:

builtin cd /home/pd/Downloads/flowguard/ml-service/training && source ../.venv/bin/activate && PYTHONPATH=.. python evaluate_gnn.py | tee /home/pd/Downloads/flowguard/docs/gnn_evaluation.txt

If it says the model file is missing, retrain it from the correct directory:

builtin cd /home/pd/Downloads/flowguard/ml-service && source .venv/bin/activate && PYTHONPATH=. python training/train_gnn.py

Then rerun the evaluation command.

Use the resulting metric honestly as:

    “Evaluated GraphSAGE using node-level classification across 20 unseen synthetic network graphs.”

Do not describe it as CICIDS2017, real-traffic, held-out flow-level, or full four-model ensemble performance.


…/ml-service/training main ? ❯ cat > /home/pd/Downloads/flowguard/ml-service/training/evaluate_gnn.py <<'PY'
"""
Evaluate the trained GraphSAGE model on unseen synthetic network graphs.

Important:
- This is a node-level synthetic evaluation.
- It is not a real CICIDS2017 evaluation.
- It is not directly comparable to flow-level Random Forest metrics.
"""

from pathlib import Path
import random
import sys

import torch
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

# ml-service/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.ml.gnn_model import FlowGraphSAGE
from app.ml.graph_builder import build_ip_graph, graph_to_pyg_data
from train_gnn import generate_synthetic_flow_graph


MODEL_DIRECTORY = PROJECT_ROOT / "app" / "models"
MODEL_PATH = MODEL_DIRECTORY / "gnn_graphsage.pt"
META_PATH = MODEL_DIRECTORY / "gnn_meta.pt"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"GNN model not found: {MODEL_PATH}")

if not META_PATH.exists():
    raise FileNotFoundError(f"GNN metadata not found: {META_PATH}")


# Load the architecture information saved during training.
metadata = torch.load(META_PATH, map_location="cpu")

model = FlowGraphSAGE(
    in_channels=int(metadata["in_channels"]),
    hidden_channels=32,
    out_channels=2,
)

model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

all_true_labels = []
all_predictions = []

# Evaluate on 20 independently generated graphs that were not used to train.
for test_seed in range(1000, 1020):
    random.seed(test_seed)
    torch.manual_seed(test_seed)

    flows, labels = generate_synthetic_flow_graph(
        n_normal_hosts=80,
        n_scanners=10,
        n_targets=120,
    )

    graph = build_ip_graph(flows)
    data, node_list = graph_to_pyg_data(graph)

    true_labels = torch.tensor(
        [labels.get(ip_address, 0) for ip_address in node_list],
        dtype=torch.long,
    )

    with torch.no_grad():
        logits = model(data.x, data.edge_index)
        predictions = logits.argmax(dim=1)

    all_true_labels.extend(true_labels.tolist())
    all_predictions.extend(predictions.tolist())


print("===== GRAPHSAGE SYNTHETIC EVALUATION =====")
print(f"Graphs evaluated: 20")
print(f"Nodes evaluated:  {len(all_true_labels)}")
print(f"Accuracy:          {accuracy_score(all_true_labels, all_predictions):.4f}")
print(
    f"Precision:         "
    f"{precision_score(all_true_labels, all_predictions, zero_division=0):.4f}"
)
print(
    f"Recall:            "
    f"{recall_score(all_true_labels, all_predictions, zero_division=0):.4f}"
)
print(
    f"F1:                "
    f"{f1_score(all_true_labels, all_predictions, zero_division=0):.4f}"
)
print("Confusion matrix:")
print(confusion_matrix(all_true_labels, all_predictions))
PY

…/ml-service/training main ? ❯ builtin cd /home/pd/Downloads/flowguard/ml-service/training && source ../.venv/bin/activate && PYTHONPATH=.. python evaluate_gnn.py | tee /home/pd/Downloads/flowguard/docs/gnn_evaluation.txt
===== GRAPHSAGE SYNTHETIC EVALUATION =====
Graphs evaluated: 20
Nodes evaluated:  4199
Accuracy:          0.9826
Precision:         1.0000
Recall:            0.6350
F1:                0.7768
Confusion matrix:
[[3999    0]
 [  73  127]]

…/ml-service/training main ? ❯

The GNN evaluation is now complete and valid for unseen synthetic graphs.
Verified result

Accuracy:  98.26%
Precision: 100.00%
Recall:    63.50%
F1:        77.68%

Confusion matrix:

                 Predicted normal  Predicted attack
Actual normal           3999               0
Actual attack              73             127

So the model produced no false alarms, but missed 73 of 200 scanner nodes. The 98.26% accuracy looks high partly because the dataset has far more normal nodes than attack nodes, so F1 = 0.7768 is the more meaningful headline.

Resume-safe wording:

    Evaluated a GraphSAGE Graph Neural Network on 20 unseen synthetic network graphs containing 4,199 nodes, achieving 1.00 precision, 0.635 recall, and 0.777 F1 for scanner-node detection.

Do not call this a CICIDS2017 result or a real-network result.
Next: prepare the kernel benchmark

First install the tools:

sudo pacman -S --needed tcpdump tcpreplay

Find your available PCAP files:

find /home/pd/Downloads/flowguard/data -type f \( -name "*.pcap" -o -name "*.pcapng" \) -printf '%s bytes  %p\n' | sort -nr

Check whether the C++ program accepts a PCAP argument:

grep -RInE "argc|argv|pcap_open_offline" /home/pd/Downloads/flowguard/capture-cpp/src /home/pd/Downloads/flowguard/capture-cpp/include

Inspect how the eBPF loader attaches XDP and prints events:

grep -nE "argc|argv|bpf_xdp_attach|bpf_program__attach_xdp|printf|fprintf|ring_buffer" /home/pd/Downloads/flowguard/capture-ebpf/loader.c

Run those three commands and paste their output. We need those details before producing a fair same-PCAP benchmark rather than another invalid live-versus-offline comparison.


…/ml-service/training main ? ❯ builtin cd /home/pd/Downloads/flowguard/ml-service/training && source ../.venv/bin/activate && PYTHONPATH=.. python evaluate_gnn.py | tee /home/pd/Downloads/flowguard/docs/gnn_evaluation.txt
===== GRAPHSAGE SYNTHETIC EVALUATION =====
Graphs evaluated: 20
Nodes evaluated:  4199
Accuracy:          0.9826
Precision:         1.0000
Recall:            0.6350
F1:                0.7768
Confusion matrix:
[[3999    0]
 [  73  127]]

…/ml-service/training main ? ❯ sudo pacman -S --needed tcpdump tcpreplay
[sudo] password for pd:
warning: tcpdump-4.99.6-1 is up to date -- skipping
resolving dependencies...
looking for conflicting packages...

Package (2)      New Version  Net Change  Download Size

extra/libdnet    1.18.2-1       0.16 MiB       0.06 MiB
extra/tcpreplay  4.5.2-1        1.05 MiB       0.27 MiB

Total Download Size:   0.33 MiB
Total Installed Size:  1.21 MiB

:: Proceed with installation? [Y/n] y
:: Retrieving packages...
 libdnet-1.18.2-1-x86_64                                            59.8 KiB   157 KiB/s 00:00 [-------------------------------------------------------] 100%
 tcpreplay-4.5.2-1-x86_64                                          279.9 KiB   524 KiB/s 00:01 [-------------------------------------------------------] 100%
 Total (2/2)                                                       339.7 KiB   487 KiB/s 00:01 [-------------------------------------------------------] 100%
(2/2) checking keys in keyring                                                                 [-------------------------------------------------------] 100%
(2/2) checking package integrity                                                               [-------------------------------------------------------] 100%
(2/2) loading package files                                                                    [-------------------------------------------------------] 100%
(2/2) checking for file conflicts                                                              [-------------------------------------------------------] 100%
(2/2) checking available disk space                                                            [-------------------------------------------------------] 100%
:: Processing package changes...
(1/2) installing libdnet                                                                       [-------------------------------------------------------] 100%
(2/2) installing tcpreplay                                                                     [-------------------------------------------------------] 100%
Optional dependencies for tcpreplay
    tcpdump: decoding of packets support [installed]
:: Running post-transaction hooks...
(1/1) Arming ConditionNeedsUpdate...

…/ml-service/training main ? ❯ find /home/pd/Downloads/flowguard/data -type f \( -name "*.pcap" -o -name "*.pcapng" \) -printf '%s bytes  %p\n' | sort -nr
24144199 bytes  /home/pd/Downloads/flowguard/data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap
144172 bytes  /home/pd/Downloads/flowguard/data/sample/real_attack.pcap
4287 bytes  /home/pd/Downloads/flowguard/data/sample/small_sample.pcap

…/ml-service/training main ? ❯ grep -RInE "argc|argv|pcap_open_offline" /home/pd/Downloads/flowguard/capture-cpp/src /home/pd/Downloads/flowguard/capture-cpp/include
/home/pd/Downloads/flowguard/capture-cpp/src/main.cpp:16:    pcap_t* handle = pcap_open_offline(pcap_path.c_str(), errbuf);
/home/pd/Downloads/flowguard/capture-cpp/src/main.cpp:52:int main(int argc, char* argv[]) {
/home/pd/Downloads/flowguard/capture-cpp/src/main.cpp:53:    std::string pcap_path = (argc > 1) ? argv[1] : "../data/sample/small_sample.pcap";
/home/pd/Downloads/flowguard/capture-cpp/src/main.cpp:54:    std::string output_path = (argc > 2) ? argv[2] : "../data/flows_output.jsonl";
/home/pd/Downloads/flowguard/capture-cpp/src/benchmark.cpp:9:int main(int argc, char** argv) {
/home/pd/Downloads/flowguard/capture-cpp/src/benchmark.cpp:10:    const char* filename = argc > 1 ? argv[1] : "../data/sample/small_sample.pcap";
/home/pd/Downloads/flowguard/capture-cpp/src/benchmark.cpp:13:    pcap_t* handle = pcap_open_offline(filename, errbuf);

…/ml-service/training main ? ❯ grep -nE "argc|argv|bpf_xdp_attach|bpf_program__attach_xdp|printf|fprintf|ring_buffer" /home/pd/Downloads/flowguard/capture-ebpf/loader.c
34:#include <stdio.h>      // printf(), fprintf(), perror()
244:        fprintf(
357:    printf(
403:        fprintf(
409:        fprintf(
451:        fprintf(
461:    printf(
476:    struct bpf_map *ring_buffer_map = NULL;
477:    struct ring_buffer *ring_buffer_reader = NULL;
517:        fprintf(
559:        fprintf(
590:        fprintf(
613:        fprintf(
650:        bpf_xdp_attach(
659:        fprintf(
673:    printf(
696:    ring_buffer_map =
703:    if (ring_buffer_map == NULL) {
704:        fprintf(
717:    int ring_buffer_map_file_descriptor =
718:        bpf_map__fd(ring_buffer_map);
721:    if (ring_buffer_map_file_descriptor < 0) {
722:        fprintf(
736:    ring_buffer__new() creates a userspace reader.
744:        ring_buffer_map_file_descriptor
758:    ring_buffer_reader =
759:        ring_buffer__new(
760:            ring_buffer_map_file_descriptor,
767:    long ring_buffer_error =
768:        libbpf_get_error(ring_buffer_reader);
771:    if (ring_buffer_error != 0) {
772:        fprintf(
775:            strerror((int)-ring_buffer_error)
778:        ring_buffer_reader = NULL;
821:    ring_buffer__poll(..., 100):
831:            ring_buffer__poll(
832:                ring_buffer_reader,
850:            fprintf(
900:            fprintf(
908:            printf(
919:    if (ring_buffer_reader != NULL) {
920:        ring_buffer__free(ring_buffer_reader);

…/ml-service/training main ? ❯ ,telll me arent we doing all ou test on some real data?

Some tests use real data, but not all of them. You currently have three different kinds of testing, and they prove different things.
Component/test	Data used	What it proves
C++ capture and flow aggregation	Real 24 MB infected-Android PCAP	Your parser and flow pipeline process real network traffic
Isolation Forest and Random Forest real-data evaluation	CICIDS2017	How those models generalize to a real labelled intrusion-detection dataset
Three-model ensemble headline metrics	Held-out generated/sample dataset	Performance on data similar to your training generator—not necessarily real-world generalization
Autoencoder evaluation	Held-out generated/sample dataset	Performance on the generated test distribution
GraphSAGE training	Synthetic IP graphs	It can learn the simulated scanner pattern
GraphSAGE evaluation just completed	20 unseen synthetic graphs	It generalizes to new synthetic graphs from the same generator
eBPF/XDP loader test	Live packets from your actual interface	Kernel capture works on real traffic
eBPF versus libpcap speed comparison	Not completed yet	No defensible speed improvement number yet
The important distinction
1. Real traffic without labels

Your infected-Android PCAP is real captured traffic:

2025-10-02-traffic-from-infected-Android-phone.pcap

This is excellent for proving:

PCAP → packet parsing → flow aggregation → JSONL → API

But unless every flow has a verified benign/attack label, it cannot reliably produce accuracy, precision, recall, or F1.
2. Real labelled benchmark data

CICIDS2017 contains real captured network activity with labels. That makes it useful for evaluating model generalization.

Your results reportedly showed:

    Isolation Forest real-data F1: 0.3232

    Random Forest attack recall: 0%

Those weaker results are actually valuable because they reveal dataset shift: a model performing well on generated data may fail on unfamiliar real traffic.
3. Synthetic labelled data

Your test_holdout.csv contains:

duration_seconds
packet_count
total_bytes
bytes_per_sec
packets_per_sec
syn_count
ack_count
fin_count
rst_count
syn_ack_ratio
rst_ratio
Label

It has labels but no original IP relationships. It appears to come from your generated dataset pipeline.

Your GraphSAGE generator explicitly creates fake addresses and traffic:

normal_ips = [...]
scanner_ips = [...]
target_ips = [...]

Therefore, the new GNN result:

Accuracy:  98.26%
Precision: 100.00%
Recall:    63.50%
F1:        77.68%

is a legitimate synthetic graph evaluation, but not a real-network evaluation.
What your project honestly proves today

You can safely say:

    Built and tested an end-to-end intrusion-detection pipeline on a 24 MB real infected-device packet capture, extracting hundreds of network flows.

    Evaluated classical machine-learning detectors on both held-out generated data and the CICIDS2017 real-world intrusion dataset, identifying substantial dataset-shift limitations.

    Developed a GraphSAGE scanner detector and evaluated it across 20 unseen synthetic network graphs containing 4,199 nodes, achieving 1.00 precision and 0.777 F1.

    Implemented and successfully attached an eBPF/XDP kernel packet-capture program to a live Linux network interface.

You should not yet say:

    Four-model ensemble achieved 98.94% accuracy on real traffic.

because the GNN is not wired into that ensemble and the headline ensemble result is not the CICIDS2017 result.

You should also not say:

    XDP was X% faster than libpcap.

because the controlled same-packet benchmark has not been completed.

So yes, you are testing on real data, but the entire project is not tested exclusively on real data. The real-data testing currently covers the packet-processing pipeline and some classical ML evaluation; the GNN evaluation remains synthetic.

i wantg all the thndg to be tetste on real data only and then get accruacy score 


FLOWGUARD_RESUME_KEYWORDS.md
File
i wantg all the thndg to be tetste on real data only and then get accruacy score     

Yes — we should rebuild FlowGuard so every machine-learning metric comes from real, labelled network traffic.

Your current report shows that the high 98.94% ensemble accuracy came from synthetic held-out data, while performance collapsed on real CICIDS2017 traffic. The infected-Android PCAP is real, but it lacks per-flow ground-truth labels, so its 723 alerts cannot be converted into accuracy.
What we will change

Real CICIDS traffic
        │
        ├── Real training split
        ├── Real validation split
        └── Real untouched test split
                    │
         ┌──────────┼──────────┬──────────┐
         ▼          ▼          ▼          ▼
 Isolation Forest  RF    Autoencoder   GraphSAGE
         └──────────┴──────────┴──────────┘
                    │
              4-model ensemble
                    │
        Accuracy / Precision / Recall / F1

Models

    Random Forest: train using real benign and attack flows.

    Isolation Forest: train only on real benign flows.

    Autoencoder: train only on real benign flows.

    GraphSAGE: train using real source/destination IP relationships.

    Ensemble: combine all four models and evaluate on the same real test set.

Important correction for GraphSAGE

Your current GraphSAGE predicts whether an IP node is a scanner. The other models classify network flows.

For a fair four-model accuracy score, GraphSAGE must become an edge-classification model:

Source IP ─── network flow ───> Destination IP
                    │
                    └── BENIGN or ATTACK

That gives every model one prediction per flow.
Accuracy does not apply to every component
Component	Correct real-data measurement
Random Forest	Accuracy, precision, recall, F1
Isolation Forest	Accuracy, precision, recall, F1
Autoencoder	Accuracy, precision, recall, F1
GraphSAGE	Accuracy, precision, recall, F1
Four-model ensemble	Accuracy, precision, recall, F1
C++ parser	Packet/flow agreement with a reference tool
libpcap capture	Captured packets, packets/sec, processing time
eBPF/XDP capture	Captured packets, packets/sec, packet loss, CPU usage
PostgreSQL/API/dashboard	End-to-end delivery success and latency

So we can obtain one genuine real-data ensemble accuracy, but eBPF itself does not have a classification accuracy score.
Step 1: inspect the real CICIDS files you already have

Run this:

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

Find all possible real datasets:

find /home/pd/Downloads/flowguard \
  -type f \( -iname "*.csv" -o -iname "*.parquet" \) \
  -printf '%s bytes  %p\n' | sort -nr

Then run this inspection script:

python - <<'PY'
from pathlib import Path
import pandas as pd

root = Path("/home/pd/Downloads/flowguard")

for path in sorted(root.rglob("*.csv")):
    try:
        frame = pd.read_csv(path, nrows=5, low_memory=False)
        columns = [str(column).strip() for column in frame.columns]

        important = [
            column for column in columns
            if any(term in column.lower() for term in [
                "label",
                "source ip",
                "destination ip",
                "src_ip",
                "dst_ip",
                "timestamp",
                "protocol",
            ])
        ]

        print("\nFILE:", path)
        print("IMPORTANT COLUMNS:", important)
        print("ALL COLUMNS:", columns)

    except Exception as error:
        print("\nFAILED:", path)
        print("ERROR:", error)
PY

We specifically need a real file containing equivalents of:

Source IP
Destination IP
Source Port
Destination Port
Protocol
Timestamp
Label

The eleven flow features are also needed:

duration_seconds
packet_count
total_bytes
bytes_per_sec
packets_per_sec
syn_count
ack_count
fin_count
rst_count
syn_ack_ratio
rst_ratio

What happens based on the result
Case 1: the real dataset includes source and destination IPs

Then all four models can be retrained and tested on real data.

We will create:

training/prepare_real_dataset.py
training/train_real_models.py
training/train_real_gnn.py
training/evaluate_real_ensemble.py
docs/real_only_evaluation.txt

Case 2: the real dataset has labels but no IP addresses

Then Random Forest, Isolation Forest, and Autoencoder can use it, but GraphSAGE cannot construct a genuine network graph.

In that case, we must use the original CICIDS files that retain source and destination IP columns.
Case 3: only the infected-Android PCAP is available

That PCAP can test the real capture pipeline, but not detection accuracy because it lacks verified labels for every flow.
Required split methodology

We should not randomly split individual rows because flows from the same capture may leak into both training and testing.

Use separate capture days or files:

Real capture files A/B/C → training
Real capture file D      → validation
Real capture file E      → final testing

The test file remains untouched until training and threshold selection are complete.
Final result format

The final report will contain:

===== REAL-ONLY FLOWGUARD EVALUATION =====

Dataset:
Training flows:
Validation flows:
Testing flows:
Benign test flows:
Attack test flows:

Isolation Forest:
Accuracy:
Precision:
Recall:
F1:

Random Forest:
Accuracy:
Precision:
Recall:
F1:

Autoencoder:
Accuracy:
Precision:
Recall:
F1:

GraphSAGE edge classifier:
Accuracy:
Precision:
Recall:
F1:

Four-model ensemble:
Accuracy:
Precision:
Recall:
F1:
False positives:
False negatives:
Confusion matrix:

Accuracy may be lower than the synthetic 98.94%, but it will be a genuine, defensible real-traffic result. Run the dataset inspection commands first; the next code must be based on the real column names rather than guessed names.

Pasted text(6).txt
Document
?

Your output confirms the key limitation:

All CICIDS2017 CSV files you have are real and labelled, but they do not contain Source IP or Destination IP columns. Therefore, the current host-based GraphSAGE model cannot be trained honestly on these CSVs. Your real_test_set.csv also contains only the 11 numerical features plus Label.
Best real-only solution

We will retrain all four models using only real CICIDS2017 rows:

    Isolation Forest: real benign training flows

    Random Forest: real benign + attack training flows

    Autoencoder: real benign training flows

    GraphSAGE: change it from an IP-host graph to a real flow-similarity graph

For the new GraphSAGE:

Each real CICIDS flow = one graph node
Similar flows = connected edges
Node label = BENIGN or ATTACK

This is still a genuine Graph Neural Network trained and tested entirely on real traffic. Resume wording would be:

    “Built a GraphSAGE flow-classification model using a feature-similarity graph constructed from real CICIDS2017 network flows.”

Do not call it an IP communication graph unless you later obtain CICIDS raw PCAPs containing the original addresses.
Real-data split

We should separate the data by capture day to avoid train/test leakage:

Training:
Monday
Tuesday
Wednesday

Validation:
Thursday

Final untouched test:
Friday

Then calculate for every model:

Accuracy
Balanced accuracy
Precision
Recall
F1
ROC-AUC
Confusion matrix

Accuracy alone can look misleading because CICIDS contains many more benign flows than attacks.
Run this next

This tells us exactly which labels and flow counts exist in every real file:

builtin cd /home/pd/Downloads/flowguard/ml-service && source .venv/bin/activate && python - <<'PY'
from pathlib import Path
import pandas as pd

root = Path("/home/pd/Downloads/flowguard/data/cicids2017")

for path in sorted(root.glob("*.csv")):
    counts = {}

    for chunk in pd.read_csv(
        path,
        usecols=lambda column: column.strip() == "Label",
        chunksize=100_000,
        low_memory=False,
    ):
        chunk.columns = [column.strip() for column in chunk.columns]
        labels = chunk["Label"].astype(str).str.strip()

        for label, count in labels.value_counts().items():
            counts[label] = counts.get(label, 0) + int(count)

    print(f"\n{path.name}")
    print(f"Total rows: {sum(counts.values()):,}")

    for label, count in sorted(counts.items()):
        print(f"  {label}: {count:,}")
PY

After this, we can create one real-only training script that rebuilds all four models and prints the final real CICIDS2017 accuracy.


flowguard/ml-service main ? ❯ builtin cd /home/pd/Downloads/flowguard/ml-service && source .venv/bin/activate && python - <<'PY'
from pathlib import Path
import pandas as pd

root = Path("/home/pd/Downloads/flowguard/data/cicids2017")

for path in sorted(root.glob("*.csv")):
    counts = {}

    for chunk in pd.read_csv(
        path,
        usecols=lambda column: column.strip() == "Label",
        chunksize=100_000,
        low_memory=False,
    ):
        chunk.columns = [column.strip() for column in chunk.columns]
        labels = chunk["Label"].astype(str).str.strip()

        for label, count in labels.value_counts().items():
            counts[label] = counts.get(label, 0) + int(count)

    print(f"\n{path.name}")
    print(f"Total rows: {sum(counts.values()):,}")

    for label, count in sorted(counts.items()):
        print(f"  {label}: {count:,}")
PY

Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
Total rows: 225,745
  BENIGN: 97,718
  DDoS: 128,027

Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
Total rows: 286,467
  BENIGN: 127,537
  PortScan: 158,930

Friday-WorkingHours-Morning.pcap_ISCX.csv
Total rows: 191,033
  BENIGN: 189,067
  Bot: 1,966

Monday-WorkingHours.pcap_ISCX.csv
Total rows: 529,918
  BENIGN: 529,918

Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
Total rows: 288,602
  BENIGN: 288,566
  Infiltration: 36

Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
Total rows: 170,366
  BENIGN: 168,186
  Web Attack � Brute Force: 1,507
  Web Attack � Sql Injection: 21
  Web Attack � XSS: 652

Tuesday-WorkingHours.pcap_ISCX.csv
Total rows: 445,909
  BENIGN: 432,074
  FTP-Patator: 7,938
  SSH-Patator: 5,897

Wednesday-workingHours.pcap_ISCX.csv
Total rows: 692,703
  BENIGN: 440,031
  DoS GoldenEye: 10,293
  DoS Hulk: 231,073
  DoS Slowhttptest: 5,499
  DoS slowloris: 5,796
  Heartbleed: 11

flowguard/ml-service main ? ❯

Good — you have enough real labelled CICIDS2017 data to retrain everything properly:

    Total real flows: 2,830,743

    Benign flows: 2,273,097

    Attack flows: 557,646

    Attack families include DDoS, PortScan, Bot, FTP/SSH brute force, multiple DoS variants, web attacks, infiltration, and Heartbleed.

The available CSVs contain flow statistics and labels, but not source/destination IPs, so the new GraphSAGE model must use a flow-similarity graph, not the earlier synthetic IP-host graph.

We will use:

Monday + Tuesday + Wednesday → real training data
Thursday                     → real validation data
Friday                       → untouched real testing data

This prevents rows from the same capture day leaking into both training and testing.
Step 1: create real-only datasets

Run this complete block:

cat > /home/pd/Downloads/flowguard/ml-service/training/prepare_real_only.py <<'PY'
"""
Create real-only FlowGuard train, validation, and test datasets.

No synthetic rows are generated.

Capture-day split:
    Monday–Wednesday -> training
    Thursday         -> validation
    Friday           -> final testing

Each output split is balanced between BENIGN and ATTACK so that accuracy
cannot become artificially high by predicting the majority class.
"""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CICIDS_ROOT = PROJECT_ROOT.parent / "data" / "cicids2017"
OUTPUT_ROOT = PROJECT_ROOT / "data" / "real_only"

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
CHUNK_SIZE = 100_000

RAW_COLUMNS = {
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Flow Bytes/s",
    "Flow Packets/s",
    "SYN Flag Count",
    "ACK Flag Count",
    "FIN Flag Count",
    "RST Flag Count",
    "Label",
}

FEATURE_COLUMNS = [
    "duration_seconds",
    "packet_count",
    "total_bytes",
    "bytes_per_sec",
    "packets_per_sec",
    "syn_count",
    "ack_count",
    "fin_count",
    "rst_count",
    "syn_ack_ratio",
    "rst_ratio",
]

SPLITS = {
    "train": {
        "files": [
            "Monday-WorkingHours.pcap_ISCX.csv",
            "Tuesday-WorkingHours.pcap_ISCX.csv",
            "Wednesday-workingHours.pcap_ISCX.csv",
        ],
        "benign_target": 10_000,
        "attack_target": 10_000,
    },
    "validation": {
        "files": [
            "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
            "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
        ],
        "benign_target": 2_000,
        "attack_target": 2_000,
    },
    "test": {
        "files": [
            "Friday-WorkingHours-Morning.pcap_ISCX.csv",
            "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
            "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
        ],
        "benign_target": 5_000,
        "attack_target": 5_000,
    },
}


def convert_chunk(raw: pd.DataFrame) -> pd.DataFrame:
    """Convert CICIDS2017 columns into FlowGuard's eleven features."""

    raw.columns = [str(column).strip() for column in raw.columns]

    labels = raw["Label"].astype(str).str.strip()

    numeric_names = [column for column in RAW_COLUMNS if column != "Label"]

    for column in numeric_names:
        raw[column] = pd.to_numeric(raw[column], errors="coerce")

    output = pd.DataFrame()

    output["duration_seconds"] = raw["Flow Duration"] / 1_000_000.0

    output["packet_count"] = (
        raw["Total Fwd Packets"] +
        raw["Total Backward Packets"]
    )

    output["total_bytes"] = (
        raw["Total Length of Fwd Packets"] +
        raw["Total Length of Bwd Packets"]
    )

    output["bytes_per_sec"] = raw["Flow Bytes/s"]
    output["packets_per_sec"] = raw["Flow Packets/s"]

    output["syn_count"] = raw["SYN Flag Count"]
    output["ack_count"] = raw["ACK Flag Count"]
    output["fin_count"] = raw["FIN Flag Count"]
    output["rst_count"] = raw["RST Flag Count"]

    output["syn_ack_ratio"] = (
        output["syn_count"] /
        (output["ack_count"] + 1.0)
    )

    output["rst_ratio"] = (
        output["rst_count"] /
        (output["packet_count"] + 1.0)
    )

    # Preserve the exact CICIDS attack name for later analysis.
    output["attack_type"] = labels

    # Binary classification:
    # 0 = BENIGN
    # 1 = any attack family
    output["Label"] = (labels != "BENIGN").astype(np.int64)

    output.replace([np.inf, -np.inf], np.nan, inplace=True)
    output.dropna(subset=FEATURE_COLUMNS, inplace=True)

    # Remove physically impossible negative values.
    valid_rows = (output[FEATURE_COLUMNS] >= 0).all(axis=1)
    output = output.loc[valid_rows].copy()

    output[FEATURE_COLUMNS] = output[FEATURE_COLUMNS].astype(np.float32)

    return output


def update_reservoir(
    current: pd.DataFrame | None,
    candidates: pd.DataFrame,
    target_size: int,
    random_generator: np.random.Generator,
) -> pd.DataFrame | None:
    """
    Keep a deterministic random sample without loading an entire capture
    file into memory.
    """

    if candidates.empty:
        return current

    candidates = candidates.copy()
    candidates["_sample_key"] = random_generator.random(len(candidates))

    if current is None:
        combined = candidates
    else:
        combined = pd.concat([current, candidates], ignore_index=True)

    if len(combined) > target_size:
        combined = combined.nsmallest(target_size, "_sample_key")

    return combined


def create_split(
    split_name: str,
    file_names: list[str],
    benign_target: int,
    attack_target: int,
) -> pd.DataFrame:
    """Create one balanced real-data split."""

    random_generator = np.random.default_rng(
        RANDOM_SEED + sum(ord(character) for character in split_name)
    )

    benign_reservoir = None
    attack_reservoir = None

    print(f"\n===== BUILDING {split_name.upper()} SPLIT =====")

    for file_name in file_names:
        path = CICIDS_ROOT / file_name

        if not path.exists():
            raise FileNotFoundError(f"Missing CICIDS file: {path}")

        print(f"Reading: {file_name}")

        for raw_chunk in pd.read_csv(
            path,
            chunksize=CHUNK_SIZE,
            low_memory=False,
            usecols=lambda column: str(column).strip() in RAW_COLUMNS,
        ):
            converted = convert_chunk(raw_chunk)

            benign_rows = converted[converted["Label"] == 0]
            attack_rows = converted[converted["Label"] == 1]

            benign_reservoir = update_reservoir(
                benign_reservoir,
                benign_rows,
                benign_target,
                random_generator,
            )

            attack_reservoir = update_reservoir(
                attack_reservoir,
                attack_rows,
                attack_target,
                random_generator,
            )

    if benign_reservoir is None:
        raise RuntimeError(f"No benign rows found for {split_name}")

    if attack_reservoir is None:
        raise RuntimeError(f"No attack rows found for {split_name}")

    benign_reservoir.drop(columns="_sample_key", inplace=True)
    attack_reservoir.drop(columns="_sample_key", inplace=True)

    result = pd.concat(
        [benign_reservoir, attack_reservoir],
        ignore_index=True,
    )

    result = result.sample(
        frac=1.0,
        random_state=RANDOM_SEED,
    ).reset_index(drop=True)

    print(f"Rows selected: {len(result):,}")
    print("Binary labels:")
    print(result["Label"].value_counts().sort_index().to_string())

    print("Attack types:")
    print(
        result.loc[result["Label"] == 1, "attack_type"]
        .value_counts()
        .to_string()
    )

    return result


def main() -> None:
    for split_name, configuration in SPLITS.items():
        dataset = create_split(
            split_name=split_name,
            file_names=configuration["files"],
            benign_target=configuration["benign_target"],
            attack_target=configuration["attack_target"],
        )

        output_path = OUTPUT_ROOT / f"{split_name}_real.csv"
        dataset.to_csv(output_path, index=False)

        print(f"Saved: {output_path}")

    print("\n===== REAL-ONLY DATASET PREPARATION COMPLETE =====")
    print(f"Training rows:   {sum(1 for _ in open(OUTPUT_ROOT / 'train_real.csv')) - 1:,}")
    print(f"Validation rows: {sum(1 for _ in open(OUTPUT_ROOT / 'validation_real.csv')) - 1:,}")
    print(f"Testing rows:    {sum(1 for _ in open(OUTPUT_ROOT / 'test_real.csv')) - 1:,}")


if __name__ == "__main__":
    main()
PY

Run it:

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate
mkdir -p /home/pd/Downloads/flowguard/docs

python training/prepare_real_only.py \
  | tee /home/pd/Downloads/flowguard/docs/real_dataset_preparation.txt

Expected final sizes:

Training rows:   20,000
Validation rows: 4,000
Testing rows:    10,000

Every row will come from real CICIDS2017 traffic:

train_real.csv       → 10,000 benign + 10,000 attacks
validation_real.csv  → 2,000 benign + 2,000 attacks
test_real.csv        → 5,000 benign + 5,000 attacks

Verify:

ls -lh /home/pd/Downloads/flowguard/ml-service/data/real_only

python - <<'PY'
import pandas as pd
from pathlib import Path

root = Path("/home/pd/Downloads/flowguard/ml-service/data/real_only")

for path in sorted(root.glob("*.csv")):
    df = pd.read_csv(path)
    print(f"\n{path.name}: {len(df):,} rows")
    print(df["Label"].value_counts().sort_index())
    print(df[df["Label"] == 1]["attack_type"].value_counts())
PY

Once these three files are created, the next phase trains and evaluates Isolation Forest, Random Forest, Autoencoder, GraphSAGE, and the four-model ensemble using only these real capture-day-separated datasets.



flowguard/ml-service main ? ❯ builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate
mkdir -p /home/pd/Downloads/flowguard/docs

python training/prepare_real_only.py \
  | tee /home/pd/Downloads/flowguard/docs/real_dataset_preparation.txt

===== BUILDING TRAIN SPLIT =====
Reading: Monday-WorkingHours.pcap_ISCX.csv
Reading: Tuesday-WorkingHours.pcap_ISCX.csv
Reading: Wednesday-workingHours.pcap_ISCX.csv
Rows selected: 20,000
Binary labels:
Label
0    10000
1    10000
Attack types:
attack_type
DoS Hulk            8692
DoS GoldenEye        366
FTP-Patator          299
SSH-Patator          222
DoS Slowhttptest     220
DoS slowloris        200
Heartbleed             1
Saved: /home/pd/Downloads/flowguard/ml-service/data/real_only/train_real.csv

===== BUILDING VALIDATION SPLIT =====
Reading: Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
Reading: Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
Rows selected: 4,000
Binary labels:
Label
0    2000
1    2000
Attack types:
attack_type
Web Attack � Brute Force      1367
Web Attack � XSS               585
Infiltration                    30
Web Attack � Sql Injection      18
Saved: /home/pd/Downloads/flowguard/ml-service/data/real_only/validation_real.csv

===== BUILDING TEST SPLIT =====
Reading: Friday-WorkingHours-Morning.pcap_ISCX.csv
Reading: Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
Reading: Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
Rows selected: 10,000
Binary labels:
Label
0    5000
1    5000
Attack types:
attack_type
PortScan    2804
DDoS        2152
Bot           44
Saved: /home/pd/Downloads/flowguard/ml-service/data/real_only/test_real.csv

===== REAL-ONLY DATASET PREPARATION COMPLETE =====
Training rows:   20,000
Validation rows: 4,000
Testing rows:    10,000

flowguard/ml-service main ? ❯ ls -lh /home/pd/Downloads/flowguard/ml-service/data/real_only
Permissions Size User Date Modified Name
.rw-r--r--  709k pd   18 Jul 20:36   test_real.csv
.rw-r--r--  1.4M pd   18 Jul 20:36   train_real.csv
.rw-r--r--  306k pd   18 Jul 20:36   validation_real.csv

flowguard/ml-service main ? ❯ python - <<'PY'
import pandas as pd
from pathlib import Path

root = Path("/home/pd/Downloads/flowguard/ml-service/data/real_only")

for path in sorted(root.glob("*.csv")):
    df = pd.read_csv(path)
    print(f"\n{path.name}: {len(df):,} rows")
    print(df["Label"].value_counts().sort_index())
    print(df[df["Label"] == 1]["attack_type"].value_counts())
PY

test_real.csv: 10,000 rows
Label
0    5000
1    5000
Name: count, dtype: int64
attack_type
PortScan    2804
DDoS        2152
Bot           44
Name: count, dtype: int64

train_real.csv: 20,000 rows
Label
0    10000
1    10000
Name: count, dtype: int64
attack_type
DoS Hulk            8692
DoS GoldenEye        366
FTP-Patator          299
SSH-Patator          222
DoS Slowhttptest     220
DoS slowloris        200
Heartbleed             1
Name: count, dtype: int64

validation_real.csv: 4,000 rows
Label
0    2000
1    2000
Name: count, dtype: int64
attack_type
Web Attack � Brute Force      1367
Web Attack � XSS               585
Infiltration                    30
Web Attack � Sql Injection      18
Name: count, dtype: int64

flowguard/ml-service main ? ❯

Perfect. Your real-only dataset preparation is complete:

Training:   20,000 real CICIDS2017 flows
Validation:  4,000 real CICIDS2017 flows
Testing:    10,000 real CICIDS2017 flows

There is no synthetic traffic in these three files. Also, the Friday test set contains DDoS, PortScan, and Bot attacks that were not present in the Monday–Wednesday training set. This makes the final score a difficult but highly defensible cross-day generalization test.

Now train and evaluate all four models.
Create the real-only evaluation script

Run this complete block:

cat > /home/pd/Downloads/flowguard/ml-service/training/train_evaluate_real_only.py <<'PY'
"""
Train and evaluate FlowGuard entirely on real CICIDS2017 network flows.

Data split:
    Monday–Wednesday -> training
    Thursday         -> validation and threshold selection
    Friday           -> final untouched test

Models:
    1. Isolation Forest
    2. Random Forest
    3. Autoencoder
    4. GraphSAGE flow-similarity Graph Neural Network

The script also evaluates a four-model voting ensemble.
"""

from __future__ import annotations

import copy
import json
import os
import random
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import torch
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from torch_geometric.data import Data
from torch_geometric.nn import SAGEConv


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

RANDOM_SEED = 42

FEATURE_COLUMNS = [
    "duration_seconds",
    "packet_count",
    "total_bytes",
    "bytes_per_sec",
    "packets_per_sec",
    "syn_count",
    "ack_count",
    "fin_count",
    "rst_count",
    "syn_ack_ratio",
    "rst_ratio",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = PROJECT_ROOT / "data" / "real_only"
MODEL_DIRECTORY = PROJECT_ROOT / "app" / "models" / "real_only"
DOCUMENT_DIRECTORY = PROJECT_ROOT.parent / "docs"

MODEL_DIRECTORY.mkdir(parents=True, exist_ok=True)
DOCUMENT_DIRECTORY.mkdir(parents=True, exist_ok=True)


def set_random_seeds(seed: int) -> None:
    """Make model training as reproducible as practical."""

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


set_random_seeds(RANDOM_SEED)

torch.set_num_threads(
    max(1, min(8, os.cpu_count() or 1))
)


# ---------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------

def load_split(file_name: str):
    """Load one prepared real CICIDS2017 split."""

    path = DATA_DIRECTORY / file_name

    if not path.exists():
        raise FileNotFoundError(f"Dataset was not found: {path}")

    dataframe = pd.read_csv(path)

    missing_columns = [
        column
        for column in FEATURE_COLUMNS + ["Label", "attack_type"]
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{file_name} is missing columns: {missing_columns}"
        )

    dataframe[FEATURE_COLUMNS] = dataframe[FEATURE_COLUMNS].apply(
        pd.to_numeric,
        errors="coerce",
    )

    dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)

    original_size = len(dataframe)

    dataframe.dropna(
        subset=FEATURE_COLUMNS + ["Label"],
        inplace=True,
    )

    dataframe.reset_index(drop=True, inplace=True)

    dropped_rows = original_size - len(dataframe)

    if dropped_rows:
        print(
            f"Dropped {dropped_rows:,} invalid rows from {file_name}"
        )

    features = dataframe[FEATURE_COLUMNS].to_numpy(
        dtype=np.float32
    )

    labels = dataframe["Label"].to_numpy(dtype=np.int64)

    return dataframe, features, labels


train_dataframe, train_features, train_labels = load_split(
    "train_real.csv"
)

validation_dataframe, validation_features, validation_labels = load_split(
    "validation_real.csv"
)

test_dataframe, test_features, test_labels = load_split(
    "test_real.csv"
)


print("===== REAL-ONLY DATASET =====")
print(f"Training rows:   {len(train_labels):,}")
print(f"Validation rows: {len(validation_labels):,}")
print(f"Testing rows:    {len(test_labels):,}")
print()


# ---------------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------------

def calculate_metrics(
    true_labels: np.ndarray,
    predictions: np.ndarray,
    attack_scores: np.ndarray | None = None,
) -> dict:
    """Calculate binary intrusion-detection metrics."""

    result = {
        "accuracy": float(
            accuracy_score(true_labels, predictions)
        ),
        "balanced_accuracy": float(
            balanced_accuracy_score(true_labels, predictions)
        ),
        "precision": float(
            precision_score(
                true_labels,
                predictions,
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                true_labels,
                predictions,
                zero_division=0,
            )
        ),
        "f1": float(
            f1_score(
                true_labels,
                predictions,
                zero_division=0,
            )
        ),
        "confusion_matrix": confusion_matrix(
            true_labels,
            predictions,
        ).tolist(),
    }

    if (
        attack_scores is not None
        and len(np.unique(true_labels)) == 2
    ):
        result["roc_auc"] = float(
            roc_auc_score(true_labels, attack_scores)
        )
    else:
        result["roc_auc"] = None

    return result


def print_metrics(model_name: str, metrics: dict) -> None:
    """Print a readable model report."""

    print(f"\n===== {model_name} =====")
    print(f"Accuracy:          {metrics['accuracy']:.4f}")
    print(
        f"Balanced accuracy: "
        f"{metrics['balanced_accuracy']:.4f}"
    )
    print(f"Precision:         {metrics['precision']:.4f}")
    print(f"Recall:            {metrics['recall']:.4f}")
    print(f"F1:                {metrics['f1']:.4f}")

    if metrics["roc_auc"] is not None:
        print(f"ROC-AUC:           {metrics['roc_auc']:.4f}")

    print("Confusion matrix:")
    print(np.asarray(metrics["confusion_matrix"]))


def find_best_threshold(
    true_labels: np.ndarray,
    attack_scores: np.ndarray,
) -> tuple[float, dict]:
    """
    Select a decision threshold using validation data only.

    The threshold maximizing F1 is selected. Balanced accuracy is used
    as a tie-breaker.
    """

    attack_scores = np.asarray(
        attack_scores,
        dtype=np.float64,
    )

    if np.all(attack_scores == attack_scores[0]):
        threshold = float(attack_scores[0])
        predictions = (
            attack_scores >= threshold
        ).astype(np.int64)

        return threshold, calculate_metrics(
            true_labels,
            predictions,
            attack_scores,
        )

    candidates = np.unique(
        np.quantile(
            attack_scores,
            np.linspace(0.0, 1.0, 501),
        )
    )

    best_threshold = float(candidates[0])
    best_metrics = None
    best_key = (-1.0, -1.0)

    for threshold in candidates:
        predictions = (
            attack_scores >= threshold
        ).astype(np.int64)

        metrics = calculate_metrics(
            true_labels,
            predictions,
            attack_scores,
        )

        comparison_key = (
            metrics["f1"],
            metrics["balanced_accuracy"],
        )

        if comparison_key > best_key:
            best_key = comparison_key
            best_threshold = float(threshold)
            best_metrics = metrics

    return best_threshold, best_metrics


def print_attack_family_recall(
    dataframe: pd.DataFrame,
    predictions: np.ndarray,
) -> None:
    """Show detection recall for each real attack family."""

    print("\nRecall by real Friday attack family:")

    attack_types = sorted(
        dataframe.loc[
            dataframe["Label"] == 1,
            "attack_type",
        ].astype(str).unique()
    )

    for attack_type in attack_types:
        mask = (
            dataframe["attack_type"].astype(str)
            == attack_type
        ).to_numpy()

        family_recall = float(
            np.mean(predictions[mask] == 1)
        )

        print(
            f"  {attack_type:<20} "
            f"{family_recall:.4f} "
            f"({int(mask.sum()):,} flows)"
        )


# ---------------------------------------------------------------------
# Feature scaling
# ---------------------------------------------------------------------

# Random Forest and GraphSAGE use this scaler.
supervised_scaler = StandardScaler()

scaled_train_features = supervised_scaler.fit_transform(
    train_features
).astype(np.float32)

scaled_validation_features = supervised_scaler.transform(
    validation_features
).astype(np.float32)

scaled_test_features = supervised_scaler.transform(
    test_features
).astype(np.float32)


# Isolation Forest and Autoencoder are trained only on real benign flows.
benign_train_features = train_features[train_labels == 0]

anomaly_scaler = StandardScaler()

scaled_benign_train_features = anomaly_scaler.fit_transform(
    benign_train_features
).astype(np.float32)

scaled_validation_anomaly_features = anomaly_scaler.transform(
    validation_features
).astype(np.float32)

scaled_test_anomaly_features = anomaly_scaler.transform(
    test_features
).astype(np.float32)


joblib.dump(
    supervised_scaler,
    MODEL_DIRECTORY / "supervised_scaler.joblib",
)

joblib.dump(
    anomaly_scaler,
    MODEL_DIRECTORY / "anomaly_scaler.joblib",
)


# ---------------------------------------------------------------------
# Model 1: Isolation Forest
# ---------------------------------------------------------------------

print("\nTraining Isolation Forest on real benign flows...")

isolation_forest = IsolationForest(
    n_estimators=300,
    max_samples="auto",
    contamination="auto",
    random_state=RANDOM_SEED,
    n_jobs=-1,
)

isolation_forest.fit(scaled_benign_train_features)

# score_samples() is higher for normal samples.
# Negating it makes larger values mean "more likely attack".
isolation_validation_scores = -isolation_forest.score_samples(
    scaled_validation_anomaly_features
)

isolation_test_scores = -isolation_forest.score_samples(
    scaled_test_anomaly_features
)

isolation_threshold, _ = find_best_threshold(
    validation_labels,
    isolation_validation_scores,
)

isolation_validation_predictions = (
    isolation_validation_scores >= isolation_threshold
).astype(np.int64)

isolation_test_predictions = (
    isolation_test_scores >= isolation_threshold
).astype(np.int64)

isolation_metrics = calculate_metrics(
    test_labels,
    isolation_test_predictions,
    isolation_test_scores,
)

print(f"Validation threshold: {isolation_threshold:.6f}")
print_metrics("ISOLATION FOREST — REAL TEST", isolation_metrics)

joblib.dump(
    isolation_forest,
    MODEL_DIRECTORY / "isolation_forest.joblib",
)


# ---------------------------------------------------------------------
# Model 2: Random Forest
# ---------------------------------------------------------------------

print("\nTraining Random Forest on real labelled flows...")

random_forest = RandomForestClassifier(
    n_estimators=500,
    min_samples_leaf=2,
    class_weight="balanced_subsample",
    random_state=RANDOM_SEED,
    n_jobs=-1,
)

random_forest.fit(
    scaled_train_features,
    train_labels,
)

random_forest_validation_scores = random_forest.predict_proba(
    scaled_validation_features
)[:, 1]

random_forest_test_scores = random_forest.predict_proba(
    scaled_test_features
)[:, 1]

random_forest_threshold, _ = find_best_threshold(
    validation_labels,
    random_forest_validation_scores,
)

random_forest_validation_predictions = (
    random_forest_validation_scores
    >= random_forest_threshold
).astype(np.int64)

random_forest_test_predictions = (
    random_forest_test_scores
    >= random_forest_threshold
).astype(np.int64)

random_forest_metrics = calculate_metrics(
    test_labels,
    random_forest_test_predictions,
    random_forest_test_scores,
)

print(
    f"Validation threshold: "
    f"{random_forest_threshold:.6f}"
)

print_metrics(
    "RANDOM FOREST — REAL TEST",
    random_forest_metrics,
)

joblib.dump(
    random_forest,
    MODEL_DIRECTORY / "random_forest.joblib",
)


# ---------------------------------------------------------------------
# Model 3: Autoencoder
# ---------------------------------------------------------------------

class FlowAutoencoder(nn.Module):
    """Autoencoder for real benign flow reconstruction."""

    def __init__(self, input_dimension: int):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(input_dimension, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
        )

        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, input_dimension),
        )

    def forward(self, features):
        encoded = self.encoder(features)
        return self.decoder(encoded)


device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"\nTraining Autoencoder on: {device}")

autoencoder = FlowAutoencoder(
    input_dimension=len(FEATURE_COLUMNS)
).to(device)

autoencoder_optimizer = torch.optim.AdamW(
    autoencoder.parameters(),
    lr=0.001,
    weight_decay=1e-5,
)

autoencoder_loss_function = nn.MSELoss()

benign_tensor = torch.tensor(
    scaled_benign_train_features,
    dtype=torch.float32,
)

benign_loader = DataLoader(
    TensorDataset(benign_tensor),
    batch_size=256,
    shuffle=True,
)

AUTOENCODER_EPOCHS = 40

for epoch in range(1, AUTOENCODER_EPOCHS + 1):
    autoencoder.train()
    total_loss = 0.0

    for (batch_features,) in benign_loader:
        batch_features = batch_features.to(device)

        autoencoder_optimizer.zero_grad()

        reconstructed_features = autoencoder(
            batch_features
        )

        loss = autoencoder_loss_function(
            reconstructed_features,
            batch_features,
        )

        loss.backward()
        autoencoder_optimizer.step()

        total_loss += (
            loss.item() * len(batch_features)
        )

    average_loss = total_loss / len(benign_tensor)

    if epoch == 1 or epoch % 10 == 0:
        print(
            f"Autoencoder epoch {epoch:02d}/"
            f"{AUTOENCODER_EPOCHS}: "
            f"loss={average_loss:.6f}"
        )


def autoencoder_scores(
    model: nn.Module,
    features: np.ndarray,
    batch_size: int = 1024,
) -> np.ndarray:
    """Calculate reconstruction error for each flow."""

    model.eval()

    tensor = torch.tensor(
        features,
        dtype=torch.float32,
    )

    loader = DataLoader(
        TensorDataset(tensor),
        batch_size=batch_size,
        shuffle=False,
    )

    scores = []

    with torch.no_grad():
        for (batch_features,) in loader:
            batch_features = batch_features.to(device)

            reconstruction = model(batch_features)

            batch_scores = torch.mean(
                (reconstruction - batch_features) ** 2,
                dim=1,
            )

            scores.extend(
                batch_scores.cpu().numpy().tolist()
            )

    return np.asarray(scores, dtype=np.float64)


autoencoder_validation_scores = autoencoder_scores(
    autoencoder,
    scaled_validation_anomaly_features,
)

autoencoder_test_scores = autoencoder_scores(
    autoencoder,
    scaled_test_anomaly_features,
)

autoencoder_threshold, _ = find_best_threshold(
    validation_labels,
    autoencoder_validation_scores,
)

autoencoder_validation_predictions = (
    autoencoder_validation_scores >= autoencoder_threshold
).astype(np.int64)

autoencoder_test_predictions = (
    autoencoder_test_scores >= autoencoder_threshold
).astype(np.int64)

autoencoder_metrics = calculate_metrics(
    test_labels,
    autoencoder_test_predictions,
    autoencoder_test_scores,
)

print(
    f"Validation threshold: "
    f"{autoencoder_threshold:.6f}"
)

print_metrics(
    "AUTOENCODER — REAL TEST",
    autoencoder_metrics,
)

torch.save(
    {
        "state_dict": autoencoder.state_dict(),
        "input_dimension": len(FEATURE_COLUMNS),
        "feature_columns": FEATURE_COLUMNS,
    },
    MODEL_DIRECTORY / "autoencoder.pt",
)


# ---------------------------------------------------------------------
# Model 4: GraphSAGE flow-similarity graph
# ---------------------------------------------------------------------

def build_similarity_graph(
    features: np.ndarray,
    labels: np.ndarray,
    neighbors_per_node: int = 8,
) -> Data:
    """
    Build a graph where:
        node = one real CICIDS2017 flow
        edge = two flows with similar feature values
    """

    number_of_nodes = len(features)

    if number_of_nodes < 2:
        raise ValueError(
            "At least two flows are required for a graph"
        )

    neighbor_count = min(
        neighbors_per_node + 1,
        number_of_nodes,
    )

    nearest_neighbors = NearestNeighbors(
        n_neighbors=neighbor_count,
        metric="euclidean",
        algorithm="auto",
        n_jobs=-1,
    )

    nearest_neighbors.fit(features)

    neighbor_indices = nearest_neighbors.kneighbors(
        features,
        return_distance=False,
    )

    source_nodes = []
    destination_nodes = []

    for node_index, neighbors in enumerate(
        neighbor_indices
    ):
        added_neighbors = 0

        for neighbor_index in neighbors:
            if int(neighbor_index) == node_index:
                continue

            source_nodes.append(node_index)
            destination_nodes.append(
                int(neighbor_index)
            )

            # Add reverse edge.
            source_nodes.append(
                int(neighbor_index)
            )
            destination_nodes.append(node_index)

            added_neighbors += 1

            if added_neighbors >= neighbors_per_node:
                break

    edge_index = torch.tensor(
        [source_nodes, destination_nodes],
        dtype=torch.long,
    )

    node_features = torch.tensor(
        features,
        dtype=torch.float32,
    )

    node_labels = torch.tensor(
        labels,
        dtype=torch.float32,
    )

    return Data(
        x=node_features,
        edge_index=edge_index,
        y=node_labels,
    )


class FlowSimilarityGraphSAGE(nn.Module):
    """GraphSAGE binary classifier for real flow nodes."""

    def __init__(
        self,
        input_dimension: int,
        hidden_dimension: int = 64,
    ):
        super().__init__()

        self.convolution_one = SAGEConv(
            input_dimension,
            hidden_dimension,
        )

        self.convolution_two = SAGEConv(
            hidden_dimension,
            hidden_dimension,
        )

        self.classifier = nn.Linear(
            hidden_dimension,
            1,
        )

        self.dropout = nn.Dropout(0.20)

    def forward(self, node_features, edge_index):
        hidden = self.convolution_one(
            node_features,
            edge_index,
        )

        hidden = torch.relu(hidden)
        hidden = self.dropout(hidden)

        hidden = self.convolution_two(
            hidden,
            edge_index,
        )

        hidden = torch.relu(hidden)

        return self.classifier(hidden).squeeze(-1)


print("\nBuilding real flow-similarity graphs...")

training_graph = build_similarity_graph(
    scaled_train_features,
    train_labels,
)

validation_graph = build_similarity_graph(
    scaled_validation_features,
    validation_labels,
)

test_graph = build_similarity_graph(
    scaled_test_features,
    test_labels,
)

print(
    f"Training graph: "
    f"{training_graph.num_nodes:,} nodes, "
    f"{training_graph.num_edges:,} directed edges"
)

print(
    f"Validation graph: "
    f"{validation_graph.num_nodes:,} nodes, "
    f"{validation_graph.num_edges:,} directed edges"
)

print(
    f"Test graph: "
    f"{test_graph.num_nodes:,} nodes, "
    f"{test_graph.num_edges:,} directed edges"
)

training_graph = training_graph.to(device)
validation_graph = validation_graph.to(device)
test_graph = test_graph.to(device)

graphsage = FlowSimilarityGraphSAGE(
    input_dimension=len(FEATURE_COLUMNS),
    hidden_dimension=64,
).to(device)

graphsage_optimizer = torch.optim.AdamW(
    graphsage.parameters(),
    lr=0.003,
    weight_decay=5e-4,
)

graphsage_loss_function = nn.BCEWithLogitsLoss()

best_graphsage_state = None
best_validation_f1 = -1.0
epochs_without_improvement = 0

GRAPHSAGE_EPOCHS = 80
GRAPHSAGE_PATIENCE = 15

print(f"\nTraining GraphSAGE on: {device}")

for epoch in range(1, GRAPHSAGE_EPOCHS + 1):
    graphsage.train()
    graphsage_optimizer.zero_grad()

    training_logits = graphsage(
        training_graph.x,
        training_graph.edge_index,
    )

    training_loss = graphsage_loss_function(
        training_logits,
        training_graph.y,
    )

    training_loss.backward()
    graphsage_optimizer.step()

    graphsage.eval()

    with torch.no_grad():
        validation_logits = graphsage(
            validation_graph.x,
            validation_graph.edge_index,
        )

        validation_probabilities = torch.sigmoid(
            validation_logits
        ).cpu().numpy()

    validation_predictions_at_half = (
        validation_probabilities >= 0.5
    ).astype(np.int64)

    validation_f1 = f1_score(
        validation_labels,
        validation_predictions_at_half,
        zero_division=0,
    )

    if validation_f1 > best_validation_f1:
        best_validation_f1 = validation_f1
        best_graphsage_state = copy.deepcopy(
            graphsage.state_dict()
        )
        epochs_without_improvement = 0
    else:
        epochs_without_improvement += 1

    if epoch == 1 or epoch % 10 == 0:
        print(
            f"GraphSAGE epoch {epoch:02d}/"
            f"{GRAPHSAGE_EPOCHS}: "
            f"loss={training_loss.item():.6f}, "
            f"validation_f1={validation_f1:.4f}"
        )

    if epochs_without_improvement >= GRAPHSAGE_PATIENCE:
        print(
            f"Early stopping at epoch {epoch}"
        )
        break


if best_graphsage_state is None:
    raise RuntimeError(
        "GraphSAGE did not produce a valid model state"
    )

graphsage.load_state_dict(best_graphsage_state)
graphsage.eval()

with torch.no_grad():
    graphsage_validation_scores = torch.sigmoid(
        graphsage(
            validation_graph.x,
            validation_graph.edge_index,
        )
    ).cpu().numpy()

    graphsage_test_scores = torch.sigmoid(
        graphsage(
            test_graph.x,
            test_graph.edge_index,
        )
    ).cpu().numpy()


graphsage_threshold, _ = find_best_threshold(
    validation_labels,
    graphsage_validation_scores,
)

graphsage_validation_predictions = (
    graphsage_validation_scores
    >= graphsage_threshold
).astype(np.int64)

graphsage_test_predictions = (
    graphsage_test_scores
    >= graphsage_threshold
).astype(np.int64)

graphsage_metrics = calculate_metrics(
    test_labels,
    graphsage_test_predictions,
    graphsage_test_scores,
)

print(
    f"Validation threshold: "
    f"{graphsage_threshold:.6f}"
)

print_metrics(
    "GRAPHSAGE — REAL TEST",
    graphsage_metrics,
)

torch.save(
    {
        "state_dict": graphsage.state_dict(),
        "input_dimension": len(FEATURE_COLUMNS),
        "hidden_dimension": 64,
        "neighbors_per_node": 8,
        "feature_columns": FEATURE_COLUMNS,
    },
    MODEL_DIRECTORY / "graphsage_flow_similarity.pt",
)


# ---------------------------------------------------------------------
# Four-model ensemble
# ---------------------------------------------------------------------

validation_model_predictions = np.column_stack(
    [
        isolation_validation_predictions,
        random_forest_validation_predictions,
        autoencoder_validation_predictions,
        graphsage_validation_predictions,
    ]
)

test_model_predictions = np.column_stack(
    [
        isolation_test_predictions,
        random_forest_test_predictions,
        autoencoder_test_predictions,
        graphsage_test_predictions,
    ]
)

validation_vote_counts = validation_model_predictions.sum(
    axis=1
)

test_vote_counts = test_model_predictions.sum(axis=1)

best_required_votes = 1
best_ensemble_validation_key = (-1.0, -1.0)

for required_votes in range(1, 5):
    validation_ensemble_predictions = (
        validation_vote_counts >= required_votes
    ).astype(np.int64)

    validation_ensemble_metrics = calculate_metrics(
        validation_labels,
        validation_ensemble_predictions,
        validation_vote_counts / 4.0,
    )

    comparison_key = (
        validation_ensemble_metrics["f1"],
        validation_ensemble_metrics[
            "balanced_accuracy"
        ],
    )

    print(
        f"\nValidation ensemble {required_votes}-of-4: "
        f"F1={validation_ensemble_metrics['f1']:.4f}, "
        f"balanced_accuracy="
        f"{validation_ensemble_metrics['balanced_accuracy']:.4f}"
    )

    if comparison_key > best_ensemble_validation_key:
        best_ensemble_validation_key = comparison_key
        best_required_votes = required_votes


ensemble_test_predictions = (
    test_vote_counts >= best_required_votes
).astype(np.int64)

ensemble_test_scores = test_vote_counts / 4.0

ensemble_metrics = calculate_metrics(
    test_labels,
    ensemble_test_predictions,
    ensemble_test_scores,
)

print(
    f"\nSelected ensemble rule using validation data: "
    f"{best_required_votes}-of-4 models"
)

print_metrics(
    "FOUR-MODEL ENSEMBLE — REAL TEST",
    ensemble_metrics,
)

print_attack_family_recall(
    test_dataframe,
    ensemble_test_predictions,
)


# ---------------------------------------------------------------------
# Save thresholds and metrics
# ---------------------------------------------------------------------

thresholds = {
    "isolation_forest": float(isolation_threshold),
    "random_forest": float(random_forest_threshold),
    "autoencoder": float(autoencoder_threshold),
    "graphsage": float(graphsage_threshold),
    "ensemble_required_votes": int(best_required_votes),
}

all_metrics = {
    "dataset": {
        "training_rows": int(len(train_labels)),
        "validation_rows": int(len(validation_labels)),
        "testing_rows": int(len(test_labels)),
        "test_benign_rows": int(
            np.sum(test_labels == 0)
        ),
        "test_attack_rows": int(
            np.sum(test_labels == 1)
        ),
    },
    "isolation_forest": isolation_metrics,
    "random_forest": random_forest_metrics,
    "autoencoder": autoencoder_metrics,
    "graphsage": graphsage_metrics,
    "four_model_ensemble": ensemble_metrics,
    "thresholds": thresholds,
}

with open(
    MODEL_DIRECTORY / "thresholds.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(thresholds, file, indent=2)

with open(
    DOCUMENT_DIRECTORY / "real_only_metrics.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(all_metrics, file, indent=2)


print("\n===== REAL-ONLY EVALUATION COMPLETE =====")
print(
    f"Models saved to: {MODEL_DIRECTORY}"
)
print(
    f"Metrics saved to: "
    f"{DOCUMENT_DIRECTORY / 'real_only_metrics.json'}"
)
PY

Run the real-only training and evaluation

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python training/train_evaluate_real_only.py \
  | tee /home/pd/Downloads/flowguard/docs/real_only_evaluation.txt

You will see progress for the Autoencoder and GraphSAGE. Let it finish unless an actual traceback appears.

After completion, show the final results:

tail -n 100 /home/pd/Downloads/flowguard/docs/real_only_evaluation.txt

Also verify the artifacts:

find /home/pd/Downloads/flowguard/ml-service/app/models/real_only \
  -maxdepth 1 -type f -printf '%f\n' | sort

The resulting four-model ensemble accuracy will now be based entirely on real, labelled CICIDS2017 traffic—not the earlier synthetic 98.94% number.


flowguard/ml-service main ? ❯ builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python training/train_evaluate_real_only.py \
  | tee /home/pd/Downloads/flowguard/docs/real_only_evaluation.txt
===== REAL-ONLY DATASET =====
Training rows:   20,000
Validation rows: 4,000
Testing rows:    10,000


Training Isolation Forest on real benign flows...
Validation threshold: 0.329398

===== ISOLATION FOREST — REAL TEST =====
Accuracy:          0.6251
Balanced accuracy: 0.6251
Precision:         0.5721
Recall:            0.9926
F1:                0.7259
ROC-AUC:           0.6558
Confusion matrix:
[[1288 3712]
 [  37 4963]]

Training Random Forest on real labelled flows...
Validation threshold: 0.023552

===== RANDOM FOREST — REAL TEST =====
Accuracy:          0.8609
Balanced accuracy: 0.8609
Precision:         0.7871
Recall:            0.9894
F1:                0.8767
ROC-AUC:           0.9036
Confusion matrix:
[[3662 1338]
 [  53 4947]]

Training Autoencoder on: cpu
Autoencoder epoch 01/40: loss=0.991777
Autoencoder epoch 10/40: loss=0.065146
Autoencoder epoch 20/40: loss=0.014158
Autoencoder epoch 30/40: loss=0.011380
Autoencoder epoch 40/40: loss=0.010787
Validation threshold: 0.000875

===== AUTOENCODER — REAL TEST =====
Accuracy:          0.7586
Balanced accuracy: 0.7586
Precision:         0.7311
Recall:            0.8180
F1:                0.7721
ROC-AUC:           0.7765
Confusion matrix:
[[3496 1504]
 [ 910 4090]]

Building real flow-similarity graphs...
Training graph: 20,000 nodes, 320,000 directed edges
Validation graph: 4,000 nodes, 64,000 directed edges
Test graph: 10,000 nodes, 160,000 directed edges

Training GraphSAGE on: cpu
GraphSAGE epoch 01/80: loss=0.717868, validation_f1=0.6695
GraphSAGE epoch 10/80: loss=0.476546, validation_f1=0.0026
Early stopping at epoch 17
Validation threshold: 0.511871

===== GRAPHSAGE — REAL TEST =====
Accuracy:          0.5539
Balanced accuracy: 0.5539
Precision:         0.5285
Recall:            0.9988
F1:                0.6913
ROC-AUC:           0.7303
Confusion matrix:
[[ 545 4455]
 [   6 4994]]

Validation ensemble 1-of-4: F1=0.6667, balanced_accuracy=0.5000

Validation ensemble 2-of-4: F1=0.7235, balanced_accuracy=0.6182

Validation ensemble 3-of-4: F1=0.8134, balanced_accuracy=0.7742

Validation ensemble 4-of-4: F1=0.8553, balanced_accuracy=0.8553

Selected ensemble rule using validation data: 4-of-4 models

===== FOUR-MODEL ENSEMBLE — REAL TEST =====
Accuracy:          0.8471
Balanced accuracy: 0.8471
Precision:         0.8696
Recall:            0.8166
F1:                0.8423
ROC-AUC:           0.9015
Confusion matrix:
[[4388  612]
 [ 917 4083]]

Recall by real Friday attack family:
  Bot                  0.0227 (44 flows)
  DDoS                 0.8499 (2,152 flows)
  PortScan             0.8035 (2,804 flows)

===== REAL-ONLY EVALUATION COMPLETE =====
Models saved to: /home/pd/Downloads/flowguard/ml-service/app/models/real_only
Metrics saved to: /home/pd/Downloads/flowguard/docs/real_only_metrics.json

flowguard/ml-service main ? ❯ tail -n 100 /home/pd/Downloads/flowguard/docs/real_only_evaluation.txt


Training Isolation Forest on real benign flows...
Validation threshold: 0.329398

===== ISOLATION FOREST — REAL TEST =====
Accuracy:          0.6251
Balanced accuracy: 0.6251
Precision:         0.5721
Recall:            0.9926
F1:                0.7259
ROC-AUC:           0.6558
Confusion matrix:
[[1288 3712]
 [  37 4963]]

Training Random Forest on real labelled flows...
Validation threshold: 0.023552

===== RANDOM FOREST — REAL TEST =====
Accuracy:          0.8609
Balanced accuracy: 0.8609
Precision:         0.7871
Recall:            0.9894
F1:                0.8767
ROC-AUC:           0.9036
Confusion matrix:
[[3662 1338]
 [  53 4947]]

Training Autoencoder on: cpu
Autoencoder epoch 01/40: loss=0.991777
Autoencoder epoch 10/40: loss=0.065146
Autoencoder epoch 20/40: loss=0.014158
Autoencoder epoch 30/40: loss=0.011380
Autoencoder epoch 40/40: loss=0.010787
Validation threshold: 0.000875

===== AUTOENCODER — REAL TEST =====
Accuracy:          0.7586
Balanced accuracy: 0.7586
Precision:         0.7311
Recall:            0.8180
F1:                0.7721
ROC-AUC:           0.7765
Confusion matrix:
[[3496 1504]
 [ 910 4090]]

Building real flow-similarity graphs...
Training graph: 20,000 nodes, 320,000 directed edges
Validation graph: 4,000 nodes, 64,000 directed edges
Test graph: 10,000 nodes, 160,000 directed edges

Training GraphSAGE on: cpu
GraphSAGE epoch 01/80: loss=0.717868, validation_f1=0.6695
GraphSAGE epoch 10/80: loss=0.476546, validation_f1=0.0026
Early stopping at epoch 17
Validation threshold: 0.511871

===== GRAPHSAGE — REAL TEST =====
Accuracy:          0.5539
Balanced accuracy: 0.5539
Precision:         0.5285
Recall:            0.9988
F1:                0.6913
ROC-AUC:           0.7303
Confusion matrix:
[[ 545 4455]
 [   6 4994]]

Validation ensemble 1-of-4: F1=0.6667, balanced_accuracy=0.5000

Validation ensemble 2-of-4: F1=0.7235, balanced_accuracy=0.6182

Validation ensemble 3-of-4: F1=0.8134, balanced_accuracy=0.7742

Validation ensemble 4-of-4: F1=0.8553, balanced_accuracy=0.8553

Selected ensemble rule using validation data: 4-of-4 models

===== FOUR-MODEL ENSEMBLE — REAL TEST =====
Accuracy:          0.8471
Balanced accuracy: 0.8471
Precision:         0.8696
Recall:            0.8166
F1:                0.8423
ROC-AUC:           0.9015
Confusion matrix:
[[4388  612]
 [ 917 4083]]

Recall by real Friday attack family:
  Bot                  0.0227 (44 flows)
  DDoS                 0.8499 (2,152 flows)
  PortScan             0.8035 (2,804 flows)

===== REAL-ONLY EVALUATION COMPLETE =====
Models saved to: /home/pd/Downloads/flowguard/ml-service/app/models/real_only
Metrics saved to: /home/pd/Downloads/flowguard/docs/real_only_metrics.json

flowguard/ml-service main ? ❯ find /home/pd/Downloads/flowguard/ml-service/app/models/real_only \
  -maxdepth 1 -type f -printf '%f\n' | sort
anomaly_scaler.joblib
autoencoder.pt
graphsage_flow_similarity.pt
isolation_forest.joblib
random_forest.joblib
supervised_scaler.joblib
thresholds.json

You have now completed a real-only machine-learning evaluation using labelled CICIDS2017 network traffic.
Verified real-data results
Model	Accuracy	Precision	Recall	F1	ROC-AUC
Isolation Forest	62.51%	57.21%	99.26%	72.59%	65.58%
Random Forest	86.09%	78.71%	98.94%	87.67%	90.36%
Autoencoder	75.86%	73.11%	81.80%	77.21%	77.65%
GraphSAGE	55.39%	52.85%	99.88%	69.13%	73.03%
Four-model ensemble	84.71%	86.96%	81.66%	84.23%	90.15%

Your test set was balanced:

5,000 real benign flows
5,000 real attack flows

Therefore, the reported accuracy is meaningful and matches balanced accuracy.
Main conclusion

The Random Forest is currently your strongest overall detector:

Accuracy: 86.09%
Recall:   98.94%
F1:       87.67%

The four-model ensemble did not beat it in accuracy or F1:

Random Forest accuracy: 86.09%
Ensemble accuracy:      84.71%

However, the ensemble produced much fewer false positives:

Random Forest:
False positives: 1,338
False negatives:    53

Four-model ensemble:
False positives:   612
False negatives:   917

So the ensemble is more conservative:

fewer false alarms
but
more missed attacks

That is why its precision is higher at 86.96%, while recall falls to 81.66%.
Real attack-family performance

The ensemble detected:

DDoS:      84.99%
PortScan:  80.35%
Bot:        2.27%

Bot detection is currently the largest weakness. Only one of the 44 Bot flows was detected.

The low Bot result is understandable because:

    Bot was absent from the Monday–Wednesday training attacks.

    Only 44 Bot flows appeared in the test sample.

    Bot behaviour can differ significantly from DoS and brute-force traffic.

Important GraphSAGE finding

GraphSAGE achieved:

Accuracy: 55.39%
Recall:   99.88%

That means it classified almost every attack correctly, but also marked most benign flows as attacks:

True negatives:    545
False positives: 4,455
False negatives:     6
True positives:  4,994

Therefore, do not claim that GraphSAGE improved accuracy. It currently behaves like a very sensitive anomaly detector.

Also describe it accurately as:

    A GraphSAGE flow-similarity graph where real CICIDS2017 flows are nodes and nearest-neighbour feature relationships form edges.

Do not describe it as an IP communication graph because the CICIDS CSV files lacked source and destination IP addresses.
Resume-safe project wording
Strong resume bullet

    Trained and evaluated four intrusion-detection models on capture-day-separated CICIDS2017 traffic, achieving 86.1% accuracy, 98.9% recall, and 0.877 F1 with Random Forest on an untouched balanced test set of 10,000 real network flows.

Ensemble bullet

    Designed a four-model ensemble combining Random Forest, Isolation Forest, a PyTorch Autoencoder, and GraphSAGE, achieving 84.7% real-traffic accuracy and 87.0% precision while reducing false positives from 1,338 to 612 compared with the standalone Random Forest.

Evaluation-methodology bullet

    Prevented train-test leakage using capture-day separation: Monday–Wednesday for training, Thursday for threshold validation, and Friday for final testing across previously unseen DDoS, PortScan, and Bot attack families.

What you can now claim

You can honestly say:

    All four machine-learning models were trained and tested using real CICIDS2017 flows.

    Thresholds and ensemble rules were selected using separate real validation data.

    Final accuracy was measured on an untouched real Friday test split.

    The test set contained attack families not present in training.

    Random Forest achieved the best overall performance.

    The ensemble reduced false positives but sacrificed recall.

You should not say:

    The four-model ensemble achieved 98.9% real-data accuracy.

    GraphSAGE improved ensemble accuracy.

    The models achieved 86% accuracy on your infected-Android PCAP.

    The eBPF/XDP path is faster than libpcap.

The infected-Android PCAP still lacks per-flow ground-truth labels, and the eBPF-versus-libpcap performance benchmark is still pending.
Final verified headline

    FlowGuard achieved 86.09% accuracy, 98.94% recall, 78.71% precision, and 0.8767 F1 using Random Forest on 10,000 real, labelled, capture-day-separated CICIDS2017 flows.


Today 10:13 PM
mkae  a md file what all we conclude and how

Created the Markdown file with the complete methodology, results, conclusions, honest resume claims, limitations, and next improvements.


Pasted markdown(1).md
File
 help me execute next step

The next step should be to wire the verified real-data Random Forest into the live pipeline first.

Do not replace ensemble.py with the uploaded example yet. That example loads the old model directory, uses the earlier two-feature GNN, contains placeholder thresholds, and changes voting to 2-of-4, while your real validation selected 4-of-4.
1. Create a safe real-model predictor

Run this entire block:

cat > /home/pd/Downloads/flowguard/ml-service/app/ml/real_only_predictor.py <<'PY'
"""
Live predictor using FlowGuard's verified real-data Random Forest.

The model was:
- trained on real CICIDS2017 Monday-Wednesday traffic,
- tuned using Thursday validation traffic,
- evaluated on untouched Friday traffic.

This module performs inference only. Live flows do not have ground-truth
labels, so its output cannot be treated as a new accuracy measurement.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import joblib
import numpy as np


FEATURE_COLUMNS = [
    "duration_seconds",
    "packet_count",
    "total_bytes",
    "bytes_per_sec",
    "packets_per_sec",
    "syn_count",
    "ack_count",
    "fin_count",
    "rst_count",
    "syn_ack_ratio",
    "rst_ratio",
]

APP_DIRECTORY = Path(__file__).resolve().parents[1]
MODEL_DIRECTORY = APP_DIRECTORY / "models" / "real_only"

SCALER_PATH = MODEL_DIRECTORY / "supervised_scaler.joblib"
MODEL_PATH = MODEL_DIRECTORY / "random_forest.joblib"
THRESHOLDS_PATH = MODEL_DIRECTORY / "thresholds.json"


class RealOnlyRandomForestPredictor:
    """Load and run the verified real-data Random Forest."""

    def __init__(self) -> None:
        required_files = [
            SCALER_PATH,
            MODEL_PATH,
            THRESHOLDS_PATH,
        ]

        missing_files = [
            str(path)
            for path in required_files
            if not path.exists()
        ]

        if missing_files:
            raise FileNotFoundError(
                "Missing real-only model files:\n"
                + "\n".join(missing_files)
            )

        self.scaler = joblib.load(SCALER_PATH)
        self.model = joblib.load(MODEL_PATH)

        with THRESHOLDS_PATH.open(
            "r",
            encoding="utf-8",
        ) as threshold_file:
            thresholds = json.load(threshold_file)

        self.threshold = float(
            thresholds["random_forest"]
        )

        model_classes = list(self.model.classes_)

        if 1 not in model_classes:
            raise ValueError(
                f"Attack class 1 is absent from model classes: "
                f"{model_classes}"
            )

        self.attack_class_index = model_classes.index(1)

    @staticmethod
    def _feature_vector(
        flow: dict[str, Any],
    ) -> np.ndarray:
        """Convert one FlowGuard flow dictionary into model order."""

        missing_features = [
            feature
            for feature in FEATURE_COLUMNS
            if feature not in flow
        ]

        if missing_features:
            raise KeyError(
                "Flow is missing required features: "
                + ", ".join(missing_features)
            )

        values = []

        for feature in FEATURE_COLUMNS:
            value = float(flow[feature])

            if not np.isfinite(value):
                raise ValueError(
                    f"Feature {feature} is not finite: {value}"
                )

            values.append(value)

        return np.asarray(
            [values],
            dtype=np.float32,
        )

    def predict(
        self,
        flow: dict[str, Any],
    ) -> dict[str, Any]:
        """Return the Random Forest attack decision and probability."""

        raw_features = self._feature_vector(flow)
        scaled_features = self.scaler.transform(raw_features)

        probabilities = self.model.predict_proba(
            scaled_features
        )[0]

        attack_probability = float(
            probabilities[self.attack_class_index]
        )

        alert = attack_probability >= self.threshold

        return {
            "alert": bool(alert),
            "predicted_label": (
                "ATTACK" if alert else "BENIGN"
            ),
            "attack_probability": round(
                attack_probability,
                6,
            ),
            "threshold": round(
                self.threshold,
                6,
            ),
            "model": "real_only_random_forest",
        }


def test_jsonl(
    jsonl_path: Path,
    maximum_flows: int,
) -> None:
    """Score several flows from an existing FlowGuard JSONL file."""

    predictor = RealOnlyRandomForestPredictor()

    scored_flows = 0

    with jsonl_path.open(
        "r",
        encoding="utf-8",
    ) as flow_file:
        for line_number, line in enumerate(
            flow_file,
            start=1,
        ):
            if not line.strip():
                continue

            try:
                flow = json.loads(line)
                result = predictor.predict(flow)

                print(
                    json.dumps(
                        {
                            "line": line_number,
                            "src_ip": flow.get("src_ip"),
                            "dst_ip": flow.get("dst_ip"),
                            **result,
                        },
                        indent=2,
                    )
                )

                scored_flows += 1

                if scored_flows >= maximum_flows:
                    break

            except Exception as error:
                print(
                    f"Skipped line {line_number}: {error}",
                    file=sys.stderr,
                )

    if scored_flows == 0:
        raise RuntimeError(
            "No compatible flows were scored."
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(
            "Usage: python -m app.ml.real_only_predictor "
            "<flows.jsonl> [maximum_flows]"
        )

    input_path = Path(sys.argv[1])
    maximum = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    test_jsonl(input_path, maximum)
PY

2. Verify the saved threshold

cat /home/pd/Downloads/flowguard/ml-service/app/models/real_only/thresholds.json

You should see a random_forest threshold near:

0.023552

3. Test it against existing FlowGuard flows

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

PYTHONPATH=. python -m app.ml.real_only_predictor \
  /home/pd/Downloads/flowguard/data/flows_output.jsonl \
  5

Expected output for each compatible flow:

{
  "line": 1,
  "src_ip": "...",
  "dst_ip": "...",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.82,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}

4. What this proves

This confirms:

C++ flow output
      ↓
11 FlowGuard features
      ↓
real CICIDS2017 scaler
      ↓
real CICIDS2017 Random Forest
      ↓
live attack probability and decision

It does not produce a new accuracy score because your live JSONL flows have no ground-truth labels.

Run the predictor command and paste its output; the following step will connect this class to your existing /analyze endpoint without breaking the current API.

Pasted text(7).txt
Document

The predictor is loading correctly. The failure is only because your C++ JSONL contains the base counters but not these four derived features:

bytes_per_sec
packets_per_sec
syn_ack_ratio
rst_ratio

All 799 flows were skipped for that same reason.

Patch the predictor so it calculates those values automatically.
1. Apply the fix

Run from anywhere:

python - <<'PY'
from pathlib import Path
import re

path = Path(
    "/home/pd/Downloads/flowguard/"
    "ml-service/app/ml/real_only_predictor.py"
)

text = path.read_text(encoding="utf-8")

pattern = r'''    @staticmethod
    def _feature_vector\(
        flow: dict\[str, Any\],
    \) -> np\.ndarray:
.*?
    def predict\('''

replacement = '''    @staticmethod
    def _feature_vector(
        flow: dict[str, Any],
    ) -> np.ndarray:
        """
        Build the eleven model features.

        The C++ capture output stores basic counters. Rate and ratio
        features are calculated here when they are not already present.
        """

        required_base_features = [
            "duration_seconds",
            "packet_count",
            "total_bytes",
            "syn_count",
            "ack_count",
            "fin_count",
            "rst_count",
        ]

        missing_features = [
            feature
            for feature in required_base_features
            if feature not in flow
        ]

        if missing_features:
            raise KeyError(
                "Flow is missing required base features: "
                + ", ".join(missing_features)
            )

        duration_seconds = float(flow["duration_seconds"])
        packet_count = float(flow["packet_count"])
        total_bytes = float(flow["total_bytes"])

        syn_count = float(flow["syn_count"])
        ack_count = float(flow["ack_count"])
        fin_count = float(flow["fin_count"])
        rst_count = float(flow["rst_count"])

        # Avoid division by zero for extremely short or empty flows.
        bytes_per_sec = float(
            flow.get(
                "bytes_per_sec",
                total_bytes / duration_seconds
                if duration_seconds > 0
                else 0.0,
            )
        )

        packets_per_sec = float(
            flow.get(
                "packets_per_sec",
                packet_count / duration_seconds
                if duration_seconds > 0
                else 0.0,
            )
        )

        syn_ack_ratio = float(
            flow.get(
                "syn_ack_ratio",
                syn_count / (ack_count + 1.0),
            )
        )

        rst_ratio = float(
            flow.get(
                "rst_ratio",
                rst_count / (packet_count + 1.0),
            )
        )

        feature_values = {
            "duration_seconds": duration_seconds,
            "packet_count": packet_count,
            "total_bytes": total_bytes,
            "bytes_per_sec": bytes_per_sec,
            "packets_per_sec": packets_per_sec,
            "syn_count": syn_count,
            "ack_count": ack_count,
            "fin_count": fin_count,
            "rst_count": rst_count,
            "syn_ack_ratio": syn_ack_ratio,
            "rst_ratio": rst_ratio,
        }

        for feature_name, value in feature_values.items():
            if not np.isfinite(value):
                raise ValueError(
                    f"Feature {feature_name} is not finite: {value}"
                )

        ordered_values = [
            feature_values[feature_name]
            for feature_name in FEATURE_COLUMNS
        ]

        return np.asarray(
            [ordered_values],
            dtype=np.float32,
        )

    def predict('''

updated_text, replacements = re.subn(
    pattern,
    replacement,
    text,
    flags=re.DOTALL,
)

if replacements != 1:
    raise SystemExit(
        f"Patch failed: expected 1 function, found {replacements}"
    )

path.write_text(updated_text, encoding="utf-8")
print(f"Updated: {path}")
PY

2. Check the Python syntax

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python -m py_compile app/ml/real_only_predictor.py

No output means the syntax is valid.
3. Run the predictor again

PYTHONPATH=. python -m app.ml.real_only_predictor \
  /home/pd/Downloads/flowguard/data/flows_output.jsonl \
  5

You should now receive five results resembling:

{
  "line": 1,
  "src_ip": "192.168.x.x",
  "dst_ip": "x.x.x.x",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.74,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}

4. Ignore the other two errors for now

These failed because the files have not been created yet:

scripts/benchmark_capture.sh
training/loao_eval.py

They were proposed future scripts, not existing project files. Also continue using the actual project path:

/home/pd/Downloads/flowguard

rather than:

~/flowguard

The immediate goal is to get five live-flow predictions successfully. After that, the real predictor gets connected to the FastAPI /analyze endpoint.


path.write_text(updated_text, encoding="utf-8")
print(f"Updated: {path}")
PY
Updated: /home/pd/Downloads/flowguard/ml-service/app/ml/real_only_predictor.py

flowguard main  ? ❯ builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python -m py_compile app/ml/real_only_predictor.py

flowguard/ml-service main  ? ❯ PYTHONPATH=. python -m app.ml.real_only_predictor \
  /home/pd/Downloads/flowguard/data/flows_output.jsonl \
  5
{
  "line": 1,
  "src_ip": "10.10.2.1",
  "dst_ip": "10.10.2.101",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.155631,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}
{
  "line": 2,
  "src_ip": "10.10.2.1",
  "dst_ip": "10.10.2.101",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.154424,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}
{
  "line": 3,
  "src_ip": "10.10.2.1",
  "dst_ip": "10.10.2.101",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.152424,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}
{
  "line": 4,
  "src_ip": "10.10.2.1",
  "dst_ip": "10.10.2.101",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.154424,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}
{
  "line": 5,
  "src_ip": "10.10.2.1",
  "dst_ip": "10.10.2.101",
  "alert": true,
  "predicted_label": "ATTACK",
  "attack_probability": 0.154424,
  "threshold": 0.023552,
  "model": "real_only_random_forest"
}

flowguard/ml-service main  ? ❯

Great — the real-data predictor is working on your C++ flow output.

All five were marked as attacks because:

attack probability ≈ 0.15
configured threshold = 0.023552

That does not prove those five flows are genuine attacks; the live PCAP lacks ground-truth labels. We will first expose the model through a separate shadow-mode API endpoint without changing or breaking your existing /analyze endpoint.
1. Create the new API route

Run:

mkdir -p /home/pd/Downloads/flowguard/ml-service/app/routes
touch /home/pd/Downloads/flowguard/ml-service/app/routes/__init__.py

Then create the route:

cat > /home/pd/Downloads/flowguard/ml-service/app/routes/real_analysis.py <<'PY'
"""
Shadow-mode API route for FlowGuard's real-data Random Forest.

This endpoint:
- reads recent C++-generated flows,
- derives missing rate and ratio features,
- scores them with the verified CICIDS2017 Random Forest,
- returns predictions without modifying the existing alert pipeline.

The results are model predictions, not verified ground-truth attacks.
"""

from __future__ import annotations

import json
import os
from collections import deque
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from app.ml.real_only_predictor import RealOnlyRandomForestPredictor


router = APIRouter(
    prefix="/real-model",
    tags=["real-model"],
)

predictor = RealOnlyRandomForestPredictor()


def resolve_flow_file() -> Path:
    """Find the FlowGuard JSONL file in local or Docker execution."""

    candidates = []

    configured_path = os.getenv("FLOWGUARD_FLOW_FILE")

    if configured_path:
        candidates.append(Path(configured_path))

    candidates.extend(
        [
            # Docker shared data volume.
            Path("/data/flows_output.jsonl"),

            # Local repository:
            # flowguard/data/flows_output.jsonl
            Path(__file__).resolve().parents[3]
            / "data"
            / "flows_output.jsonl",
        ]
    )

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "flows_output.jsonl was not found. Checked: "
        + ", ".join(str(path) for path in candidates)
    )


@router.get("/health")
def real_model_health() -> dict:
    """Confirm that the real-data model and flow file are available."""

    try:
        flow_file = resolve_flow_file()

        return {
            "status": "ok",
            "model": "real_only_random_forest",
            "threshold": predictor.threshold,
            "flow_file": str(flow_file),
            "mode": "shadow",
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error


@router.post("/analyze")
def analyze_real_flows(
    limit: int = Query(
        default=50,
        ge=1,
        le=5000,
    ),
) -> dict:
    """
    Score the most recent flows without saving alerts.

    Shadow mode lets us inspect behaviour before replacing the current
    production ensemble.
    """

    try:
        flow_file = resolve_flow_file()
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    recent_lines: deque[tuple[int, str]] = deque(
        maxlen=limit
    )

    try:
        with flow_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            for line_number, line in enumerate(
                file,
                start=1,
            ):
                if line.strip():
                    recent_lines.append(
                        (line_number, line)
                    )

    except OSError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not read flow file: {error}",
        ) from error

    results = []
    errors = []

    for line_number, line in recent_lines:
        try:
            flow = json.loads(line)
            prediction = predictor.predict(flow)

            results.append(
                {
                    "line": line_number,
                    "src_ip": flow.get("src_ip"),
                    "dst_ip": flow.get("dst_ip"),
                    "src_port": flow.get("src_port"),
                    "dst_port": flow.get("dst_port"),
                    "protocol": flow.get("protocol"),
                    **prediction,
                }
            )

        except Exception as error:
            errors.append(
                {
                    "line": line_number,
                    "error": str(error),
                }
            )

    alert_count = sum(
        1
        for result in results
        if result["alert"]
    )

    benign_count = len(results) - alert_count

    return {
        "mode": "shadow",
        "model": "real_only_random_forest",
        "threshold": predictor.threshold,
        "flow_file": str(flow_file),
        "requested": limit,
        "analyzed": len(results),
        "alerts": alert_count,
        "benign": benign_count,
        "errors": len(errors),
        "results": results,
        "error_details": errors[:20],
        "warning": (
            "Predictions are not verified attacks because live flows "
            "do not contain ground-truth labels."
        ),
    }
PY

2. Register the route in app/main.py

Run this safe patch:

python - <<'PY'
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/"
    "ml-service/app/main.py"
)

text = path.read_text(encoding="utf-8")

marker = "# FlowGuard real-data shadow endpoint"

if marker in text:
    print("Real-data route is already registered.")
else:
    addition = """

# FlowGuard real-data shadow endpoint
from app.routes.real_analysis import router as real_analysis_router
app.include_router(real_analysis_router)
"""

    path.write_text(
        text.rstrip() + addition + "\n",
        encoding="utf-8",
    )

    print(f"Updated: {path}")
PY

3. Check syntax and imports

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python -m py_compile \
  app/main.py \
  app/routes/real_analysis.py \
  app/ml/real_only_predictor.py

No output means the syntax is correct.

Test importing the complete API:

PYTHONPATH=. python -c "from app.main import app; print([route.path for route in app.routes if 'real-model' in route.path])"

Expected:

['/real-model/health', '/real-model/analyze']

4. Start FastAPI

Keep this terminal open:

PYTHONPATH=. uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload

5. Test it from another terminal

Health check:

curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool

Run shadow analysis on the five most recent flows:

curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=5" \
  | python -m json.tool

This completes:

C++ packet parsing
        ↓
JSONL flow aggregation
        ↓
derived flow features
        ↓
real CICIDS2017 scaler
        ↓
real CICIDS2017 Random Forest
        ↓
FastAPI response

Keep this in shadow mode until we inspect the API output and decide whether the very low 0.023552 threshold is suitable for live alert generation.


flowguard/ml-service main  ? ❯ python - <<'PY'
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/"
    "ml-service/app/main.py"
)

text = path.read_text(encoding="utf-8")

marker = "# FlowGuard real-data shadow endpoint"

if marker in text:
    print("Real-data route is already registered.")
else:
    addition = """

# FlowGuard real-data shadow endpoint
from app.routes.real_analysis import router as real_analysis_router
app.include_router(real_analysis_router)
"""

    path.write_text(
        text.rstrip() + addition + "\n",
        encoding="utf-8",
    )

    print(f"Updated: {path}")
PY
Updated: /home/pd/Downloads/flowguard/ml-service/app/main.py

flowguard/ml-service main  ? ❯ builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python -m py_compile \
  app/main.py \
  app/routes/real_analysis.py \
  app/ml/real_only_predictor.py

flowguard/ml-service main  ? ❯ PYTHONPATH=. python -c "from app.main import app; print([route.path for route in app.routes if 'real-model' in route.path])"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from app.main import app; print([route.path for route in app.routes if 'real-model' in route.path])
    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/pd/Downloads/flowguard/ml-service/app/main.py", line 1, in <module>
    from app.ml.ensemble import EnsembleDetector
ImportError: cannot import name 'EnsembleDetector' from 'app.ml.ensemble' (/home/pd/Downloads/flowguard/ml-service/app/ml/ensemble.py)

Your new route is fine. The API fails earlier because app/main.py expects a class named:

EnsembleDetector

but app/ml/ensemble.py currently defines a different class name, most likely Ensemble.

Use a backward-compatible alias instead of rewriting the API.
1. Back up and patch ensemble.py

builtin cd /home/pd/Downloads/flowguard/ml-service

cp app/ml/ensemble.py app/ml/ensemble.py.bak

python - <<'PY'
from pathlib import Path
import ast

path = Path("app/ml/ensemble.py")
source = path.read_text(encoding="utf-8")
tree = ast.parse(source)

class_names = {
    node.name
    for node in tree.body
    if isinstance(node, ast.ClassDef)
}

print("Classes found:", sorted(class_names))

if "EnsembleDetector" in class_names:
    print("EnsembleDetector already exists.")

elif "Ensemble" in class_names:
    alias = "\n\n# Backward-compatible class name expected by app.main\nEnsembleDetector = Ensemble\n"

    if "EnsembleDetector = Ensemble" not in source:
        path.write_text(
            source.rstrip() + alias,
            encoding="utf-8",
        )

    print("Added alias: EnsembleDetector = Ensemble")

else:
    raise SystemExit(
        "Neither EnsembleDetector nor Ensemble exists in ensemble.py"
    )
PY

2. Check syntax

python -m py_compile \
  app/ml/ensemble.py \
  app/main.py \
  app/routes/real_analysis.py

3. Test the API import again

PYTHONPATH=. python -c "from app.main import app; print([route.path for route in app.routes if 'real-model' in route.path])"

Expected:

['/real-model/health', '/real-model/analyze']

If a new error appears after this, paste only that new traceback.


flowguard/ml-service main  ? ✗ builtin cd /home/pd/Downloads/flowguard/ml-service

cp app/ml/ensemble.py app/ml/ensemble.py.bak

python - <<'PY'
from pathlib import Path
import ast

path = Path("app/ml/ensemble.py")
source = path.read_text(encoding="utf-8")
tree = ast.parse(source)

class_names = {
    node.name
    for node in tree.body
    if isinstance(node, ast.ClassDef)
}

print("Classes found:", sorted(class_names))

if "EnsembleDetector" in class_names:
    print("EnsembleDetector already exists.")

elif "Ensemble" in class_names:
    alias = "\n\n# Backward-compatible class name expected by app.main\nEnsembleDetector = Ensemble\n"

    if "EnsembleDetector = Ensemble" not in source:
        path.write_text(
            source.rstrip() + alias,
            encoding="utf-8",
        )

    print("Added alias: EnsembleDetector = Ensemble")

else:
    raise SystemExit(
        "Neither EnsembleDetector nor Ensemble exists in ensemble.py"
    )
PY
Classes found: ['Ensemble']
Added alias: EnsembleDetector = Ensemble

flowguard/ml-service main  ? ❯ python -m py_compile \
  app/ml/ensemble.py \
  app/main.py \
  app/routes/real_analysis.py

flowguard/ml-service main  ? ❯ PYTHONPATH=. python -c "from app.main import app; print([route.path for route in app.routes if 'real-model' in route.path])"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from app.main import app; print([route.path for route in app.routes if 'real-model' in route.path])
    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/pd/Downloads/flowguard/ml-service/app/main.py", line 19, in <module>
    detector = EnsembleDetector()
  File "/home/pd/Downloads/flowguard/ml-service/app/ml/ensemble.py", line 38, in __init__
    self.gnn.load_state_dict(torch.load(f"{model_dir}/gnn_graphsage.pt"))
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/pd/Downloads/flowguard/ml-service/.venv/lib/python3.14/site-packages/torch/nn/modules/module.py", line 2638, in load_state_dict
    raise RuntimeError(
    ...<3 lines>...
    )
RuntimeError: Error(s) in loading state_dict for FlowGraphSAGE:
	size mismatch for conv1.lin_l.weight: copying a param with shape torch.Size([32, 4]) from checkpoint, the shape in current model is torch.Size([32, 2]).
	size mismatch for conv1.lin_r.weight: copying a param with shape torch.Size([32, 4]) from checkpoint, the shape in current model is torch.Size([32, 2]).

flowguard/ml-service main  ? ✗?

The checkpoint was trained with 4 input features, but ensemble.py creates the GNN with only 2 input features:

checkpoint: 4 inputs
current model: 2 inputs

Patch it to infer the correct input size automatically.

Run:

builtin cd /home/pd/Downloads/flowguard/ml-service

python - <<'PY'
from pathlib import Path
import re

path = Path("app/ml/ensemble.py")
text = path.read_text(encoding="utf-8")

pattern = r'''self\.gnn\s*=\s*FlowGraphSAGE\(in_channels=2\)
\s*self\.gnn\.load_state_dict\(torch\.load\(f"\{model_dir\}/gnn_graphsage\.pt"\)\)'''

replacement = '''gnn_checkpoint_path = f"{model_dir}/gnn_graphsage.pt"
        gnn_state_dict = torch.load(
            gnn_checkpoint_path,
            map_location="cpu",
        )

        # Infer the input feature count directly from the saved checkpoint.
        gnn_input_channels = int(
            gnn_state_dict["conv1.lin_l.weight"].shape[1]
        )

        self.gnn = FlowGraphSAGE(
            in_channels=gnn_input_channels
        )

        self.gnn.load_state_dict(gnn_state_dict)'''

updated, count = re.subn(
    pattern,
    replacement,
    text,
)

if count != 1:
    raise SystemExit(
        f"Patch failed: expected 1 matching GNN block, found {count}"
    )

path.write_text(updated, encoding="utf-8")

print("Updated GNN loader.")
print("Input channels will now be inferred from the checkpoint.")
PY

Check syntax:

python -m py_compile \
  app/ml/ensemble.py \
  app/main.py \
  app/routes/real_analysis.py

Then test the API import again:

PYTHONPATH=. python -c "
from app.main import app
print([route.path for route in app.routes if 'real-model' in route.path])
"

Expected:

['/real-model/health', '/real-model/analyze']

This fixes the immediate mismatch without hardcoding 4. If the GNN is retrained later with a different number of features, the loader will adapt automatically.


flowguard/ml-service main  ? ✗ builtin cd /home/pd/Downloads/flowguard/ml-service

python - <<'PY'
from pathlib import Path
import re

path = Path("app/ml/ensemble.py")
text = path.read_text(encoding="utf-8")

pattern = r'''self\.gnn\s*=\s*FlowGraphSAGE\(in_channels=2\)
\s*self\.gnn\.load_state_dict\(torch\.load\(f"\{model_dir\}/gnn_graphsage\.pt"\)\)'''

replacement = '''gnn_checkpoint_path = f"{model_dir}/gnn_graphsage.pt"
        gnn_state_dict = torch.load(
            gnn_checkpoint_path,
            map_location="cpu",
        )

        # Infer the input feature count directly from the saved checkpoint.
        gnn_input_channels = int(
            gnn_state_dict["conv1.lin_l.weight"].shape[1]
        )

        self.gnn = FlowGraphSAGE(
            in_channels=gnn_input_channels
        )

        self.gnn.load_state_dict(gnn_state_dict)'''

updated, count = re.subn(
    pattern,
    replacement,
    text,
)

if count != 1:
    raise SystemExit(
        f"Patch failed: expected 1 matching GNN block, found {count}"
    )

path.write_text(updated, encoding="utf-8")

print("Updated GNN loader.")
print("Input channels will now be inferred from the checkpoint.")
PY
Updated GNN loader.
Input channels will now be inferred from the checkpoint.

flowguard/ml-service main  ? ❯ python -m py_compile \
  app/ml/ensemble.py \
  app/main.py \
  app/routes/real_analysis.py

flowguard/ml-service main  ? ❯ PYTHONPATH=. python -c "
from app.main import app
print([route.path for route in app.routes if 'real-model' in route.path])
"
Traceback (most recent call last):
  File "<string>", line 3, in <module>
    print([route.path for route in app.routes if 'real-model' in route.path])
                                                                 ^^^^^^^^^^
AttributeError: '_IncludedRouter' object has no attribute 'path'

flowguard/ml-service main  ? ✗

The API import now succeeds. The error is only from the route-inspection command, because one object in app.routes has no .path attribute.

Run this safer check:

PYTHONPATH=. python - <<'PY'
from app.main import app

paths = [
    getattr(route, "path", None)
    for route in app.routes
]

print([
    path
    for path in paths
    if path and "real-model" in path
])
PY

Expected:

['/real-model/health', '/real-model/analyze']

Then start FastAPI:

PYTHONPATH=. uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload

Keep that terminal open. In another terminal, run:

curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool

Then:

curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=5" \
  | python -m json.tool

Your GNN checkpoint mismatch is fixed; this latest error does not indicate a model or API failure.


flowguard main  ? ❯ curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool
{
    "status": "ok",
    "model": "real_only_random_forest",
    "threshold": 0.023552277985182894,
    "flow_file": "/home/pd/Downloads/flowguard/data/flows_output.jsonl",
    "mode": "shadow"
}

flowguard main  ? ❯ curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=5" \
  | python -m json.tool
{
    "mode": "shadow",
    "model": "real_only_random_forest",
    "threshold": 0.023552277985182894,
    "flow_file": "/home/pd/Downloads/flowguard/data/flows_output.jsonl",
    "requested": 5,
    "analyzed": 5,
    "alerts": 5,
    "benign": 0,
    "errors": 0,
    "results": [
        {
            "line": 795,
            "src_ip": "43.160.255.143",
            "dst_ip": "10.10.2.101",
            "src_port": 8080,
            "dst_port": 56540,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.38435,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 796,
            "src_ip": "43.160.255.143",
            "dst_ip": "10.10.2.101",
            "src_port": 8080,
            "dst_port": 56548,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.082423,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 797,
            "src_ip": "45.207.200.251",
            "dst_ip": "10.10.2.101",
            "src_port": 80,
            "dst_port": 34800,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.385731,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 798,
            "src_ip": "45.207.200.251",
            "dst_ip": "10.10.2.101",
            "src_port": 80,
            "dst_port": 45152,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.219635,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 799,
            "src_ip": "45.207.207.168",
            "dst_ip": "10.10.2.101",
            "src_port": 80,
            "dst_port": 38408,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.36909,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        }
    ],
    "error_details": [],
    "warning": "Predictions are not verified attacks because live flows do not contain ground-truth labels."
}

flowguard main  ? ❯

It is working end to end:

C++ flow capture
→ JSONL
→ derived features
→ real CICIDS2017 scaler
→ real-data Random Forest
→ FastAPI shadow endpoint

The next step is threshold analysis. Your current threshold, 0.023552, is very low, so nearly any probability above 2.35% becomes an alert. Do not connect it to permanent alert storage yet.
1. Analyze all 799 flows

mkdir -p /home/pd/Downloads/flowguard/docs

curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=799" \
  > /home/pd/Downloads/flowguard/docs/live_shadow_predictions.json

Verify:

python -m json.tool \
  /home/pd/Downloads/flowguard/docs/live_shadow_predictions.json \
  | head -n 30

2. Compare different thresholds

Run:

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "live_shadow_predictions.json"
)

payload = json.loads(path.read_text(encoding="utf-8"))
results = payload["results"]

probabilities = sorted(
    float(result["attack_probability"])
    for result in results
)

def percentile(values, fraction):
    if not values:
        return 0.0

    index = round((len(values) - 1) * fraction)
    return values[index]

print("===== LIVE SHADOW-MODE SUMMARY =====")
print(f"Flows analysed: {len(probabilities)}")
print(f"Minimum probability: {min(probabilities):.6f}")
print(f"Median probability:  {percentile(probabilities, 0.50):.6f}")
print(f"75th percentile:     {percentile(probabilities, 0.75):.6f}")
print(f"90th percentile:     {percentile(probabilities, 0.90):.6f}")
print(f"95th percentile:     {percentile(probabilities, 0.95):.6f}")
print(f"Maximum probability: {max(probabilities):.6f}")

print("\n===== ALERT COUNTS BY THRESHOLD =====")

for threshold in [
    0.023552,
    0.05,
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.70,
]:
    alerts = sum(
        probability >= threshold
        for probability in probabilities
    )

    percentage = (
        100.0 * alerts / len(probabilities)
        if probabilities
        else 0.0
    )

    print(
        f"Threshold {threshold:>8.6f}: "
        f"{alerts:>4}/{len(probabilities)} alerts "
        f"({percentage:>6.2f}%)"
    )
PY

3. Show the most suspicious flows

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "live_shadow_predictions.json"
)

payload = json.loads(path.read_text(encoding="utf-8"))

ranked = sorted(
    payload["results"],
    key=lambda item: item["attack_probability"],
    reverse=True,
)

print("===== TOP 20 MODEL-PREDICTED FLOWS =====")

for number, flow in enumerate(ranked[:20], start=1):
    print(
        f"{number:02d}. "
        f"probability={flow['attack_probability']:.6f} | "
        f"{flow.get('src_ip')}:{flow.get('src_port')} -> "
        f"{flow.get('dst_ip')}:{flow.get('dst_port')} | "
        f"{flow.get('protocol')}"
    )
PY

What we are deciding

The output will help choose an operating mode:

Low threshold
→ catches more attacks
→ produces more false alarms

High threshold
→ produces fewer false alarms
→ may miss more attacks

Your verified CICIDS2017 metrics still belong to threshold 0.023552. Changing the live threshold does not change those documented test metrics unless we evaluate the new threshold again on the labelled test set.

Paste the alert-count table and top 20 flows next.


flowguard main  ? ❯ curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool
{
    "status": "ok",
    "model": "real_only_random_forest",
    "threshold": 0.023552277985182894,
    "flow_file": "/home/pd/Downloads/flowguard/data/flows_output.jsonl",
    "mode": "shadow"
}

flowguard main  ? ❯ curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=5" \
  | python -m json.tool
{
    "mode": "shadow",
    "model": "real_only_random_forest",
    "threshold": 0.023552277985182894,
    "flow_file": "/home/pd/Downloads/flowguard/data/flows_output.jsonl",
    "requested": 5,
    "analyzed": 5,
    "alerts": 5,
    "benign": 0,
    "errors": 0,
    "results": [
        {
            "line": 795,
            "src_ip": "43.160.255.143",
            "dst_ip": "10.10.2.101",
            "src_port": 8080,
            "dst_port": 56540,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.38435,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 796,
            "src_ip": "43.160.255.143",
            "dst_ip": "10.10.2.101",
            "src_port": 8080,
            "dst_port": 56548,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.082423,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 797,
            "src_ip": "45.207.200.251",
            "dst_ip": "10.10.2.101",
            "src_port": 80,
            "dst_port": 34800,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.385731,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 798,
            "src_ip": "45.207.200.251",
            "dst_ip": "10.10.2.101",
            "src_port": 80,
            "dst_port": 45152,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.219635,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 799,
            "src_ip": "45.207.207.168",
            "dst_ip": "10.10.2.101",
            "src_port": 80,
            "dst_port": 38408,
            "protocol": "TCP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.36909,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        }
    ],
    "error_details": [],
    "warning": "Predictions are not verified attacks because live flows do not contain ground-truth labels."
}

flowguard main  ? ❯ mkdir -p /home/pd/Downloads/flowguard/docs

curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=799" \
  > /home/pd/Downloads/flowguard/docs/live_shadow_predictions.json

flowguard main  ? ❯ python -m json.tool \
  /home/pd/Downloads/flowguard/docs/live_shadow_predictions.json \
  | head -n 30
{
    "mode": "shadow",
    "model": "real_only_random_forest",
    "threshold": 0.023552277985182894,
    "flow_file": "/home/pd/Downloads/flowguard/data/flows_output.jsonl",
    "requested": 799,
    "analyzed": 799,
    "alerts": 762,
    "benign": 37,
    "errors": 0,
    "results": [
        {
            "line": 1,
            "src_ip": "10.10.2.1",
            "dst_ip": "10.10.2.101",
            "src_port": 53,
            "dst_port": 1159,
            "protocol": "UDP",
            "alert": true,
            "predicted_label": "ATTACK",
            "attack_probability": 0.155631,
            "threshold": 0.023552,
            "model": "real_only_random_forest"
        },
        {
            "line": 2,
            "src_ip": "10.10.2.1",
            "dst_ip": "10.10.2.101",
            "src_port": 53,
            "dst_port": 1711,

flowguard main  ? ❯
flowguard main  ? ❯ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "live_shadow_predictions.json"
)

payload = json.loads(path.read_text(encoding="utf-8"))
results = payload["results"]

probabilities = sorted(
    float(result["attack_probability"])
    for result in results
)

def percentile(values, fraction):
    if not values:
        return 0.0

    index = round((len(values) - 1) * fraction)
    return values[index]

print("===== LIVE SHADOW-MODE SUMMARY =====")
print(f"Flows analysed: {len(probabilities)}")
print(f"Minimum probability: {min(probabilities):.6f}")
print(f"Median probability:  {percentile(probabilities, 0.50):.6f}")
print(f"75th percentile:     {percentile(probabilities, 0.75):.6f}")
print(f"90th percentile:     {percentile(probabilities, 0.90):.6f}")
print(f"95th percentile:     {percentile(probabilities, 0.95):.6f}")
print(f"Maximum probability: {max(probabilities):.6f}")

print("\n===== ALERT COUNTS BY THRESHOLD =====")

for threshold in [
    0.023552,
    0.05,
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.70,
]:
    alerts = sum(
        probability >= threshold
        for probability in probabilities
    )

    percentage = (
        100.0 * alerts / len(probabilities)
        if probabilities
        else 0.0
    )

    print(
        f"Threshold {threshold:>8.6f}: "
        f"{alerts:>4}/{len(probabilities)} alerts "
        f"({percentage:>6.2f}%)"
    )
PY
===== LIVE SHADOW-MODE SUMMARY =====
Flows analysed: 799
Minimum probability: 0.003667
Median probability:  0.270419
75th percentile:     0.418763
90th percentile:     0.456239
95th percentile:     0.469807
Maximum probability: 0.616022

===== ALERT COUNTS BY THRESHOLD =====
Threshold 0.023552:  762/799 alerts ( 95.37%)
Threshold 0.050000:  756/799 alerts ( 94.62%)
Threshold 0.100000:  731/799 alerts ( 91.49%)
Threshold 0.200000:  514/799 alerts ( 64.33%)
Threshold 0.300000:  371/799 alerts ( 46.43%)
Threshold 0.400000:  251/799 alerts ( 31.41%)
Threshold 0.500000:    5/799 alerts (  0.63%)
Threshold 0.700000:    0/799 alerts (  0.00%)

flowguard main  ? ❯
flowguard main  ? ❯ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "live_shadow_predictions.json"
)

payload = json.loads(path.read_text(encoding="utf-8"))

ranked = sorted(
    payload["results"],
    key=lambda item: item["attack_probability"],
    reverse=True,
)

print("===== TOP 20 MODEL-PREDICTED FLOWS =====")

for number, flow in enumerate(ranked[:20], start=1):
    print(
        f"{number:02d}. "
        f"probability={flow['attack_probability']:.6f} | "
        f"{flow.get('src_ip')}:{flow.get('src_port')} -> "
        f"{flow.get('dst_ip')}:{flow.get('dst_port')} | "
        f"{flow.get('protocol')}"
    )
PY
===== TOP 20 MODEL-PREDICTED FLOWS =====
01. probability=0.616022 | 142.250.138.139:443 -> 10.10.2.101:60046 | TCP
02. probability=0.524693 | 10.10.2.101:55566 -> 101.32.207.8:8080 | TCP
03. probability=0.516668 | 10.10.2.101:55560 -> 101.32.207.8:8080 | TCP
04. probability=0.513736 | 10.10.2.101:57660 -> 173.194.208.94:443 | TCP
05. probability=0.513736 | 10.10.2.101:57674 -> 173.194.208.94:443 | TCP
06. probability=0.492760 | 10.10.2.101:40782 -> 101.32.207.8:8080 | TCP
07. probability=0.490528 | 10.10.2.101:40810 -> 101.32.207.8:8080 | TCP
08. probability=0.490528 | 10.10.2.101:40298 -> 154.90.54.222:8080 | TCP
09. probability=0.490528 | 10.10.2.101:54066 -> 43.157.1.82:8080 | TCP
10. probability=0.490528 | 10.10.2.101:46096 -> 43.157.184.190:8080 | TCP
11. probability=0.490528 | 10.10.2.101:44200 -> 43.160.255.143:8080 | TCP
12. probability=0.488850 | 43.157.184.190:8080 -> 10.10.2.101:41176 | TCP
13. probability=0.488528 | 10.10.2.101:45086 -> 43.159.143.39:8080 | TCP
14. probability=0.486856 | 10.10.2.101:40798 -> 101.32.207.8:8080 | TCP
15. probability=0.484508 | 43.157.184.190:8080 -> 10.10.2.101:41154 | TCP
16. probability=0.484508 | 43.157.184.190:8080 -> 10.10.2.101:41162 | TCP
17. probability=0.482174 | 43.157.184.190:8080 -> 10.10.2.101:37784 | TCP
18. probability=0.478303 | 101.32.207.8:8080 -> 10.10.2.101:38848 | TCP
19. probability=0.472808 | 101.32.207.8:8080 -> 10.10.2.101:40112 | TCP
20. probability=0.472808 | 101.32.207.8:8080 -> 10.10.2.101:45962 | TCP

flowguard main  ? ❯

Pasted text(8).txt
Document
?

Your threshold tuning is complete.

The correct mode is balanced:

Threshold: 0.0235
Accuracy:  86.09%
Precision: 78.71%
Recall:    98.94%
F1:        87.67%

The high_recall mode only increased recall slightly—from 98.94% to 99.18%—but caused many more false positives and reduced accuracy to 78.08%. Also, your model could not achieve the requested 95% validation precision, so the script fell back to the same threshold as balanced; high_precision is therefore not a genuinely distinct mode. Thresholds such as 0.5 must not be used because validation recall collapsed to 0.4%.

Now connect the saved balanced threshold to the API.
1. Patch the predictor to load operational modes

builtin cd /home/pd/Downloads/flowguard/ml-service

python - <<'PY'
from pathlib import Path

path = Path("app/ml/real_only_predictor.py")
text = path.read_text(encoding="utf-8")

if "import os" not in text:
    text = text.replace(
        "import json\n",
        "import json\nimport os\n",
        1,
    )

old_constant = '''THRESHOLDS_PATH = MODEL_DIRECTORY / "thresholds.json"'''

new_constant = '''THRESHOLDS_PATH = MODEL_DIRECTORY / "thresholds.json"
OPERATIONAL_THRESHOLDS_PATH = (
    MODEL_DIRECTORY / "rf_operational_thresholds.json"
)'''

text = text.replace(
    old_constant,
    new_constant,
    1,
)

old_files = '''        required_files = [
            SCALER_PATH,
            MODEL_PATH,
            THRESHOLDS_PATH,
        ]'''

new_files = '''        required_files = [
            SCALER_PATH,
            MODEL_PATH,
            OPERATIONAL_THRESHOLDS_PATH,
        ]'''

text = text.replace(
    old_files,
    new_files,
    1,
)

old_threshold_block = '''        with THRESHOLDS_PATH.open(
            "r",
            encoding="utf-8",
        ) as threshold_file:
            thresholds = json.load(threshold_file)

        self.threshold = float(
            thresholds["random_forest"]
        )'''

new_threshold_block = '''        with OPERATIONAL_THRESHOLDS_PATH.open(
            "r",
            encoding="utf-8",
        ) as threshold_file:
            threshold_configuration = json.load(
                threshold_file
            )

        self.operational_mode = os.getenv(
            "RF_OPERATIONAL_MODE",
            "balanced",
        ).strip().lower()

        available_modes = threshold_configuration[
            "thresholds"
        ]

        if self.operational_mode not in available_modes:
            raise ValueError(
                f"Unknown RF_OPERATIONAL_MODE: "
                f"{self.operational_mode}. "
                f"Available modes: "
                f"{sorted(available_modes)}"
            )

        self.threshold = float(
            available_modes[self.operational_mode]
        )'''

if old_threshold_block not in text:
    raise SystemExit(
        "Could not find the old threshold-loading block."
    )

text = text.replace(
    old_threshold_block,
    new_threshold_block,
    1,
)

old_return = '''            "threshold": round(
                self.threshold,
                6,
            ),
            "model": "real_only_random_forest",'''

new_return = '''            "threshold": round(
                self.threshold,
                6,
            ),
            "operational_mode": self.operational_mode,
            "model": "real_only_random_forest",'''

text = text.replace(
    old_return,
    new_return,
    1,
)

path.write_text(text, encoding="utf-8")

print(f"Updated: {path}")
PY

2. Update the API health response

python - <<'PY'
from pathlib import Path

path = Path("app/routes/real_analysis.py")
text = path.read_text(encoding="utf-8")

old = '''            "threshold": predictor.threshold,
            "flow_file": str(flow_file),'''

new = '''            "threshold": predictor.threshold,
            "operational_mode": predictor.operational_mode,
            "flow_file": str(flow_file),'''

text = text.replace(old, new, 1)

old_second = '''        "threshold": predictor.threshold,
        "flow_file": str(flow_file),'''

new_second = '''        "threshold": predictor.threshold,
        "operational_mode": predictor.operational_mode,
        "flow_file": str(flow_file),'''

text = text.replace(old_second, new_second, 1)

path.write_text(text, encoding="utf-8")
print(f"Updated: {path}")
PY

3. Validate

python -m py_compile \
  app/ml/real_only_predictor.py \
  app/routes/real_analysis.py \
  app/main.py

4. Restart FastAPI in balanced mode

Stop the current Uvicorn process with Ctrl+C, then run:

RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload

5. Confirm the selected mode

In another terminal:

curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool

Expected:

{
    "status": "ok",
    "model": "real_only_random_forest",
    "threshold": 0.0235,
    "operational_mode": "balanced",
    "mode": "shadow"
}

Keep it in shadow mode. The 95.37% alert rate on the infected-Android capture suggests strong distribution shift, not that 95% of those flows are confirmed malicious.


flowguard main  ? ❯ curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool
{
    "status": "ok",
    "model": "real_only_random_forest",
    "threshold": 0.0235,
    "operational_mode": "balanced",
    "flow_file": "/home/pd/Downloads/flowguard/data/flows_output.jsonl",
    "mode": "shadow"
}

Perfect — the real-data Random Forest is now loaded through FastAPI in balanced shadow mode.

Next, verify predictions under the new operational configuration:

curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=20" \
  | python -m json.tool

Then inspect where your existing /analyze endpoint is defined before we connect the new model:

grep -RInE '@app\.(post|get)\("/analyze"|@router\.(post|get)\("/analyze"|def analyze' \
  /home/pd/Downloads/flowguard/ml-service/app

Also show the surrounding code:

grep -RInE -B 15 -A 80 \
  '@app\.(post|get)\("/analyze"|@router\.(post|get)\("/analyze"|def analyze' \
  /home/pd/Downloads/flowguard/ml-service/app

The next integration will use an environment switch such as:

DETECTION_MODEL=legacy
DETECTION_MODEL=real_rf
DETECTION_MODEL=compare

compare mode will run both systems side by side without replacing your existing alert pipeline. Paste the output of the two grep commands next.

Pasted text(9).txt
Document
?

Your output confirms two things:

    /analyze still uses the legacy ensemble and can persist alerts only when persist=true.

    /real-model/analyze runs the real-data Random Forest separately in shadow mode.

The safest next step is a comparison endpoint. It runs both models on the same flows but saves nothing to PostgreSQL.
1. Add /analyze/compare

Run:

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python - <<'PY'
from pathlib import Path

path = Path("app/main.py")
text = path.read_text(encoding="utf-8")

marker = "# FlowGuard legacy-versus-real comparison endpoint"

if marker in text:
    print("Comparison endpoint is already registered.")
else:
    addition = r'''

# FlowGuard legacy-versus-real comparison endpoint
from app.ml.real_only_predictor import RealOnlyRandomForestPredictor

comparison_real_predictor = RealOnlyRandomForestPredictor()


@app.post("/analyze/compare")
async def compare_detection_models(
    limit: int = 100,
):
    """
    Run the legacy ensemble and real-data Random Forest on the same
    recent flows.

    This endpoint never persists alerts. It is for shadow comparison only.
    """

    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )

    all_flows = read_all_flows()
    flows = all_flows[-limit:]

    start_line = max(
        1,
        len(all_flows) - len(flows) + 1,
    )

    results = []

    legacy_alerts = 0
    real_rf_alerts = 0

    both_alert = 0
    both_benign = 0
    legacy_only = 0
    real_rf_only = 0

    errors = []

    for position, flow in enumerate(
        flows,
        start=start_line,
    ):
        try:
            normalized_features = normalize_flow(flow)

            legacy_feature_row = [
                normalized_features.get(column, 0.0)
                for column in FEATURE_COLUMNS
            ]

            legacy_result = detector.score(
                legacy_feature_row
            )

            real_result = (
                comparison_real_predictor.predict(flow)
            )

            legacy_is_alert = bool(
                legacy_result.get("is_anomaly", False)
            )

            real_is_alert = bool(
                real_result["alert"]
            )

            legacy_alerts += int(legacy_is_alert)
            real_rf_alerts += int(real_is_alert)

            if legacy_is_alert and real_is_alert:
                agreement_type = "both_alert"
                both_alert += 1

            elif not legacy_is_alert and not real_is_alert:
                agreement_type = "both_benign"
                both_benign += 1

            elif legacy_is_alert:
                agreement_type = "legacy_only"
                legacy_only += 1

            else:
                agreement_type = "real_rf_only"
                real_rf_only += 1

            results.append(
                {
                    "line": position,
                    "src_ip": flow.get("src_ip"),
                    "dst_ip": flow.get("dst_ip"),
                    "src_port": flow.get("src_port"),
                    "dst_port": flow.get("dst_port"),
                    "protocol": flow.get("protocol"),
                    "legacy_alert": legacy_is_alert,
                    "real_rf_alert": real_is_alert,
                    "agreement": agreement_type,
                    "real_rf_probability": (
                        real_result["attack_probability"]
                    ),
                    "real_rf_threshold": (
                        real_result["threshold"]
                    ),
                    "real_rf_operational_mode": (
                        real_result["operational_mode"]
                    ),
                }
            )

        except Exception as error:
            errors.append(
                {
                    "line": position,
                    "error": str(error),
                }
            )

    analyzed = len(results)

    agreements = both_alert + both_benign

    agreement_rate = (
        agreements / analyzed
        if analyzed
        else 0.0
    )

    return {
        "mode": "compare-shadow",
        "total_available_flows": len(all_flows),
        "requested": limit,
        "analyzed": analyzed,
        "errors": len(errors),
        "legacy_alerts": legacy_alerts,
        "real_rf_alerts": real_rf_alerts,
        "agreement": {
            "both_alert": both_alert,
            "both_benign": both_benign,
            "legacy_only": legacy_only,
            "real_rf_only": real_rf_only,
            "agreement_rate": round(
                agreement_rate,
                6,
            ),
        },
        "persistence_enabled": False,
        "results": results,
        "error_details": errors[:20],
        "warning": (
            "These are model comparisons, not verified attack labels."
        ),
    }
'''

    path.write_text(
        text.rstrip() + addition + "\n",
        encoding="utf-8",
    )

    print(f"Updated: {path}")
PY

2. Check syntax

python -m py_compile \
  app/main.py \
  app/ml/real_only_predictor.py

No output means it passed.
3. Confirm the route exists

PYTHONPATH=. python - <<'PY'
from app.main import app

print([
    getattr(route, "path", None)
    for route in app.routes
    if getattr(route, "path", None)
    == "/analyze/compare"
])
PY

Expected:

['/analyze/compare']

4. Restart FastAPI

Stop the current Uvicorn process with Ctrl+C, then run:

RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload

5. Compare both detectors

In another terminal:

curl -s -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  > /home/pd/Downloads/flowguard/docs/model_comparison.json

Show the summary without printing all 100 results:

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "model_comparison.json"
)

data = json.loads(
    path.read_text(encoding="utf-8")
)

print("===== MODEL COMPARISON =====")
print("Analyzed:", data["analyzed"])
print("Errors:", data["errors"])
print("Legacy alerts:", data["legacy_alerts"])
print("Real RF alerts:", data["real_rf_alerts"])
print("Both alert:", data["agreement"]["both_alert"])
print("Both benign:", data["agreement"]["both_benign"])
print("Legacy only:", data["agreement"]["legacy_only"])
print("Real RF only:", data["agreement"]["real_rf_only"])
print(
    "Agreement rate:",
    f"{data['agreement']['agreement_rate'] * 100:.2f}%"
)
PY

This keeps the existing alert pipeline untouched while measuring exactly how differently the old ensemble and real-data model behave.


flowguard main  ? ❯ RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
bash: command not found: uvicorn

flowguard main  ? ✗ curl -s -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  > /home/pd/Downloads/flowguard/docs/model_comparison.json

flowguard main  ? ❯
flowguard main  ? ❯ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "model_comparison.json"
)

data = json.loads(
    path.read_text(encoding="utf-8")
)

print("===== MODEL COMPARISON =====")
print("Analyzed:", data["analyzed"])
print("Errors:", data["errors"])
print("Legacy alerts:", data["legacy_alerts"])
print("Real RF alerts:", data["real_rf_alerts"])
print("Both alert:", data["agreement"]["both_alert"])
print("Both benign:", data["agreement"]["both_benign"])
print("Legacy only:", data["agreement"]["legacy_only"])
print("Real RF only:", data["agreement"]["real_rf_only"])
print(
    "Agreement rate:",
    f"{data['agreement']['agreement_rate'] * 100:.2f}%"
)
PY
===== MODEL COMPARISON =====
Analyzed: 0
Errors: 100
Legacy alerts: 0
Real RF alerts: 0
Both alert: 0
Both benign: 0
Legacy only: 0
Real RF only: 0
Agreement rate: 0.00%

flowguard main  ? ❯ 
flowguard main  ? ❯ builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python - <<'PY'
from pathlib import Path

path = Path("app/main.py")
text = path.read_text(encoding="utf-8")

marker = "# FlowGuard legacy-versus-real comparison endpoint"

if marker in text:
    print("Comparison endpoint is already registered.")
else:
    addition = r'''

# FlowGuard legacy-versus-real comparison endpoint
from app.ml.real_only_predictor import RealOnlyRandomForestPredictor

comparison_real_predictor = RealOnlyRandomForestPredictor()


@app.post("/analyze/compare")
async def compare_detection_models(
    limit: int = 100,
):
    """
    Run the legacy ensemble and real-data Random Forest on the same
    recent flows.

    This endpoint never persists alerts. It is for shadow comparison only.
    """

    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )

    all_flows = read_all_flows()
    flows = all_flows[-limit:]

    start_line = max(
        1,
        len(all_flows) - len(flows) + 1,
    )

    results = []

    legacy_alerts = 0
    real_rf_alerts = 0

    both_alert = 0
    both_benign = 0
    legacy_only = 0
    real_rf_only = 0

    errors = []

    for position, flow in enumerate(
        flows,
        start=start_line,
    ):
        try:
            normalized_features = normalize_flow(flow)

            legacy_feature_row = [
                normalized_features.get(column, 0.0)
                for column in FEATURE_COLUMNS
            ]

            legacy_result = detector.score(
                legacy_feature_row
            )

            real_result = (
                comparison_real_predictor.predict(flow)
            )

            legacy_is_alert = bool(
                legacy_result.get("is_anomaly", False)
            )

            real_is_alert = bool(
                real_result["alert"]
            )

            legacy_alerts += int(legacy_is_alert)
            real_rf_alerts += int(real_is_alert)

            if legacy_is_alert and real_is_alert:
                agreement_type = "both_alert"
                both_alert += 1

            elif not legacy_is_alert and not real_is_alert:
                agreement_type = "both_benign"
                both_benign += 1

            elif legacy_is_alert:
                agreement_type = "legacy_only"
                legacy_only += 1

            else:
                agreement_type = "real_rf_only"
                real_rf_only += 1

            results.append(
                {
                    "line": position,
                    "src_ip": flow.get("src_ip"),
                    "dst_ip": flow.get("dst_ip"),
                    "src_port": flow.get("src_port"),
                    "dst_port": flow.get("dst_port"),
                    "protocol": flow.get("protocol"),
                    "legacy_alert": legacy_is_alert,
                    "real_rf_alert": real_is_alert,
                    "agreement": agreement_type,
                    "real_rf_probability": (
                        real_result["attack_probability"]
                    ),
                    "real_rf_threshold": (
                        real_result["threshold"]
                    ),
                    "real_rf_operational_mode": (
                        real_result["operational_mode"]
                    ),
                }
            )

        except Exception as error:
            errors.append(
                {
                    "line": position,
                    "error": str(error),
                }
            )

    analyzed = len(results)

    agreements = both_alert + both_benign

    agreement_rate = (
        agreements / analyzed
        if analyzed
        else 0.0
    )

    return {
        "mode": "compare-shadow",
        "total_available_flows": len(all_flows),
        "requested": limit,
        "analyzed": analyzed,
        "errors": len(errors),
        "legacy_alerts": legacy_alerts,
        "real_rf_alerts": real_rf_alerts,
        "agreement": {
            "both_alert": both_alert,
            "both_benign": both_benign,
            "legacy_only": legacy_only,
            "real_rf_only": real_rf_only,
            "agreement_rate": round(
                agreement_rate,
                6,
            ),
        },
        "persistence_enabled": False,
        "results": results,
        "error_details": errors[:20],
        "warning": (
            "These are model comparisons, not verified attack labels."
        ),
    }
'''

    path.write_text(
        text.rstrip() + addition + "\n",
        encoding="utf-8",
    )

    print(f"Updated: {path}")
PY
Updated: app/main.py

flowguard/ml-service main  ? ❯ python -m py_compile \
  app/main.py \
  app/ml/real_only_predictor.py

flowguard/ml-service main  ? ❯ PYTHONPATH=. python - <<'PY'
from app.main import app

print([
    getattr(route, "path", None)
    for route in app.routes
    if getattr(route, "path", None)
    == "/analyze/compare"
])
PY
['/analyze/compare']

flowguard/ml-service main  ? ❯ RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
INFO:     Will watch for changes in these directories: ['/home/pd/Downloads/flowguard/ml-service']
ERROR:    [Errno 98] Address already in use

flowguard/ml-service main  ? ✗ RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
INFO:     Will watch for changes in these directories: ['/home/pd/Downloads/flowguard/ml-service']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2891373] using StatReload
INFO:     Started server process [2891474]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:60050 - "POST /analyze/compare?limit=100 HTTP/1.1" 200 OK

The server is now running correctly. The earlier Analyzed: 0, Errors: 100 result was generated before the updated comparison endpoint was running, so that saved JSON is stale.

Keep Uvicorn open and run this in another terminal:

curl --fail-with-body -sS -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  -o /home/pd/Downloads/flowguard/docs/model_comparison.json

Now print the new summary and any errors:

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/model_comparison.json"
)

data = json.loads(path.read_text(encoding="utf-8"))

print("===== MODEL COMPARISON =====")
print("Mode:", data.get("mode"))
print("Analyzed:", data.get("analyzed"))
print("Errors:", data.get("errors"))
print("Legacy alerts:", data.get("legacy_alerts"))
print("Real RF alerts:", data.get("real_rf_alerts"))

agreement = data.get("agreement", {})

print("Both alert:", agreement.get("both_alert"))
print("Both benign:", agreement.get("both_benign"))
print("Legacy only:", agreement.get("legacy_only"))
print("Real RF only:", agreement.get("real_rf_only"))
print(
    "Agreement rate:",
    f"{agreement.get('agreement_rate', 0) * 100:.2f}%"
)

errors = data.get("error_details", [])

if errors:
    print("\n===== FIRST ERRORS =====")
    for error in errors[:10]:
        print(error)
PY

The first uvicorn: command not found happened because the virtual environment was not active. The later 200 OK confirms the request reached the newly running API, but the fresh summary will tell us whether both models actually scored the flows.


flowguard main  ? ❯ RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
bash: command not found: uvicorn

flowguard main  ? ✗ curl -s -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  > /home/pd/Downloads/flowguard/docs/model_comparison.json

flowguard main  ? ❯
flowguard main  ? ❯ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/"
    "model_comparison.json"
)

data = json.loads(
    path.read_text(encoding="utf-8")
)

print("===== MODEL COMPARISON =====")
print("Analyzed:", data["analyzed"])
print("Errors:", data["errors"])
print("Legacy alerts:", data["legacy_alerts"])
print("Real RF alerts:", data["real_rf_alerts"])
print("Both alert:", data["agreement"]["both_alert"])
print("Both benign:", data["agreement"]["both_benign"])
print("Legacy only:", data["agreement"]["legacy_only"])
print("Real RF only:", data["agreement"]["real_rf_only"])
print(
    "Agreement rate:",
    f"{data['agreement']['agreement_rate'] * 100:.2f}%"
)
PY
===== MODEL COMPARISON =====
Analyzed: 0
Errors: 100
Legacy alerts: 0
Real RF alerts: 0
Both alert: 0
Both benign: 0
Legacy only: 0
Real RF only: 0
Agreement rate: 0.00%

flowguard main  ? ❯ curl --fail-with-body -sS -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  -o /home/pd/Downloads/flowguard/docs/model_comparison.json

flowguard main  ? ❯
flowguard main  ? ❯ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/model_comparison.json"
)

data = json.loads(path.read_text(encoding="utf-8"))

print("===== MODEL COMPARISON =====")
print("Mode:", data.get("mode"))
print("Analyzed:", data.get("analyzed"))
print("Errors:", data.get("errors"))
print("Legacy alerts:", data.get("legacy_alerts"))
print("Real RF alerts:", data.get("real_rf_alerts"))

agreement = data.get("agreement", {})

print("Both alert:", agreement.get("both_alert"))
print("Both benign:", agreement.get("both_benign"))
print("Legacy only:", agreement.get("legacy_only"))
print("Real RF only:", agreement.get("real_rf_only"))
print(
    "Agreement rate:",
    f"{agreement.get('agreement_rate', 0) * 100:.2f}%"
)

errors = data.get("error_details", [])

if errors:
    print("\n===== FIRST ERRORS =====")
    for error in errors[:10]:
        print(error)
PY
===== MODEL COMPARISON =====
Mode: compare-shadow
Analyzed: 0
Errors: 100
Legacy alerts: 0
Real RF alerts: 0
Both alert: 0
Both benign: 0
Legacy only: 0
Real RF only: 0
Agreement rate: 0.00%

===== FIRST ERRORS =====
{'line': 700, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 701, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 702, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 703, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 704, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 705, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 706, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 707, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 708, 'error': "'Ensemble' object has no attribute 'score'"}
{'line': 709, 'error': "'Ensemble' object has no attribute 'score'"}

flowguard main  ? ❯

The cause is clear: your legacy Ensemble exposes score_flow(...), not score(...). The comparison endpoint called the wrong method for all 100 flows. The ensemble result also uses "alert" rather than "is_anomaly".

Keep Uvicorn running. In another terminal, patch only the comparison endpoint:

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python - <<'PY'
from pathlib import Path

path = Path("app/main.py")
text = path.read_text(encoding="utf-8")

marker = "# FlowGuard legacy-versus-real comparison endpoint"

if marker not in text:
    raise SystemExit("Comparison endpoint marker was not found.")

before, comparison_section = text.split(marker, 1)

old_call = """legacy_result = detector.score(
                legacy_feature_row
            )"""

new_call = """legacy_result = detector.score_flow(
                legacy_feature_row
            )"""

old_result = """legacy_result.get("is_anomaly", False)"""
new_result = """legacy_result.get("alert", False)"""

if old_call not in comparison_section:
    raise SystemExit("Could not find detector.score in comparison endpoint.")

if old_result not in comparison_section:
    raise SystemExit("Could not find legacy is_anomaly lookup.")

comparison_section = comparison_section.replace(
    old_call,
    new_call,
    1,
)

comparison_section = comparison_section.replace(
    old_result,
    new_result,
    1,
)

path.write_text(
    before + marker + comparison_section,
    encoding="utf-8",
)

print("Updated comparison endpoint to use score_flow() and alert.")
PY

Check syntax:

python -m py_compile app/main.py

Because Uvicorn is running with --reload, it should restart automatically. Check its terminal for:

Application startup complete.

Then rerun the comparison:

curl --fail-with-body -sS -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  -o /home/pd/Downloads/flowguard/docs/model_comparison.json

Print the result:

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/model_comparison.json"
)

data = json.loads(path.read_text(encoding="utf-8"))
agreement = data.get("agreement", {})

print("===== MODEL COMPARISON =====")
print("Analyzed:", data.get("analyzed"))
print("Errors:", data.get("errors"))
print("Legacy alerts:", data.get("legacy_alerts"))
print("Real RF alerts:", data.get("real_rf_alerts"))
print("Both alert:", agreement.get("both_alert"))
print("Both benign:", agreement.get("both_benign"))
print("Legacy only:", agreement.get("legacy_only"))
print("Real RF only:", agreement.get("real_rf_only"))
print(
    "Agreement rate:",
    f"{agreement.get('agreement_rate', 0) * 100:.2f}%"
)

for error in data.get("error_details", [])[:5]:
    print("ERROR:", error)
PY

This patch only changes the shadow comparison endpoint; it does not persist alerts or replace either detector.

Pasted text(10).txt
Document
?

Great — the comparison endpoint now works correctly.
Result

Flows analyzed: 100
Errors: 0

Legacy ensemble alerts: 85
Real Random Forest alerts: 100

Both marked attack: 85
Both marked benign: 0
Legacy only: 0
Real RF only: 15

Agreement: 85%

This means the real-data Random Forest is more sensitive than the legacy ensemble. It flagged 15 additional flows, but because these live flows have no ground-truth labels, we cannot say whether those 15 are true attacks or false positives.

Keep both models in shadow mode for now.
Inspect the 15 disagreement flows

Run:

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/model_comparison.json"
)

data = json.loads(path.read_text(encoding="utf-8"))

disagreements = [
    result
    for result in data["results"]
    if result["agreement"] == "real_rf_only"
]

print("===== REAL RF ONLY FLOWS =====")
print("Total:", len(disagreements))

for number, flow in enumerate(disagreements, start=1):
    print(
        f"{number:02d}. "
        f"probability={flow['real_rf_probability']:.6f} | "
        f"{flow.get('src_ip')}:{flow.get('src_port')} -> "
        f"{flow.get('dst_ip')}:{flow.get('dst_port')} | "
        f"{flow.get('protocol')}"
    )
PY

Do not enable persist=true for the real RF yet. The current safe architecture is:

Legacy ensemble → existing alert pipeline
Real RF → shadow comparison only



flowguard main  ? ✗ builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python - <<'PY'
from pathlib import Path

path = Path("app/main.py")
text = path.read_text(encoding="utf-8")

marker = "# FlowGuard legacy-versus-real comparison endpoint"

if marker not in text:
    raise SystemExit("Comparison endpoint marker was not found.")

before, comparison_section = text.split(marker, 1)

old_call = """legacy_result = detector.score(
                legacy_feature_row
            )"""

new_call = """legacy_result = detector.score_flow(
                legacy_feature_row
            )"""

old_result = """legacy_result.get("is_anomaly", False)"""
new_result = """legacy_result.get("alert", False)"""

if old_call not in comparison_section:
    raise SystemExit("Could not find detector.score in comparison endpoint.")

if old_result not in comparison_section:
    raise SystemExit("Could not find legacy is_anomaly lookup.")

comparison_section = comparison_section.replace(
    old_call,
    new_call,
    1,
)

comparison_section = comparison_section.replace(
    old_result,
    new_result,
    1,
)

path.write_text(
    before + marker + comparison_section,
    encoding="utf-8",
)

print("Updated comparison endpoint to use score_flow() and alert.")
PY
Updated comparison endpoint to use score_flow() and alert.

flowguard/ml-service main  ? ❯ python -m py_compile app/main.py

flowguard/ml-service main  ? ❯ curl --fail-with-body -sS -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  -o /home/pd/Downloads/flowguard/docs/model_comparison.json

flowguard/ml-service main  ? ❯
flowguard/ml-service main  ? ❯ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/model_comparison.json"
)

data = json.loads(path.read_text(encoding="utf-8"))
agreement = data.get("agreement", {})

print("===== MODEL COMPARISON =====")
print("Analyzed:", data.get("analyzed"))
print("Errors:", data.get("errors"))
print("Legacy alerts:", data.get("legacy_alerts"))
print("Real RF alerts:", data.get("real_rf_alerts"))
print("Both alert:", agreement.get("both_alert"))
print("Both benign:", agreement.get("both_benign"))
print("Legacy only:", agreement.get("legacy_only"))
print("Real RF only:", agreement.get("real_rf_only"))
print(
    "Agreement rate:",
    f"{agreement.get('agreement_rate', 0) * 100:.2f}%"
)

for error in data.get("error_details", [])[:5]:
    print("ERROR:", error)
PY
===== MODEL COMPARISON =====
Analyzed: 100
Errors: 0
Legacy alerts: 85
Real RF alerts: 100
Both alert: 85
Both benign: 0
Legacy only: 0
Real RF only: 15
Agreement rate: 85.00%

flowguard/ml-service main  ? ❯ ^C

flowguard/ml-service main  ? ✗
flowguard/ml-service main  ? ✗ python - <<'PY'
import json
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/docs/model_comparison.json"
)

data = json.loads(path.read_text(encoding="utf-8"))

disagreements = [
    result
    for result in data["results"]
    if result["agreement"] == "real_rf_only"
]

print("===== REAL RF ONLY FLOWS =====")
print("Total:", len(disagreements))

for number, flow in enumerate(disagreements, start=1):
    print(
        f"{number:02d}. "
        f"probability={flow['real_rf_probability']:.6f} | "
        f"{flow.get('src_ip')}:{flow.get('src_port')} -> "
        f"{flow.get('dst_ip')}:{flow.get('dst_port')} | "
        f"{flow.get('protocol')}"
    )
PY
===== REAL RF ONLY FLOWS =====
Total: 15
01. probability=0.082423 | 43.157.1.82:8080 -> 10.10.2.101:59072 | TCP
02. probability=0.082690 | 43.157.184.190:8080 -> 10.10.2.101:37286 | TCP
03. probability=0.320024 | 43.157.184.190:8080 -> 10.10.2.101:37740 | TCP
04. probability=0.328078 | 43.157.184.190:8080 -> 10.10.2.101:37752 | TCP
05. probability=0.270603 | 43.157.184.190:8080 -> 10.10.2.101:37756 | TCP
06. probability=0.320024 | 43.159.143.39:8080 -> 10.10.2.101:46514 | TCP
07. probability=0.328078 | 43.159.143.39:8080 -> 10.10.2.101:46516 | TCP
08. probability=0.267563 | 43.159.143.39:8080 -> 10.10.2.101:46530 | TCP
09. probability=0.270990 | 43.159.99.24:8080 -> 10.10.2.101:44172 | TCP
10. probability=0.343764 | 43.159.99.24:8080 -> 10.10.2.101:44174 | TCP
11. probability=0.269931 | 43.159.99.24:8080 -> 10.10.2.101:44186 | TCP
12. probability=0.320024 | 43.160.255.143:8080 -> 10.10.2.101:47276 | TCP
13. probability=0.328078 | 43.160.255.143:8080 -> 10.10.2.101:47292 | TCP
14. probability=0.256603 | 43.160.255.143:8080 -> 10.10.2.101:47298 | TCP
15. probability=0.082423 | 43.160.255.143:8080 -> 10.10.2.101:56548 | TCP

This is a meaningful result. The 15 disagreements are not random:

    Every one is inbound TCP traffic.

    Every source uses port 8080.

    They come from a small group of repeated source IPs.

    They all target your local host 10.10.2.101.

    Random Forest probabilities range from about 0.082 to 0.344.

    The legacy ensemble marked all 15 benign.

So this is better interpreted as one repeated traffic pattern involving several hosts, not 15 unrelated attacks. It is still not proof that the traffic is malicious.
Generate a detailed disagreement report

Run:

builtin cd /home/pd/Downloads/flowguard/ml-service
source .venv/bin/activate

python - <<'PY'
import csv
import json
from collections import defaultdict
from pathlib import Path

project = Path("/home/pd/Downloads/flowguard")

comparison_path = project / "docs/model_comparison.json"
flow_path = project / "data/flows_output.jsonl"
output_path = project / "docs/real_rf_only_flows.csv"

comparison = json.loads(
    comparison_path.read_text(encoding="utf-8")
)

flows = []

with flow_path.open("r", encoding="utf-8") as file:
    for line in file:
        if line.strip():
            flows.append(json.loads(line))

disagreements = [
    result
    for result in comparison["results"]
    if result["agreement"] == "real_rf_only"
]

rows = []

for result in disagreements:
    line_number = int(result["line"])
    flow = flows[line_number - 1]

    duration = float(flow.get("duration_seconds", 0.0))
    packet_count = float(flow.get("packet_count", 0.0))
    total_bytes = float(flow.get("total_bytes", 0.0))
    syn_count = float(flow.get("syn_count", 0.0))
    ack_count = float(flow.get("ack_count", 0.0))
    rst_count = float(flow.get("rst_count", 0.0))

    rows.append(
        {
            "line": line_number,
            "src_ip": flow.get("src_ip"),
            "dst_ip": flow.get("dst_ip"),
            "src_port": flow.get("src_port"),
            "dst_port": flow.get("dst_port"),
            "protocol": flow.get("protocol"),
            "duration_seconds": duration,
            "packet_count": packet_count,
            "total_bytes": total_bytes,
            "bytes_per_sec": (
                total_bytes / duration
                if duration > 0
                else 0.0
            ),
            "packets_per_sec": (
                packet_count / duration
                if duration > 0
                else 0.0
            ),
            "syn_count": syn_count,
            "ack_count": ack_count,
            "fin_count": flow.get("fin_count", 0),
            "rst_count": rst_count,
            "syn_ack_ratio": syn_count / (ack_count + 1.0),
            "rst_ratio": rst_count / (packet_count + 1.0),
            "rf_probability": result["real_rf_probability"],
        }
    )

with output_path.open(
    "w",
    encoding="utf-8",
    newline="",
) as output_file:
    writer = csv.DictWriter(
        output_file,
        fieldnames=rows[0].keys(),
    )
    writer.writeheader()
    writer.writerows(rows)

groups = defaultdict(list)

for row in rows:
    groups[row["src_ip"]].append(row)

print("===== DISAGREEMENT GROUPS BY SOURCE IP =====")

for source_ip, source_rows in sorted(
    groups.items(),
    key=lambda item: len(item[1]),
    reverse=True,
):
    probabilities = [
        row["rf_probability"]
        for row in source_rows
    ]

    destination_ports = sorted(
        {
            row["dst_port"]
            for row in source_rows
        }
    )

    print(
        f"{source_ip}: "
        f"{len(source_rows)} flows | "
        f"average probability={sum(probabilities) / len(probabilities):.6f} | "
        f"maximum={max(probabilities):.6f} | "
        f"destination ports={destination_ports}"
    )

print("\n===== FLOW FEATURES =====")

for row in rows:
    print(
        f"line={row['line']} | "
        f"{row['src_ip']}:{row['src_port']} -> "
        f"{row['dst_ip']}:{row['dst_port']} | "
        f"packets={row['packet_count']:.0f} | "
        f"bytes={row['total_bytes']:.0f} | "
        f"duration={row['duration_seconds']:.6f}s | "
        f"pps={row['packets_per_sec']:.2f} | "
        f"syn={row['syn_count']:.0f} | "
        f"ack={row['ack_count']:.0f} | "
        f"rst={row['rst_count']:.0f} | "
        f"probability={row['rf_probability']:.6f}"
    )

print(f"\nSaved: {output_path}")
PY

The report will be saved here:

/home/pd/Downloads/flowguard/docs/real_rf_only_flows.csv

The correct architecture remains:

Individual flows
      ↓
Both models score them
      ↓
Group repeated flows by source IP and time window
      ↓
Create one consolidated incident alert

Do not create 15 separate permanent alerts for this pattern; later we

i wanta  metic how fast is thta ebpf laye is fater than the cpp layer , metrices

Yes. We should produce an actual measured speedup, not an assumed “eBPF is faster” claim.

Your current programs cannot yet be compared fairly:

    The C++ program reads a PCAP file using pcap_open_offline() and also performs queueing, flow aggregation and JSON output.

    The eBPF loader captures from a live interface and currently prints and flushes every packet event, which adds major terminal I/O overhead.

So timing the current binaries directly would give a misleading number.
Metrics we will calculate

1. Throughput
   packets processed per second

2. Processing cost
   nanoseconds per packet

3. Packet-loss rate
   sent packets versus successfully processed packets

4. CPU usage
   CPU time and CPU percentage

5. Speedup
   eBPF packets/sec ÷ C++ packets/sec

6. CPU efficiency
   packets processed per CPU-second

Example final result format:

C++ libpcap throughput:     420,000 packets/sec
eBPF/XDP throughput:      1,260,000 packets/sec
eBPF speedup:                  3.00×
C++ packet cost:              2,381 ns/packet
eBPF packet cost:               794 ns/packet
C++ packet loss:               3.20%
eBPF packet loss:              0.10%

Those are only example numbers—we will generate your real numbers.
Step 1: Find the benchmark PCAP and tools

Run exactly this:

builtin cd /home/pd/Downloads/flowguard

echo "===== AVAILABLE PCAP FILES ====="

find /home/pd/Downloads/flowguard \
  -type f \
  \( -iname "*.pcap" -o -iname "*.pcapng" \) \
  -printf "%s bytes  %p\n" \
  | sort -nr \
  | head -n 20

echo
echo "===== REQUIRED TOOLS ====="

for tool in tcpreplay tcpdump perf bpftool clang cmake; do
    printf "%-12s : " "$tool"

    if command -v "$tool" >/dev/null 2>&1; then
        command -v "$tool"
    else
        echo "MISSING"
    fi
done

echo
echo "===== NETWORK INTERFACES ====="
ip -br link

Paste only that output next.

Then we will build a controlled benchmark using:

same PCAP
same packet count
same virtual interface
no terminal printing
multiple runs
median result

The benchmark will generate:

docs/ebpf_vs_cpp_benchmark.json
docs/ebpf_vs_cpp_benchmark.md
docs/ebpf_vs_cpp_runs.csv

Until that benchmark is complete, the honest project statement remains that eBPF/XDP was implemented but its speed advantage over the C++ layer has not yet been measured.


flowguard main ❯ builtin cd /home/pd/Downloads/flowguard

echo "===== AVAILABLE PCAP FILES ====="

find /home/pd/Downloads/flowguard \
  -type f \
  \( -iname "*.pcap" -o -iname "*.pcapng" \) \
  -printf "%s bytes  %p\n" \
  | sort -nr \
  | head -n 20

echo
echo "===== REQUIRED TOOLS ====="

for tool in tcpreplay tcpdump perf bpftool clang cmake; do
    printf "%-12s : " "$tool"

    if command -v "$tool" >/dev/null 2>&1; then
        command -v "$tool"
    else
        echo "MISSING"
    fi
done

echo
echo "===== NETWORK INTERFACES ====="
ip -br link
===== AVAILABLE PCAP FILES =====
24144199 bytes  /home/pd/Downloads/flowguard/data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap
144172 bytes  /home/pd/Downloads/flowguard/data/sample/real_attack.pcap
38861 bytes  /home/pd/Downloads/flowguard/capture-cpp/build/small_sample.pcap
4287 bytes  /home/pd/Downloads/flowguard/data/sample/small_sample.pcap

===== REQUIRED TOOLS =====
tcpreplay    : /usr/bin/tcpreplay
tcpdump      : /usr/bin/tcpdump
perf         : MISSING
bpftool      : /usr/bin/bpftool
clang        : /usr/bin/clang
cmake        : /usr/bin/cmake

===== NETWORK INTERFACES =====
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>
wlan0            UP             30:03:c8:3c:83:c5 <BROADCAST,MULTICAST,UP,LOWER_UP>
br-14c11fcfc44a  DOWN           02:3b:46:7a:ef:84 <NO-CARRIER,BROADCAST,MULTICAST,UP>
docker0          DOWN           4e:1a:12:f3:af:d6 <NO-CARRIER,BROADCAST,MULTICAST,UP>
kdeap0           UP             32:03:c8:3c:83:c5 <BROADCAST,MULTICAST,UP,LOWER_UP>

flowguard main ❯

Good. We’ll use the 24.1 MB infected-Android PCAP as the common workload. perf is optional; bpftool can give us the eBPF program’s exact kernel runtime.

First create a fair C++ packet-parser-only benchmark. Your existing benchmark also performs flow aggregation, so it would not be a clean comparison against XDP.
1. Create the C++ parser benchmark

cat > /home/pd/Downloads/flowguard/capture-cpp/src/parser_benchmark.cpp <<'CPP'
#include "PacketParser.hpp"

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <pcap.h>
#include <string>
#include <time.h>
#include <vector>

struct StoredPacket {
    pcap_pkthdr header{};
    std::vector<u_char> data;
};

static std::uint64_t process_cpu_time_ns()
{
    timespec value{};
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &value);

    return (
        static_cast<std::uint64_t>(value.tv_sec) * 1'000'000'000ULL
        + static_cast<std::uint64_t>(value.tv_nsec)
    );
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        std::cerr
            << "Usage: " << argv[0]
            << " <pcap-file> [repetitions]\n";
        return 1;
    }

    const std::string pcap_path = argv[1];
    const int repetitions = argc >= 3
        ? std::max(1, std::stoi(argv[2]))
        : 7;

    char error_buffer[PCAP_ERRBUF_SIZE]{};

    pcap_t *handle = pcap_open_offline(
        pcap_path.c_str(),
        error_buffer
    );

    if (handle == nullptr) {
        std::cerr << "Could not open PCAP: "
                  << error_buffer << "\n";
        return 1;
    }

    std::vector<StoredPacket> packets;

    pcap_pkthdr *header = nullptr;
    const u_char *packet_data = nullptr;

    while (true) {
        const int result = pcap_next_ex(
            handle,
            &header,
            &packet_data
        );

        if (result == 1) {
            StoredPacket packet;
            packet.header = *header;

            packet.data.assign(
                packet_data,
                packet_data + header->caplen
            );

            packets.push_back(std::move(packet));
        } else if (result == -2) {
            break;
        } else if (result == -1) {
            std::cerr << "PCAP read error: "
                      << pcap_geterr(handle) << "\n";
            pcap_close(handle);
            return 1;
        }
    }

    pcap_close(handle);

    if (packets.empty()) {
        std::cerr << "PCAP contains no packets.\n";
        return 1;
    }

    PacketParser parser;

    // Warm-up run, excluded from measurements.
    std::uint64_t warmup_checksum = 0;

    for (const StoredPacket &packet : packets) {
        const auto parsed = parser.parse(
            &packet.header,
            packet.data.data()
        );

        if (parsed.has_value()) {
            warmup_checksum += parsed->packet_length;
            warmup_checksum += parsed->src_port;
            warmup_checksum += parsed->dst_port;
        }
    }

    std::vector<double> wall_ns_per_packet;
    std::vector<double> cpu_ns_per_packet;
    std::vector<double> packets_per_second;
    std::vector<double> cpu_percentages;

    std::uint64_t final_checksum = warmup_checksum;
    std::size_t parsed_packets = 0;

    std::cout << std::fixed << std::setprecision(3);
    std::cout << "Packets loaded: " << packets.size() << "\n";
    std::cout << "Repetitions: " << repetitions << "\n\n";

    for (int run = 1; run <= repetitions; ++run) {
        std::uint64_t checksum = 0;
        std::size_t parsed = 0;

        const std::uint64_t cpu_start =
            process_cpu_time_ns();

        const auto wall_start =
            std::chrono::steady_clock::now();

        for (const StoredPacket &packet : packets) {
            const auto result = parser.parse(
                &packet.header,
                packet.data.data()
            );

            if (result.has_value()) {
                ++parsed;

                checksum += result->packet_length;
                checksum += result->src_port;
                checksum += result->dst_port;
                checksum += result->tcp_flags;
                checksum += result->src_ip.size();
                checksum += result->dst_ip.size();
            }
        }

        const auto wall_end =
            std::chrono::steady_clock::now();

        const std::uint64_t cpu_end =
            process_cpu_time_ns();

        const double wall_ns =
            std::chrono::duration<double, std::nano>(
                wall_end - wall_start
            ).count();

        const double cpu_ns =
            static_cast<double>(cpu_end - cpu_start);

        const double inspected =
            static_cast<double>(packets.size());

        const double wall_cost =
            wall_ns / inspected;

        const double cpu_cost =
            cpu_ns / inspected;

        const double throughput =
            inspected * 1'000'000'000.0 / wall_ns;

        const double cpu_percentage =
            100.0 * cpu_ns / wall_ns;

        wall_ns_per_packet.push_back(wall_cost);
        cpu_ns_per_packet.push_back(cpu_cost);
        packets_per_second.push_back(throughput);
        cpu_percentages.push_back(cpu_percentage);

        parsed_packets = parsed;
        final_checksum ^= checksum;

        std::cout
            << "Run " << run
            << ": inspected=" << packets.size()
            << " parsed=" << parsed
            << " wall_ns_per_packet=" << wall_cost
            << " cpu_ns_per_packet=" << cpu_cost
            << " packets_per_second=" << throughput
            << " cpu_percent=" << cpu_percentage
            << "\n";
    }

    auto median = [](std::vector<double> values) {
        std::sort(values.begin(), values.end());
        return values[values.size() / 2];
    };

    std::cout << "\n===== C++ PARSER MEDIAN =====\n";
    std::cout
        << "CPP_TOTAL_PACKETS=" << packets.size() << "\n";
    std::cout
        << "CPP_PARSED_PACKETS=" << parsed_packets << "\n";
    std::cout
        << "CPP_MEDIAN_WALL_NS_PER_PACKET="
        << median(wall_ns_per_packet) << "\n";
    std::cout
        << "CPP_MEDIAN_CPU_NS_PER_PACKET="
        << median(cpu_ns_per_packet) << "\n";
    std::cout
        << "CPP_MEDIAN_PACKETS_PER_SECOND="
        << median(packets_per_second) << "\n";
    std::cout
        << "CPP_MEDIAN_CPU_PERCENT="
        << median(cpu_percentages) << "\n";
    std::cout
        << "CHECKSUM=" << final_checksum << "\n";

    return 0;
}
CPP

2. Register it in CMake

python - <<'PY'
from pathlib import Path

path = Path(
    "/home/pd/Downloads/flowguard/"
    "capture-cpp/CMakeLists.txt"
)

text = path.read_text(encoding="utf-8")

marker = "# FlowGuard packet-parser-only benchmark"

if marker not in text:
    text += """

# FlowGuard packet-parser-only benchmark
add_executable(
    flowguard_parser_benchmark
    src/parser_benchmark.cpp
    src/PacketParser.cpp
)

target_link_libraries(
    flowguard_parser_benchmark
    pcap
)

target_compile_options(
    flowguard_parser_benchmark
    PRIVATE
    -O3
)
"""

    path.write_text(text, encoding="utf-8")
    print("Added flowguard_parser_benchmark.")
else:
    print("Benchmark target already exists.")
PY

3. Build it in Release mode

builtin cd /home/pd/Downloads/flowguard

cmake \
  -S capture-cpp \
  -B capture-cpp/build-benchmark \
  -DCMAKE_BUILD_TYPE=Release

cmake \
  --build capture-cpp/build-benchmark \
  --target flowguard_parser_benchmark \
  -j"$(nproc)"

4. Run seven measured repetitions

capture-cpp/build-benchmark/flowguard_parser_benchmark \
  data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap \
  7 \
  | tee docs/cpp_parser_benchmark.txt

The important output will look like:

CPP_MEDIAN_WALL_NS_PER_PACKET=...
CPP_MEDIAN_CPU_NS_PER_PACKET=...
CPP_MEDIAN_PACKETS_PER_SECOND=...
CPP_MEDIAN_CPU_PERCENT=...

After this, we will attach a silent benchmark XDP program to a temporary veth interface and obtain:

EBPF_RUNTIME_NS_PER_PACKET
EBPF_PACKETS_PER_SECOND_EQUIVALENT
EBPF_SUSTAINED_REPLAY_PPS
EBPF_PACKET_LOSS_PERCENT
EBPF_VS_CPP_SPEEDUP



flowguard main  ? ❯ capture-cpp/build-benchmark/flowguard_parser_benchmark \
  data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap \
  7 \
  | tee docs/cpp_parser_benchmark.txt
Packets loaded: 29125
Repetitions: 7

Run 1: inspected=29125 parsed=29125 wall_ns_per_packet=110.278 cpu_ns_per_packet=108.456 packets_per_second=9067962.864 cpu_percent=98.348
Run 2: inspected=29125 parsed=29125 wall_ns_per_packet=100.470 cpu_ns_per_packet=99.877 packets_per_second=9953212.213 cpu_percent=99.409
Run 3: inspected=29125 parsed=29125 wall_ns_per_packet=136.940 cpu_ns_per_packet=134.828 packets_per_second=7302474.643 cpu_percent=98.458
Run 4: inspected=29125 parsed=29125 wall_ns_per_packet=128.016 cpu_ns_per_packet=127.151 packets_per_second=7811544.511 cpu_percent=99.324
Run 5: inspected=29125 parsed=29125 wall_ns_per_packet=128.340 cpu_ns_per_packet=111.315 packets_per_second=7791799.896 cpu_percent=86.734
Run 6: inspected=29125 parsed=29125 wall_ns_per_packet=106.409 cpu_ns_per_packet=105.689 packets_per_second=9397719.895 cpu_percent=99.324
Run 7: inspected=29125 parsed=29125 wall_ns_per_packet=102.140 cpu_ns_per_packet=101.490 packets_per_second=9790435.929 cpu_percent=99.363

===== C++ PARSER MEDIAN =====
CPP_TOTAL_PACKETS=29125
CPP_PARSED_PACKETS=29125
CPP_MEDIAN_WALL_NS_PER_PACKET=110.278
CPP_MEDIAN_CPU_NS_PER_PACKET=108.456
CPP_MEDIAN_PACKETS_PER_SECOND=9067962.864
CPP_MEDIAN_CPU_PERCENT=99.324
CHECKSUM=1454654?

Your C++ baseline is now measured:

Packets:                    29,125
Median processing cost:     108.456 ns/packet CPU
Median wall cost:           110.278 ns/packet
Equivalent throughput:      9,067,963 packets/second
CPU usage:                  99.324%

The ? after CHECKSUM=1454654 is only your shell prompt, not an error.

We should not benchmark the existing XDP program directly because it updates a source map, starts dropping after 500 packets from a source, and sends events through a ring buffer. That would cause different packets to follow different execution paths.

We will create a dedicated XDP parser benchmark that parses the same Ethernet, IPv4, TCP and UDP fields without terminal or JSON overhead. Your C++ parser also performs IP-to-string conversion, which remains part of its measured userspace cost.
1. Create the eBPF benchmark program

cat > /home/pd/Downloads/flowguard/capture-ebpf/xdp_parser_benchmark.c <<'C'
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/in.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>

#include <bpf/bpf_endian.h>
#include <bpf/bpf_helpers.h>


struct benchmark_stats {
    __u64 packets;
    __u64 bytes;
    __u64 checksum;
};


/*
 * Per-CPU storage avoids lock contention while ensuring that parsed
 * values have an observable side effect and cannot be optimized away.
 */
struct {
    __uint(type, BPF_MAP_TYPE_PERCPU_ARRAY);
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, struct benchmark_stats);
} parser_benchmark_stats SEC(".maps");


SEC("xdp")
int xdp_parser_benchmark(struct xdp_md *context)
{
    void *packet_start =
        (void *)(long)context->data;

    void *packet_end =
        (void *)(long)context->data_end;

    struct ethhdr *ethernet_header =
        packet_start;

    if ((void *)(ethernet_header + 1) > packet_end) {
        return XDP_PASS;
    }

    if (
        ethernet_header->h_proto
        != bpf_htons(ETH_P_IP)
    ) {
        return XDP_PASS;
    }

    struct iphdr *ipv4_header =
        (void *)(ethernet_header + 1);

    if ((void *)(ipv4_header + 1) > packet_end) {
        return XDP_PASS;
    }

    if (
        ipv4_header->version != 4
        || ipv4_header->ihl < 5
    ) {
        return XDP_PASS;
    }

    __u32 ipv4_header_length =
        (__u32)ipv4_header->ihl * 4;

    if (
        (void *)ipv4_header + ipv4_header_length
        > packet_end
    ) {
        return XDP_PASS;
    }

    __u16 source_port = 0;
    __u16 destination_port = 0;

    void *transport_header =
        (void *)ipv4_header + ipv4_header_length;

    if (ipv4_header->protocol == IPPROTO_TCP) {
        struct tcphdr *tcp_header =
            transport_header;

        if ((void *)(tcp_header + 1) <= packet_end) {
            source_port =
                bpf_ntohs(tcp_header->source);

            destination_port =
                bpf_ntohs(tcp_header->dest);
        }
    } else if (
        ipv4_header->protocol == IPPROTO_UDP
    ) {
        struct udphdr *udp_header =
            transport_header;

        if ((void *)(udp_header + 1) <= packet_end) {
            source_port =
                bpf_ntohs(udp_header->source);

            destination_port =
                bpf_ntohs(udp_header->dest);
        }
    }

    __u32 stats_key = 0;

    struct benchmark_stats *stats =
        bpf_map_lookup_elem(
            &parser_benchmark_stats,
            &stats_key
        );

    if (stats != NULL) {
        stats->packets += 1;

        stats->bytes +=
            (__u64)(
                context->data_end
                - context->data
            );

        stats->checksum +=
            (__u64)ipv4_header->saddr
            + (__u64)ipv4_header->daddr
            + (__u64)source_port
            + (__u64)destination_port
            + (__u64)ipv4_header->protocol;
    }

    return XDP_PASS;
}


char program_license[] SEC("license") = "GPL";
C

2. Compile it

builtin cd /home/pd/Downloads/flowguard

clang \
  -O2 \
  -g \
  -target bpf \
  -D__TARGET_ARCH_x86 \
  -c capture-ebpf/xdp_parser_benchmark.c \
  -o capture-ebpf/xdp_parser_benchmark.o

Verify:

file capture-ebpf/xdp_parser_benchmark.o

It should report an eBPF ELF object.
3. Create the complete benchmark script

mkdir -p scripts docs/benchmark-logs

cat > scripts/benchmark_ebpf_vs_cpp.sh <<'BASH'
#!/usr/bin/env bash

set -Eeuo pipefail


ROOT="/home/pd/Downloads/flowguard"

PCAP="$ROOT/data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap"

CPP_RESULTS="$ROOT/docs/cpp_parser_benchmark.txt"

BPF_OBJECT="$ROOT/capture-ebpf/xdp_parser_benchmark.o"

CSV_OUTPUT="$ROOT/docs/ebpf_vs_cpp_runs.csv"
JSON_OUTPUT="$ROOT/docs/ebpf_vs_cpp_benchmark.json"
MARKDOWN_OUTPUT="$ROOT/docs/ebpf_vs_cpp_benchmark.md"

LOG_DIRECTORY="$ROOT/docs/benchmark-logs"

TX_INTERFACE="fgbench_tx"
RX_INTERFACE="fgbench_rx"

PIN_PATH="/sys/fs/bpf/flowguard_xdp_parser_benchmark"

RUNS=7
PCAP_LOOPS=50

ATTACH_MODE="unknown"

OLD_BPF_STATS="$(
    cat /proc/sys/kernel/bpf_stats_enabled
)"


cleanup()
{
    set +e

    sudo ip link set \
        dev "$RX_INTERFACE" \
        xdp off \
        >/dev/null 2>&1

    sudo ip link set \
        dev "$RX_INTERFACE" \
        xdpgeneric off \
        >/dev/null 2>&1

    sudo rm -f "$PIN_PATH"

    sudo ip link delete \
        "$TX_INTERFACE" \
        >/dev/null 2>&1

    sudo sysctl -q -w \
        kernel.bpf_stats_enabled="$OLD_BPF_STATS" \
        >/dev/null 2>&1
}


trap cleanup EXIT


read_program_stats()
{
    sudo bpftool -j prog show pinned "$PIN_PATH" |
        python -c '
import json
import sys

data = json.load(sys.stdin)

if isinstance(data, list):
    data = data[0]

print(
    int(data.get("run_time_ns", 0)),
    int(data.get("run_cnt", 0)),
)
'
}


mkdir -p "$LOG_DIRECTORY"

for required_file in \
    "$PCAP" \
    "$CPP_RESULTS" \
    "$BPF_OBJECT"
do
    if [[ ! -f "$required_file" ]]; then
        echo "Missing required file: $required_file" >&2
        exit 1
    fi
done


for required_command in \
    bpftool \
    clang \
    ip \
    python \
    tcpreplay
do
    if ! command -v "$required_command" >/dev/null 2>&1; then
        echo "Missing command: $required_command" >&2
        exit 1
    fi
done


CPP_TOTAL_PACKETS="$(
    awk -F= '
        /^CPP_TOTAL_PACKETS=/ {
            print $2
        }
    ' "$CPP_RESULTS"
)"

CPP_CPU_NS="$(
    awk -F= '
        /^CPP_MEDIAN_CPU_NS_PER_PACKET=/ {
            print $2
        }
    ' "$CPP_RESULTS"
)"

CPP_WALL_NS="$(
    awk -F= '
        /^CPP_MEDIAN_WALL_NS_PER_PACKET=/ {
            print $2
        }
    ' "$CPP_RESULTS"
)"

CPP_PPS="$(
    awk -F= '
        /^CPP_MEDIAN_PACKETS_PER_SECOND=/ {
            print $2
        }
    ' "$CPP_RESULTS"
)"


if [[ -z "$CPP_TOTAL_PACKETS" ]]; then
    echo "Could not read C++ packet count." >&2
    exit 1
fi


EXPECTED_PACKETS=$(
    (
        CPP_TOTAL_PACKETS
        * PCAP_LOOPS
    )
)


echo "C++ packets per PCAP: $CPP_TOTAL_PACKETS"
echo "PCAP loops per run: $PCAP_LOOPS"
echo "Expected packets per run: $EXPECTED_PACKETS"
echo "eBPF measured runs: $RUNS"
echo


sudo -v

sudo sysctl -q -w \
    kernel.bpf_stats_enabled=1


if ! mountpoint -q /sys/fs/bpf; then
    echo "/sys/fs/bpf is not mounted." >&2
    exit 1
fi


sudo ip link delete \
    "$TX_INTERFACE" \
    >/dev/null 2>&1 || true

sudo rm -f "$PIN_PATH"


sudo ip link add \
    "$TX_INTERFACE" \
    type veth \
    peer name "$RX_INTERFACE"

sudo ip link set "$TX_INTERFACE" up
sudo ip link set "$RX_INTERFACE" up


sudo bpftool prog load \
    "$BPF_OBJECT" \
    "$PIN_PATH" \
    type xdp


if sudo ip link set \
    dev "$RX_INTERFACE" \
    xdp pinned "$PIN_PATH" \
    2>"$LOG_DIRECTORY/native-attach-error.txt"
then
    ATTACH_MODE="native"
else
    echo "Native XDP attach failed; trying generic XDP."

    sudo ip link set \
        dev "$RX_INTERFACE" \
        xdpgeneric pinned "$PIN_PATH"

    ATTACH_MODE="generic"
fi


echo "XDP attach mode: $ATTACH_MODE"
echo


printf '%s\n' \
    "run,expected_packets,xdp_run_count,runtime_ns,wall_seconds,kernel_ns_per_packet,kernel_equivalent_pps,replay_pps,delivery_percent" \
    > "$CSV_OUTPUT"


for run_number in $(seq 1 "$RUNS"); do
    read -r runtime_before count_before \
        < <(read_program_stats)

    start_time_ns="$(date +%s%N)"

    sudo tcpreplay \
        --intf1="$TX_INTERFACE" \
        --topspeed \
        --preload-pcap \
        --loop="$PCAP_LOOPS" \
        "$PCAP" \
        >"$LOG_DIRECTORY/tcpreplay-run-${run_number}.txt" \
        2>&1

    end_time_ns="$(date +%s%N)"

    # Allow final ingress processing to complete before reading counters.
    sleep 0.2

    read -r runtime_after count_after \
        < <(read_program_stats)

    runtime_delta=$(
        (
            runtime_after
            - runtime_before
        )
    )

    count_delta=$(
        (
            count_after
            - count_before
        )
    )

    wall_time_ns=$(
        (
            end_time_ns
            - start_time_ns
        )
    )

    if (( count_delta <= 0 )); then
        echo "Run $run_number received zero XDP packets." >&2
        exit 1
    fi

    metrics="$(
        awk \
            -v runtime="$runtime_delta" \
            -v packets="$count_delta" \
            -v wall="$wall_time_ns" \
            -v expected="$EXPECTED_PACKETS" \
            'BEGIN {
                kernel_ns = runtime / packets
                kernel_pps = 1000000000 / kernel_ns
                wall_seconds = wall / 1000000000
                replay_pps = packets / wall_seconds
                delivery = 100 * packets / expected

                printf "%.9f %.3f %.3f %.3f %.6f",
                    wall_seconds,
                    kernel_ns,
                    kernel_pps,
                    replay_pps,
                    delivery
            }'
    )"

    read -r \
        wall_seconds \
        kernel_ns_per_packet \
        kernel_equivalent_pps \
        replay_pps \
        delivery_percent \
        <<< "$metrics"

    printf '%s\n' \
        "$run_number,$EXPECTED_PACKETS,$count_delta,$runtime_delta,$wall_seconds,$kernel_ns_per_packet,$kernel_equivalent_pps,$replay_pps,$delivery_percent" \
        >> "$CSV_OUTPUT"

    echo \
        "Run $run_number: " \
        "xdp_packets=$count_delta " \
        "kernel_ns_per_packet=$kernel_ns_per_packet " \
        "kernel_equivalent_pps=$kernel_equivalent_pps " \
        "replay_pps=$replay_pps " \
        "delivery=$delivery_percent%"
done


python - \
    "$CSV_OUTPUT" \
    "$JSON_OUTPUT" \
    "$MARKDOWN_OUTPUT" \
    "$CPP_TOTAL_PACKETS" \
    "$CPP_CPU_NS" \
    "$CPP_WALL_NS" \
    "$CPP_PPS" \
    "$ATTACH_MODE" \
    "$PCAP_LOOPS" \
    <<'PY'
import csv
import json
import statistics
import sys
from pathlib import Path


(
    csv_path,
    json_path,
    markdown_path,
    cpp_packets,
    cpp_cpu_ns,
    cpp_wall_ns,
    cpp_pps,
    attach_mode,
    pcap_loops,
) = sys.argv[1:]


with Path(csv_path).open(
    "r",
    encoding="utf-8",
    newline="",
) as file:
    rows = list(csv.DictReader(file))


def values(column: str) -> list[float]:
    return [
        float(row[column])
        for row in rows
    ]


ebpf_kernel_ns = statistics.median(
    values("kernel_ns_per_packet")
)

ebpf_kernel_pps = statistics.median(
    values("kernel_equivalent_pps")
)

ebpf_replay_pps = statistics.median(
    values("replay_pps")
)

delivery_percent = statistics.median(
    values("delivery_percent")
)

cpp_cpu_ns_value = float(cpp_cpu_ns)
cpp_wall_ns_value = float(cpp_wall_ns)
cpp_pps_value = float(cpp_pps)

cpu_cost_speedup = (
    cpp_cpu_ns_value / ebpf_kernel_ns
)

wall_cost_speedup = (
    cpp_wall_ns_value / ebpf_kernel_ns
)

equivalent_throughput_speedup = (
    ebpf_kernel_pps / cpp_pps_value
)

packet_loss_percent = max(
    0.0,
    100.0 - delivery_percent,
)


report = {
    "workload": {
        "pcap": (
            "2025-10-02-traffic-from-infected-Android-phone.pcap"
        ),
        "packets_per_loop": int(cpp_packets),
        "pcap_loops_per_run": int(pcap_loops),
        "measured_runs": len(rows),
    },
    "cpp_parser": {
        "median_cpu_ns_per_packet": cpp_cpu_ns_value,
        "median_wall_ns_per_packet": cpp_wall_ns_value,
        "median_packets_per_second": cpp_pps_value,
    },
    "ebpf_xdp_parser": {
        "attach_mode": attach_mode,
        "median_kernel_ns_per_packet": ebpf_kernel_ns,
        "median_kernel_equivalent_pps": ebpf_kernel_pps,
        "median_sustained_replay_pps": ebpf_replay_pps,
        "median_delivery_percent": delivery_percent,
        "median_packet_loss_percent": packet_loss_percent,
    },
    "comparison": {
        "cpu_cost_speedup_x": cpu_cost_speedup,
        "wall_cost_speedup_x": wall_cost_speedup,
        "equivalent_throughput_speedup_x": (
            equivalent_throughput_speedup
        ),
        "kernel_cost_reduction_percent": (
            100.0
            * (
                1.0
                - ebpf_kernel_ns / cpp_cpu_ns_value
            )
        ),
    },
}


Path(json_path).write_text(
    json.dumps(report, indent=2),
    encoding="utf-8",
)


markdown = f"""# FlowGuard eBPF/XDP vs C++ Parser Benchmark

## Workload

- PCAP packets: {int(cpp_packets):,}
- PCAP loops per eBPF run: {int(pcap_loops)}
- Measured runs: {len(rows)}
- XDP attachment mode: `{attach_mode}`

## Median results

| Metric | C++ parser | eBPF/XDP parser |
|---|---:|---:|
| Processing cost | {cpp_cpu_ns_value:,.3f} ns/packet | {ebpf_kernel_ns:,.3f} ns/packet |
| Equivalent throughput | {cpp_pps_value:,.0f} packets/s | {ebpf_kernel_pps:,.0f} packets/s |
| Sustained replay throughput | Not measured | {ebpf_replay_pps:,.0f} packets/s |
| Packet delivery | Not applicable | {delivery_percent:.4f}% |
| Packet loss | Not applicable | {packet_loss_percent:.4f}% |

## Comparison

- eBPF processing-cost speedup: **{cpu_cost_speedup:.2f}×**
- Equivalent-throughput speedup: **{equivalent_throughput_speedup:.2f}×**
- Kernel processing-cost reduction: **{report["comparison"]["kernel_cost_reduction_percent"]:.2f}%**

## Interpretation

The processing-cost comparison measures the average runtime of the
XDP parser in the kernel against the measured CPU cost of the C++
userspace packet parser.

The sustained replay value measures the complete test path, including
tcpreplay, the virtual Ethernet pair, kernel scheduling and XDP.

These metrics do not include FlowGuard ML inference or database work.
"""


Path(markdown_path).write_text(
    markdown,
    encoding="utf-8",
)


print("\n===== FINAL BENCHMARK =====")
print(
    f"C++ CPU cost:            "
    f"{cpp_cpu_ns_value:.3f} ns/packet"
)
print(
    f"eBPF kernel cost:        "
    f"{ebpf_kernel_ns:.3f} ns/packet"
)
print(
    f"eBPF cost speedup:       "
    f"{cpu_cost_speedup:.2f}x"
)
print(
    f"C++ equivalent PPS:      "
    f"{cpp_pps_value:,.0f}"
)
print(
    f"eBPF equivalent PPS:     "
    f"{ebpf_kernel_pps:,.0f}"
)
print(
    f"Throughput speedup:      "
    f"{equivalent_throughput_speedup:.2f}x"
)
print(
    f"Sustained replay PPS:    "
    f"{ebpf_replay_pps:,.0f}"
)
print(
    f"Delivery rate:           "
    f"{delivery_percent:.4f}%"
)
print(
    f"Packet-loss rate:        "
    f"{packet_loss_percent:.4f}%"
)

print(f"\nSaved CSV:      {csv_path}")
print(f"Saved JSON:     {json_path}")
print(f"Saved Markdown: {markdown_path}")
PY
BASH

4. Run it

chmod +x scripts/benchmark_ebpf_vs_cpp.sh

./scripts/benchmark_ebpf_vs_cpp.sh

This will ask for your sudo password and run seven eBPF measurements of approximately 1,456,250 packets each.

The final output will directly state:

eBPF cost speedup:       ...x
Throughput speedup:      ...x
Sustained replay PPS:    ...
Packet-loss rate:        ...%

Paste the ===== FINAL BENCHMARK ===== section after it finishes.

Pasted text(11).txt
Document
?

The script has invalid Bash arithmetic blocks. It used:

$(
    (
        CPP_TOTAL_PACKETS * PCAP_LOOPS
    )
)

Bash interpreted CPP_TOTAL_PACKETS as a command, causing the errors shown.

Patch all four arithmetic blocks:

builtin cd /home/pd/Downloads/flowguard

python - <<'PY'
from pathlib import Path
import re

path = Path("scripts/benchmark_ebpf_vs_cpp.sh")
text = path.read_text(encoding="utf-8")

replacements = {
    r'''EXPECTED_PACKETS=\$\(\s*
        \(\s*
            CPP_TOTAL_PACKETS\s*
            \*\s*
            PCAP_LOOPS\s*
        \)\s*
    \)''': 'EXPECTED_PACKETS=$((CPP_TOTAL_PACKETS * PCAP_LOOPS))',

    r'''runtime_delta=\$\(\s*
        \(\s*
            runtime_after\s*
            -\s*
            runtime_before\s*
        \)\s*
    \)''': 'runtime_delta=$((runtime_after - runtime_before))',

    r'''count_delta=\$\(\s*
        \(\s*
            count_after\s*
            -\s*
            count_before\s*
        \)\s*
    \)''': 'count_delta=$((count_after - count_before))',

    r'''wall_time_ns=\$\(\s*
        \(\s*
            end_time_ns\s*
            -\s*
            start_time_ns\s*
        \)\s*
    \)''': 'wall_time_ns=$((end_time_ns - start_time_ns))',
}

total = 0

for pattern, replacement in replacements.items():
    text, count = re.subn(
        pattern,
        replacement,
        text,
        flags=re.VERBOSE,
    )
    total += count
    print(f"Patched: {replacement} ({count})")

if total != 4:
    raise SystemExit(
        f"Expected to patch 4 arithmetic blocks, patched {total}"
    )

path.write_text(text, encoding="utf-8")
print(f"\nUpdated: {path}")
PY

Check the script:

bash -n scripts/benchmark_ebpf_vs_cpp.sh &&
echo "Bash syntax is valid"

Confirm the corrected lines:

grep -nE \
  'EXPECTED_PACKETS=|runtime_delta=|count_delta=|wall_time_ns=' \
  scripts/benchmark_ebpf_vs_cpp.sh

You should see:

EXPECTED_PACKETS=$((CPP_TOTAL_PACKETS * PCAP_LOOPS))
runtime_delta=$((runtime_after - runtime_before))
count_delta=$((count_after - count_before))
wall_time_ns=$((end_time_ns - start_time_ns))

Then run the benchmark again:

./scripts/benchmark_ebpf_vs_cpp.sh

Your established C++ baseline remains:

CPU cost:       108.456 ns/packet
Wall cost:      110.278 ns/packet
Throughput:     9,067,963 packets/second

The script will now measure the eBPF side and calculate the actual speedup.



flowguard main  ? ❯ chmod +x scripts/benchmark_ebpf_vs_cpp.sh

./scripts/benchmark_ebpf_vs_cpp.sh
./scripts/benchmark_ebpf_vs_cpp.sh: line 156: CPP_TOTAL_PACKETS: command not found
./scripts/benchmark_ebpf_vs_cpp.sh: line 157: capture-cpp: command not found
[sudo] password for pd:

flowguard main  ? ✗
flowguard main  ? ✗ builtin cd /home/pd/Downloads/flowguard

python - <<'PY'
from pathlib import Path
import re

path = Path("scripts/benchmark_ebpf_vs_cpp.sh")
text = path.read_text(encoding="utf-8")

replacements = {
    r'''EXPECTED_PACKETS=\$\(\s*
        \(\s*
            CPP_TOTAL_PACKETS\s*
            \*\s*
            PCAP_LOOPS\s*
        \)\s*
    \)''': 'EXPECTED_PACKETS=$((CPP_TOTAL_PACKETS * PCAP_LOOPS))',

    r'''runtime_delta=\$\(\s*
        \(\s*
            runtime_after\s*
            -\s*
            runtime_before\s*
        \)\s*
    \)''': 'runtime_delta=$((runtime_after - runtime_before))',

    r'''count_delta=\$\(\s*
        \(\s*
            count_after\s*
            -\s*
            count_before\s*
        \)\s*
    \)''': 'count_delta=$((count_after - count_before))',

    r'''wall_time_ns=\$\(\s*
        \(\s*
            end_time_ns\s*
            -\s*
            start_time_ns\s*
        \)\s*
    \)''': 'wall_time_ns=$((end_time_ns - start_time_ns))',
}

total = 0

for pattern, replacement in replacements.items():
    text, count = re.subn(
        pattern,
        replacement,
        text,
        flags=re.VERBOSE,
    )
    total += count
    print(f"Patched: {replacement} ({count})")

if total != 4:
    raise SystemExit(
        f"Expected to patch 4 arithmetic blocks, patched {total}"
    )

path.write_text(text, encoding="utf-8")
print(f"\nUpdated: {path}")
PY
Patched: EXPECTED_PACKETS=$((CPP_TOTAL_PACKETS * PCAP_LOOPS)) (1)
Patched: runtime_delta=$((runtime_after - runtime_before)) (1)
Patched: count_delta=$((count_after - count_before)) (1)
Patched: wall_time_ns=$((end_time_ns - start_time_ns)) (1)

Updated: scripts/benchmark_ebpf_vs_cpp.sh

flowguard main  ? ❯ bash -n scripts/benchmark_ebpf_vs_cpp.sh &&
echo "Bash syntax is valid"
Bash syntax is valid

flowguard main  ? ❯ grep -nE \
  'EXPECTED_PACKETS=|runtime_delta=|count_delta=|wall_time_ns=' \
  scripts/benchmark_ebpf_vs_cpp.sh
151:EXPECTED_PACKETS=$((CPP_TOTAL_PACKETS * PCAP_LOOPS))
244:    runtime_delta=$((runtime_after - runtime_before))
246:    count_delta=$((count_after - count_before))
248:    wall_time_ns=$((end_time_ns - start_time_ns))?

Yes, the four arithmetic lines are fixed correctly.

The final ? you typed is most likely just your question, not part of the script. Verify the actual line once:

sed -n '248p' scripts/benchmark_ebpf_vs_cpp.sh | cat -A

Correct output should end like this:

    wall_time_ns=$((end_time_ns - start_time_ns))$

Then run the benchmark:

./scripts/benchmark_ebpf_vs_cpp.sh

It will:

    create temporary fgbench_tx and fgbench_rx interfaces,

    attach the XDP benchmark,

    replay about 1,456,250 packets per run,

    perform seven runs,

    clean up the XDP program and interfaces automatically.

Paste the output beginning from:

XDP attach mode:

through:

===== FINAL BENCHMARK =====



flowguard main  ? ❯ sed -n '248p' scripts/benchmark_ebpf_vs_cpp.sh | cat -A
    wall_time_ns=$((end_time_ns - start_time_ns))$

flowguard main  ? ❯ ./scripts/benchmark_ebpf_vs_cpp.sh
C++ packets per PCAP: 29125
PCAP loops per run: 50
Expected packets per run: 1456250
eBPF measured runs: 7

XDP attach mode: native

Run 1:  xdp_packets=1456269  kernel_ns_per_packet=56.326  kernel_equivalent_pps=17753819.371  replay_pps=349222.638  delivery=100.001305%
Run 2:  xdp_packets=1456251  kernel_ns_per_packet=65.205  kernel_equivalent_pps=15336273.136  replay_pps=302079.975  delivery=100.000069%
Run 3:  xdp_packets=1456251  kernel_ns_per_packet=55.595  kernel_equivalent_pps=17987284.688  replay_pps=353057.518  delivery=100.000069%
Run 4:  xdp_packets=1456250  kernel_ns_per_packet=62.301  kernel_equivalent_pps=16051174.705  replay_pps=316329.887  delivery=100.000000%
Run 5:  xdp_packets=1456250  kernel_ns_per_packet=62.830  kernel_equivalent_pps=15915903.263  replay_pps=313105.650  delivery=100.000000%
Run 6:  xdp_packets=1456251  kernel_ns_per_packet=61.371  kernel_equivalent_pps=16294299.064  replay_pps=320640.357  delivery=100.000069%
Run 7:  xdp_packets=1456250  kernel_ns_per_packet=64.625  kernel_equivalent_pps=15473868.289  replay_pps=306540.196  delivery=100.000000%

===== FINAL BENCHMARK =====
C++ CPU cost:            108.456 ns/packet
eBPF kernel cost:        62.301 ns/packet
eBPF cost speedup:       1.74x
C++ equivalent PPS:      9,067,963
eBPF equivalent PPS:     16,051,175
Throughput speedup:      1.77x
Sustained replay PPS:    316,330
Delivery rate:           100.0001%
Packet-loss rate:        0.0000%

Saved CSV:      /home/pd/Downloads/flowguard/docs/ebpf_vs_cpp_runs.csv
Saved JSON:     /home/pd/Downloads/flowguard/docs/ebpf_vs_cpp_benchmark.json
Saved Markdown: /home/pd/Downloads/flowguard/docs/ebpf_vs_cpp_benchmark.md

Your benchmark is successful. Native XDP/eBPF is measurably faster than the C++ userspace parser on your machine.
Final metrics
Metric	C++ parser	eBPF/XDP parser
Processing cost	108.456 ns/packet	62.301 ns/packet
Equivalent throughput	9.07 million packets/s	16.05 million packets/s
Sustained replay throughput	—	316,330 packets/s
Packet loss	—	0.0000%
Improvement

    eBPF processing speedup: 1.74×

    eBPF throughput speedup: 1.77×

    Processing-cost reduction: approximately 42.6%

    Throughput increase: approximately 77%

    XDP attachment mode: native

    Packets tested: about 1.456 million per run

    Measured runs: 7

Simple meaning

For every packet:

C++ userspace parser: 108.456 nanoseconds
eBPF/XDP parser:       62.301 nanoseconds

So the eBPF parser used roughly 46 fewer nanoseconds per packet.

At its measured processing cost:

C++:   ~9.07 million packets/second
eBPF: ~16.05 million packets/second

Therefore, your defensible claim is:

    FlowGuard’s native XDP/eBPF packet-processing layer achieved 1.74× lower per-packet processing cost and 1.77× higher equivalent throughput than its C++ userspace parser, processing packets in 62.3 ns versus 108.5 ns across seven benchmark runs.

Important interpretation

The 316,330 packets/s sustained replay rate is not the maximum eBPF processing capacity. It measures the entire testing pipeline:

PCAP → tcpreplay → veth interface → Linux networking → XDP

That result is mainly limited by replay generation, virtual interfaces and kernel scheduling.

The 16.05 million packets/s figure is the parser’s runtime-equivalent throughput, calculated from its measured kernel execution cost.

The delivery rate slightly exceeding 100%:

100.0001%

means a few extra background/control packets crossed the virtual interface. It does not mean more PCAP packets were magically created. Report packet loss as approximately 0%, not delivery above 100%.
Resume version

    Benchmarked FlowGuard’s native XDP/eBPF packet parser against a C++ userspace parser across seven runs and 1.45M+ packets per run, achieving 1.77× higher equivalent throughput, 42.6% lower per-packet processing cost, and approximately zero packet loss.

Your benchmark evidence is saved in:

docs/ebpf_vs_cpp_runs.csv
docs/ebpf_vs_cpp_benchmark.json
docs/ebpf_vs_cpp_benchmark.md


now make a final md with full detils od bproject with all keywrda and metrices for my resime ,, full detiled md

Created the complete 1,300-line FlowGuard resume and portfolio dossier with:

    Resume-ready 1-line, 3-bullet, 4-bullet, and detailed versions

    Full architecture and component explanation

    C++17/libpcap, eBPF/XDP, FastAPI, ML, PostgreSQL, Redis, Prisma, Docker, and Nginx details

    Real CICIDS2017 methodology and verified model metrics

    Complete confusion-matrix and attack-family analysis

    XDP vs C++ benchmark metrics

    ATS keyword bank

    Role-specific bullets for software, backend, ML, and cybersecurity jobs

    Interview walkthroughs and technical talking points

    Safe claims and claims to avoid

    Future improvements and portfolio description

The document uses the defensible real-data headline rather than the older synthetic result, and includes the verified capture-day-separated methodology and ensemble trade-offs. It also reflects the verified repository architecture and Docker stack.


now also ehlp me write detaield readme # FlowGuard

FlowGuard is a network-flow anomaly detection project with four main parts:

- capture-cpp: C++ packet-to-flow aggregation
- ml-service: FastAPI inference service backed by PostgreSQL and Redis
- dashboard: static HTML dashboard served by Nginx
- docker-compose.yml: end-to-end local stack definition

This README reflects the setup verified on Friday, July 17, 2026.

## What It Does

FlowGuard reads captured network flows, extracts security features, and scores
them with an ensemble of:

- Isolation Forest for unsupervised anomaly detection
- Random Forest for supervised attack classification
- PyTorch Autoencoder for reconstruction-error anomaly detection

An alert is raised when at least 2 of the 3 models vote anomalous.

## Verified Status

Verified on Friday, July 17, 2026:

- docker compose up -d --build succeeds
- API health check returns 200 at http://127.0.0.1:8000/health
- Dashboard returns 200 at http://127.0.0.1:8080
- GET /flows/recent returns captured sample flow data
- Python tests pass: 8 passed
- Held-out evaluation completed on ml-service/data/sample/test_holdout.csv

## Project Layout

text
flowguard/
├── capture-cpp/
├── capture-ebpf/
├── dashboard/
├── data/
├── docs/
├── ml-service/
├── docker-compose.yml
└── HOW_TO_RUN.md



## Quick Start

bash
docker compose up -d --build



Then check:

bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/flows/recent?limit=2



Open:

- Dashboard: 
http://127.0.0.1:8080
- API docs: http://127.0.0.1:8000/docs

## Render Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/puneetdixit200/flowguard)

This repo includes `render.yaml` for one Docker web service, one Render Postgres database, and one Render Key Value instance. The hosted service serves the dashboard at `/` and the API at the same origin.

Free Render limits apply: the web service can spin down after idle time, Free Postgres expires after 30 days, and Free Key Value does not persist data across restarts.

Notes:

- PostgreSQL and Redis are intentionally not published to host ports in
  docker-compose.yml. They are only used internally by the compose network.
- The ML container waits for Postgres and Redis, runs prisma db push, then
  starts Uvicorn.
- First startup of ml-service takes a few extra seconds because Prisma
  generates its client during container boot.

## Manual Run

If you want to run only the API locally:

bash
cd ml-service
PYTHONPATH=. .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000



If you want to evaluate the saved models locally:

bash
cd ml-service
PYTHONPATH=. .venv/bin/python training/evaluate_models.py



## Test Results

Python API tests:

bash
cd ml-service
PYTHONPATH=. .venv/bin/python -m pytest tests -q



Verified result on Friday, July 17, 2026:

text
8 passed



## Model Metrics

Held-out test set: 
940 rows total

- Benign: 830
- Attacks: 110

Ensemble results:

- Accuracy: 0.9894
- Precision: 0.9630
- Recall: 0.9455
- F1: 0.9541
- False positives: 4
- False negatives: 6

Full report: [docs/evaluation_report.txt](/home/pd/Downloads/flowguard/docs/evaluation_report.txt)

Additional model notes:

- [docs/ml-models.md](/home/pd/Downloads/flowguard/docs/ml-models.md)
- [docs/false-positive-analysis.md](/home/pd/Downloads/flowguard/docs/false-positive-analysis.md)
- [docs/case-study.md](/home/pd/Downloads/flowguard/docs/case-study.md)
- [docs/threading-model.md](/home/pd/Downloads/flowguard/docs/threading-model.md)

## API Endpoints

- GET /health
- GET /flows/recent?limit=20
- POST /analyze
- GET /alerts
- GET /alerts/{alert_id}
- GET /metrics/model
- POST /analyse/real

## Docker Notes

Docker-specific fixes applied and verified:

- dashboard/Dockerfile now serves the existing static dashboard with Nginx
  instead of expecting a missing React/Vite build pipeline
- ml-service/Dockerfile installs CPU-only PyTorch wheels instead of pulling
  large default GPU stacks
- ml-service waits for Postgres and Redis before startup
- Redis host and port are environment-driven, so the service works in compose
- Prisma client generation is built into the image and refreshed at container
  startup after schema sync
- .dockerignore files prevent local build outputs and virtualenv contents from
  bloating the image contexts

I created a complete, professional GitHub README that updates the older README’s three-model prototype description and historical 98.94% result with the latest real-data evaluation, shadow-mode routes, four-model research pipeline, and XDP benchmark.

It includes:

    Project overview and table of contents

    Verified ML and XDP performance metrics

    Full system architecture

    C++ capture and flow-aggregation design

    eBPF/XDP implementation

    All 11 engineered features

    CICIDS2017 capture-day-separated methodology

    Individual model and ensemble results

    Confusion matrices and attack-family analysis

    Legacy versus real-model distinction

    Shadow-mode API documentation

    Docker Compose and manual setup instructions

    C++ and Python testing commands

    Benchmark reproduction instructions

    Limitations, honest claims, roadmap, resume bullets, and ATS keywords

    Portable relative paths instead of /home/pd/... links

The API section also covers the newly added real-model and comparison routes present in the current backend. The deployment section reflects the five-service PostgreSQL, Redis, capture, ML, and dashboard Compose architecture.

Replace the repository’s existing README.md with this file before committing.


Library
/
PROJECT 1
/FlowGuard_Detailed_README.md

# FlowGuard

> A full-stack network intrusion detection and traffic-analysis platform built with C++17, native XDP/eBPF, FastAPI, scikit-learn, PyTorch, PyTorch Geometric, PostgreSQL, Redis, Prisma ORM, Docker Compose, and Nginx.

FlowGuard converts raw network packets into flow-level security telemetry, evaluates each flow using multiple machine-learning approaches, and exposes the resulting detections through a REST API and monitoring dashboard.

The project combines three engineering areas:

- **Systems and networking:** C++ packet parsing, multithreading, flow aggregation, libpcap, Linux networking, native XDP/eBPF, BPF maps, and ring buffers.
- **Machine learning:** Random Forest, Isolation Forest, Autoencoder, GraphSAGE, feature engineering, threshold tuning, capture-day-separated evaluation, and ensemble analysis.
- **Backend and infrastructure:** FastAPI, PostgreSQL, Prisma ORM, Redis pub/sub, Docker Compose, Nginx, health checks, persistence, and shadow deployment.

---

## Table of Contents

- [Highlights](#highlights)
- [Verified Results](#verified-results)
- [What FlowGuard Does](#what-flowguard-does)
- [Architecture](#architecture)
- [Project Components](#project-components)
- [Network Features](#network-features)
- [Machine-Learning Models](#machine-learning-models)
- [Dataset and Evaluation Methodology](#dataset-and-evaluation-methodology)
- [Real-Data Model Results](#real-data-model-results)
- [eBPF/XDP Performance Benchmark](#ebpfxdp-performance-benchmark)
- [Live Shadow-Mode Evaluation](#live-shadow-mode-evaluation)
- [Project Layout](#project-layout)
- [Requirements](#requirements)
- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
- [Manual C++ Capture Run](#manual-c-capture-run)
- [Manual FastAPI Run](#manual-fastapi-run)
- [eBPF/XDP Build and Run](#ebpfxdp-build-and-run)
- [Model Training and Evaluation](#model-training-and-evaluation)
- [Benchmark Reproduction](#benchmark-reproduction)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Generated Artifacts](#generated-artifacts)
- [Docker and Infrastructure Notes](#docker-and-infrastructure-notes)
- [Design Decisions](#design-decisions)
- [Limitations and Honest Interpretation](#limitations-and-honest-interpretation)
- [Roadmap](#roadmap)
- [Resume-Ready Summary](#resume-ready-summary)
- [Technology Keywords](#technology-keywords)

---

## Highlights

- Multithreaded **C++17/libpcap** packet-to-flow processing pipeline.
- Ethernet, IPv4, TCP, UDP, and ICMP parsing.
- Bounded producer-consumer queue with backpressure.
- Five-tuple flow aggregation and TCP flag statistics.
- Native **XDP/eBPF** packet parsing and early filtering.
- Kernel-to-userspace communication through a BPF ring buffer.
- FastAPI inference service with batch analysis and alert persistence.
- PostgreSQL-backed alert storage through Prisma ORM.
- Redis-based internal messaging/pub-sub support.
- Random Forest, Isolation Forest, PyTorch Autoencoder, and GraphSAGE.
- Real CICIDS2017 training and capture-day-separated final evaluation.
- Validation-selected Random Forest operating thresholds.
- Shadow deployment and legacy-versus-real model comparison.
- Reproducible C++ versus XDP performance benchmark.
- Docker Compose orchestration for the complete local stack.

---

## Verified Results

### Real-data intrusion-detection result

The strongest individual model was Random Forest:

| Metric | Result |
|---|---:|
| Test flows | 10,000 |
| Benign flows | 5,000 |
| Attack flows | 5,000 |
| Accuracy | **86.09%** |
| Precision | **78.71%** |
| Recall | **98.94%** |
| F1 score | **0.8767** |
| ROC-AUC | **0.9036** |
| False positives | 1,338 |
| False negatives | 53 |

The test data was separated by capture day from the training and validation data.

### Native XDP/eBPF performance result

| Metric | C++ userspace parser | Native XDP/eBPF parser |
|---|---:|---:|
| Processing cost | 108.456 ns/packet | **62.301 ns/packet** |
| Equivalent throughput | 9.07 million packets/s | **16.05 million packets/s** |
| Processing-cost reduction | — | **42.6%** |
| Equivalent-throughput improvement | — | **1.77×** |
| Sustained complete replay path | — | 316,330 packets/s |
| Observed packet loss | — | approximately 0% |

The XDP benchmark used seven measured runs and approximately 1.46 million replayed packets per run.

### Four-model ensemble result

The strict four-model ensemble prioritized agreement and reduced false alarms:

| Metric | Result |
|---|---:|
| Accuracy | 84.71% |
| Precision | **86.96%** |
| Recall | 81.66% |
| F1 score | 0.8423 |
| False positives | 612 |
| False negatives | 917 |
| False-positive reduction vs Random Forest | **54.3%** |

The ensemble improved precision and reduced false positives, but it also missed more attacks. Random Forest therefore remains the strongest general headline model.

---

## What FlowGuard Does

FlowGuard implements the following pipeline:

1. Read packets from a PCAP file or inspect live ingress traffic.
2. Validate Ethernet and IPv4 headers.
3. Parse TCP, UDP, ICMP, ports, lengths, timestamps, and TCP flags.
4. Convert packets into a structured `PacketInfo` representation.
5. Group packets into flows using a network five-tuple.
6. Calculate duration, traffic volume, rate, and TCP-behaviour features.
7. Emit completed flows as JSON Lines.
8. Load the flows into a FastAPI inference service.
9. Score each flow with one or more detection models.
10. Compare model decisions in shadow mode.
11. Optionally persist alerts in PostgreSQL.
12. Expose flows, alerts, metrics, and health state through REST endpoints.
13. Display operational data through an Nginx-served dashboard.

---

## Architecture

```text
                         ┌──────────────────────────────┐
                         │ PCAP replay or live traffic  │
                         └──────────────┬───────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
        ┌────────────────────────┐              ┌────────────────────────┐
        │ C++17/libpcap capture  │              │ Native XDP/eBPF path   │
        │ Userspace packet path  │              │ Kernel ingress path    │
        └────────────┬───────────┘              └────────────┬───────────┘
                     │                                       │
                     ▼                                       ▼
        ┌────────────────────────┐              ┌────────────────────────┐
        │ PacketParser           │              │ BPF maps / ring buffer │
        │ Ethernet/IP/TCP/UDP    │              │ pass/drop/event output │
        └────────────┬───────────┘              └────────────┬───────────┘
                     │                                       │
                     └───────────────────┬───────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Five-tuple aggregation │
                            │ Packet/byte/TCP stats  │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ JSONL feature pipeline │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ FastAPI ML service     │
                            │ Normalization/scoring  │
                            └────────────┬───────────┘
                                         ▼
          ┌──────────────────────────────────────────────────────────┐
          │ Random Forest │ Isolation Forest │ Autoencoder │ GraphSAGE │
          └──────────────────────────────┬───────────────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Shadow comparison /    │
                            │ voting / alert logic   │
                            └────────────┬───────────┘
                                         ▼
                  ┌──────────────────────┴──────────────────────┐
                  ▼                                             ▼
        ┌────────────────────────┐                  ┌────────────────────────┐
        │ PostgreSQL + Prisma    │                  │ Redis pub/sub          │
        │ Durable alert storage  │                  │ Internal notifications │
        └────────────┬───────────┘                  └────────────┬───────────┘
                     └───────────────────┬───────────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Nginx dashboard        │
                            │ Flows/alerts/metrics   │
                            └────────────────────────┘
```

---

## Project Components

### `capture-cpp`

The C++17 layer is responsible for packet parsing and flow aggregation.

Key responsibilities:

- Open PCAP files through libpcap.
- Parse Ethernet and IPv4 packet structure.
- Extract transport protocol and ports.
- Record packet size and nanosecond timestamp representation.
- Extract TCP SYN, ACK, FIN, and RST flags.
- Send parsed packets through a bounded blocking queue.
- Aggregate packets into flows.
- Write completed flow records to JSONL.

Concurrency model:

```text
Capture thread
    │
    ▼
BlockingQueue<PacketInfo>
    │
    ▼
Aggregation thread
```

The bounded queue provides backpressure when aggregation is slower than capture and prevents unrestricted memory growth.

### `capture-ebpf`

The eBPF layer performs packet inspection at the Linux XDP hook.

Implemented concepts:

- Native XDP attachment.
- Safe packet-bound checks required by the eBPF verifier.
- Ethernet and IPv4 parsing.
- Variable-length IPv4 header handling.
- TCP and UDP port extraction.
- Per-source tracking through BPF maps.
- Demonstration early-drop action.
- BPF ring-buffer event transfer.
- libbpf userspace loader.
- Signal-based cleanup and XDP detach.
- Dedicated silent benchmark program.

### `ml-service`

The Python service provides:

- Flow normalization.
- Feature generation.
- Saved-model loading.
- Legacy ensemble inference.
- Real-data Random Forest inference.
- Operational-threshold selection.
- Shadow-mode scoring.
- Side-by-side model comparison.
- Optional alert persistence.
- Alert lookup.
- Model metric reporting.
- OpenAPI documentation.

### `dashboard`

The verified dashboard is a static HTML/CSS/JavaScript interface served by Nginx.

It is intended to display:

- Recent network flows.
- Detected anomalies.
- Persisted alerts.
- Model and system metrics.
- Basic operational health.

### `docker-compose.yml`

The local stack contains:

- PostgreSQL 16
- Redis 7
- C++ capture service
- FastAPI ML service
- Nginx dashboard

PostgreSQL and Redis are kept inside the Compose network and are not intentionally exposed through host ports.

---

## Network Features

The real-data model pipeline uses 11 flow-level features:

| Feature | Meaning |
|---|---|
| `duration_seconds` | Time between first and last packet |
| `packet_count` | Number of packets in the flow |
| `total_bytes` | Total transferred bytes |
| `bytes_per_sec` | Byte-transfer rate |
| `packets_per_sec` | Packet rate |
| `syn_count` | TCP SYN flags observed |
| `ack_count` | TCP ACK flags observed |
| `fin_count` | TCP FIN flags observed |
| `rst_count` | TCP RST flags observed |
| `syn_ack_ratio` | SYN count relative to ACK activity |
| `rst_ratio` | RST count relative to packet count |

Derived features:

```text
bytes_per_sec   = total_bytes / duration_seconds
packets_per_sec = packet_count / duration_seconds
syn_ack_ratio   = syn_count / (ack_count + 1)
rst_ratio       = rst_count / (packet_count + 1)
```

Zero-duration flows are handled safely to avoid division by zero.

---

## Machine-Learning Models

### Random Forest

A supervised binary attack classifier trained on labelled benign and malicious traffic.

Strengths:

- Best overall real-data F1 score.
- Very high attack recall.
- Direct attack-probability output.
- Feature-importance support.
- Fast CPU inference.

### Isolation Forest

An unsupervised anomaly detector trained on benign traffic.

Strengths:

- Does not require attack labels during fitting.
- Detects outliers that differ from normal behaviour.
- Provides an independent anomaly signal.

Observed limitation:

- Very high recall but excessive false positives on the final real-data test split.

### PyTorch Autoencoder

A neural anomaly detector trained to reconstruct benign feature vectors.

Detection principle:

```text
low reconstruction error  → resembles learned benign behaviour
high reconstruction error → possible anomaly
```

The reconstruction threshold is selected from validation behaviour.

### GraphSAGE

A graph neural network implemented with PyTorch Geometric.

For the real CICIDS2017 experiment:

- Each flow is represented as a node.
- Similar flows are connected through feature-space proximity.
- GraphSAGE aggregates neighbourhood information.
- The correct description is a **flow-similarity graph model**.

The CICIDS2017 CSV files used in this experiment did not provide source and destination IP columns, so this model must not be described as a host-communication graph.

### Legacy three-model ensemble

The original project path combines:

- Isolation Forest
- Random Forest
- Autoencoder

An anomaly is raised when at least two of the three models agree.

This path belongs to the earlier prototype/held-out evaluation.

### Real-data four-model ensemble

The research evaluation combines:

- Random Forest
- Isolation Forest
- Autoencoder
- GraphSAGE

The evaluated strict agreement rule reduced false positives but caused a substantial recall drop.

---

## Dataset and Evaluation Methodology

### CICIDS2017 data

Total labelled records available locally:

| Category | Count |
|---|---:|
| Total | 2,830,743 |
| Benign | 2,273,097 |
| Attack | 557,646 |

Attack families represented in the source collection include:

- DDoS
- PortScan
- Bot
- FTP-Patator
- SSH-Patator
- DoS Hulk
- DoS GoldenEye
- DoS Slowhttptest
- DoS slowloris
- Heartbleed
- Web Attack — Brute Force
- Web Attack — XSS
- Web Attack — SQL Injection
- Infiltration

### Capture-day-separated splits

Instead of randomly mixing rows from the same capture files, FlowGuard separates the data by collection day:

| Split | Capture days | Benign | Attack | Total |
|---|---|---:|---:|---:|
| Training | Monday–Wednesday | 10,000 | 10,000 | 20,000 |
| Validation | Thursday | 2,000 | 2,000 | 4,000 |
| Final test | Friday | 5,000 | 5,000 | 10,000 |

The validation set is used for threshold selection. The Friday test split remains untouched until final evaluation.

### Why day separation matters

Random row splitting can produce overly optimistic results when nearly identical flows from the same capture occur in both training and test data.

Day-separated evaluation provides a more difficult test of:

- Cross-day generalization.
- Traffic-distribution changes.
- Previously unseen or sparsely represented attack families.
- Threshold robustness.
- Resistance to train-test leakage.

---

## Real-Data Model Results

### Binary classification metrics

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Isolation Forest | 62.51% | 57.21% | 99.26% | 72.59% |
| Random Forest | **86.09%** | 78.71% | **98.94%** | **87.67%** |
| Autoencoder | 75.86% | 73.11% | 81.80% | 77.21% |
| GraphSAGE | 55.39% | 52.85% | 99.88% | 69.13% |
| Strict four-model ensemble | 84.71% | **86.96%** | 81.66% | 84.23% |

Random Forest ROC-AUC:

```text
0.9036
```

### Confusion matrices

Format:

```text
[[true negatives, false positives],
 [false negatives, true positives]]
```

Random Forest:

```text
[[3662, 1338],
 [  53, 4947]]
```

Strict four-model ensemble:

```text
[[4388,  612],
 [ 917, 4083]]
```

### Operational trade-off

Compared with Random Forest, the ensemble:

- Reduced false positives from 1,338 to 612.
- Reduced false positives by 54.3%.
- Increased precision from 78.71% to 86.96%.
- Increased false negatives from 53 to 917.
- Reduced attack recall from 98.94% to 81.66%.

The ensemble is useful when false alarms are especially expensive, but Random Forest is the stronger general detector.

### Per-family ensemble recall

| Attack family | Recall | Test flows |
|---|---:|---:|
| DDoS | 84.99% | 2,152 |
| PortScan | 80.35% | 2,804 |
| Bot | 2.27% | 44 |

Bot recall was poor because the final sampling included few Bot flows and the training-day attack data did not provide equivalent Bot coverage.

---

## eBPF/XDP Performance Benchmark

### Workload

- PCAP: infected-Android traffic capture.
- PCAP size: approximately 24 MB.
- Packets per PCAP loop: 29,125.
- XDP replay loops per measured run: 50.
- Expected packets per measured run: 1,456,250.
- Measured runs: 7.
- XDP attachment mode: native.
- C++ build: Release mode with `-O3`.
- XDP benchmark: silent parser using a per-CPU map.
- Runtime measurement: kernel BPF program statistics through `bpftool`.

### Median C++ result

```text
C++ median CPU cost:          108.456 ns/packet
C++ median wall cost:         110.278 ns/packet
C++ equivalent throughput:    9,067,963 packets/s
```

### Median native-XDP result

```text
XDP median kernel cost:       62.301 ns/packet
XDP equivalent throughput:    16,051,175 packets/s
XDP sustained replay rate:    316,330 packets/s
XDP observed packet loss:     approximately 0%
```

### Improvement

```text
Processing-cost speedup:      1.74×
Equivalent-throughput gain:   1.77×
Processing-cost reduction:    42.6%
Equivalent-throughput rise:   approximately 77%
```

### Interpretation

The 16.05 million packets/s result is equivalent throughput calculated from measured kernel execution time.

The 316,330 packets/s result measures the complete replay path:

```text
PCAP
  → tcpreplay
  → virtual Ethernet pair
  → Linux ingress path
  → native XDP program
```

The complete replay rate includes replay generation, veth, scheduling, and other kernel overhead. It should not be described as the XDP parser's maximum theoretical capacity.

A measured delivery rate slightly above 100% was caused by a few additional control/interface packets. It is reported as approximately 100% delivery and approximately 0% loss.

---

## Live Shadow-Mode Evaluation

The selected real-data Random Forest is integrated into FastAPI without replacing the legacy alert pipeline.

### Real-model health example

```json
{
  "status": "ok",
  "model": "real_only_random_forest",
  "threshold": 0.0235,
  "operational_mode": "balanced",
  "flow_file": "data/flows_output.jsonl",
  "mode": "shadow"
}
```

### Operational mode

Select the threshold configuration through:

```bash
RF_OPERATIONAL_MODE=balanced
```

The balanced threshold was selected on the Thursday validation split.

### Model-comparison endpoint

The comparison route runs the legacy ensemble and real-data Random Forest on the same recent flows without writing alerts.

Verified comparison over 100 flows:

| Metric | Result |
|---|---:|
| Analyzed | 100 |
| Errors | 0 |
| Legacy alerts | 85 |
| Real Random Forest alerts | 100 |
| Both alert | 85 |
| Both benign | 0 |
| Legacy only | 0 |
| Real Random Forest only | 15 |
| Agreement | 85% |

The 15 disagreements shared a repeated inbound TCP/source-port-8080 pattern.

These live flows did not contain ground-truth labels. Therefore, the results show model disagreement and alert volume—not verified attacks or live accuracy.

---

## Historical Prototype Result

The earlier synthetic/held-out prototype used 940 rows:

- 830 benign
- 110 attacks

The legacy 2-of-3 ensemble achieved:

| Metric | Result |
|---|---:|
| Accuracy | 98.94% |
| Precision | 96.30% |
| Recall | 94.55% |
| F1 | 95.41% |
| False positives | 4 |
| False negatives | 6 |

This result is retained for project history and regression comparison. It is not the main real-data headline.

---

## Project Layout

Representative layout:

```text
flowguard/
├── capture-cpp/
│   ├── include/
│   │   ├── BlockingQueue.hpp
│   │   ├── FeatureEmitter.hpp
│   │   ├── FlowAggregator.hpp
│   │   ├── FlowKey.hpp
│   │   ├── FlowStats.hpp
│   │   ├── JsonSerializer.hpp
│   │   ├── PacketInfo.hpp
│   │   └── PacketParser.hpp
│   ├── src/
│   │   ├── main.cpp
│   │   ├── PacketParser.cpp
│   │   ├── FlowAggregator.cpp
│   │   ├── FeatureEmitter.cpp
│   │   ├── JsonSerializer.cpp
│   │   ├── benchmark.cpp
│   │   └── parser_benchmark.cpp
│   ├── tests/
│   ├── CMakeLists.txt
│   └── Dockerfile
├── capture-ebpf/
│   ├── xdp_filter.bpf.c
│   ├── xdp_filter.o
│   ├── loader.c
│   ├── loader
│   ├── xdp_parser_benchmark.c
│   └── xdp_parser_benchmark.o
├── ml-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── ml/
│   │   │   ├── ensemble.py
│   │   │   └── real_only_predictor.py
│   │   ├── routes/
│   │   │   └── real_analysis.py
│   │   ├── services/
│   │   └── models/
│   │       └── real_only/
│   ├── data/
│   │   └── real_only/
│   ├── training/
│   │   ├── train_evaluate_real_only.py
│   │   └── tune_real_rf_thresholds.py
│   ├── tests/
│   ├── prisma/
│   ├── requirements.txt
│   └── Dockerfile
├── dashboard/
│   ├── index.html
│   └── Dockerfile
├── data/
│   ├── sample/
│   ├── attack_samples/
│   ├── cicids2017/
│   └── flows_output.jsonl
├── docs/
│   ├── cpp_parser_benchmark.txt
│   ├── ebpf_vs_cpp_runs.csv
│   ├── ebpf_vs_cpp_benchmark.json
│   ├── ebpf_vs_cpp_benchmark.md
│   └── model_comparison.json
├── scripts/
│   └── benchmark_ebpf_vs_cpp.sh
├── docker-compose.yml
├── HOW_TO_RUN.md
└── README.md
```

Some generated datasets, model artifacts, PCAPs, and build outputs may be intentionally excluded from Git.

---

## Requirements

### General

- Linux
- Git
- Docker and Docker Compose
- Python 3
- CMake
- A C++17 compiler

### C++ capture

- libpcap
- pthread support

### eBPF/XDP

- Linux kernel with eBPF and XDP support
- Clang/LLVM
- libbpf and development headers
- bpftool
- Linux networking tools (`ip`)
- Root privileges for loading and attaching XDP programs

### Benchmarking

- tcpreplay
- tcpdump
- Python 3
- `kernel.bpf_stats_enabled` support

---

## Quick Start with Docker Compose

From the repository root:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

Expected services:

```text
postgres
redis
capture
ml-service
dashboard
```

Check the API:

```bash
curl http://127.0.0.1:8000/health
curl "http://127.0.0.1:8000/flows/recent?limit=2"
```

Open:

- Dashboard: `http://127.0.0.1:8080`
- OpenAPI documentation: `http://127.0.0.1:8000/docs`

View logs:

```bash
docker compose logs -f ml-service
```

Stop the stack:

```bash
docker compose down
```

Remove the PostgreSQL volume as well:

```bash
docker compose down -v
```

---

## Manual C++ Capture Run

### Configure and compile

```bash
cmake \
  -S capture-cpp \
  -B capture-cpp/build \
  -DCMAKE_BUILD_TYPE=Release

cmake \
  --build capture-cpp/build \
  -j"$(nproc)"
```

### Process a PCAP

```bash
./capture-cpp/build/flowguard_capture \
  data/sample/small_sample.pcap \
  data/flows_output.jsonl
```

### Inspect output

```bash
head -n 5 data/flows_output.jsonl
```

Each line represents one aggregated flow.

---

## Manual FastAPI Run

From the repository root:

```bash
cd ml-service
source .venv/bin/activate
```

Run the selected real-data operating mode:

```bash
RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
python -m uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
```

Using `python -m uvicorn` avoids relying on a globally installed `uvicorn` command.

Check the service:

```bash
curl -s http://127.0.0.1:8000/health | python -m json.tool
```

Check the real model:

```bash
curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool
```

Run shadow inference:

```bash
curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=20" \
  | python -m json.tool
```

Compare detectors:

```bash
curl -s -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  | python -m json.tool
```

---

## eBPF/XDP Build and Run

### Compile the XDP program

From the repository root:

```bash
clang \
  -O2 \
  -g \
  -target bpf \
  -D__TARGET_ARCH_x86 \
  -c capture-ebpf/xdp_filter.bpf.c \
  -o capture-ebpf/xdp_filter.o
```

Verify the object:

```bash
file capture-ebpf/xdp_filter.o
```

Expected type:

```text
ELF 64-bit LSB relocatable, eBPF
```

### Compile the userspace loader

```bash
cc \
  -O2 \
  -g \
  capture-ebpf/loader.c \
  -o capture-ebpf/loader \
  $(pkg-config --cflags --libs libbpf)
```

### Attach to an interface

First identify the interface:

```bash
ip -br link
```

Then run the loader from the directory containing `xdp_filter.o`:

```bash
cd capture-ebpf
sudo ./loader wlan0
```

Replace `wlan0` with the correct interface.

Press `Ctrl+C` to stop the loader and detach the XDP program.

### Warning

The demonstration packet threshold in `xdp_filter.bpf.c` counts packets over the lifetime of the BPF map entry. It is not a time-windowed packets-per-second production rate limiter.

---

## Model Training and Evaluation

### Expected real-data locations

```text
data/cicids2017/
ml-service/data/real_only/
```

### Real-only training/evaluation

From `ml-service`:

```bash
PYTHONPATH=. \
.venv/bin/python \
training/train_evaluate_real_only.py
```

### Operational-threshold tuning

```bash
PYTHONPATH=. \
.venv/bin/python \
training/tune_real_rf_thresholds.py
```

Generated real-model artifacts are stored under:

```text
ml-service/app/models/real_only/
```

Expected artifacts include:

```text
random_forest.joblib
supervised_scaler.joblib
isolation_forest.joblib
anomaly_scaler.joblib
autoencoder.pt
graphsage_flow_similarity.pt
thresholds.json
rf_operational_thresholds.json
```

### Important reproducibility note

Do not select thresholds using the final Friday test set. The project uses Thursday validation data for threshold selection and Friday data only for final evaluation.

---

## Benchmark Reproduction

### C++ parser benchmark

```bash
./capture-cpp/build-benchmark/flowguard_parser_benchmark \
  data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap \
  7 \
  | tee docs/cpp_parser_benchmark.txt
```

### Full XDP versus C++ benchmark

```bash
chmod +x scripts/benchmark_ebpf_vs_cpp.sh
./scripts/benchmark_ebpf_vs_cpp.sh
```

The script:

- Enables BPF runtime statistics temporarily.
- Creates a temporary veth pair.
- Loads and pins the benchmark XDP program.
- Attaches it in native mode when supported.
- Replays the PCAP multiple times.
- Reads BPF runtime and packet counters.
- Calculates median metrics.
- Writes CSV, JSON, and Markdown reports.
- Detaches XDP and removes the temporary interfaces.

Generated output:

```text
docs/ebpf_vs_cpp_runs.csv
docs/ebpf_vs_cpp_benchmark.json
docs/ebpf_vs_cpp_benchmark.md
```

The benchmark requires `sudo`.

---

## API Reference

### Health

```http
GET /health
```

Basic API health check.

### Recent flows

```http
GET /flows/recent?limit=20
```

Returns the most recent captured flow records.

### Legacy batch analysis

```http
POST /analyze?offset=0&limit=100&persist=false
```

Parameters:

| Parameter | Meaning |
|---|---|
| `offset` | Starting flow index |
| `limit` | Batch size, up to 1,000 |
| `persist` | Save detected anomalies to PostgreSQL |

Use `persist=false` while validating behaviour.

### Alerts

```http
GET /alerts
GET /alerts/{alert_id}
```

Retrieves persisted alerts.

### Historical model metrics

```http
GET /metrics/model
```

Returns the historical held-out prototype metrics. This endpoint does not represent the final real-only Random Forest evaluation.

### Real-data model health

```http
GET /real-model/health
```

Returns:

- Model identifier
- Selected operational threshold
- Operational mode
- Resolved flow file
- Shadow-mode state

### Real-data shadow analysis

```http
POST /real-model/analyze?limit=50
```

Scores recent flows with the real-only Random Forest.

It does not persist alerts.

### Detector comparison

```http
POST /analyze/compare?limit=100
```

Runs the legacy ensemble and real Random Forest on the same recent flows.

Returns:

- Alert totals
- Agreement categories
- Agreement rate
- Real Random Forest probabilities
- Per-flow disagreement information
- Error details

The comparison route never persists alerts.

### Legacy real-capture route

```http
POST /analyse/real
```

This older experimental route is retained for compatibility. Prefer the `/real-model/*` routes for current shadow evaluation.

---

## Testing

### Python tests

```bash
cd ml-service

PYTHONPATH=. \
.venv/bin/python \
-m pytest tests -q
```

Previously verified result:

```text
8 passed
```

Re-run the suite after modifying inference routes or model-loading code.

### C++ tests

Configure and build:

```bash
cmake \
  -S capture-cpp \
  -B capture-cpp/build \
  -DCMAKE_BUILD_TYPE=Debug

cmake \
  --build capture-cpp/build \
  -j"$(nproc)"
```

Run registered tests:

```bash
ctest \
  --test-dir capture-cpp/build \
  --output-on-failure
```

C++ test targets cover areas such as:

- Flow key ordering
- Flow aggregation
- Blocking queue behaviour
- Packet parsing
- JSON serialization

### Syntax checks

Python:

```bash
python -m py_compile \
  ml-service/app/main.py \
  ml-service/app/ml/real_only_predictor.py \
  ml-service/app/routes/real_analysis.py
```

Bash:

```bash
bash -n scripts/benchmark_ebpf_vs_cpp.sh
```

---

## Generated Artifacts

### Model artifacts

```text
ml-service/app/models/real_only/
├── anomaly_scaler.joblib
├── autoencoder.pt
├── graphsage_flow_similarity.pt
├── isolation_forest.joblib
├── random_forest.joblib
├── rf_operational_thresholds.json
├── supervised_scaler.joblib
└── thresholds.json
```

### Evaluation artifacts

```text
docs/
├── cpp_parser_benchmark.txt
├── ebpf_vs_cpp_runs.csv
├── ebpf_vs_cpp_benchmark.json
├── ebpf_vs_cpp_benchmark.md
├── model_comparison.json
└── rf_threshold_tuning.txt
```

### Prepared real-data splits

```text
ml-service/data/real_only/
├── train_real.csv
├── validation_real.csv
└── test_real.csv
```

Large datasets, model files, PCAPs, and generated build files may need Git LFS or external storage rather than ordinary Git commits.

---

## Docker and Infrastructure Notes

### PostgreSQL

PostgreSQL provides durable alert storage.

The Compose configuration uses:

```text
database: flowguard
user: flowguard_user
```

Credentials in the development Compose file are for local use only and must be replaced for deployment.

### Prisma ORM

Prisma provides schema-driven database access.

The ML container startup performs:

1. Wait for PostgreSQL.
2. Wait for Redis.
3. Run `prisma db push`.
4. Run `prisma generate`.
5. Start Uvicorn.

### Redis

Redis is used inside the Compose network for messaging/pub-sub support.

It is not intentionally exposed to the host.

### Capture permissions

The capture container receives:

```text
NET_ADMIN
NET_RAW
```

These capabilities are required for packet-capture and networking operations but should be minimized in production.

### ML image

The ML image installs CPU-only PyTorch packages to avoid pulling unnecessary GPU/CUDA layers for the local CPU inference workflow.

### Dashboard image

The verified dashboard container serves the static dashboard through Nginx.

---

## Design Decisions

### JSONL between C++ and Python

JSON Lines was selected because it is:

- Human-readable.
- Append-friendly.
- Easy to debug with standard shell tools.
- Supported directly by Python.
- Independent of the C++ process lifetime.
- Suitable for replay and offline evaluation.

### Bounded queue instead of an unbounded queue

A bounded queue prevents the capture thread from consuming unlimited memory if the aggregation thread cannot keep pace.

### Model loading at startup

Saved models are loaded once when the API process starts rather than once per request. This reduces inference latency and avoids repeated disk deserialization.

### Shadow deployment

The real-data model does not immediately replace or persist into the existing alert path.

Shadow deployment allows FlowGuard to measure:

- Alert volume.
- Model disagreement.
- Probability distribution.
- Feature-semantic mismatch.
- Domain shift.
- Runtime errors.

### Day-separated evaluation

Capture-day separation was selected to reduce leakage and make the model prove that it can generalize beyond the exact capture distribution used for fitting.

### Median benchmark reporting

Performance results use medians across repeated runs to reduce sensitivity to scheduler noise and occasional outliers.

---

## Limitations and Honest Interpretation

FlowGuard is an engineering and research project, not a production-certified intrusion-detection appliance.

### Live predictions are not ground truth

A live model label of `ATTACK` is a prediction, not confirmation of malicious activity.

Accuracy, precision, and recall require labelled data.

### High live alert rate indicates possible domain shift

The real-only Random Forest produced a high alert rate on the infected-host capture. This can reflect:

- Truly unusual traffic.
- Different feature semantics.
- Dataset-to-live distribution shift.
- Poor probability calibration.
- Incomplete flow reconstruction.

It must not be described as a verified attack rate.

### Balanced final test set

The final test set intentionally contains equal benign and attack counts.

This makes model comparison clear but does not represent the natural attack prevalence of most real networks.

### GraphSAGE limitations

The GraphSAGE model had extremely high recall but very poor benign classification.

It demonstrates graph-learning implementation but requires:

- Better graph construction.
- Calibration.
- Class weighting.
- Additional validation.
- More representative graph data.

### Infected-Android PCAP labels

The infected-Android PCAP does not provide per-flow ground-truth labels.

It is valid for:

- Systems benchmarking.
- Replay.
- End-to-end testing.
- Shadow inference.
- Disagreement analysis.

It is not valid for reporting classification accuracy.

### eBPF benchmark scope

The benchmark compares implemented parser-level cost.

It does not include:

- Flow aggregation parity.
- Machine-learning inference.
- PostgreSQL persistence.
- Redis publication.
- Dashboard latency.
- Complete packet-to-alert latency.

### Demonstration drop threshold

The original XDP source counter is lifetime-based. Production rate limiting requires a time-windowed policy.

---

## Roadmap

### Detection quality

- Probability calibration using isotonic regression or Platt scaling.
- Evaluation on naturally imbalanced traffic.
- Precision-recall curves and confidence intervals.
- Leave-one-attack-family-out testing.
- Better Bot-family coverage.
- Weighted voting or stacking instead of strict agreement.
- Incident-level alert grouping.
- Feature-semantic alignment between C++ flows and CICIDS flow generation.

### Graph learning

- True IP host-communication graphs.
- Temporal graph construction.
- Class-weighted GraphSAGE loss.
- Focal loss.
- Graph mini-batching.
- Validation-based early stopping.
- Neighbourhood and edge-feature ablation studies.

### eBPF/XDP

- Time-windowed packet-rate limiting.
- Production per-CPU counters.
- Ring-buffer loss counters.
- IPv6 parsing.
- VLAN support.
- AF_XDP experiment.
- Multi-core scaling benchmark.
- Physical-NIC benchmark.
- Packet-to-alert latency measurement.

### Backend and operations

- Prometheus metrics.
- Grafana dashboards.
- Authentication and role-based access.
- Model registry and rollback.
- Alert deduplication.
- Deployment-specific secrets.
- CI for Python, C++, Docker, and eBPF verifier checks.
- Structured logging and tracing.

---

## Resume-Ready Summary

### Detailed version

> Built FlowGuard, a full-stack network intrusion detection platform using C++17/libpcap, native XDP/eBPF, FastAPI, PostgreSQL, Redis, Prisma ORM, and Docker Compose. Trained Random Forest, Isolation Forest, a PyTorch Autoencoder, and GraphSAGE on capture-day-separated CICIDS2017 data; Random Forest achieved 86.09% accuracy, 98.94% recall, 78.71% precision, and 0.8767 F1 on 10,000 real labelled flows. Benchmarked native XDP across seven runs and approximately 1.46 million packets per run, achieving 1.77× higher equivalent throughput and 42.6% lower per-packet processing cost than the C++ userspace parser.

### Compact bullets

- Built a C++17/Python network intrusion detection pipeline using libpcap, native XDP/eBPF, five-tuple flow aggregation, FastAPI, PostgreSQL, Redis, and Docker Compose.
- Achieved **86.09% accuracy, 98.94% recall, and 0.8767 F1** with Random Forest on **10,000 real capture-day-separated CICIDS2017 flows**.
- Reduced Random Forest false positives by **54.3%** with a strict four-model ensemble, improving precision to **86.96%** while documenting the recall trade-off.
- Benchmarked native XDP at **62.3 ns/packet and 16.05M equivalent packets/s**, delivering **1.77× higher equivalent throughput** than the C++ parser.

---

## Technology Keywords

### Languages and systems

```text
C++17, C, Python, SQL, Bash, JavaScript, Linux, systems programming,
multithreading, producer-consumer, bounded queue, backpressure, mutex,
condition variable, atomic state, kernel programming
```

### Networking

```text
libpcap, PCAP, tcpreplay, Ethernet, IPv4, TCP, UDP, ICMP, five-tuple,
flow aggregation, TCP flags, packet parsing, network telemetry,
network intrusion detection, NIDS, DDoS, PortScan, Bot detection
```

### eBPF/XDP

```text
eBPF, XDP, native XDP, libbpf, bpftool, BPF maps, per-CPU maps,
ring buffer, kernel-space packet processing, packet filtering,
nanoseconds per packet, packets per second
```

### Machine learning

```text
scikit-learn, PyTorch, PyTorch Geometric, Random Forest,
Isolation Forest, Autoencoder, GraphSAGE, GNN, anomaly detection,
supervised learning, unsupervised learning, feature engineering,
threshold tuning, ensemble learning, ROC-AUC, precision, recall,
F1 score, confusion matrix, domain shift, data leakage,
capture-day separation, model generalization, shadow deployment
```

### Backend and DevOps

```text
FastAPI, REST API, Uvicorn, PostgreSQL, Prisma ORM, Redis, pub/sub,
Docker, Docker Compose, Nginx, CMake, Clang, health checks,
model serving, persistent storage, internal service networking
```

---

## Security and Research Notice

FlowGuard is intended for authorized defensive-security research, learning, benchmarking, and controlled network monitoring.

Only capture, replay, or inspect traffic on systems and networks where you have permission.

Model outputs should be reviewed by a human analyst before being treated as confirmed security incidents.

---

## Current Verified Headline

> **FlowGuard achieved 86.09% accuracy, 98.94% recall, and 0.8767 F1 on 10,000 real capture-day-separated CICIDS2017 flows, while its native XDP parser delivered 1.77× higher equivalent throughput and 42.6% lower per-packet processing cost than its C++ userspace parser.**

Library
/
PROJECT 1
/FlowGuard_Detailed_README.md

# FlowGuard

> A full-stack network intrusion detection and traffic-analysis platform built with C++17, native XDP/eBPF, FastAPI, scikit-learn, PyTorch, PyTorch Geometric, PostgreSQL, Redis, Prisma ORM, Docker Compose, and Nginx.

FlowGuard converts raw network packets into flow-level security telemetry, evaluates each flow using multiple machine-learning approaches, and exposes the resulting detections through a REST API and monitoring dashboard.

The project combines three engineering areas:

- **Systems and networking:** C++ packet parsing, multithreading, flow aggregation, libpcap, Linux networking, native XDP/eBPF, BPF maps, and ring buffers.
- **Machine learning:** Random Forest, Isolation Forest, Autoencoder, GraphSAGE, feature engineering, threshold tuning, capture-day-separated evaluation, and ensemble analysis.
- **Backend and infrastructure:** FastAPI, PostgreSQL, Prisma ORM, Redis pub/sub, Docker Compose, Nginx, health checks, persistence, and shadow deployment.

---

## Table of Contents

- [Highlights](#highlights)
- [Verified Results](#verified-results)
- [What FlowGuard Does](#what-flowguard-does)
- [Architecture](#architecture)
- [Project Components](#project-components)
- [Network Features](#network-features)
- [Machine-Learning Models](#machine-learning-models)
- [Dataset and Evaluation Methodology](#dataset-and-evaluation-methodology)
- [Real-Data Model Results](#real-data-model-results)
- [eBPF/XDP Performance Benchmark](#ebpfxdp-performance-benchmark)
- [Live Shadow-Mode Evaluation](#live-shadow-mode-evaluation)
- [Project Layout](#project-layout)
- [Requirements](#requirements)
- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
- [Manual C++ Capture Run](#manual-c-capture-run)
- [Manual FastAPI Run](#manual-fastapi-run)
- [eBPF/XDP Build and Run](#ebpfxdp-build-and-run)
- [Model Training and Evaluation](#model-training-and-evaluation)
- [Benchmark Reproduction](#benchmark-reproduction)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Generated Artifacts](#generated-artifacts)
- [Docker and Infrastructure Notes](#docker-and-infrastructure-notes)
- [Design Decisions](#design-decisions)
- [Limitations and Honest Interpretation](#limitations-and-honest-interpretation)
- [Roadmap](#roadmap)
- [Resume-Ready Summary](#resume-ready-summary)
- [Technology Keywords](#technology-keywords)

---

## Highlights

- Multithreaded **C++17/libpcap** packet-to-flow processing pipeline.
- Ethernet, IPv4, TCP, UDP, and ICMP parsing.
- Bounded producer-consumer queue with backpressure.
- Five-tuple flow aggregation and TCP flag statistics.
- Native **XDP/eBPF** packet parsing and early filtering.
- Kernel-to-userspace communication through a BPF ring buffer.
- FastAPI inference service with batch analysis and alert persistence.
- PostgreSQL-backed alert storage through Prisma ORM.
- Redis-based internal messaging/pub-sub support.
- Random Forest, Isolation Forest, PyTorch Autoencoder, and GraphSAGE.
- Real CICIDS2017 training and capture-day-separated final evaluation.
- Validation-selected Random Forest operating thresholds.
- Shadow deployment and legacy-versus-real model comparison.
- Reproducible C++ versus XDP performance benchmark.
- Docker Compose orchestration for the complete local stack.

---

## Verified Results

### Real-data intrusion-detection result

The strongest individual model was Random Forest:

| Metric | Result |
|---|---:|
| Test flows | 10,000 |
| Benign flows | 5,000 |
| Attack flows | 5,000 |
| Accuracy | **86.09%** |
| Precision | **78.71%** |
| Recall | **98.94%** |
| F1 score | **0.8767** |
| ROC-AUC | **0.9036** |
| False positives | 1,338 |
| False negatives | 53 |

The test data was separated by capture day from the training and validation data.

### Native XDP/eBPF performance result

| Metric | C++ userspace parser | Native XDP/eBPF parser |
|---|---:|---:|
| Processing cost | 108.456 ns/packet | **62.301 ns/packet** |
| Equivalent throughput | 9.07 million packets/s | **16.05 million packets/s** |
| Processing-cost reduction | — | **42.6%** |
| Equivalent-throughput improvement | — | **1.77×** |
| Sustained complete replay path | — | 316,330 packets/s |
| Observed packet loss | — | approximately 0% |

The XDP benchmark used seven measured runs and approximately 1.46 million replayed packets per run.

### Four-model ensemble result

The strict four-model ensemble prioritized agreement and reduced false alarms:

| Metric | Result |
|---|---:|
| Accuracy | 84.71% |
| Precision | **86.96%** |
| Recall | 81.66% |
| F1 score | 0.8423 |
| False positives | 612 |
| False negatives | 917 |
| False-positive reduction vs Random Forest | **54.3%** |

The ensemble improved precision and reduced false positives, but it also missed more attacks. Random Forest therefore remains the strongest general headline model.

---

## What FlowGuard Does

FlowGuard implements the following pipeline:

1. Read packets from a PCAP file or inspect live ingress traffic.
2. Validate Ethernet and IPv4 headers.
3. Parse TCP, UDP, ICMP, ports, lengths, timestamps, and TCP flags.
4. Convert packets into a structured `PacketInfo` representation.
5. Group packets into flows using a network five-tuple.
6. Calculate duration, traffic volume, rate, and TCP-behaviour features.
7. Emit completed flows as JSON Lines.
8. Load the flows into a FastAPI inference service.
9. Score each flow with one or more detection models.
10. Compare model decisions in shadow mode.
11. Optionally persist alerts in PostgreSQL.
12. Expose flows, alerts, metrics, and health state through REST endpoints.
13. Display operational data through an Nginx-served dashboard.

---

## Architecture

```text
                         ┌──────────────────────────────┐
                         │ PCAP replay or live traffic  │
                         └──────────────┬───────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
        ┌────────────────────────┐              ┌────────────────────────┐
        │ C++17/libpcap capture  │              │ Native XDP/eBPF path   │
        │ Userspace packet path  │              │ Kernel ingress path    │
        └────────────┬───────────┘              └────────────┬───────────┘
                     │                                       │
                     ▼                                       ▼
        ┌────────────────────────┐              ┌────────────────────────┐
        │ PacketParser           │              │ BPF maps / ring buffer │
        │ Ethernet/IP/TCP/UDP    │              │ pass/drop/event output │
        └────────────┬───────────┘              └────────────┬───────────┘
                     │                                       │
                     └───────────────────┬───────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Five-tuple aggregation │
                            │ Packet/byte/TCP stats  │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ JSONL feature pipeline │
                            └────────────┬───────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ FastAPI ML service     │
                            │ Normalization/scoring  │
                            └────────────┬───────────┘
                                         ▼
          ┌──────────────────────────────────────────────────────────┐
          │ Random Forest │ Isolation Forest │ Autoencoder │ GraphSAGE │
          └──────────────────────────────┬───────────────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Shadow comparison /    │
                            │ voting / alert logic   │
                            └────────────┬───────────┘
                                         ▼
                  ┌──────────────────────┴──────────────────────┐
                  ▼                                             ▼
        ┌────────────────────────┐                  ┌────────────────────────┐
        │ PostgreSQL + Prisma    │                  │ Redis pub/sub          │
        │ Durable alert storage  │                  │ Internal notifications │
        └────────────┬───────────┘                  └────────────┬───────────┘
                     └───────────────────┬───────────────────────┘
                                         ▼
                            ┌────────────────────────┐
                            │ Nginx dashboard        │
                            │ Flows/alerts/metrics   │
                            └────────────────────────┘
```

---

## Project Components

### `capture-cpp`

The C++17 layer is responsible for packet parsing and flow aggregation.

Key responsibilities:

- Open PCAP files through libpcap.
- Parse Ethernet and IPv4 packet structure.
- Extract transport protocol and ports.
- Record packet size and nanosecond timestamp representation.
- Extract TCP SYN, ACK, FIN, and RST flags.
- Send parsed packets through a bounded blocking queue.
- Aggregate packets into flows.
- Write completed flow records to JSONL.

Concurrency model:

```text
Capture thread
    │
    ▼
BlockingQueue<PacketInfo>
    │
    ▼
Aggregation thread
```

The bounded queue provides backpressure when aggregation is slower than capture and prevents unrestricted memory growth.

### `capture-ebpf`

The eBPF layer performs packet inspection at the Linux XDP hook.

Implemented concepts:

- Native XDP attachment.
- Safe packet-bound checks required by the eBPF verifier.
- Ethernet and IPv4 parsing.
- Variable-length IPv4 header handling.
- TCP and UDP port extraction.
- Per-source tracking through BPF maps.
- Demonstration early-drop action.
- BPF ring-buffer event transfer.
- libbpf userspace loader.
- Signal-based cleanup and XDP detach.
- Dedicated silent benchmark program.

### `ml-service`

The Python service provides:

- Flow normalization.
- Feature generation.
- Saved-model loading.
- Legacy ensemble inference.
- Real-data Random Forest inference.
- Operational-threshold selection.
- Shadow-mode scoring.
- Side-by-side model comparison.
- Optional alert persistence.
- Alert lookup.
- Model metric reporting.
- OpenAPI documentation.

### `dashboard`

The verified dashboard is a static HTML/CSS/JavaScript interface served by Nginx.

It is intended to display:

- Recent network flows.
- Detected anomalies.
- Persisted alerts.
- Model and system metrics.
- Basic operational health.

### `docker-compose.yml`

The local stack contains:

- PostgreSQL 16
- Redis 7
- C++ capture service
- FastAPI ML service
- Nginx dashboard

PostgreSQL and Redis are kept inside the Compose network and are not intentionally exposed through host ports.

---

## Network Features

The real-data model pipeline uses 11 flow-level features:

| Feature | Meaning |
|---|---|
| `duration_seconds` | Time between first and last packet |
| `packet_count` | Number of packets in the flow |
| `total_bytes` | Total transferred bytes |
| `bytes_per_sec` | Byte-transfer rate |
| `packets_per_sec` | Packet rate |
| `syn_count` | TCP SYN flags observed |
| `ack_count` | TCP ACK flags observed |
| `fin_count` | TCP FIN flags observed |
| `rst_count` | TCP RST flags observed |
| `syn_ack_ratio` | SYN count relative to ACK activity |
| `rst_ratio` | RST count relative to packet count |

Derived features:

```text
bytes_per_sec   = total_bytes / duration_seconds
packets_per_sec = packet_count / duration_seconds
syn_ack_ratio   = syn_count / (ack_count + 1)
rst_ratio       = rst_count / (packet_count + 1)
```

Zero-duration flows are handled safely to avoid division by zero.

---

## Machine-Learning Models

### Random Forest

A supervised binary attack classifier trained on labelled benign and malicious traffic.

Strengths:

- Best overall real-data F1 score.
- Very high attack recall.
- Direct attack-probability output.
- Feature-importance support.
- Fast CPU inference.

### Isolation Forest

An unsupervised anomaly detector trained on benign traffic.

Strengths:

- Does not require attack labels during fitting.
- Detects outliers that differ from normal behaviour.
- Provides an independent anomaly signal.

Observed limitation:

- Very high recall but excessive false positives on the final real-data test split.

### PyTorch Autoencoder

A neural anomaly detector trained to reconstruct benign feature vectors.

Detection principle:

```text
low reconstruction error  → resembles learned benign behaviour
high reconstruction error → possible anomaly
```

The reconstruction threshold is selected from validation behaviour.

### GraphSAGE

A graph neural network implemented with PyTorch Geometric.

For the real CICIDS2017 experiment:

- Each flow is represented as a node.
- Similar flows are connected through feature-space proximity.
- GraphSAGE aggregates neighbourhood information.
- The correct description is a **flow-similarity graph model**.

The CICIDS2017 CSV files used in this experiment did not provide source and destination IP columns, so this model must not be described as a host-communication graph.

### Legacy three-model ensemble

The original project path combines:

- Isolation Forest
- Random Forest
- Autoencoder

An anomaly is raised when at least two of the three models agree.

This path belongs to the earlier prototype/held-out evaluation.

### Real-data four-model ensemble

The research evaluation combines:

- Random Forest
- Isolation Forest
- Autoencoder
- GraphSAGE

The evaluated strict agreement rule reduced false positives but caused a substantial recall drop.

---

## Dataset and Evaluation Methodology

### CICIDS2017 data

Total labelled records available locally:

| Category | Count |
|---|---:|
| Total | 2,830,743 |
| Benign | 2,273,097 |
| Attack | 557,646 |

Attack families represented in the source collection include:

- DDoS
- PortScan
- Bot
- FTP-Patator
- SSH-Patator
- DoS Hulk
- DoS GoldenEye
- DoS Slowhttptest
- DoS slowloris
- Heartbleed
- Web Attack — Brute Force
- Web Attack — XSS
- Web Attack — SQL Injection
- Infiltration

### Capture-day-separated splits

Instead of randomly mixing rows from the same capture files, FlowGuard separates the data by collection day:

| Split | Capture days | Benign | Attack | Total |
|---|---|---:|---:|---:|
| Training | Monday–Wednesday | 10,000 | 10,000 | 20,000 |
| Validation | Thursday | 2,000 | 2,000 | 4,000 |
| Final test | Friday | 5,000 | 5,000 | 10,000 |

The validation set is used for threshold selection. The Friday test split remains untouched until final evaluation.

### Why day separation matters

Random row splitting can produce overly optimistic results when nearly identical flows from the same capture occur in both training and test data.

Day-separated evaluation provides a more difficult test of:

- Cross-day generalization.
- Traffic-distribution changes.
- Previously unseen or sparsely represented attack families.
- Threshold robustness.
- Resistance to train-test leakage.

---

## Real-Data Model Results

### Binary classification metrics

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Isolation Forest | 62.51% | 57.21% | 99.26% | 72.59% |
| Random Forest | **86.09%** | 78.71% | **98.94%** | **87.67%** |
| Autoencoder | 75.86% | 73.11% | 81.80% | 77.21% |
| GraphSAGE | 55.39% | 52.85% | 99.88% | 69.13% |
| Strict four-model ensemble | 84.71% | **86.96%** | 81.66% | 84.23% |

Random Forest ROC-AUC:

```text
0.9036
```

### Confusion matrices

Format:

```text
[[true negatives, false positives],
 [false negatives, true positives]]
```

Random Forest:

```text
[[3662, 1338],
 [  53, 4947]]
```

Strict four-model ensemble:

```text
[[4388,  612],
 [ 917, 4083]]
```

### Operational trade-off

Compared with Random Forest, the ensemble:

- Reduced false positives from 1,338 to 612.
- Reduced false positives by 54.3%.
- Increased precision from 78.71% to 86.96%.
- Increased false negatives from 53 to 917.
- Reduced attack recall from 98.94% to 81.66%.

The ensemble is useful when false alarms are especially expensive, but Random Forest is the stronger general detector.

### Per-family ensemble recall

| Attack family | Recall | Test flows |
|---|---:|---:|
| DDoS | 84.99% | 2,152 |
| PortScan | 80.35% | 2,804 |
| Bot | 2.27% | 44 |

Bot recall was poor because the final sampling included few Bot flows and the training-day attack data did not provide equivalent Bot coverage.

---

## eBPF/XDP Performance Benchmark

### Workload

- PCAP: infected-Android traffic capture.
- PCAP size: approximately 24 MB.
- Packets per PCAP loop: 29,125.
- XDP replay loops per measured run: 50.
- Expected packets per measured run: 1,456,250.
- Measured runs: 7.
- XDP attachment mode: native.
- C++ build: Release mode with `-O3`.
- XDP benchmark: silent parser using a per-CPU map.
- Runtime measurement: kernel BPF program statistics through `bpftool`.

### Median C++ result

```text
C++ median CPU cost:          108.456 ns/packet
C++ median wall cost:         110.278 ns/packet
C++ equivalent throughput:    9,067,963 packets/s
```

### Median native-XDP result

```text
XDP median kernel cost:       62.301 ns/packet
XDP equivalent throughput:    16,051,175 packets/s
XDP sustained replay rate:    316,330 packets/s
XDP observed packet loss:     approximately 0%
```

### Improvement

```text
Processing-cost speedup:      1.74×
Equivalent-throughput gain:   1.77×
Processing-cost reduction:    42.6%
Equivalent-throughput rise:   approximately 77%
```

### Interpretation

The 16.05 million packets/s result is equivalent throughput calculated from measured kernel execution time.

The 316,330 packets/s result measures the complete replay path:

```text
PCAP
  → tcpreplay
  → virtual Ethernet pair
  → Linux ingress path
  → native XDP program
```

The complete replay rate includes replay generation, veth, scheduling, and other kernel overhead. It should not be described as the XDP parser's maximum theoretical capacity.

A measured delivery rate slightly above 100% was caused by a few additional control/interface packets. It is reported as approximately 100% delivery and approximately 0% loss.

---

## Live Shadow-Mode Evaluation

The selected real-data Random Forest is integrated into FastAPI without replacing the legacy alert pipeline.

### Real-model health example

```json
{
  "status": "ok",
  "model": "real_only_random_forest",
  "threshold": 0.0235,
  "operational_mode": "balanced",
  "flow_file": "data/flows_output.jsonl",
  "mode": "shadow"
}
```

### Operational mode

Select the threshold configuration through:

```bash
RF_OPERATIONAL_MODE=balanced
```

The balanced threshold was selected on the Thursday validation split.

### Model-comparison endpoint

The comparison route runs the legacy ensemble and real-data Random Forest on the same recent flows without writing alerts.

Verified comparison over 100 flows:

| Metric | Result |
|---|---:|
| Analyzed | 100 |
| Errors | 0 |
| Legacy alerts | 85 |
| Real Random Forest alerts | 100 |
| Both alert | 85 |
| Both benign | 0 |
| Legacy only | 0 |
| Real Random Forest only | 15 |
| Agreement | 85% |

The 15 disagreements shared a repeated inbound TCP/source-port-8080 pattern.

These live flows did not contain ground-truth labels. Therefore, the results show model disagreement and alert volume—not verified attacks or live accuracy.

---

## Historical Prototype Result

The earlier synthetic/held-out prototype used 940 rows:

- 830 benign
- 110 attacks

The legacy 2-of-3 ensemble achieved:

| Metric | Result |
|---|---:|
| Accuracy | 98.94% |
| Precision | 96.30% |
| Recall | 94.55% |
| F1 | 95.41% |
| False positives | 4 |
| False negatives | 6 |

This result is retained for project history and regression comparison. It is not the main real-data headline.

---

## Project Layout

Representative layout:

```text
flowguard/
├── capture-cpp/
│   ├── include/
│   │   ├── BlockingQueue.hpp
│   │   ├── FeatureEmitter.hpp
│   │   ├── FlowAggregator.hpp
│   │   ├── FlowKey.hpp
│   │   ├── FlowStats.hpp
│   │   ├── JsonSerializer.hpp
│   │   ├── PacketInfo.hpp
│   │   └── PacketParser.hpp
│   ├── src/
│   │   ├── main.cpp
│   │   ├── PacketParser.cpp
│   │   ├── FlowAggregator.cpp
│   │   ├── FeatureEmitter.cpp
│   │   ├── JsonSerializer.cpp
│   │   ├── benchmark.cpp
│   │   └── parser_benchmark.cpp
│   ├── tests/
│   ├── CMakeLists.txt
│   └── Dockerfile
├── capture-ebpf/
│   ├── xdp_filter.bpf.c
│   ├── xdp_filter.o
│   ├── loader.c
│   ├── loader
│   ├── xdp_parser_benchmark.c
│   └── xdp_parser_benchmark.o
├── ml-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── ml/
│   │   │   ├── ensemble.py
│   │   │   └── real_only_predictor.py
│   │   ├── routes/
│   │   │   └── real_analysis.py
│   │   ├── services/
│   │   └── models/
│   │       └── real_only/
│   ├── data/
│   │   └── real_only/
│   ├── training/
│   │   ├── train_evaluate_real_only.py
│   │   └── tune_real_rf_thresholds.py
│   ├── tests/
│   ├── prisma/
│   ├── requirements.txt
│   └── Dockerfile
├── dashboard/
│   ├── index.html
│   └── Dockerfile
├── data/
│   ├── sample/
│   ├── attack_samples/
│   ├── cicids2017/
│   └── flows_output.jsonl
├── docs/
│   ├── cpp_parser_benchmark.txt
│   ├── ebpf_vs_cpp_runs.csv
│   ├── ebpf_vs_cpp_benchmark.json
│   ├── ebpf_vs_cpp_benchmark.md
│   └── model_comparison.json
├── scripts/
│   └── benchmark_ebpf_vs_cpp.sh
├── docker-compose.yml
├── HOW_TO_RUN.md
└── README.md
```

Some generated datasets, model artifacts, PCAPs, and build outputs may be intentionally excluded from Git.

---

## Requirements

### General

- Linux
- Git
- Docker and Docker Compose
- Python 3
- CMake
- A C++17 compiler

### C++ capture

- libpcap
- pthread support

### eBPF/XDP

- Linux kernel with eBPF and XDP support
- Clang/LLVM
- libbpf and development headers
- bpftool
- Linux networking tools (`ip`)
- Root privileges for loading and attaching XDP programs

### Benchmarking

- tcpreplay
- tcpdump
- Python 3
- `kernel.bpf_stats_enabled` support

---

## Quick Start with Docker Compose

From the repository root:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

Expected services:

```text
postgres
redis
capture
ml-service
dashboard
```

Check the API:

```bash
curl http://127.0.0.1:8000/health
curl "http://127.0.0.1:8000/flows/recent?limit=2"
```

Open:

- Dashboard: `http://127.0.0.1:8080`
- OpenAPI documentation: `http://127.0.0.1:8000/docs`

View logs:

```bash
docker compose logs -f ml-service
```

Stop the stack:

```bash
docker compose down
```

Remove the PostgreSQL volume as well:

```bash
docker compose down -v
```

---

## Manual C++ Capture Run

### Configure and compile

```bash
cmake \
  -S capture-cpp \
  -B capture-cpp/build \
  -DCMAKE_BUILD_TYPE=Release

cmake \
  --build capture-cpp/build \
  -j"$(nproc)"
```

### Process a PCAP

```bash
./capture-cpp/build/flowguard_capture \
  data/sample/small_sample.pcap \
  data/flows_output.jsonl
```

### Inspect output

```bash
head -n 5 data/flows_output.jsonl
```

Each line represents one aggregated flow.

---

## Manual FastAPI Run

From the repository root:

```bash
cd ml-service
source .venv/bin/activate
```

Run the selected real-data operating mode:

```bash
RF_OPERATIONAL_MODE=balanced \
PYTHONPATH=. \
python -m uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
```

Using `python -m uvicorn` avoids relying on a globally installed `uvicorn` command.

Check the service:

```bash
curl -s http://127.0.0.1:8000/health | python -m json.tool
```

Check the real model:

```bash
curl -s http://127.0.0.1:8000/real-model/health \
  | python -m json.tool
```

Run shadow inference:

```bash
curl -s -X POST \
  "http://127.0.0.1:8000/real-model/analyze?limit=20" \
  | python -m json.tool
```

Compare detectors:

```bash
curl -s -X POST \
  "http://127.0.0.1:8000/analyze/compare?limit=100" \
  | python -m json.tool
```

---

## eBPF/XDP Build and Run

### Compile the XDP program

From the repository root:

```bash
clang \
  -O2 \
  -g \
  -target bpf \
  -D__TARGET_ARCH_x86 \
  -c capture-ebpf/xdp_filter.bpf.c \
  -o capture-ebpf/xdp_filter.o
```

Verify the object:

```bash
file capture-ebpf/xdp_filter.o
```

Expected type:

```text
ELF 64-bit LSB relocatable, eBPF
```

### Compile the userspace loader

```bash
cc \
  -O2 \
  -g \
  capture-ebpf/loader.c \
  -o capture-ebpf/loader \
  $(pkg-config --cflags --libs libbpf)
```

### Attach to an interface

First identify the interface:

```bash
ip -br link
```

Then run the loader from the directory containing `xdp_filter.o`:

```bash
cd capture-ebpf
sudo ./loader wlan0
```

Replace `wlan0` with the correct interface.

Press `Ctrl+C` to stop the loader and detach the XDP program.

### Warning

The demonstration packet threshold in `xdp_filter.bpf.c` counts packets over the lifetime of the BPF map entry. It is not a time-windowed packets-per-second production rate limiter.

---

## Model Training and Evaluation

### Expected real-data locations

```text
data/cicids2017/
ml-service/data/real_only/
```

### Real-only training/evaluation

From `ml-service`:

```bash
PYTHONPATH=. \
.venv/bin/python \
training/train_evaluate_real_only.py
```

### Operational-threshold tuning

```bash
PYTHONPATH=. \
.venv/bin/python \
training/tune_real_rf_thresholds.py
```

Generated real-model artifacts are stored under:

```text
ml-service/app/models/real_only/
```

Expected artifacts include:

```text
random_forest.joblib
supervised_scaler.joblib
isolation_forest.joblib
anomaly_scaler.joblib
autoencoder.pt
graphsage_flow_similarity.pt
thresholds.json
rf_operational_thresholds.json
```

### Important reproducibility note

Do not select thresholds using the final Friday test set. The project uses Thursday validation data for threshold selection and Friday data only for final evaluation.

---

## Benchmark Reproduction

### C++ parser benchmark

```bash
./capture-cpp/build-benchmark/flowguard_parser_benchmark \
  data/attack_samples/2025-10-02-traffic-from-infected-Android-phone.pcap \
  7 \
  | tee docs/cpp_parser_benchmark.txt
```

### Full XDP versus C++ benchmark

```bash
chmod +x scripts/benchmark_ebpf_vs_cpp.sh
./scripts/benchmark_ebpf_vs_cpp.sh
```

The script:

- Enables BPF runtime statistics temporarily.
- Creates a temporary veth pair.
- Loads and pins the benchmark XDP program.
- Attaches it in native mode when supported.
- Replays the PCAP multiple times.
- Reads BPF runtime and packet counters.
- Calculates median metrics.
- Writes CSV, JSON, and Markdown reports.
- Detaches XDP and removes the temporary interfaces.

Generated output:

```text
docs/ebpf_vs_cpp_runs.csv
docs/ebpf_vs_cpp_benchmark.json
docs/ebpf_vs_cpp_benchmark.md
```

The benchmark requires `sudo`.

---

## API Reference

### Health

```http
GET /health
```

Basic API health check.

### Recent flows

```http
GET /flows/recent?limit=20
```

Returns the most recent captured flow records.

### Legacy batch analysis

```http
POST /analyze?offset=0&limit=100&persist=false
```

Parameters:

| Parameter | Meaning |
|---|---|
| `offset` | Starting flow index |
| `limit` | Batch size, up to 1,000 |
| `persist` | Save detected anomalies to PostgreSQL |

Use `persist=false` while validating behaviour.

### Alerts

```http
GET /alerts
GET /alerts/{alert_id}
```

Retrieves persisted alerts.

### Historical model metrics

```http
GET /metrics/model
```

Returns the historical held-out prototype metrics. This endpoint does not represent the final real-only Random Forest evaluation.

### Real-data model health

```http
GET /real-model/health
```

Returns:

- Model identifier
- Selected operational threshold
- Operational mode
- Resolved flow file
- Shadow-mode state

### Real-data shadow analysis

```http
POST /real-model/analyze?limit=50
```

Scores recent flows with the real-only Random Forest.

It does not persist alerts.

### Detector comparison

```http
POST /analyze/compare?limit=100
```

Runs the legacy ensemble and real Random Forest on the same recent flows.

Returns:

- Alert totals
- Agreement categories
- Agreement rate
- Real Random Forest probabilities
- Per-flow disagreement information
- Error details

The comparison route never persists alerts.

### Legacy real-capture route

```http
POST /analyse/real
```

This older experimental route is retained for compatibility. Prefer the `/real-model/*` routes for current shadow evaluation.

---

## Testing

### Python tests

```bash
cd ml-service

PYTHONPATH=. \
.venv/bin/python \
-m pytest tests -q
```

Previously verified result:

```text
8 passed
```

Re-run the suite after modifying inference routes or model-loading code.

### C++ tests

Configure and build:

```bash
cmake \
  -S capture-cpp \
  -B capture-cpp/build \
  -DCMAKE_BUILD_TYPE=Debug

cmake \
  --build capture-cpp/build \
  -j"$(nproc)"
```

Run registered tests:

```bash
ctest \
  --test-dir capture-cpp/build \
  --output-on-failure
```

C++ test targets cover areas such as:

- Flow key ordering
- Flow aggregation
- Blocking queue behaviour
- Packet parsing
- JSON serialization

### Syntax checks

Python:

```bash
python -m py_compile \
  ml-service/app/main.py \
  ml-service/app/ml/real_only_predictor.py \
  ml-service/app/routes/real_analysis.py
```

Bash:

```bash
bash -n scripts/benchmark_ebpf_vs_cpp.sh
```

---

## Generated Artifacts

### Model artifacts

```text
ml-service/app/models/real_only/
├── anomaly_scaler.joblib
├── autoencoder.pt
├── graphsage_flow_similarity.pt
├── isolation_forest.joblib
├── random_forest.joblib
├── rf_operational_thresholds.json
├── supervised_scaler.joblib
└── thresholds.json
```

### Evaluation artifacts

```text
docs/
├── cpp_parser_benchmark.txt
├── ebpf_vs_cpp_runs.csv
├── ebpf_vs_cpp_benchmark.json
├── ebpf_vs_cpp_benchmark.md
├── model_comparison.json
└── rf_threshold_tuning.txt
```

### Prepared real-data splits

```text
ml-service/data/real_only/
├── train_real.csv
├── validation_real.csv
└── test_real.csv
```

Large datasets, model files, PCAPs, and generated build files may need Git LFS or external storage rather than ordinary Git commits.

---

## Docker and Infrastructure Notes

### PostgreSQL

PostgreSQL provides durable alert storage.

The Compose configuration uses:

```text
database: flowguard
user: flowguard_user
```

Credentials in the development Compose file are for local use only and must be replaced for deployment.

### Prisma ORM

Prisma provides schema-driven database access.

The ML container startup performs:

1. Wait for PostgreSQL.
2. Wait for Redis.
3. Run `prisma db push`.
4. Run `prisma generate`.
5. Start Uvicorn.

### Redis

Redis is used inside the Compose network for messaging/pub-sub support.

It is not intentionally exposed to the host.

### Capture permissions

The capture container receives:

```text
NET_ADMIN
NET_RAW
```

These capabilities are required for packet-capture and networking operations but should be minimized in production.

### ML image

The ML image installs CPU-only PyTorch packages to avoid pulling unnecessary GPU/CUDA layers for the local CPU inference workflow.

### Dashboard image

The verified dashboard container serves the static dashboard through Nginx.

---

## Design Decisions

### JSONL between C++ and Python

JSON Lines was selected because it is:

- Human-readable.
- Append-friendly.
- Easy to debug with standard shell tools.
- Supported directly by Python.
- Independent of the C++ process lifetime.
- Suitable for replay and offline evaluation.

### Bounded queue instead of an unbounded queue

A bounded queue prevents the capture thread from consuming unlimited memory if the aggregation thread cannot keep pace.

### Model loading at startup

Saved models are loaded once when the API process starts rather than once per request. This reduces inference latency and avoids repeated disk deserialization.

### Shadow deployment

The real-data model does not immediately replace or persist into the existing alert path.

Shadow deployment allows FlowGuard to measure:

- Alert volume.
- Model disagreement.
- Probability distribution.
- Feature-semantic mismatch.
- Domain shift.
- Runtime errors.

### Day-separated evaluation

Capture-day separation was selected to reduce leakage and make the model prove that it can generalize beyond the exact capture distribution used for fitting.

### Median benchmark reporting

Performance results use medians across repeated runs to reduce sensitivity to scheduler noise and occasional outliers.

---

## Limitations and Honest Interpretation

FlowGuard is an engineering and research project, not a production-certified intrusion-detection appliance.

### Live predictions are not ground truth

A live model label of `ATTACK` is a prediction, not confirmation of malicious activity.

Accuracy, precision, and recall require labelled data.

### High live alert rate indicates possible domain shift

The real-only Random Forest produced a high alert rate on the infected-host capture. This can reflect:

- Truly unusual traffic.
- Different feature semantics.
- Dataset-to-live distribution shift.
- Poor probability calibration.
- Incomplete flow reconstruction.

It must not be described as a verified attack rate.

### Balanced final test set

The final test set intentionally contains equal benign and attack counts.

This makes model comparison clear but does not represent the natural attack prevalence of most real networks.

### GraphSAGE limitations

The GraphSAGE model had extremely high recall but very poor benign classification.

It demonstrates graph-learning implementation but requires:

- Better graph construction.
- Calibration.
- Class weighting.
- Additional validation.
- More representative graph data.

### Infected-Android PCAP labels

The infected-Android PCAP does not provide per-flow ground-truth labels.

It is valid for:

- Systems benchmarking.
- Replay.
- End-to-end testing.
- Shadow inference.
- Disagreement analysis.

It is not valid for reporting classification accuracy.

### eBPF benchmark scope

The benchmark compares implemented parser-level cost.

It does not include:

- Flow aggregation parity.
- Machine-learning inference.
- PostgreSQL persistence.
- Redis publication.
- Dashboard latency.
- Complete packet-to-alert latency.

### Demonstration drop threshold

The original XDP source counter is lifetime-based. Production rate limiting requires a time-windowed policy.

---

## Roadmap

### Detection quality

- Probability calibration using isotonic regression or Platt scaling.
- Evaluation on naturally imbalanced traffic.
- Precision-recall curves and confidence intervals.
- Leave-one-attack-family-out testing.
- Better Bot-family coverage.
- Weighted voting or stacking instead of strict agreement.
- Incident-level alert grouping.
- Feature-semantic alignment between C++ flows and CICIDS flow generation.

### Graph learning

- True IP host-communication graphs.
- Temporal graph construction.
- Class-weighted GraphSAGE loss.
- Focal loss.
- Graph mini-batching.
- Validation-based early stopping.
- Neighbourhood and edge-feature ablation studies.

### eBPF/XDP

- Time-windowed packet-rate limiting.
- Production per-CPU counters.
- Ring-buffer loss counters.
- IPv6 parsing.
- VLAN support.
- AF_XDP experiment.
- Multi-core scaling benchmark.
- Physical-NIC benchmark.
- Packet-to-alert latency measurement.

### Backend and operations

- Prometheus metrics.
- Grafana dashboards.
- Authentication and role-based access.
- Model registry and rollback.
- Alert deduplication.
- Deployment-specific secrets.
- CI for Python, C++, Docker, and eBPF verifier checks.
- Structured logging and tracing.

---

## Resume-Ready Summary

### Detailed version

> Built FlowGuard, a full-stack network intrusion detection platform using C++17/libpcap, native XDP/eBPF, FastAPI, PostgreSQL, Redis, Prisma ORM, and Docker Compose. Trained Random Forest, Isolation Forest, a PyTorch Autoencoder, and GraphSAGE on capture-day-separated CICIDS2017 data; Random Forest achieved 86.09% accuracy, 98.94% recall, 78.71% precision, and 0.8767 F1 on 10,000 real labelled flows. Benchmarked native XDP across seven runs and approximately 1.46 million packets per run, achieving 1.77× higher equivalent throughput and 42.6% lower per-packet processing cost than the C++ userspace parser.

### Compact bullets

- Built a C++17/Python network intrusion detection pipeline using libpcap, native XDP/eBPF, five-tuple flow aggregation, FastAPI, PostgreSQL, Redis, and Docker Compose.
- Achieved **86.09% accuracy, 98.94% recall, and 0.8767 F1** with Random Forest on **10,000 real capture-day-separated CICIDS2017 flows**.
- Reduced Random Forest false positives by **54.3%** with a strict four-model ensemble, improving precision to **86.96%** while documenting the recall trade-off.
- Benchmarked native XDP at **62.3 ns/packet and 16.05M equivalent packets/s**, delivering **1.77× higher equivalent throughput** than the C++ parser.

---

## Technology Keywords

### Languages and systems

```text
C++17, C, Python, SQL, Bash, JavaScript, Linux, systems programming,
multithreading, producer-consumer, bounded queue, backpressure, mutex,
condition variable, atomic state, kernel programming
```

### Networking

```text
libpcap, PCAP, tcpreplay, Ethernet, IPv4, TCP, UDP, ICMP, five-tuple,
flow aggregation, TCP flags, packet parsing, network telemetry,
network intrusion detection, NIDS, DDoS, PortScan, Bot detection
```

### eBPF/XDP

```text
eBPF, XDP, native XDP, libbpf, bpftool, BPF maps, per-CPU maps,
ring buffer, kernel-space packet processing, packet filtering,
nanoseconds per packet, packets per second
```

### Machine learning

```text
scikit-learn, PyTorch, PyTorch Geometric, Random Forest,
Isolation Forest, Autoencoder, GraphSAGE, GNN, anomaly detection,
supervised learning, unsupervised learning, feature engineering,
threshold tuning, ensemble learning, ROC-AUC, precision, recall,
F1 score, confusion matrix, domain shift, data leakage,
capture-day separation, model generalization, shadow deployment
```

### Backend and DevOps

```text
FastAPI, REST API, Uvicorn, PostgreSQL, Prisma ORM, Redis, pub/sub,
Docker, Docker Compose, Nginx, CMake, Clang, health checks,
model serving, persistent storage, internal service networking
```

---

## Security and Research Notice

FlowGuard is intended for authorized defensive-security research, learning, benchmarking, and controlled network monitoring.

Only capture, replay, or inspect traffic on systems and networks where you have permission.

Model outputs should be reviewed by a human analyst before being treated as confirmed security incidents.

---

## Current Verified Headline

> **FlowGuard achieved 86.09% accuracy, 98.94% recall, and 0.8767 F1 on 10,000 real capture-day-separated CICIDS2017 flows, while its native XDP parser delivered 1.77× higher equivalent throughput and 42.6% lower per-packet processing cost than its C++ userspace parser.**
