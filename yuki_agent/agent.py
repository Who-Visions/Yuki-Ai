import datetime
import re

def get_current_time() -> str:
    """Returns the current time in UTC."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together."""
    return a + b

class YukiAgent:
    """Simple agent that responds to queries and uses tools."""
    
    def query(self, input: dict) -> dict:
        """
        Query the agent with a user message.
        """
        # Extract user input
        if isinstance(input, dict):
            if 'messages' in input:
                user_input = input['messages'][-1]['content'] if input['messages'] else ''
            elif 'input' in input:
                user_input = input['input']
            else:
                user_input = str(input)
        else:
            user_input = str(input)
        
        user_input_lower = user_input.lower()
        
        # Check if asking for time
        if 'time' in user_input_lower:
            result = f"🕐 The current time is: {get_current_time()}"
        
        # Check if asking for math
        elif '+' in user_input or 'add' in user_input_lower or any(word in user_input_lower for word in ['sum', 'plus', 'math']):
            try:
                # Try to extract two numbers
                numbers = re.findall(r'-?\d+\.?\d*', user_input)
                if len(numbers) >= 2:
                    a, b = float(numbers[0]), float(numbers[1])
                    result = f"🧮 The sum of {a} and {b} is: **{add_numbers(a, b)}**"
                else:
                    result = "I can add two numbers! Try: 'What is 50 + 75?' or 'Add 123 and 456'"
            except Exception as e:
                result = f"I can add numbers, but I had trouble parsing that. Try: '50 + 25' (Error: {e})"
        
        # Default greeting/help
        else:
            result = f"👋 Hello! You said: '{user_input}'\n\nI can help with:\n• ⏰ Time: Ask 'What time is it?'\n• ➕ Math: Ask 'What is 50 + 25?'"
        
        return {'output': result}
    
    def set_up(self):
        """Initialize if needed."""
        pass

# Vertex AI looks for 'root_agent'
root_agent = YukiAgent()
