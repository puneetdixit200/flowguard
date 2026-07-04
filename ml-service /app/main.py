from fastapi import FastAPI

app = FastAPI(title="FlowGuard API")  # fastapi app

# temporary in memory data

recent_flows = [
    {
        "src_ip": "192.168.1.10",
        "dst_ip": "8.8.8.8",
        "scr_port": 51514,
        "dst_port": 53,
        "protocol": "UDP",
        "packet_count": 12,
        "total_bytes": 1024,
        "severity": "low",
    }
]

alerts = [
    {
        "id": 1,
        "message": "Possible scan behviour",
        "severity": "medium",
        "source": "baseline-model",
    }
]


@app.get("/health")
def health():
    return {"status": "ok"}  # basic health checkpoint


@app.get("/flows/recent")
def get_recent_flows():
    # return recent flow sumamries
    return recent_flows


@app.get("/alerts")
def get_alerts():
    # return recent flow sumamries
    return alerts
