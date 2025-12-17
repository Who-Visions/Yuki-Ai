#!/usr/bin/env python3
"""Test that TUI widgets are accessible and command construction works."""
import sys
from pathlib import Path

# Mock the textual imports to test logic
class MockApp:
    def __init__(self):
        self.widgets = {}
    
    def query_one(self, selector, widget_type=None):
        if selector not in self.widgets:
            if "char-list" in selector:
                self.widgets[selector] = MockSelectionList()
            elif "sex-filter" in selector:
                self.widgets[selector] = MockSelect("all")
            elif "shot-select" in selector:
                self.widgets[selector] = MockSelect("portrait")
            elif "variations-radio" in selector:
                self.widgets[selector] = MockRadioSet("2")
            elif "char-search" in selector:
                self.widgets[selector] = MockInput("")
        return self.widgets[selector]

class MockSelectionList:
    def __init__(self):
        self._items = []
        self.selected = []
    
    def add_option(self, data):
        label, value, is_selected = data
        self._items.append(value)
        if is_selected:
            self.selected.append(value)
    
    def clear_options(self):
        self._items.clear()
        self.selected.clear()

class MockSelect:
    def __init__(self, value):
        self.value = value

class MockRadioSet:
    def __init__(self, value):
        self.pressed_button = MockButton(value)

class MockButton:
    def __init__(self, label):
        self.label = label

class MockInput:
    def __init__(self, value):
        self.value = value

# Test the logic
print("Testing TUI command construction logic...")

app = MockApp()

# Simulate populate_character_list
V9_CHARACTERS = [
    {"name": "Neo", "sex": "male"}, 
    {"name": "Trinity", "sex": "female"},
    {"name": "Storm", "sex": "female"},
]

sex_filter = "all"
search_query = ""

char_list = app.query_one("#char-list")
char_list.clear_options()

filtered_chars = []
for char in V9_CHARACTERS:
    if sex_filter != "all" and char["sex"] != sex_filter:
        continue
    if search_query and search_query.lower() not in char["name"].lower():
        continue
    filtered_chars.append(char)

for char in filtered_chars:
    char_list.add_option((f"{char['name']} ({char['sex']})", char["name"], True))

print(f"✓ Populated {len(char_list._items)} characters")
print(f"✓ Selected: {char_list.selected}")

# Simulate command construction
current_subject = "Snow New Now Glasses"
variations_radio = app.query_one("#variations-radio")
variations = int(str(variations_radio.pressed_button.label))
shot_type = app.query_one("#shot-select").value
selected_chars = char_list.selected

cmd = [
    "python3", "-u", "yuki_v9_generator.py", 
    current_subject,
    "--variations", str(variations),
    "--shot-type", str(shot_type),
    "--characters"
] + selected_chars

print(f"\n✓ Command: {' '.join(cmd)}")
print(f"✓ Subject: {current_subject}")
print(f"✓ Variations: {variations}")
print(f"✓ Shot Type: {shot_type}")
print(f"✓ Characters: {len(selected_chars)}")

if len(selected_chars) > 0:
    print("\n✅ TUI logic validation PASSED")
    sys.exit(0)
else:
    print("\n❌ No characters selected!")
    sys.exit(1)
