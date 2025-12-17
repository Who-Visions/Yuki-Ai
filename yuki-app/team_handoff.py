#!/usr/bin/env python3
"""
🎹 Yuki Team Handoff Trigger
============================
Automates the handoff between the three development personas:
- 🖤 Ebony (Backend/V8/API)
- 🤍 Ivory (UI/UX/Frontend)
- 🩵 Cyan (Testing/Polish/Infrastructure)

Usage:
    python team_handoff.py status          # View current team status
    python team_handoff.py --to cyan       # Trigger handoff to Cyan
    python team_handoff.py --to ivory      # Trigger handoff to Ivory
    python team_handoff.py --to ebony      # Trigger handoff to Ebony
"""

import os
import sys
import argparse
import datetime
import re

# Configuration
HANDOFF_FILE = "TEAM_HANDOFF.md"

# Persona Definitions
PERSONAS = {
    "ebony": {
        "emoji": "🖤",
        "role": "Backend & V8 Integration",
        "description": "API, Database, V8 Pipeline, Facial IP",
        "greeting": "Ebony online. Systems nominal.",
        "color": "\033[90m" # Gray
    },
    "ivory": {
        "emoji": "🤍",
        "role": "UI/UX & Frontend",
        "description": "React Native, Animations, User Flow, Design",
        "greeting": "Ivory here. Let's make it beautiful.",
        "color": "\033[97m" # White
    },
    "cyan": {
        "emoji": "🩵",
        "role": "Polish & Infrastructure",
        "description": "Testing, Refactoring, DevOps, Stability",
        "greeting": "Cyan reporting. Optimizing parameters.",
        "color": "\033[96m" # Cyan
    }
}

RESET_COLOR = "\033[0m"

def load_handoff_file():
    if not os.path.exists(HANDOFF_FILE):
        print(f"❌ Error: {HANDOFF_FILE} not found.")
        sys.exit(1)
    with open(HANDOFF_FILE, "r", encoding="utf-8") as f:
        return f.read()

def parse_status(content):
    """Simple parsing of the markdown to find checked items."""
    stats = {}
    for key, data in PERSONAS.items():
        # Find section
        match = re.search(f"## {data['emoji']} (.*?)(\n---|\n$)", content, re.DOTALL)
        if match:
            section = match.group(1)
            # Count checks
            completed = section.count("✅")
            pending = section.count("- ") - completed
            stats[key] = {"completed": completed, "pending": pending}
    return stats

def print_status(content):
    stats = parse_status(content)
    print("\n🎹 Yuki Team Status Report")
    print("==========================")
    
    for key, data in PERSONAS.items():
        stat = stats.get(key, {"completed": 0, "pending": 0})
        color = data["color"]
        print(f"{color}{data['emoji']} {key.capitalize()}: {stat['completed']} Completed / {stat['pending']} Pending{RESET_COLOR}")

    print("\nTo trigger a handoff, run: python team_handoff.py --to [name]")

def generate_handoff_prompt(target_persona, from_persona="auto"):
    """Generates the prompt for the user to paste."""
    
    target = PERSONAS.get(target_persona)
    if not target:
        return "Error: Unknown persona"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    prompt = f"""
*** 🚨 HANDOFF TRIGGERED ***
Please copy and paste the following block into your chat to switch contexts:

```text
[SYSTEM: ACTIVATE PERSONA {target_persona.upper()}]
Timestamp: {timestamp}
Target: {target['emoji']} {target_persona.capitalize()} ({target['role']})

Directives:
1. Acknowledge handoff.
2. Review 'TEAM_HANDOFF.md' for latest task status.
3. Current Objective: {target['description']}
4. Resume pending tasks from your zone.

Greeting: "{target['greeting']}"
```
"""
    return prompt

def main():
    parser = argparse.ArgumentParser(description="Trigger Yuki Team Handoffs")
    parser.add_argument("action", nargs="?", default="status", help="Action: status")
    parser.add_argument("--to", help="Target persona to switch to")
    
    args = parser.parse_args()

    content = load_handoff_file()

    if args.to:
        target = args.to.lower()
        if target in PERSONAS:
            print(f"\n{PERSONAS[target]['color']}Initiating Handoff Protocol...{RESET_COLOR}")
            print(generate_handoff_prompt(target))
            
            # Here we could theoretically write to the file to mark "Active", 
            # but the Prompt is the real trigger.
        else:
            print(f"❌ Unknown persona: {target}")
            print("Available: ebony, ivory, cyan")
    else:
        print_status(content)

if __name__ == "__main__":
    main()
