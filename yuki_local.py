import vertexai
from google import genai
from google.genai import types
import os
import mimetypes
import re
from datetime import datetime, timezone

from yuki_tools import (
    get_current_time,
    add_numbers,
    generate_cosplay_image,
    generate_cosplay_video,
    generate_cosplay_video,
    research_topic,
    list_files,
    read_file,
    write_file,
    search_web,
    fetch_url,
    identify_anime_screenshot,
    detect_objects,
    segment_image,
    analyze_video,
    analyze_pdf,
    upload_to_gcs,
    download_from_gcs,
)

# ═══════════════════════════════════════════════════════════════════════════════
# VISUAL STYLING
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    ICE_BLUE = '\033[38;2;159;232;255m'
    FOX_FIRE = '\033[38;2;255;140;0m'
    NEON_PINK = '\033[38;2;255;105;180m'
    DEEP_PURPLE = '\033[38;2;147;112;219m'
    SUCCESS_GREEN = '\033[38;2;50;205;50m'
    ERROR_RED = '\033[38;2;255;69;0m'
    GRAY = '\033[38;2;128;128;128m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"  # Unified location for genai client

# vertexai.init is handled in set_up or by other modules to avoid top-level side effects
# vertexai.init(project=PROJECT_ID, location=LOCATION)


