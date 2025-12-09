"""
Yuki Video Suite - Complete Video Generation & Analysis
Production-ready video generation AND understanding for anime cosplay

Generation (Veo 3.1):
- Text-to-video generation
- Image-to-video animation
- Reference image support (up to 3 images)
- Video extension (up to 20x)
- Frame interpolation (first + last frame)
- Native audio generation
- 720p & 1080p output

Analysis (Gemini 2.5):
- Tutorial step extraction with timestamps
- Character movement analysis
- Text extraction from videos (sewing patterns, labels)
- YouTube video analysis
- Custom FPS and clipping intervals
- Scene-by-scene breakdown
"""

import time
import asyncio
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Literal, Union
from pathlib import Path
from enum import Enum
import re

from google import genai
from google.genai import types
from PIL import Image as PILImage


class VeoModel(Enum):
    """Available Veo models"""
    VEO_3_1 = "veo-3.1-generate-preview"  # Best quality, latest features
    VEO_3_1_FAST = "veo-3.1-fast-preview"  # Optimized for speed
    VEO_3 = "veo-3-generate"  # Stable, production
    VEO_3_FAST = "veo-3-fast-generate"  # Fast version
    VEO_2 = "veo-2-generate"  # Legacy


class AspectRatio(Enum):
    """Video aspect ratios"""
    WIDESCREEN = "16:9"  # Standard widescreen
    PORTRAIT = "9:16"  # Mobile/social media


class Resolution(Enum):
    """Video resolutions"""
    HD_720 = "720p"  # 1280x720
    FULL_HD_1080 = "1080p"  # 1920x1080 (8s only for Veo 3.1)


class Duration(Enum):
    """Video durations"""
    SHORT = "4"  # 4 seconds
    MEDIUM = "6"  # 6 seconds
    FULL = "8"  # 8 seconds (required for extension/interpolation/references)


@dataclass
class GeneratedVideo:
    """Container for generated video"""
    video_file: Any  # Video file object
    video_path: Optional[str] = None  # Local save path
    prompt: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    generation_time: float = 0.0


