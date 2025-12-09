# Yuki Model Strategy - Complete Model Hierarchy

## 🧠 **Gemini Model Hierarchy**

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                           │
│              Gemini 3 Pro Preview (Planning)                     │
│         Complex multi-agent task delegation                      │
│                     Location: global                             │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────────┐
│                    REASONING LAYER                               │
│              Gemini 2.5 Pro (Complex Problems)                   │
│      1M token context, grounding, code execution                 │
│    Perfect for: Prompt optimization, quality analysis            │
│              Location: us-central1, global                       │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────────┐
│                   GENERATION LAYER                               │
│                                                                  │
│  ┌────────────────────────┐  ┌─────────────────────────────┐  │
│  │ Gemini 3 Pro Image     │  │ Gemini 2.5 Flash Image      │  │
│  │ (Nano Banana Pro)      │  │ (Fast Fallback)             │  │
│  │ Primary image gen      │  │ Speed + cost efficiency     │  │
│  │ Location: global       │  │ Location: us-central1       │  │
│  └────────────────────────┘  └─────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────────┐
│                    WORKER LAYER                                  │
│              Gemini 2.5 Flash (Fast Tasks)                       │
│        Sub-agents, parallel processing, speed                    │
│              Location: us-central1                               │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎯 **When to Use Each Model**

### **1. Gemini 3 Pro Preview** (`gemini-3-pro-preview`)
**Use for**: Top-level orchestration, multi-agent planning
- Breaking down complex tasks into sub-tasks
- Delegating work to Gemini 2.5 Pro or 2.5 Flash
- Synthesizing results from multiple agents
- Strategic decision-making

**Location**: `global`  
**Context**: 2M tokens  
**Cost**: Highest  

**Example**:
```python
# Plan full cosplay generation campaign
orchestrator_prompt = """
Create a comprehensive plan to generate 100 cosplay variations
for 10 characters across 5 anime series.

Break down into:
1. Character schema extraction tasks
2. Prompt optimization strategy
3. Generation batches
4. Quality validation steps

Delegate sub-tasks to appropriate models.
"""
```

---

### **2. Gemini 2.5 Pro** ⭐ **NEW!** (`gemini-2.5-pro`)
**Use for**: Advanced reasoning, complex problem solving
- **Prompt optimization** - Analyze what works, improve prompts
- **Quality analysis** - Evaluate generated images
- **Face schema refinement** - Complex geometric calculations
- **Learning system** - Extract insights from generation history
- **Grounding** - Google Search for accurate character info

**Location**: `us-central1`, `global`  
**Context**: 1M tokens (!!!)  
**Cost**: Medium-High  

**Capabilities**:
- ✅ Grounding with Google Search
- ✅ Code execution
- ✅ Thinking mode
- ✅ 1M token context (can analyze entire codebases!)
- ✅ Structured output

**Example**:
```python
# Optimize prompts based on generation history
prompt = """
Analyze these 100 cosplay generations and identify patterns:
- Which prompts achieved highest identity preservation?
- What lighting terms improved realism?
- Which model settings work best for each character type?

Use Google Search to verify character details.
Execute code to calculate statistical correlations.
Output optimized prompt template.
"""

response = genai_client.models.generate_content(
    model="gemini-2.5-pro",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(google_search=types.GoogleSearch()),
            types.Tool(code_execution=types.CodeExecution())
        ],
        thinking_config=types.ThinkingConfig(
            thinking_budget=10000  # Deep reasoning
        )
    )
)
```

---

### **3. Gemini 3 Pro Image Preview** (`gemini-3-pro-image-preview`)
**Use for**: Primary image generation (Nano Banana Pro)
- Ultra-realistic 4K cosplay generation
- Hidden reasoning layer
- Character consistency without LoRAs
- Professional photography quality

**Location**: `global`  
**Resolution**: Up to 4K  
**Cost**: Highest per image  

---

### **4. Gemini 2.5 Flash Image** (`gemini-2.5-flash-image`)
**Use for**: Fast image generation, fallback
- Quick iterations
- Preview generations
- Cost-efficient at scale
- Fallback when Gemini 3 is unavailable

**Location**: `us-central1`  
**Resolution**: Up to 2K  
**Cost**: Lowest per image  

---

### **5. Gemini 2.5 Flash** (`gemini-2.5-flash`)
**Use for**: Fast workers, parallel tasks
- Batch face schema extraction
- Parallel prompt generation
- Quick database queries
- Sub-agent tasks

**Location**: `us-central1`  
**Context**: 1M tokens  
**Cost**: Lowest  

---

## 🔄 **Complete Workflow Example**

