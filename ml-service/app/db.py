"""
Single shared Prisma client instance — connecting once at startup avoids
opening a new database connection on every request.
"""

from prisma import Prisma

_prisma_client =None
async def get_prisme()-> Prisma:
    global _prisma_client
    if _prisma_client is None:
        _prisma_client = Prisma()
        await _prisma_client.connect()
    return _prisma_client