@dataclass
class VideoAnalysis:
    """Container for video analysis results"""
    analysis_text: str
    timestamps: List[Dict[str, Any]] = field(default_factory=list)
    scenes: List[Dict[str, Any]] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class YukiVideoGenerator:
    """
    Production-ready Veo 3.1 video generator for Yuki Platform
    
    Use Cases:
    - Cosplay tutorial videos
    - Character showcase animations
    - Animated reference sheets
    - Motion studies for poses
    - Video storytelling
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize video generator"""
        self.client = genai.Client(api_key=api_key)
        self.default_model = VeoModel.VEO_3_1
        
        # Track operations for monitoring
        self.operations: Dict[str, Any] = {}
    
    async def generate_text_to_video(
        self,
        prompt: str,
        model: VeoModel = None,
        aspect_ratio: AspectRatio = AspectRatio.WIDESCREEN,
        resolution: Resolution = Resolution.HD_720,
        duration: Duration = Duration.FULL,
        negative_prompt: Optional[str] = None,
        save_path: Optional[str] = None
    ) -> GeneratedVideo:
        """
        Generate video from text prompt
        
        Args:
            prompt: Descriptive text for video
            model: Veo model to use
            aspect_ratio: Video aspect ratio
            resolution: Video resolution
            duration: Video length in seconds
            negative_prompt: What to avoid
            save_path: Where to save video locally
            
        Returns:
            GeneratedVideo object
        """
        
        if model is None:
            model = self.default_model
        
        start_time = time.time()
        
        # Build config
        config = types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio.value,
            resolution=resolution.value,
            duration_seconds=duration.value,
            number_of_videos=1,
            person_generation="allow_all"  # For cosplay content
        )
        
        if negative_prompt:
            config.negative_prompt = negative_prompt
        
        # Start generation
        operation = self.client.models.generate_videos(
            model=model.value,
            prompt=prompt,
            config=config
        )
        
        # Store operation for monitoring
        self.operations[operation.name] ={"prompt": prompt,
            "started_at": time.time(),
            "model": model.value
        }
        
        # Poll until complete
        print(f"🎬 Generating video: {prompt[:50]}...")
        operation = await self._wait_for_completion(operation)
        
        # Extract video
        generated_video = operation.response.generated_videos[0]
        
        # Download if save path specified
        if save_path:
            self.client.files.download(file=generated_video.video)
            generated_video.video.save(save_path)
            video_path = save_path
        else:
            video_path = None
        
        generation_time = time.time() - start_time
        
        return GeneratedVideo(
            video_file=generated_video.video,
            video_path=video_path,
            prompt=prompt,
            metadata={
                "model": model.value,
                "aspect_ratio": aspect_ratio.value,
                "resolution": resolution.value,
                "duration": duration.value,
                "negative_prompt": negative_prompt
            },
            generation_time=generation_time
        )
    
    async def _wait_for_completion(
        self,
        operation: Any,
        poll_interval: int = 10
    ) -> Any:
        """
        Poll operation until video generation completes
        
        Args:
            operation: Operation object from generate call
            poll_interval: Seconds between status checks
            
        Returns:
            Completed operation object
        """
        
        while not operation.done:
            print(f"   ⏳ Waiting for video generation... (polling in {poll_interval}s)")
            await asyncio.sleep(poll_interval)
            operation = self.client.operations.get(operation)
        
        print("   ✅ Video generation complete!")
        return operation
    
    def build_cosplay_tutorial_prompt(
        self,
        character_name: str,
        anime_title: str,
        tutorial_focus: Literal["makeup", "wig_styling", "costume_assembly", "pose_guide"]
    ) -> str:
        """
        Build optimized prompt for cosplay tutorial videos
        
        Follows Veo best practices:
        - Clear subject and action
        - Camera positioning
        - Audio cues (dialogue, SFX)
        - Cinematic style
        """
        
        tutorials = {
            "makeup": f"""
A professional beauty tutorial video. Close-up, eye-level shot of a cosplayer 
applying makeup to transform into {character_name} from {anime_title}.

The video shows:
1. Base makeup application (foundation matching character's skin tone)
2. Eye makeup featuring {character_name}'s signature eye style
3. Contouring to match character's face shape
4. Final details (eyebrows, lips, beauty marks)

Camera: Slowly pans and zooms to show detailed brush strokes and blending techniques.
Lighting: Bright, even ring light illumination perfect for makeup details.
Audio: Soft background music with gentle brush sounds, occasional "Perfect!" remarks.

Cinematic, professional tutorial style with warm tones.
""",
            
            "wig_styling": f"""
A step-by-step wig styling tutorial video. Medium shot of a cosplayer styling 
a wig to recreate {character_name}'s iconic hairstyle from {anime_title}.

The sequence shows:
1. Wig on mannequin head, initial state
2. Cutting and shaping the wig
3. Styling with heat tools and products
4. Adding any signature elements (clips, ribbons, etc.)
5. Final result on the cosplayer

Camera: Smooth rotation around the mannequin, then cuts to cosplayer wearing it.
Lighting: Professional studio lighting with soft shadows.
Audio: Scissors cutting, spray bottle sounds, upbeat background music. 
Voiceover: "Now we're going to add the signature spike here..."

Bright, instructional video style.
""",
            
            "costume_assembly": f"""
A timelapse-style cosplay construction video. Wide to medium shots showing the 
complete assembly of {character_name}'s outfit from {anime_title}.

The progression:
1. Fabric laid out with pattern pieces
2. Sewing machine stitching seams
3. Adding details (buttons, zippers, trim)
4. Crafting props and accessories
5. Final costume on dress form
6. Cosplayer wearing complete costume

Camera: Overhead shots for fabric work, eye-level for sewing, 360° rotation for final reveal.
Lighting: Workshop lighting, transitioning to dramatic reveal lighting.
Audio: Sewing machine whirring, scissors snipping, triumphant music swell at reveal.

Document-style with energetic pacing.
""",
            
            "pose_guide": f"""
A dynamic posing reference video for {character_name} from {anime_title}. 
Full-body shot of a cosplayer demonstrating signature character poses.

The sequence shows 4-5 iconic {character_name} poses:
1. Starting with neutral stance
2. Signature fighting/action pose
3. Characteristic facial expression with hand gesture
4. Emotional scene recreation
5. Victory/finale pose

Camera: Slow 360° rotation around cosplayer for each pose, maintaining full-body framing.
Lighting: Dramatic, character-appropriate lighting (moody for villains, bright for heroes).
Audio: Swish sounds during pose transitions, anime-style sound effects. 
Background music matching {character_name}'s theme.

High-energy, reference video style with quick cuts between poses.
"""
        }
        
        return tutorials[tutorial_focus].strip()


