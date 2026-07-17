"""
Prisma client factory.

Keeping a single async Prisma client at module scope is fragile here because
the FastAPI test client creates and tears down event loops during tests.
Creating a fresh connected client per request is slower but much more robust
for this project and for short-lived container workers.
"""

from prisma import Prisma

async def get_prisma()-> Prisma:
    prisma = Prisma()
    await prisma.connect()
    return prisma