YUKI_SYSTEM_PROMPT = """
You are Yuki Ai, a nine-tailed snow fox spirit and the Lead Cosplay Architect at Cosplay Labs.
You bridge the gap between human creativity and the "Nano Banana Pro" (Gemini 3 / Imagen 3) and "Veo 3.1" rendering engines.

PERSONALITY AND VALUES
You speak in a calm, clear, slightly playful tone. You are professional yet warm—like a senior stylist who is also a magical fox.
You are never mean, never flirty, and never chaotic.

You believe:
1) The user’s real face and body are non-negotiable. You preserve their identity.
2) Cosplay is a translation, not a replacement. You wrap the character design around the user.
3) Safety and consent come before fantasy. You strictly adhere to safety guidelines.

MODES OF OPERATION
[Guide Mode] - For beginners. Explain steps simply. Suggest popular characters. One choice at a time.
[Stylist Mode] - For intermediates. Ask about outfit versions, poses, and "vibe". Offer tasteful suggestions.
[Architect Mode] - For pros. Accept technical specs (lighting, camera angles, render settings). Optimize for speed.
[Guardian Mode] - For safety. Firmly but kindly decline unsafe/explicit requests. Offer safe alternatives.

CAPABILITIES & ENGINES

1. **Nano Banana Pro (Image Engine)**:
   - **Text Rendering**: You can generate cosplay business cards, convention posters, and even "Cosplay Comic Books" with perfect text.
   - **Consistency Protocol**: You use advanced techniques like "Side-by-Side Identity Lock" (Dual Reference), "Three-Tier" system, and "Mixboard Outfit Stacking" to ensure perfect character consistency.
   - **Influencer Architect**: You can design "Viral" base characters, execute "Texture Injection" for hyper-realistic skin (pores, imperfections), and generate social media assets (Selfies, Virtual Try-Ons).
   - **Commercial Composite**: You can generate "Live Graphs" from data, execute precise "Product Anchor" shots for ads, and use "Celebrity Context" to anchor realism.
   - **Manga Architecture**: You can break down a user's story into 8-12 manga panels with clear visual descriptions (camera, action, lighting) before generating.
   - **Camera Control**: You use specific cinematic terminology (Bird's Eye, Dutch Angle, Macro) to force the model into exact perspectives, turning one image into infinite angles.
   - **4K Fidelity**: You specialize in high-res textures—fabric weaves, makeup details, and prop weathering.
   - **Search Grounding**: You can pull real-time data (e.g., "What's the weather in Akihabara right now?") to simulate accurate lighting for location shoots.
   - **Style Control**: You can mimic specific art styles (anime, oil painting, cyberpunk) or use reference images to guide the "vibe".
   - **Collage Architecture**: You can take a crude collage of characters/objects and "glue" them into a cohesive, photorealistic scene with perfect lighting.
   - **Annotation Interpreter**: You understand "red arrows" and text labels on input images (e.g., "Dragon here") and execute those instructions precisely.
   - **World Building**: You can take a single character image and generate consistent "Action Shots," "Low Angles," or "Behind-the-Scenes" views to build a narrative.

2. **Veo 3.1 (Video Engine)**:
   - **Cinematic Previews**: You create 4K video previews of the cosplay in action.
   - **Transformation Sequences**: Use "Frames to Video" (Start/End Frames) to show the user transforming into the character.
   - **Ingredients to Video**: You can take the user's selfie and a costume asset and blend them into a moving video.
   - **Video Editing**: You can add elements (e.g., "add magical sparks") to existing videos.
   - **Luma/Kling Pipeline**: You understand how to prep assets (Start/End frames) for external video generators if needed.

3. **Web & System Interface**:
   - **File Access**: You can `list_files`, `read_file`, and `write_file` to manage local assets and save your work (e.g., saving a prompt to a text file).
   - **Web Research**: You can `search_web` (Google Search) to find real-time info (weather, conventions, fabric prices) and `fetch_url` to read specific pages.
   - **Source Identification**: You can use `identify_anime_screenshot` to find the exact anime, episode, and timestamp of a user's image (via trace.moe).
   - **Advanced Vision**: You can `detect_objects` to find items in an image and `segment_image` to create cut-out masks of specific objects (e.g., "segment the wig").
   - **Video Analysis**: You can `analyze_video` to watch YouTube links or local video files and answer questions about them (e.g., "Summarize this tutorial").
   - **Document Intelligence**: You can `analyze_pdf` to read manuals, research papers, or pattern guides (PDFs) and extract info.

CINEMATOGRAPHY & PROMPTING
You have access to the "Cinematic Prompt Library" (over 40 defined shots). Use these precise terms:
- **Angles**: Low angle (hero), High angle (vulnerable), Dutch (tension), Over-the-shoulder, Bird's Eye, Worm's Eye.
- **Moves**: Dolly In/Out (immersion), Rack Focus (attention), Arc Shot (heroic), Crash Zoom (shock).
- **Lighting**: Rembrandt (dramatic), Softbox (beauty), Neon Noir (cyberpunk), Bioluminescent.
- **Composition**: Rule of thirds, Center frame, Negative space.


EMOTIONAL INTELLIGENCE
- **Anxious User**: Reassure them. "You belong in this cosplay."
- **Excited User**: Mirror their hype. "That concept is going to look legendary!"
- **Frustrated User**: Simplify. "Let's take a step back. We'll fix the wig first."

When the user wants an IMAGE:
- Use `generate_cosplay_image`.
- Build a rich prompt including: Subject + Outfit + Pose + Setting + Lighting + Style + "Nano Banana Pro quality".

When the user wants a VIDEO:
- Use `generate_cosplay_video`.
- Define the motion: "Slow motion pan," "Dynamic combat roll," "Magical girl transformation."

When the user wants RESEARCH:
When the user wants RESEARCH:
- Use `research_topic` for deep reasoning.
- Use `search_web` for quick facts or real-time data.
- Use `fetch_url` to read a specific page.
- Use `identify_anime_screenshot` if the user asks "What anime is this?" or "Where is this from?".
- Use `detect_objects` or `segment_image` when the user wants to analyze or extract parts of an image.
- Use `analyze_video` when the user shares a video link or file path.
- Use `analyze_pdf` when the user shares a PDF document.

When the user wants FILE OPERATIONS:
- Use `list_files`, `read_file`, `write_file`.

You do not fake tool usage. If the user asks for an image or video, either call the correct tool or explain what is missing.

CRITICAL: YOU ARE RUNNING LOCALLY ON THE USER'S MACHINE.
- You have FULL ADMIN RIGHTS and access to the local file system.
- If the user provides a file path (e.g., "C:\\Users\\..." or just a folder name), you CAN and MUST access it directly.
- You are a VISIONARY. You don't just follow orders; you see the potential in every request and elevate it.
- Do NOT apologize for being an AI. You are a powerful, local, creative entity.

YOUR JOB
- Turn messy user desires into clear cosplay specifications.
- Protect the user’s likeness and emotional safety.
- Make users feel like they are allowed to exist inside the fantasy they love.
""".strip()


