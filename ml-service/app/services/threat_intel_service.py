"""
Checks flagged flows against a local threat intel table.
This is what lets your report say "X% of alerts correlated with known threat
intel" instead of just "the model said so" — a named skill area recruiters
explicitly look for.
"""
import csv
from app.db import get_prisma

async def seed_threat_intel():
    """laod csv into postgres once, during first run"""
    prisma = await get_prisma()
    existing = await prisma.threatintelentry.count()
    if existing>0:
        return

    with open("data/threat_intel_seed.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            await prisma.threatintelentry.create(data={
                "ip": row["ip"],
                "category": row["category"],
                "source": row["source"],
            })

async def check_ip(ip:str)->dict:
    """return match info if IP is a known bad IP"""
    prisma = await get_prisma()
    match = await prisma.threatintelentry.find_unique(where={"ip": ip})
    if match:
        return {"matched": True, "note": f"Matches known {match.category} ({match.source})"}
    return {"matched": False, "note": ""}
