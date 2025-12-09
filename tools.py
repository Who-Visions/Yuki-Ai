import datetime
import os
from google import genai
from google.genai import types
import base64
import urllib.request
from html.parser import HTMLParser
import re
from google.cloud import storage
import json
import io
from PIL import Image, ImageDraw
import numpy as np
import wave

def get_current_time() -> str:
    """Returns the current time in UTC."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together."""
    return a + b

def generate_cosplay_image(prompt: str, aspect_ratio: str = "3:4", resolution: str = "1024x1024", use_search: bool = False, model: str = "gemini-3-pro-image-preview", reference_image_paths: list = None, number_of_images: int = 1) -> str:
    """
    Generates a cosplay preview image using Google's GenAI models (Nano Banana Pro / Imagen 3).
    
    Args:
        prompt: The detailed image generation prompt.
        aspect_ratio: The aspect ratio (e.g., "1:1", "3:4", "4:3", "16:9"). Defaults to "3:4".
        resolution: The resolution (e.g., "1K", "2K", "4K" for Gemini 3; "1024x1024" for Imagen). Defaults to "1024x1024".
        use_search: Whether to use Google Search grounding (Gemini 3 only).
        model: The model to use. Defaults to 'gemini-3-pro-image-preview'.
        reference_image_paths: Optional list of paths to local reference images (Gemini 3 only).
        number_of_images: Number of variations to generate (1, 2, or 4). Defaults to 1.
    
    Returns:
        str: The file path(s) of the saved image(s), or an error message.
    """
    print(f"\n[🎨 GENERATING IMAGE] Model: {model}")
    print(f"    Prompt: {prompt[:50]}...")
    print(f"    Aspect Ratio: {aspect_ratio} | Resolution: {resolution} | Search: {use_search} | Count: {number_of_images}")
    if reference_image_paths:
        print(f"    Reference Images: {len(reference_image_paths)} files")
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_files = []

    try:
        # Determine location
        location = "us-central1"
        if "gemini-3" in model:
            location = "global"
            
        client = genai.Client(vertexai=True, project="gifted-cooler-479623-r7", location=location)
        
        if "gemini" in model:
            # Gemini 3.0 Image Generation (Nano Banana Pro)
            
            # Add search tool if requested
            tools_list = []
            if use_search:
                tools_list.append(types.Tool(google_search=types.GoogleSearch()))
            
            # Prepare contents
            contents = [prompt]
            
            # Handle Reference Images
            if reference_image_paths:
                for path in reference_image_paths:
                    if os.path.exists(path):
                        try:
                            with open(path, "rb") as f:
                                img_bytes = f.read()
                            # Determine mime type
                            mime_type = "image/png" if path.lower().endswith(".png") else "image/jpeg"
                            contents.append(types.Part.from_bytes(data=img_bytes, mime_type=mime_type))
                        except Exception as e:
                            print(f"    ⚠️ Failed to load reference image {path}: {e}")
            
            # Map resolution
            gemini_resolution = resolution
            if "x" in resolution:
                gemini_resolution = "1K" # Default fallback
            
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],
                    candidate_count=number_of_images,
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio,
                        image_size=gemini_resolution 
                    ),
                    tools=tools_list if tools_list else None
                )
            )
            
            # Handle Gemini 3.0 response (Multiple Candidates)
            if response.candidates:
                for i, candidate in enumerate(response.candidates):
                    for part in candidate.content.parts:
                        if part.text:
                            print(f"    [Thinking/Text]: {part.text[:100]}...")
                        if part.inline_data:
                            filename = f"generated_images/yuki_{timestamp}_{i+1}.png"
                            with open(filename, "wb") as f:
                                f.write(part.inline_data.data)
                            saved_files.append(filename)
                            print(f"    ✓ Image saved to: {filename}")
            
            if not saved_files:
                 return "Error: No image found in Gemini response."
            
        else:
            # Imagen Generation (Legacy / Fast)
            response = client.models.generate_images(
                model=model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=number_of_images,
                    aspect_ratio=aspect_ratio,
                    safety_filter_level="block_medium_and_above",
                    person_generation="allow_adult"
                )
            )
            
            if hasattr(response, 'generated_images'):
                for i, image in enumerate(response.generated_images):
                    filename = f"generated_images/yuki_{timestamp}_{i+1}.png"
                    with open(filename, "wb") as f:
                        f.write(image.image.image_bytes)
                    saved_files.append(filename)
                    print(f"    ✓ Image saved to: {filename}")
            else:
                return "Error: No image generated by Imagen."
        
        return f"Images generated successfully: {', '.join(saved_files)}"

    except Exception as e:
        print(f"    ❌ Error generating image: {e}")
        return f"Failed to generate image: {str(e)}"

