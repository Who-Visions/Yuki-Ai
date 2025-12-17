#!/usr/bin/env python3
"""
🦊 Yuki A2A Trigger Script
==========================
Demonstrates how to "trigger" the Yuki agent using Python and the A2A Protocol.
This script sends a structured A2A message to Yuki's cloud endpoint.

Usage:
    python trigger_yuki.py "[Your Message]"
"""

import asyncio
import json
import sys
import uuid
import httpx
from datetime import datetime

# Configuration
YUKI_URL = "https://yuki-ai-914641083224.us-central1.run.app"
AGENT_NAME = "TriggerScript"

async def trigger_yuki(message_text: str):
    """
    Triggers Yuki by sending a message via the A2A protocol.
    """
    print(f"\n🚀 Triggering Yuki at: {YUKI_URL}")
    print(f"📝 Message: {message_text}\n")

    # 1. Construct the A2A Message Payload
    # Using 'v1/message:send' - The standard A2A endpoint
    payload = {
        "message": {
            "role": "user",
            "parts": [
                {
                    "kind": "text", 
                    "text": message_text
                }
            ],
            "messageId": str(uuid.uuid4()),
            "contextId": str(uuid.uuid4()) # New context for this trigger
        }
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # 2. Send the POST request
            response = await client.post(
                f"{YUKI_URL}/v1/message:send",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            # 3. Process Response
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Success (Status {response.status_code})")
                
                # Extract the text from the A2A response format
                if "result" in data and "parts" in data["result"]:
                    for part in data["result"]["parts"]:
                        if part.get("kind") == "text":
                            print("\n🦊 Yuki Says:\n" + "─" * 20)
                            print(part.get("text"))
                            print("─" * 20 + "\n")
                else:
                    print("⚠️  Received raw response:", data)
            
            else:
                print(f"❌ Failed (Status {response.status_code})")
                print("Response:", response.text)

        except Exception as e:
            print(f"💥 Error: {str(e)}")

def main():
    # Get message from args or use default
    msg = "Kon kon! Status report?"
    if len(sys.argv) > 1:
        msg = " ".join(sys.argv[1:])
    
    asyncio.run(trigger_yuki(msg))

if __name__ == "__main__":
    main()
