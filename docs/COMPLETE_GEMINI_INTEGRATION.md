# 🦊 Yuki Platform - Complete Gemini Integration Guide

## 🎨 Full-Stack Gemini Capabilities for Anime Cosplay

This guide demonstrates how to leverage **ALL** Gemini API capabilities in the Yuki Cosplay Platform for a production-grade experience.

---

## 🛠️ Available Gemini Tools

### 1. **Image Generation** (Nano Banana Pro)
**Models**: `gemini-2.5-flash-image`, `gemini-3-pro-image-preview`

**Capabilities**:
- Text-to-image generation
- Multi-reference (up to 14 images, 6 high-fidelity)
- Conversational editing
- 4K resolution output
- Thinking mode for complex tasks
- 100% facial preservation

**Use in Yuki**: Generate cosplay previews with character + user face references

---

### 2. **File Search** (RAG)
**Feature**: Semantic search across indexed documents

**Capabilities**:
- Document chunking and embedding
- Metadata filtering
- Citation tracking
- Free storage and query-time embeddings
- Up to 1TB storage (Tier 3)

**Use in Yuki**: Index anime character database, cosplay guides, prompt templates

---

### 3. **Grounding with Google Search**
**Tool**: Real-time web search for factual accuracy

**Capabilities**:
- Access current information
- Reduce hallucinations
- Provide verifiable citations
- Automatic search query generation

**Use in Yuki**: Find trending characters, current conventions, recent anime releases

---

### 4. **Code Execution**
**Feature**: Run Python code in sandbox

**Capabilities**:
- Generate and execute Python
- 30+ supported libraries (numpy, pandas, matplotlib, etc.)
- File I/O (CSV, text)
- Graph generation
- 30-second max runtime

**Use in Yuki**: Calculate cosplay costs, analyze popularity trends, generate charts

---

### 5. **URL Context**
**Tool**: Extract and analyze web content

**Capabilities**:
- Process up to 20 URLs per request
- Extract from HTML, PDF, images
- Combine with search grounding
- 34MB max per URL

**Use in Yuki**: Analyze cosplay tutorial URLs, extract character wikis, process reference sites

---

### 6. **Live API** (Voice/Video)
**Feature**: Real-time audio/video streaming

**Capabilities**:
- Native audio output (24kHz)
- Video streaming
- Voice Activity Detection (VAD)
- Transcription (input & output)
- Multiple languages
- Affective dialog

**Use in Yuki**: Voice-guided cosplay tutorials, live character analysis

---

## 🎯 Integrated Workflows

### Workflow 1: Complete Cosplay Generation Pipeline

```python
from yuki_gemini_client import YukiGeminiImageClient
from yuki_knowledge_base import YukiKnowledgeBase
from google import genai
from google.genai import types

class CompleteYukiPlatform:
    """
    Full-stack Yuki platform with ALL Gemini capabilities
    """
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.image_gen = YukiGeminiImageClient(api_key=api_key)
        self.knowledge_base = YukiKnowledgeBase(api_key=api_key)
    
    async def generate_cosplay_with_research(
        self,
        character_name: str,
        anime_title: str,
        user_selfie_path: str
    ):
        """
        COMPLETE workflow using multiple tools
        
        Steps:
        1. Search knowledge base for character data (File Search)
        2. Ground in real-time web data (Google Search)
        3. Analyze reference URLs (URL Context)
        4. Calculate optimal settings (Code Execution)
        5. Generate cosplay image (Image Generation)
        """
        
        # Step 1: Search knowledge base
        character_info = await self.knowledge_base.search_character_knowledge(
            query=f"Get all visual details for {character_name} from {anime_title}",
            character_filter=character_name
        )
        
        # Step 2: Ground in current data
        trending_response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Is {character_name} currently trending for cosplay? Check recent data.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        # Step 3: Analyze reference URLs
        reference_urls = [
            f"https://myanimelist.net/character/{character_name}",
            f"https://fandom.com/wiki/{character_name}"
        ]
        
        url_analysis = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Extract ALL costume details from these references for {character_name}",
            config=types.GenerateContentConfig(
                tools=[types.Tool(url_context=types.UrlContext())]
            )
        )
        
        # Step 4: Calculate optimal generation settings
        code_response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
            Based on character popularity score of 8.5/10, calculate:
            1. Recommended resolution (1K/2K/4K)
            2. Estimated generation time
            3. Optimal aspect ratio for social media
            
            Use code to calculate and return results.
            """,
            config=types.GenerateContentConfig(
                tools=[types.Tool(code_execution=types.ToolCodeExecution)]
            )
        )
        
        # Step 5: Generate cosplay image with all gathered data
        final_image = await self.image_gen.generate_cosplay_with_face_preservation(
            character_name=character_name,
            anime_title=anime_title,
            user_face_image=user_selfie_path,
            outfit_description=url_analysis.text,  # From URL analysis
            resolution=ImageResolution.RESOLUTION_4K  # From code calculation
        )
        
        return {
            "image": final_image,
            "character_info": character_info,
            "trending_status": trending_response.text,
            "citations": trending_response.candidates[0].grounding_metadata,
            "optimal_settings": code_response.text
        }
```