def generate_cosplay_video(prompt: str, image_path: str = None, aspect_ratio: str = "16:9", model: str = "veo-3.1-generate-001") -> str:
    """
    Generates a cosplay video using Google's Veo models.
    
    Args:
        prompt: The video generation prompt.
        image_path: Optional path to an input image (for image-to-video).
        aspect_ratio: The aspect ratio (e.g., "16:9", "9:16"). Defaults to "16:9".
        model: The model to use. Defaults to 'veo-3.1-generate-001'.
        
    Returns:
        str: The file path of the saved video, or an error message.
    """
    print(f"\n[🎥 GENERATING VIDEO] Model: {model}")
    print(f"    Prompt: {prompt[:50]}...")
    print(f"    Aspect Ratio: {aspect_ratio}")
    
    try:
        client = genai.Client(vertexai=True, project="gifted-cooler-479623-r7", location="us-central1")
        
        if image_path:
            # Image-to-Video
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            
            img_part = types.Part.from_data(data=image_bytes, mime_type="image/png")
            
            response = client.models.generate_videos(
                model=model,
                prompt=prompt,
                image=img_part,
                config=types.GenerateVideosConfig(
                    number_of_videos=1,
                    aspect_ratio=aspect_ratio
                )
            )
        else:
            # Text-to-Video
            response = client.models.generate_videos(
                model=model,
                prompt=prompt,
                config=types.GenerateVideosConfig(
                    number_of_videos=1,
                    aspect_ratio=aspect_ratio
                )
            )
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_images/yuki_video_{timestamp}.mp4"
        
        if hasattr(response, 'generated_videos'):
            video = response.generated_videos[0]
            with open(filename, "wb") as f:
                f.write(video.video.video_bytes)
            print(f"    ✓ Video saved to: {filename}")
            return f"Video generated successfully and saved to {filename}"
        else:
            return "Error: No video generated."

    except Exception as e:
        print(f"    ❌ Error generating video: {e}")
        return f"Failed to generate video: {str(e)}"

def research_topic(topic: str) -> str:
    """
    Performs deep research and reasoning on a topic using Gemini 3.0 Pro.
    Use this for complex questions, planning, or when 'thinking' is required.
    
    Args:
        topic: The research topic or complex question.
        
    Returns:
        str: The detailed research result.
    """
    print(f"\n[🧠 DEEP RESEARCH] Topic: {topic[:50]}...")
    
    try:
        # Gemini 3.0 requires global location
        client = genai.Client(vertexai=True, project="gifted-cooler-479623-r7", location="global")
        
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=topic,
            config=types.GenerateContentConfig(
                temperature=0.7,
                # thinking_level="high" # Uncomment if supported by SDK version
            )
        )
        
        print("    ✓ Research complete.")
        return response.text
        
    except Exception as e:
        print(f"    ❌ Error performing research: {e}")
        return f"Failed to perform research: {str(e)}"

def list_files(directory: str = ".") -> str:
    """
    Lists files in the specified directory.
    
    Args:
        directory: The directory to list. Defaults to current directory.
        
    Returns:
        str: A list of files or an error message.
    """
    print(f"\n[📂 LISTING FILES] Directory: {directory}")
    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"