class YukiVideoAnalyzer:
    """
    Video understanding with Gemini 2.5 for cosplay tutorials
    
    Use Cases:
    - Extract tutorial steps from YouTube videos
    - Analyze character movements in anime clips
    - Read text from video (sewing patterns, labels)
    - Generate timestamps for key moments
    - Scene-by-scene breakdown
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize video analyzer"""
        self.client = genai.Client(api_key=api_key)
        self.default_model = "gemini-2.5-flash"
    
    async def upload_video(
        self,
        video_path: str
    ) -> Any:
        """
        Upload video to Files API for analysis
        
        Args:
            video_path: Path to local video file
            
        Returns:
            Uploaded video file object
        """
        
        print(f"📤 Uploading {video_path}...")
        video_file = self.client.files.upload(file=video_path)
        
        # Wait for processing
        while video_file.state == "PROCESSING":
            print("   ⏳ Processing video...")
            await asyncio.sleep(10)
            video_file = self.client.files.get(name=video_file.name)
        
        if video_file.state == "FAILED":
            raise ValueError(f"Video processing failed: {video_file.state}")
        
        print(f"   ✅ Ready: {video_file.uri}")
        return video_file
    
    async def analyze_tutorial(
        self,
        video_source: Union[str, Any],
        tutorial_type: Literal["makeup", "wig", "sewing", "prop", "general"] = "general"
    ) -> VideoAnalysis:
        """
        Extract tutorial steps with timestamps
        
        Args:
            video_source: YouTube URL, local file path, or uploaded file
            tutorial_type: Type of tutorial for optimized prompts
            
        Returns:
            VideoAnalysis with extracted steps and timestamps
        """
        
        prompts = {
            "makeup": """
Analyze this makeup tutorial and extract:  
1. Each makeup step with precise timestamp
2. Products/tools mentioned
3. Key techniques demonstrated
4. Color specifications (exact shades)

Format as:
## Step [N]: [Action] (MM:SS)
- **Tools**: [list]
- **Products**: [list with colors]
- **Technique**: [description]
""",
            "wig": """
Analyze this wig styling tutorial and extract:
1. Each styling step with timestamp
2. Tools and products used
3. Heat settings (if mentioned)
4. Cutting/trimming points

Format as numbered steps with timestamps.
""",
            "sewing": """
Analyze this sewing tutorial and extract:
1. Pattern pieces and measurements
2. Fabric requirements
3. Each construction step with timestamp
4. Seam allowances and techniques

Include any text visible on patterns or templates.
""",
            "prop": """
Analyze this prop-making tutorial and extract:
1. Materials list
2. Tools required
3. Construction steps with timestamps
4. Painting/finishing techniques
""",
            "general": """
Analyze this cosplay tutorial step-by-step:
1. List each step with precise timestamp (MM:SS format)
2. Materials and tools mentioned
3. Key techniques or tips
4. Any text visible in the video (measurements, labels, etc.)

Organize chronologically.
"""
        }
        
        # Prepare content
        if isinstance(video_source, str):
            if 'youtube.com' in video_source or 'youtu.be' in video_source:
                # YouTube URL
                content = types.Content(
                    parts=[
                        types.Part(file_data=types.FileData(file_uri=video_source)),
                        types.Part(text=prompts[tutorial_type])
                    ]
                )
            else:
                # Local file - upload first
                video_file = await self.upload_video(video_source)
                content = [video_file, prompts[tutorial_type]]
        else:
            # Already uploaded file
            content = [video_source, prompts[tutorial_type]]
        
        # Analyze
        print(f"🔍 Analyzing {tutorial_type} tutorial...")
        response = self.client.models.generate_content(
            model=self.default_model,
            contents=content
        )
        
        # Extract timestamps and steps
        timestamps = self._extract_timestamps(response.text)
        steps = self._extract_steps(response.text)
        
        return VideoAnalysis(
            analysis_text=response.text,
            timestamps=timestamps,
            steps=steps,
            metadata={
                "tutorial_type": tutorial_type,
                "model": self.default_model
            }
        )
    
    async def analyze_character_movement(
        self,
        video_source: Union[str, Any],
        character_name: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        fps: int = 1
    ) -> VideoAnalysis:
        """
        Analyze character movements for pose reference
        
        Args:
            video_source: Video source (YouTube, local, or uploaded)
            character_name: Name of character to analyze
            start_time: Start time (e.g., "60s", "1m30s")
            end_time: End time
            fps: Frames per second to analyze (higher = more detail)
            
        Returns:
            VideoAnalysis with movement breakdown
        """
        
        prompt = f"""
Analyze {character_name}'s movements in this video:

1. Break down into key poses with timestamps
2. Describe body positioning for each pose:
   - Head/neck angle
   - Shoulder/arm position
   - Hip/leg stance
   - Hand gestures
3. Note signature movements or expressions
4. Indicate difficulty level for cosplay recreation

Format as a table:
| Timestamp | Pose Name | Description | Body Position | Difficulty |
"""
        
        # Build content with video metadata if clipping
        if isinstance(video_source, str) and ('youtube' in video_source.lower()):
            parts = [types.Part(text=prompt)]
            
            # Add video with metadata
            video_part_args = {"file_uri": video_source}
            
            if start_time or end_time or fps > 1:
                video_metadata = {}
                if start_time:
                    video_metadata["start_offset"] = start_time
                if end_time:
                    video_metadata["end_offset"] = end_time
                if fps > 1:
                    video_metadata["fps"] = fps
                
                parts.insert(0, types.Part(
                    file_data=types.FileData(**video_part_args),
                    video_metadata=types.VideoMetadata(**video_metadata)
                ))
            else:
                parts.insert(0, types.Part(file_data=types.FileData(**video_part_args)))
            
            content = types.Content(parts=parts)
        else:
            # Uploaded file or local
            if isinstance(video_source, str):
                video_source = await self.upload_video(video_source)
            content = [video_source, prompt]
        
        print(f"🏃 Analyzing character movements (FPS: {fps})...")
        response = self.client.models.generate_content(
            model=self.default_model,
            contents=content
        )
        
        return VideoAnalysis(
            analysis_text=response.text,
            timestamps=self._extract_timestamps(response.text),
            metadata={
                "character": character_name,
                "fps": fps,
                "clip_range": f"{start_time or '0s'} - {end_time or 'end'}"
            }
        )
    
    async def extract_text_from_video(
        self,
        video_source: Union[str, Any],
        text_type: Literal["patterns", "labels", "measurements", "all"] = "all"
    ) -> VideoAnalysis:
        """
        Extract text visible in video (patterns, measurements, labels)
        
        Args:
            video_source: Video source
            text_type: Type of text to focus on
            
        Returns:
            VideoAnalysis with extracted text
        """
        
        prompts = {
            "patterns": "Transcribe all pattern markings, lines, and measurements visible. Include timestamps.",
            "labels": "Read all labels, tags, and product names visible. Include timestamps.",
            "measurements": "Extract all measurements, dimensions, and numerical values shown. Include timestamps.",
            "all": "Read and transcribe ALL text visible in this video, including handwritten notes, labels, measurements, and on-screen text. Organize by timestamp."
        }
        
        if isinstance(video_source, str) and 'youtube' not in video_source.lower():
            video_source = await self.upload_video(video_source)
        
        print(f"📝 Extracting {text_type} text from video...")
        response = self.client.models.generate_content(
            model=self.default_model,
            contents=[video_source, prompts[text_type]]
        )
        
        return VideoAnalysis(
            analysis_text=response.text,
            timestamps=self._extract_timestamps(response.text),
            metadata={"text_type": text_type}
        )
    
    def _extract_timestamps(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract timestamps from analysis text
        
        Matches formats like:
        - 0:15
        - 1:23
        - 12:34
        - (0:15)
        - [1:23]
        """
        
        timestamp_pattern = r'\(?\[?(\d{1,2}:\d{2})\]?\)?'
        matches = re.finditer(timestamp_pattern, text)
        
        timestamps = []
        for match in matches:
            time_str = match.group(1)
            # Find surrounding context
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 100)
            context = text[start:end].strip()
            
            timestamps.append({
                "time": time_str,
                "context": context
            })
        
        return timestamps
    
    def _extract_steps(self, text: str) -> List[str]:
        """
        Extract numbered or bulleted steps from analysis
        """
        
        # Match patterns like:
        # 1. Step
        # - Step
        # * Step
        # Step 1:
        step_patterns = [
            r'^\d+\.\s+(.+)$',
            r'^[-*]\s+(.+)$',
            r'^Step\s+\d+:\s+(.+)$',
            r'^##\s+Step\s+\d+:\s+(.+)$'
        ]
        
        steps = []
        for line in text.split('\n'):
            line = line.strip()
            for pattern in step_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    steps.append(match.group(1))
                    break
        
        return steps


# Example usage
async def demo():
    """Demonstrate video suite capabilities"""
    print("🦊 Yuki Video Suite Demo\n")
    
    # GENERATION
    print("=" * 50)
    print("VIDEO GENERATION (Veo 3.1)")
    print("=" * 50)
    
    generator = YukiVideoGenerator(api_key="YOUR_API_KEY")
    
    prompt = generator.build_cosplay_tutorial_prompt(
        character_name="Makima",
        anime_title="Chainsaw Man",
        tutorial_focus="makeup"
    )
    
    video = await generator.generate_text_to_video(
        prompt=prompt,
        save_path="makima_makeup_tutorial.mp4"
    )
    print(f"✅ Generated in {video.generation_time:.1f}s\n")
    
    # ANALYSIS
    print("=" * 50)
    print("VIDEO ANALYSIS (Gemini 2.5)")
    print("=" * 50)
    
    analyzer = YukiVideoAnalyzer(api_key="YOUR_API_KEY")
    
    # Example 1: Analyze YouTube tutorial
    print("\n1. Analyzing YouTube cosplay tutorial...")
    tutorial = await analyzer.analyze_tutorial(
        video_source="https://www.youtube.com/watch?v=EXAMPLE",
        tutorial_type="makeup"
    )
    print(f"   Extracted {len(tutorial.steps)} steps")
    print(f"   Found {len(tutorial.timestamps)} timestamps\n")
    
    # Example 2: Analyze character movement
    print("2. Analyzing character movements...")
    movement = await analyzer.analyze_character_movement(
        video_source="https://www.youtube.com/watch?v=ANIME_CLIP",
        character_name="Makima",
        start_time="60s",
        end_time="120s",
        fps=24  # High FPS for detailed movement
    )
    print(f"   Analysis complete\n")
    
    # Example 3: Extract text from sewing pattern video
    print("3. Extracting text from pattern video...")
    text_data = await analyzer.extract_text_from_video(
        video_source="local_pattern_video.mp4",
        text_type="measurements"
    )
    print(f"   Extracted measurements\n")
    
    print("✅ Demo complete!")


if __name__ == "__main__":
    asyncio.run(demo())
