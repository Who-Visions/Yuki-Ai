#!/usr/bin/env python3
"""
Quick test runner for Yuki Agent (without deploying).
Use this instead of deploy_yuki.py when you just want to test!
"""

import vertexai
from vertexai.preview import reasoning_engines
import json

# Latest deployment info
YUKI_RESOURCE = "projects/914641083224/locations/us-central1/reasoningEngines/8735413174494298112"
DEPLOYED_AT = "2025-12-01 09:25:00"

BANNER = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⡈⢯⡉⠓⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠻⣉⠹⠷⠀⠀⠀⠙⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⠞⠀⠀⠀⠀⠀⠀⠀⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⢈⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡇⠀⠹⠝⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⠞⠀⣀⣠⣤⣤⠄⠀⠀⢠⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠚⠢⠼⠿⠟⢛⣾⠃⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡴⣻⠃⠀⠀⠀⠀⢸⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⢻⡷⠁⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢰⢽⡟⠁⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢾⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⢧⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⣷⣱⡀⠀⠀⠀⠀⣸⠀⠀⠀⠈⢻⣦⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣷⡙⣆⠀⠀⣾⠃⠀⠀⠀⠀⠈⢽⡆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠸⡇⢷⡏⠃⢠⠇⠀⠀⣀⠄⠀⠀⠀⣿⡖⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡇⢨⠇⠀⡼⢀⠔⠊⠀⠀⠀⠀⠀⠘⣯⣄⢀⠀
⠀⠀⠀⠀⠀⠀⠀⢰⡇⣼⡀⣰⣷⠁⠀⠀⠀⠀⠀⠀⠀⠀⣇⢻⣧⡄
⠀⠀⠀⠀⣀⣮⣿⣿⣿⣿⣯⡭⢉⠟⠛⠳⢤⣄⣀⣀⣀⣀⡴⢠⠨⢻⣿
⠀⠀⢀⣾⣿⣿⣿⣿⣿⢏⠓⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢨⣿
⠀⣰⣿⣿⣿⣿⣿⣿⣿⡱⠌⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢭⣾⠏
⣰⡿⠟⠋⠛⢿⣿⣿⣿⣊⠡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣼⡿⠋⠀
⠋⠁⠀⠀⠀⠀⠈⠑⠿⢶⣄⣀⣀⣀⣀⣀⣄⣤⡶⠿⠟⠋⠁⠀⠀⠀⠀

      [ YUKI_AI v0.5 ] Nine Tailed Snow Fox
      Cosplay Preview Agent
"""

print(BANNER)
print("=" * 70)
print(f"  Resource: ...{YUKI_RESOURCE[-10:]}")
print(f"  Deployed: {DEPLOYED_AT}")
print()

try:
    # Initialize
    vertexai.init(project="gifted-cooler-479623-r7", location="us-central1")
    
    # Load agent
    agent = reasoning_engines.ReasoningEngine(YUKI_RESOURCE)
    
    # Get test query from user or use default
    print("Enter your query (or press ENTER for default test):")
    user_query = input("> ").strip()
    
    if not user_query:
        user_query = "What time is it right now?"
    
    print(f"\n🧪 Testing: '{user_query}'")
    print()
    
    # Query the agent
    response = agent.query(user_instruction=user_query)
    
    print("✅ Response:")
    print(json.dumps(response, indent=2))
    print()
    
    if response and 'output' in response:
        print(f"📝 Yuki: {response['output']}")
    
    print("\n" + "=" * 70)
    print("  ✓ TEST COMPLETE")
    print("=" * 70)
    
except Exception as e:
    print('❌ Error:', e)
    import traceback
    traceback.print_exc()