def read_file(filepath: str) -> str:
    """
    Reads the content of a local file.
    
    Args:
        filepath: The path to the file to read.
        
    Returns:
        str: The content of the file or an error message.
    """
    print(f"\n[📖 READING FILE] Path: {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def upload_to_gcs(filepath: str, content: str, bucket_name: str = "yuki-persistent-storage") -> str:
    """
    Uploads content to a Google Cloud Storage bucket.
    
    Args:
        filepath: The destination path in the bucket (and local filename).
        content: The content to upload.
        bucket_name: The GCS bucket name.
        
    Returns:
        str: Success message or error.
    """
    print(f"\n[☁️ SYNCING TO CLOUD] Bucket: {bucket_name} | Path: {filepath}")
    try:
        storage_client = storage.Client(project="gifted-cooler-479623-r7")
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filepath)
        blob.upload_from_string(content)
        return f"Successfully uploaded to gs://{bucket_name}/{filepath}"
    except Exception as e:
        return f"Error uploading to GCS: {e}"

def upload_file_to_gcs(local_path: str, gcs_path: str, bucket_name: str = "yuki-persistent-storage") -> str:
    """
    Uploads a local file to a Google Cloud Storage bucket.
    
    Args:
        local_path: The path to the local file.
        gcs_path: The destination path in the bucket.
        bucket_name: The GCS bucket name.
        
    Returns:
        str: Success message or error.
    """
    print(f"\n[☁️ UPLOADING TO CLOUD] Path: {local_path} -> gs://{bucket_name}/{gcs_path}")
    try:
        storage_client = storage.Client(project="gifted-cooler-479623-r7")
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(gcs_path)
        blob.upload_from_filename(local_path)
        return f"Successfully uploaded {local_path} to gs://{bucket_name}/{gcs_path}"
    except Exception as e:
        return f"Error uploading to GCS: {e}"

def download_from_gcs(gcs_path: str, local_path: str, bucket_name: str = "yuki-persistent-storage") -> str:
    """
    Downloads content from a Google Cloud Storage bucket to a local file.
    
    Args:
        gcs_path: The path in the bucket to download from.
        local_path: The local destination path.
        bucket_name: The GCS bucket name.
        
    Returns:
        str: Success message or error.
    """
    print(f"\n[☁️ DOWNLOADING FROM CLOUD] Bucket: {bucket_name} | Path: {gcs_path} -> {local_path}")
    try:
        storage_client = storage.Client(project="gifted-cooler-479623-r7")
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(gcs_path)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(local_path) if os.path.dirname(local_path) else ".", exist_ok=True)
        
        blob.download_to_filename(local_path)
        return f"Successfully downloaded gs://{bucket_name}/{gcs_path} to {local_path}"
    except Exception as e:
        return f"Error downloading from GCS: {e}"

def write_file(filepath: str, content: str) -> str:
    """
    Writes content to a GCS bucket first (persistence), then to a local file.
    
    Args:
        filepath: The path to the file to write.
        content: The content to write.
        
    Returns:
        str: Success message or error message.
    """
    # 1. Sync to Cloud Bucket
    gcs_result = upload_to_gcs(filepath, content)
    print(f"    {gcs_result}")
    
    # 2. Write Locally
    print(f"\n[💾 WRITING LOCAL] Path: {filepath}")
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Synced to Cloud ({gcs_result}) and wrote to local file: {filepath}"
    except Exception as e:
        return f"Synced to Cloud but failed to write local file: {e}"

def search_web(query: str) -> str:
    """
    Performs a Google Search to answer a query using Gemini's grounding capabilities.
    
    Args:
        query: The search query.
        
    Returns:
        str: A summary of the search results.
    """
    print(f"\n[🔍 SEARCHING WEB] Query: {query[:50]}...")
    try:
        client = genai.Client(vertexai=True, project="gifted-cooler-479623-r7", location="global")
        
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=f"Answer this query using Google Search: {query}",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                response_mime_type="text/plain"
            )
        )
        return response.text
    except Exception as e:
        return f"Error searching web: {e}"

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
    def handle_data(self, d):
        self.result.append(d)
    def get_text(self):
        return ''.join(self.result)

def fetch_url(url: str) -> str:
    """
    Fetches and extracts text content from a URL.
    
    Args:
        url: The URL to fetch.
        
    Returns:
        str: The text content of the page.
    """
    print(f"\n[🌐 FETCHING URL] {url}")
    try:
        # Basic header to avoid 403s on some sites
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
            
        # Simple HTML to Text
        s = HTMLTextExtractor()
        s.feed(html_content)
        text = s.get_text()
        
        # Clean up whitespace
        clean_text = re.sub(r'\s+', ' ', text).strip()
        return clean_text[:10000] + "..." if len(clean_text) > 10000 else clean_text
        
    except Exception as e:
        return f"Error fetching URL: {e}"