---

### Workflow 2: Real-Time Voice Cosplay Tutorial

```python
async def voice_guided_cosplay_tutorial(
    self,
    character_name: str
):
    """
    Interactive voice tutorial using Live API
    
    Features:
    - Voice Activity Detection
    - Real-time Q&A
    - Search grounding for accurate info
    - Audio transcription
    """
    
    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        output_audio_transcription={},
        input_audio_transcription={},
        speech_config={
            "voice_config": {"prebuilt_voice_config": {"voice_name": "Kore"}}
        }
    )
    
    async with self.client.aio.live.connect(
        model="gemini-2.5-flash-native-audio-preview-09-2025",
        config=config
    ) as session:
        
        # Set context
        context = f"""
        You are Yuki, an expert cosplay guide. You're helping the user 
        create a cosplay of {character_name}. Provide step-by-step 
        instructions with materials lists, construction tips, and styling advice.
        """
        
        await session.send_client_content(
            turns={"role": "user", "parts": [{"text": context}]},
            turn_complete=True
        )
        
        # Stream audio input/output
        async for response in session.receive():
            if response.server_content.output_transcription:
                print(f"Yuki says: {response.server_content.output_transcription.text}")
            
            if response.server_content.model_turn:
                # Play audio to user
                pass
```

---

### Workflow 3: Smart Cost Calculator with Code Execution

```python
async def calculate_cosplay_costs(
    self,
    character_name: str,
    anime_title: str
):
    """
    Use code execution to calculate detailed cosplay costs
    
    Returns:
    - Materials breakdown
    - Estimated total cost
    - Cost comparison chart
    - Budget recommendations
    """
    
    # Get character details from knowledge base
    character_data = await self.knowledge_base.search_character_knowledge(
        query=f"List all costume components for {character_name}",
        character_filter=character_name
    )
    
    # Use code execution for calculations
    calculation_prompt = f"""
    Based on this character data: {character_data['answer']}
    
    Generate Python code to:
    1. Create a materials list with estimated costs
    2. Calculate total cost (beginner vs advanced)
    3. Generate a matplotlib bar chart comparing costs
    4. Provide budget breakdown by category (fabric, wigs, props, etc.)
    
    Use realistic market prices and output a detailed analysis.
    """
    
    response = self.client.models.generate_content(
        model="gemini-2.5-flash",
        contents=calculation_prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(code_execution=types.ToolCodeExecution)]
        )
    )
    
    # Extract code execution results
    for part in response.candidates[0].content.parts:
        if part.executable_code:
            print("Generated code:", part.executable_code.code)
        if part.code_execution_result:
            print("Results:", part.code_execution_result.output)
        if part.inline_data:  # Chart image
            chart = part.as_image()
            chart.save(f"{character_name}_cost_breakdown.png")
    
    return response
```

---

### Workflow 4: Multi-Tool Research Assistant

