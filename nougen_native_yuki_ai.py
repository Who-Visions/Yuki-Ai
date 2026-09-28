# Auto-generated NouGen Substrate & MsgNode Native Integration
import os, sys, json, urllib.request, time

MSGNODE_URL = "http://127.0.0.1:8766/api/send"

def nougen_query(topic):
    import subprocess
    res = subprocess.run(["python3", "/Users/kushboygroup/.gemini/Who_Mac_Mini_indexer.py", "--query", topic], capture_output=True, text=True)
    return res.stdout.strip()

def nougen_send(sender, target, msg, shards=None):
    payload = {"sender": sender, "target": target, "message": msg, "context_shards": shards or []}
    try:
        req = urllib.request.Request(MSGNODE_URL, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=3) as resp: pass
    except Exception:
        pass

# Native identity: Yuki-Ai