def identify_anime_screenshot(image_path: str) -> str:
    """
    Identifies the anime, episode, and timestamp from a screenshot using trace.moe API.
    
    Args:
        image_path: Path to the local image file.
        
    Returns:
        str: JSON result with anime details or error message.
    """
    print(f"\n[🕵️ IDENTIFYING ANIME] Path: {image_path}")
    import json
    
    # Updated URL to include anilistInfo and cutBorders as per documentation
    url = "https://api.trace.moe/search?anilistInfo&cutBorders"
    
    try:
        if not os.path.exists(image_path):
            return f"Error: File not found at {image_path}"

        with open(image_path, "rb") as f:
            image_data = f.read()
            
        # trace.moe accepts raw image body in POST
        req = urllib.request.Request(url, data=image_data, method='POST')
        req.add_header('Content-Type', 'application/octet-stream') 
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        # Format the output nicely
        if result.get("result"):
            top_match = result["result"][0]
            
            # Extract Anilist Info if available
            anilist = top_match.get("anilist", {})
            title_native = anilist.get("title", {}).get("native", "Unknown")
            title_romaji = anilist.get("title", {}).get("romaji", "Unknown")
            title_english = anilist.get("title", {}).get("english", "Unknown")
            is_adult = anilist.get("isAdult", False)
            
            filename = top_match.get("filename", "Unknown")
            episode = top_match.get("episode", "Unknown")
            similarity = top_match.get("similarity", 0)
            timestamp = top_match.get("from", 0)
            video_preview = top_match.get("video", "")
            image_preview = top_match.get("image", "")
            
            # Convert timestamp to MM:SS
            minutes = int(timestamp // 60)
            seconds = int(timestamp % 60)
            time_str = f"{minutes}:{seconds:02d}"
            
            output = (
                f"Found match: {title_english} ({title_native})\n"
                f"Episode: {episode} | Time: {time_str}\n"
                f"Similarity: {similarity:.2%}\n"
                f"Adult Content: {'Yes' if is_adult else 'No'}\n"
                f"Video Preview: {video_preview}\n"
                f"(Source: trace.moe)"
            )
            return output
        else:
            return "No match found."
            
    except Exception as e:
        return f"Error identifying anime: {e}"

def detect_objects(image_path: str, prompt: str = "Detect all prominent items.") -> str:
    """
    Detects objects in an image and returns their bounding boxes using Gemini 2.5 Flash.
    
    Args:
        image_path: Path to the local image file.
        prompt: Instruction for what to detect (e.g., "Detect all cats").
        
    Returns:
        str: JSON string of detected objects and their bounding boxes.
    """
    print(f"\n[👁️ DETECTING OBJECTS] Path: {image_path} | Prompt: {prompt}")
    try:
        if not os.path.exists(image_path):
            return f"Error: File not found at {image_path}"
            
        client = genai.Client(vertexai=True, project="gifted-cooler-479623-r7", location="us-central1")
        
        # Load image
        image = Image.open(image_path)
        
        # Configure for JSON output
        config = types.GenerateContentConfig(
            response_mime_type="application/json"
        )
        
        full_prompt = f"{prompt} The box_2d should be [ymin, xmin, ymax, xmax] normalized to 0-1000."
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-001",
            contents=[image, full_prompt],
            config=config
        )
        
        return response.text
        
    except Exception as e:
        return f"Error detecting objects: {e}"