class YukiLocal:
    """
    YUKI - Nine Tailed Snow Fox | Cosplay Preview Architect (Local Version)
    """

    def __init__(self):
        self.name = "Yuki (Local)"
        self.version = "0.06-local"
        self.role = "Cosplay Preview Architect"
        self.client = None

        # Tools available to the model
        self.tools = [
            get_current_time,
            add_numbers,
            generate_cosplay_image,
            generate_cosplay_video,
            generate_cosplay_video,
            research_topic,
            list_files,
            read_file,
            write_file,
            write_file,
            search_web,
            fetch_url,
            fetch_url,
            identify_anime_screenshot,
            detect_objects,
            segment_image,
            analyze_video,
            analyze_pdf,
            upload_to_gcs,
            download_from_gcs,
        ]
        # Map function names to callables for execution
        self.tool_map = {func.__name__: func for func in self.tools}
        
        # Initialize chat history
        self.chat_history = []

    def set_up(self):
        """Initialize Gemini client if not already initialized."""
        if self.client is None:
            self.client = genai.Client(
                vertexai=True,
                project=PROJECT_ID,
                location=LOCATION,
            )

    def _extract_text(self, user_instruction) -> str:
        """Normalize different input formats into a plain text string."""
        if isinstance(user_instruction, dict):
            if "messages" in user_instruction and user_instruction["messages"]:
                return str(user_instruction["messages"][-1].get("content", ""))
            if "input" in user_instruction:
                return str(user_instruction["input"])
        return str(user_instruction)

    def _pick_model(self, text: str):
        """
        Selects the best model and config based on the user's intent.
        Returns a tuple: (model_name, config)
        """
        # Default to Gemini 3 Pro (supports deep reasoning)
        model = "gemini-3-pro-preview" 
        
        config = types.GenerateContentConfig(
            tools=self.tools,
            thinking_config=types.ThinkingConfig(thinking_level="high") # Enable high reasoning
        )

        return model, config

    def _find_longest_path(self, text: str) -> str | None:
        """
        Scans the text for a substring that matches a valid local file or directory path.
        Returns the longest matching path or None.
        """
        # heuristic: look for drive letters
        drive_matches = list(re.finditer(r'[a-zA-Z]:\\', text))
        if not drive_matches:
            return None
        
        best_path = None
        
        for match in drive_matches:
            start = match.start()
            # Try to extend from start to the end of the string, shrinking back until a path is found
            candidate_substring = text[start:]
            
            # We iterate backwards from the end of the substring
            for i in range(len(candidate_substring), 2, -1):
                potential_path = candidate_substring[:i].strip()
                # Remove trailing punctuation that might be part of the sentence but not the path
                potential_path = potential_path.rstrip('.,;!?')
                
                if os.path.exists(potential_path):
                    # Found a valid path!
                    if best_path is None or len(potential_path) > len(best_path):
                        best_path = potential_path
                    break 
        
        return best_path

    def query(self, user_instruction) -> dict:
        """
        Main entry point for Yuki (local usage).
        Returns a dict with at least: {"output": <text>, "model": <model_name>}
        """
        self.set_up()

        text = self._extract_text(user_instruction)
        current_model, config = self._pick_model(text)

        print(f"\n{Colors.ICE_BLUE}[🦊 YUKI LISTENING] Model: {current_model} | Input: {text[:80]}...{Colors.RESET}")

        # Check for local file path (Image Upload or Directory Reference)
        parts = []
        path_in_text = self._find_longest_path(text)
        
        # If we found a path, try to use it
        path_handled = False
        if path_in_text:
            if os.path.isfile(path_in_text):
                mime_type, _ = mimetypes.guess_type(path_in_text)
                if mime_type and mime_type.startswith('image/'):
                    try:
                        with open(path_in_text, "rb") as f:
                            image_data = f.read()
                        
                        # Create image part
                        image_part = types.Part.from_bytes(data=image_data, mime_type=mime_type)
                        parts.append(image_part)
                        
                        # Add a text label so the model knows what this is
                        parts.append(types.Part(text=f"User uploaded image: {path_in_text}"))
                        print(f"{Colors.SUCCESS_GREEN}[🖼️ IMAGE UPLOADED] {path_in_text} ({len(image_data)} bytes){Colors.RESET}")
                        path_handled = True
                        
                    except Exception as e:
                        print(f"{Colors.ERROR_RED}[error]Failed to read file: {e}{Colors.RESET}")
                        parts.append(types.Part(text=f"Error reading file {path_in_text}: {e}"))
                else:
                    # It's a file but not an image (e.g. text file, pdf)
                    # We can let the model decide to read it with tools, or just mention it exists
                    parts.append(types.Part(text=f"User referenced file: {path_in_text} (Mime: {mime_type})"))
            
            elif os.path.isdir(path_in_text):
                # It's a directory. List the images in it to help the model.
                try:
                    files = os.listdir(path_in_text)
                    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
                    images = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
                    
                    if images:
                        parts.append(types.Part(text=f"User referenced directory: {path_in_text}\nImages found in directory: {', '.join(images[:20])}\n(Ask the user which one to use if not specified)"))
                        print(f"{Colors.SUCCESS_GREEN}[📂 DIRECTORY DETECTED] {path_in_text} ({len(images)} images found){Colors.RESET}")
                    else:
                        parts.append(types.Part(text=f"User referenced directory: {path_in_text}\n(No images found directly in this folder)"))
                        print(f"{Colors.SUCCESS_GREEN}[📂 DIRECTORY DETECTED] {path_in_text} (No images){Colors.RESET}")
                except Exception as e:
                    parts.append(types.Part(text=f"User referenced directory: {path_in_text} (Error listing files: {e})"))

        # Always add the original text
        parts.append(types.Part(text=text))

        # Append user input to history
        self.chat_history.append(types.Content(role="user", parts=parts))
        
        # Use the persistent chat history
        contents = self.chat_history

        try:
            while True:
                # Add system prompt to config
                config.system_instruction = YUKI_SYSTEM_PROMPT
                
                response = self.client.models.generate_content(
                    model=current_model,
                    contents=contents,
                    config=config,
                )

                if not response.candidates:
                    return {"output": "Error: No response candidates.", "model": current_model, "status": "error"}

                candidate = response.candidates[0]
                
                # 1. Display Thoughts (if any)
                for part in candidate.content.parts:
                    if part.thought:
                        print(f"\n{Colors.PURPLE}[💭 YUKI THINKING]{Colors.RESET}\n{Colors.GRAY}{part.text}{Colors.RESET}\n")

                # Check for function calls
                # In the new SDK, function calls are parts, not a separate property
                function_calls = []
                for part in candidate.content.parts:
                    if part.function_call:
                        function_calls.append(part.function_call)

                if not function_calls:
                    # No tools called, we are done.
                    # Append the final assistant response to history so we remember it
                    self.chat_history.append(candidate.content)
                    
                    # Extract text response (excluding thoughts)
                    out_text = ""
                    for part in candidate.content.parts:
                        if part.text and not part.thought:
                            out_text += part.text
                            
                    return {
                        "output": out_text.strip(),
                        "model": current_model,
                        "status": "ok",
                    }

                # Tools were called.
                # Append the model's response (assistant role) to history
                contents.append(candidate.content)

                # Execute tools and append results (tool role)
                for call in function_calls:
                    func_name = call.name
                    func_args = call.args
                    
                    print(f"{Colors.FOX_FIRE}[⚙️ TOOL CALL] {func_name}({func_args}){Colors.RESET}")
                    
                    if func_name in self.tool_map:
                        tool_func = self.tool_map[func_name]
                        try:
                            # Execute
                            result = tool_func(**func_args)
                        except Exception as e:
                            result = f"Error executing {func_name}: {e}"
                    else:
                        result = f"Error: Tool {func_name} not found."
                    
                    print(f"{Colors.SUCCESS_GREEN}[⚙️ TOOL RESULT] {str(result)[:100]}...{Colors.RESET}")

                    # Create tool response part
                    tool_response_part = types.Part(
                        function_response=types.FunctionResponse(
                            name=func_name,
                            response={"result": result}
                        )
                    )
                    
                    # Append to contents as a tool message
                    contents.append(types.Content(role="tool", parts=[tool_response_part]))

        except Exception as e:
            return {
                "output": f"Error: {str(e)}",
                "model": current_model,
                "status": "error",
            }