```python
from google import genai
from google.genai import types

PROJECT_ID = "gifted-cooler-479623-r7"

# Initialize clients for different models
orchestrator_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
reasoning_client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
flash_client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")

# ============================================================================
# STEP 1: Orchestration (Gemini 3 Pro)
# ============================================================================

plan_response = orchestrator_client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="""
    User wants to generate Edward Elric from FMA as Dante from DMC.
    
    Plan the optimal workflow:
    1. What face schema extraction approach?
    2. Which prompt template to use?
    3. What model settings?
    4. How to validate quality?
    """
)

plan = plan_response.text

# ============================================================================
# STEP 2: Reasoning (Gemini 2.5 Pro) - Optimize Prompt
# ============================================================================

prompt_optimization = reasoning_client.models.generate_content(
    model="gemini-2.5-pro",
    contents=f"""
    Based on this plan: {plan}
    
    And our generation history showing:
    - 95% success rate with "ultra-realistic 4K" prefix
    - "visible skin pores" increases realism by 15%
    - "Sony A7R V, 85mm" improves DSLR quality
    
    Generate the optimal prompt for Edward → Dante transformation.
    
    Use Google Search to verify:
    - Dante's exact costume details
    - Edward's facial features
    
    Use code execution to calculate ideal prompt length.
    """,
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(google_search=types.GoogleSearch()),
            types.Tool(code_execution=types.CodeExecution())
        ],
        response_mime_type="application/json",
        thinking_config=types.ThinkingConfig(thinking_budget=5000)
    )
)

optimized_prompt = prompt_optimization.text

# ============================================================================
# STEP 3: Generation (Gemini 3 Pro Image)
# ============================================================================

image_response = orchestrator_client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[optimized_prompt, source_image],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="3:4",
            image_size="4K"
        )
    )
)

# ============================================================================
# STEP 4: Quality Analysis (Gemini 2.5 Pro)
# ============================================================================

quality_analysis = reasoning_client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
        "Analyze this generated cosplay image:",
        generated_image,
        source_image,
        """
        Evaluate:
        1. Identity preservation (0-100%)
        2. Costume accuracy (0-100%)
        3. Image quality (0-100%)
        4. What worked well?
        5. What could improve?
        
        Output structured JSON analysis.
        """
    ],
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)

# ============================================================================
# STEP 5: Learning (Gemini 2.5 Pro) - Extract Insights
# ============================================================================

learning = reasoning_client.models.generate_content(
    model="gemini-2.5-pro",
    contents=f"""
    Based on this generation quality: {quality_analysis.text}
    
    And our learning database showing 1,000 previous generations,
    extract actionable insights:
    
    1. What prompt patterns correlate with high quality?
    2. How should we adjust parameters for next iteration?
    3. What new techniques should we test?
    
    Execute statistical analysis code.
    Output: Structured learnings with confidence scores.
    """,
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.CodeExecution())],
        response_mime_type="application/json"
    )
)
```

---

## 📊 **Cost Optimization Strategy**

| Task | Model | Why |
|------|-------|-----|
| Planning | Gemini 3 Pro | Best orchestration |
| Prompt optimization | Gemini 2.5 Pro | Reasoning + grounding |
| Face schema extraction | Gemini 3 Pro (primary) → 2.5 Flash (fallback) | Quality first, cost second |
| Image generation | Gemini 3 Pro Image → 2.5 Flash Image | Best quality, fallback |
| Quality analysis | Gemini 2.5 Pro | Advanced vision + reasoning |
| Batch processing | Gemini 2.5 Flash | Speed + cost |
| Learning extraction | Gemini 2.5 Pro | Code execution + thinking |

---

## 🎯 **Updated Model Selection Logic**

```python
def select_model(task_type: str, priority: str = "quality") -> str:
    """
    Intelligent model selection
    """
    
    if task_type == "orchestration":
        return "gemini-3-pro-preview"
    
    elif task_type == "reasoning":
        # Use 2.5 Pro for complex reasoning
        return "gemini-2.5-pro"
    
    elif task_type == "image_generation":
        if priority == "quality":
            return "gemini-3-pro-image-preview"
        elif priority == "speed":
            return "gemini-2.5-flash-image"
    
    elif task_type == "analysis":
        # 2.5 Pro for deep analysis
        return "gemini-2.5-pro"
    
    elif task_type == "batch_worker":
        # 2.5 Flash for speed
        return "gemini-2.5-flash"
    
    return "gemini-2.5-flash"  # Safe default
```

---

## 💡 **Key Advantages of 2.5 Pro**

1. **1M Token Context** - Can analyze entire generation history
2. **Grounding** - Verify character details with Google Search
3. **Code Execution** - Statistical analysis of what works
4. **Thinking Mode** - Deep reasoning for optimization
5. **Structured Output** - Clean JSON for learnings
6. **Video Understanding** - Analyze reference videos
7. **Audio Support** - Process voice acting samples

---

## 🚀 **Integration into Yuki**

Gemini 2.5 Pro is now the **reasoning brain** of Yuki:

- **Prompt Optimizer** - Analyzes what works, improves prompts
- **Quality Analyst** - Evaluates generations with reasoning
- **Learning System** - Extracts insights from history
- **Research Assistant** - Grounds character info with search
- **Code Analyst** - Statistical analysis of patterns

**This completes the model hierarchy! 🎉**

---

**Gemini 3 Pro** = Orchestrator (delegates)  
**Gemini 2.5 Pro** ⭐ = Reasoning (optimizes)  
**Gemini 3 Pro Image** = Generation (creates)  
**Gemini 2.5 Flash** = Workers (executes)  

**Now you have the complete enterprise AI stack!** 🔥