def segment_image(image_path: str, prompt: str = "Segment all prominent items.") -> str:
    """
    Segments objects in an image and saves masks using Gemini 2.5 Flash.
    
    Args:
        image_path: Path to the local image file.
        prompt: Instruction for what to segment.
        
    Returns:
        str: Path to the directory containing saved masks.
    """
    print(f"\n[✂️ SEGMENTING IMAGE] Path: {image_path} | Prompt: {prompt}")
    try:
        if not os.path.exists(image_path):
            return f"Error: File not found at {image_path}"
            
        client = genai.Client(vertexai=True, project="gifted-cooler-479623-r7", location="us-central1")
        
        # Load and resize image (max 1024 for segmentation)
        im = Image.open(image_path)
        im.thumbnail([1024, 1024], Image.Resampling.LANCZOS)
        
        full_prompt = f"""
        {prompt}
        Output a JSON list of segmentation masks where each entry contains the 2D
        bounding box in the key "box_2d", the segmentation mask in key "mask", and
        the text label in the key "label". Use descriptive labels.
        """
        
        # Disable thinking for segmentation as per docs
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-001",
            contents=[full_prompt, im],
            config=config
        )
        
        # Parse JSON (handle markdown fencing)
        json_output = response.text
        if "```json" in json_output:
            json_output = json_output.split("```json")[1].split("```")[0]
        elif "```" in json_output:
            json_output = json_output.split("```")[1].split("```")[0]
            
        items = json.loads(json_output)
        
        # Create output directory
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"segmentation_outputs/seg_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        saved_files = []
        
        for i, item in enumerate(items):
            # Process mask
            png_str = item.get("mask", "")
            if not png_str.startswith("data:image/png;base64,"):
                continue

            png_str = png_str.removeprefix("data:image/png;base64,")
            mask_data = base64.b64decode(png_str)
            mask = Image.open(io.BytesIO(mask_data))
            
            # Get bounding box to resize mask
            box = item["box_2d"]
            y0 = int(box[0] / 1000 * im.size[1])
            x0 = int(box[1] / 1000 * im.size[0])
            y1 = int(box[2] / 1000 * im.size[1])
            x1 = int(box[3] / 1000 * im.size[0])
            
            if x1 > x0 and y1 > y0:
                mask = mask.resize((x1 - x0, y1 - y0), Image.Resampling.BILINEAR)
                
                # Save mask
                label = item.get("label", "object").replace(" ", "_")
                mask_filename = f"{label}_{i}_mask.png"
                mask_path = os.path.join(output_dir, mask_filename)
                mask.save(mask_path)
                saved_files.append(mask_filename)
        
        return f"Segmentation complete. Saved {len(saved_files)} masks to {output_dir}"
        
    except Exception as e:
        return f"Error segmenting image: {e}"

def analyze_video(video_path: str, prompt: str = "Describe this video in detail.") -> str:
    """
    Analyzes a video file or YouTube URL using Gemini 2.5 Flash.
    
    Args:
        video_path: Path to a local video file or a YouTube URL.
        prompt: The question or instruction for the video analysis.
        
    Returns:
        str: The model's analysis of the video.
    """
    print(f"\n[🎥 ANALYZING VIDEO] Source: {video_path} | Prompt: {prompt}")
    try:
        client = genai.Client(vertexai=True, project="gifted-cooler-479623-r7", location="us-central1")
        
        contents = [prompt]
        
        # Check if it's a YouTube URL
        if "youtube.com" in video_path or "youtu.be" in video_path:
             contents.append(
                 types.Part(
                     file_data=types.FileData(file_uri=video_path)
                 )
             )
        # Check if it's a local file
        elif os.path.exists(video_path):
            print("    Uploading video to File API (this may take a moment)...")
            # Upload file using File API (best for videos)
            video_file = client.files.upload(file=video_path)
            
            # Wait for processing to complete (simple check)
            import time
            while video_file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(2)
                video_file = client.files.get(name=video_file.name)
            print(" Done.")
            
            if video_file.state.name == "FAILED":
                return "Error: Video processing failed."
                
            contents.append(video_file)
        else:
            return f"Error: Invalid video path or URL: {video_path}"

        response = client.models.generate_content(
            model="gemini-2.5-flash-001",
            contents=contents
        )
        
        return response.text
        
    except Exception as e:
        return f"Error analyzing video: {e}"

