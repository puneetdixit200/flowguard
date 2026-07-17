'''
reddis connecion +pub/sub helper

Publisher side: alert_service.py calls publish_alert() whenever a new alert is created.
Subscriber side: websocket.py listens and pushes to connected dashboard clients. [web:83]
'''

import json
import os
import redis

#decode_response is True means we get the plian strings back intread of bytes

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)

ALERT_CHANNEL ="flowguard:alerts"

def publish_alert(alert:dict):
    '''fire-and-forget bradcast - any connected subscribers will receive the alert'''
    redis_client.publish(ALERT_CHANNEL, json.dumps(alert,default=str))

def cache_recent_alert_count():
    '''simple redis counter- demostrate redis as chache'''
    redis_client.incr("flowguard:alert_count")

def get_cached_alert_count()-> int:
    val = redis_client.get("flowguard:alert_count")
    return int(val) if val else 0