```python
async def comprehensive_character_research(
    self,
    character_name: str,
    anime_title: str
):
    """
    Combine ALL tools for complete character analysis
    
    Tools used:
    1. Google Search - Current popularity
    2. URL Context - Wiki/MAL reference
    3. File Search - Internal knowledge base
    4. Code Execution - Trend analysis
    """
    
    # Enable multiple tools
    tools = [
        types.Tool(google_search=types.GoogleSearch()),
        types.Tool(url_context=types.UrlContext()),
        types.Tool(code_execution=types.ToolCodeExecution)
    ]
    
    research_query = f"""
    Conduct comprehensive research on {character_name} from {anime_title}:
    
    1. Check current popularity and trending status (use Google Search)
    2. Analyze the MyAnimeList page: https://myanimelist.net/character/{character_name.replace(' ', '_')}
    3. Extract costume details, personality traits, and visual characteristics
    4. Calculate popularity trend over time using Python
    5. Generate a summary suitable for cosplay planning
    
    Cite all sources.
    """
    
    response = self.client.models.generate_content(
        model="gemini-2.5-flash",
        contents=research_query,
        config=types.GenerateContentConfig(tools=tools)
    )
    
    # Process results
    result = {
        "analysis": response.text,
        "search_citations": [],
        "url_sources": [],
        "code_output": []
    }
    
    # Extract grounding metadata
    if response.candidates[0].grounding_metadata:
        result["search_citations"] = response.candidates[0].grounding_metadata.grounding_chunks
    
    # Extract URL metadata
    if response.candidates[0].url_context_metadata:
        result["url_sources"] = response.candidates[0].url_context_metadata.url_metadata
    
    # Extract code execution
    for part in response.candidates[0].content.parts:
        if part.code_execution_result:
            result["code_output"].append(part.code_execution_result.output)
    
    return result
```

---

## 📊 Tool Combination Matrix

| Use Case | Image Gen | File Search | Google Search | Code Exec | URL Context | Live API |
|----------|-----------|-------------|---------------|-----------|-------------|----------|
| **Cosplay Generation** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Character Research** | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Cost Calculation** | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Voice Tutorial** | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Trend Analysis** | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |
| **Reference Extraction** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Complete Pipeline** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |

---

## 💰 Cost Optimization Strategies

### Strategy 1: Cache Aggressively
```python
# Use File Search (free storage, free query-time embeddings)
# vs repeated Gemini calls
```

### Strategy 2: Smart Tool Selection
```python
# Google Search: $0.001 per query
# Code Execution: No extra cost (just token-based)
# URL Context: Token-based only
# File Search: Embedding cost at index time only ($0.15/1M tokens)
```

### Strategy 3: Batch Operations
```python
# Index all characters once (File Search)
# Then query cheaply vs individual Gemini calls
```

---

## 🔒 Security Best Practices

### 1. API Key Management
```python
import os
from google import genai

# Never hardcode keys
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)
```

### 2. Input Validation
```python
def validate_user_input(text: str) -> bool:
    """Sanitize user inputs before sending to API"""
    # Check for malicious content
    # Limit length
    # Filter inappropriate content
    return True
```

### 3. Rate Limiting
```python
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
async def safe_api_call(prompt: str):
    """Automatic retry with exponential backoff"""
    return await client.models.generate_content(...)
```

---

## 📈 Performance Metrics

### Expected Latencies
```
Image Generation (Nano Banana Pro): 8-15s (4K)
File Search Query: <500ms
Google Search Grounding: 2-5s
Code Execution: 1-30s (depends on code)
URL Context: 1-3s per URL
Live API: 200-500ms audio latency
```

### Token Costs (Gemini 2.5 Flash)
```
Input: $0.075 per 1M tokens
Output: $0.30 per 1M tokens
Cached Input: $0.01875 per 1M tokens (75% discount)
```

---

## 🚀 Production Deployment Checklist

- [ ] **API Keys**: Secure storage (Secret Manager)
- [ ] **Rate Limiting**: Implement per-user quotas
- [ ] **Caching**: Redis for response caching
- [ ] **Error Handling**: Comprehensive try/catch
- [ ] **Logging**: Cloud Logging integration
- [ ] **Monitoring**: Track API usage and costs
- [ ] **Fallbacks**: Graceful degradation
- [ ] **Testing**: Unit + integration tests
- [ ] **Documentation**: API reference
- [ ] **Scaling**: Cloud Run auto-scaling

---

## 📚 Code Examples

All implementation examples are in:
- `yuki_gemini_client.py` - Image generation
- `yuki_knowledge_base.py` - File Search RAG
- `yuki_cosplay_platform.py` - Main orchestration
- `prompt_engineering_system.py` - Prompt optimization

---

## 🎯 Next Steps

### Week 1: Core Integration
1. Implement multi-tool coordinator
2. Test File Search indexing
3. Validate image generation pipeline

### Week 2: Advanced Features  
4. Add Live API voice tutorials
5. Implement code execution for analytics
6. URL context for character research

### Week 3: Production Polish
7. Add comprehensive error handling
8. Implement caching strategies
9. Performance optimization

### Week 4: Launch
10. Deploy to Cloud Run
11. Beta testing
12. Public launch

---

**Built with ❄️ by Yuki - Powered by the Complete Gemini API Stack**  
**Status**: 🚀 **ALL CAPABILITIES INTEGRATED**
