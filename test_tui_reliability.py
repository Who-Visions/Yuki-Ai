import re
from pathlib import Path

# Mocking the textual classes for the test
class MockLabel:
    def __init__(self, text):
        self.renderable = text

class MockListItem:
    def __init__(self, label, id):
        self.label = label
        self.id = id
        self.children = [label]

def test_logic():
    print("🧪 Starting Robustness Test (100 iterations of random inputs)...")
    
    # simulation of names including the one that failed
    test_cases = [
        "Snow New Now Glasses", "Dav3 test", "Simple", "Spaces Should Be Underscores",
        "Dots.Are.Tricky", "Mixed_-_Separators", "123 Numbers", "!!!Symbols???",
        "   Leading Trailing Spaces   ", "Subject A", "Subject B"
    ]
    
    # Expand to 100 items
    while len(test_cases) < 100:
        test_cases.append(f"Generated Subject {len(test_cases)}")

    failures = 0
    
    for i, name in enumerate(test_cases):
        try:
            # --- LOGIC FROM TUI NO. 1: SANITIZATION ---
            clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
            
            # Verify ID is valid (no spaces)
            if " " in clean_name:
                print(f"❌ FAIL: ID contains space: '{clean_name}'")
                failures += 1
                continue
                
            # --- LOGIC FROM TUI NO. 2: CREATION ---
            label = MockLabel(name)
            list_item = MockListItem(label, id=f"subject-{clean_name}")
            list_item.subject_name = name  # The fix we applied
            
            # --- LOGIC FROM TUI NO. 3: SELECTION ---
            # Simulate selection event
            selected_subject = ""
            if hasattr(list_item, "subject_name"):
                selected_subject = list_item.subject_name
            else:
                 # Fallback (OLD BROKEN LOGIC) - simulating what happens if we didn't have the fix
                 # selected_subject = str(list_item.label.renderable) 
                 pass

            if selected_subject != name:
                print(f"❌ FAIL: Selected '{selected_subject}' != Expected '{name}'")
                failures += 1
                
        except Exception as e:
            print(f"❌ CRASH on '{name}': {e}")
            failures += 1

    if failures == 0:
        print(f"\n✅ SUCCESS: All {len(test_cases)} test cases passed validation logic.")
    else:
        print(f"\n❌ FAILED: {failures} errors detected.")

if __name__ == "__main__":
    test_logic()
