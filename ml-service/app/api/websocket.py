"""
WebSocket endpoint that streams live alerts to the dashboard.
This replaces 5-second polling with instant push updates via Redis Pub/Sub. [web:81]
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.storage.redis_client import redis_client, ALERT_CHANNEL
import asyncio
import json

router = APIRouter()

@router.websocket("/stream/alerts")
async def stream_alerts(websocket: WebSocket):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    pubsub.subscribe(ALERT_CHANNEL)

    try:
        while True:
            # get_message with timeout keeps this loop non-blocking so the
            # websocket can also detect disconnects promptly.
            message = pubsub.get_message(timeout=1.0)
            if message and message["type"] == "message":
                await websocket.send_text(message["data"])
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pubsub.unsubscribe(ALERT_CHANNEL)