def analyze_pdf(pdf_path: str, prompt: str = "Summarize this document.") -> str:
    """
    Analyzes a PDF file or URL using Gemini 2.5 Flash.
    
    Args:
        pdf_path: Path to a local PDF file or a URL.
        prompt: The question or instruction for the PDF analysis.
        
    Returns:
        str: The model's analysis of the PDF.
    """
    print(f"\n[📄 ANALYZING PDF] Source: {pdf_path} | Prompt: {prompt}")
    try:
        client = genai.Client(vertexai=True, project="gifted-cooler-479623-r7", location="us-central1")
        
        contents = [prompt]
        
        # Check if it's a URL
        if pdf_path.startswith("http"):
            # For URLs, we can fetch bytes and pass inline if small, or use File API
            # For simplicity and robustness with large docs, we'll use File API via a temp download
            # But the user guide suggests File API for URLs too if we use httpx/io. 
            # Let's try direct File API upload if the SDK supports it, otherwise download first.
            # The SDK's client.files.upload accepts a file path or IO.
            
            import urllib.request
            import io
            
            print("    Downloading PDF from URL...")
            with urllib.request.urlopen(pdf_path) as response:
                pdf_data = response.read()
                
            pdf_io = io.BytesIO(pdf_data)
            
            print("    Uploading PDF to File API...")
            pdf_file = client.files.upload(file=pdf_io, config={'mime_type': 'application/pdf'})
            contents.append(pdf_file)

        # Check if it's a local file
        elif os.path.exists(pdf_path):
            print("    Uploading PDF to File API...")
            pdf_file = client.files.upload(file=pdf_path)
            contents.append(pdf_file)
        else:
            return f"Error: Invalid PDF path or URL: {pdf_path}"

        response = client.models.generate_content(
            model="gemini-2.5-flash-001",
            contents=contents
        )
        
        return response.text
        
    except Exception as e:
        return f"Error analyzing PDF: {e}"

def generate_audio(text: str, voice: str = "Kore", speaker_map: dict = None) -> str:
    """
    Generates audio from text using Gemini 2.5 Flash TTS.
    
    Args:
        text: The text to speak.
        voice: The voice name for single speaker (default: 'Kore').
        speaker_map: Dictionary mapping speaker names to voices for multi-speaker (e.g., {'Joe': 'Kore', 'Jane': 'Puck'}).
        
    Returns:
        str: Path to the saved audio file.
    """
    print(f"\n[🔊 GENERATING AUDIO] Voice: {voice} | Text: {text[:50]}...")
    try:
        client = genai.Client(vertexai=True, project="gifted-cooler-479623-r7", location="us-central1")
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_audio/yuki_audio_{timestamp}.wav"
        os.makedirs("generated_audio", exist_ok=True)
        
        config_args = {
            "response_modalities": ["AUDIO"]
        }
        
        if speaker_map:
            # Multi-speaker config
            speakers = []
            for name, voice_name in speaker_map.items():
                speakers.append(
                    types.SpeakerVoiceConfig(
                        speaker=name,
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice_name)
                        )
                    )
                )
            config_args["speech_config"] = types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(speaker_voice_configs=speakers)
            )
        else:
            # Single speaker config
            config_args["speech_config"] = types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)
                )
            )

        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=types.GenerateContentConfig(**config_args)
        )
        
        # Save audio
        if response.candidates and response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            if part.inline_data:
                with wave.open(filename, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(24000)
                    wf.writeframes(part.inline_data.data)
                return f"Audio generated successfully: {filename}"
        
        return "Error: No audio data returned."
        
    except Exception as e:
        return f"Error generating audio: {e}"

def analyze_audio(audio_path: str, prompt: str = "Describe this audio clip.") -> str:
    """
    Analyzes an audio file using Gemini 2.5 Flash.
    
    Args:
        audio_path: Path to a local audio file.
        prompt: The question or instruction for the audio analysis.
        
    Returns:
        str: The model's analysis of the audio.
    """
    print(f"\n[🎤 ANALYZING AUDIO] Source: {audio_path} | Prompt: {prompt}")
    try:
        if not os.path.exists(audio_path):
            return f"Error: File not found at {audio_path}"
            
        client = genai.Client(vertexai=True, project="gifted-cooler-479623-r7", location="us-central1")
        
        print("    Uploading audio to File API...")
        audio_file = client.files.upload(file=audio_path)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-001",
            contents=[prompt, audio_file]
        )
        
        return response.text
        
    except Exception as e:
        return f"Error analyzing audio: {e}"







