"""
Pulls real scale numbers straight from your running Postgres database
via Prisma — total flows processed, total alerts, severity breakdown,
threat intel matches. These are your "system scale" resume numbers.
"""
import asyncio
from app.db import get_prisma

async def main():
    prisma = await get_prisma()

    total_flows = await prisma.flow.count()
    total_alerts = await prisma.alert.count()

    critical = await prisma.alert.count(where={"severity": "critical"})
    high = await prisma.alert.count(where={"severity": "high"})
    medium = await prisma.alert.count(where={"severity": "medium"})
    low = await prisma.alert.count(where={"severity": "low"})

    threat_matches = await prisma.alert.count(where={"threatIntelMatch": True})

    print("===== SYSTEM SCALE METRICS =====")
    print(f"Total flows processed: {total_flows}")
    print(f"Total alerts generated: {total_alerts}")
    print(f"  Critical: {critical} | High: {high} | Medium: {medium} | Low: {low}")
    print(f"Threat intel correlated alerts: {threat_matches}")
    if total_flows > 0:
        print(f"Alert rate: {(total_alerts/total_flows)*100:.2f}% of flows flagged")

asyncio.run(main())
