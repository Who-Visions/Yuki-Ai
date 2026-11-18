<!-- nougen-readme-compiler: v1 -->

<!-- nougen-readme-compiler: extensions: footer -->

# 🦊 Yuki Agent v0.05

A Vertex AI Reasoning Engine agent powered by Gemini 3 Pro.

## 📚 Contents
- [Quick Start](#quick-start)
- [Files](#files)
- [Current Deployment](#current-deployment)
- [Test Example](#test-example)
- [Documentation](#documentation)
- [About Yuki](#about-yuki)

## 🚀 Quick Start

### Local Testing (No Deployment)

```bash
# Windows
activate_yuki.bat
python run_yuki.py

# Or directly
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run_yuki.py
```

### Deploy to Vertex AI

⚠️ **Warning:** Only run this when you actually want to deploy a new version!

```bash
python deploy_yuki.py
```

## 📋 Files

- **`deploy_yuki.py`** - Main deployment script (deploys to Vertex AI)
- **`run_yuki.py`** - Test runner (no deployment, interactive)
- **`test_yuki_final.py`** - Quick verification test
- **`activate_yuki.bat`** - Activate venv with helper info
- **`tools.py`** - Tool definitions (get_current_time, add_numbers)
- **`DEPLOYMENT_YUKI.md`** - Complete deployment guide
- **`DEPLOYMENT_LOG.md`** - Full session history and learnings

## 🎯 Current Deployment

**Resource Name:**
```
projects/914641083224/locations/us-central1/reasoningEngines/2780528567203659776
```

**Deployed:** 2025-12-01 08:01:43
**Model:** gemini-3-pro-preview
**Location:** us-central1 (with global routing for Gemini 3)

## 🧪 Test Example

```python
import vertexai
from vertexai.preview import reasoning_engines

vertexai.init(project="gifted-cooler-479623-r7", location="us-central1")

agent = reasoning_engines.ReasoningEngine(
    "projects/914641083224/locations/us-central1/reasoningEngines/2780528567203659776"
)

response = agent.query(user_instruction="What time is it?")
print(response)
# {'output': 'The current time is 2025-12-01 12:47:08 UTC.'}
```

## 📚 Documentation

See **DEPLOYMENT_YUKI.md** for:
- Architecture details
- Configuration guide
- Deployment steps
- Troubleshooting

## 🦊 About Yuki

Yuki is a sophisticated AI agent designed to serve as the "Cosplay Preview Architect" for the Nano Banana 3.0 render pipeline. She acts as an intelligent interface between user selfies and the cosplay rendering system, using advanced reasoning capabilities to guide the preview generation process.

**Key Features:**
- ✅ Gemini 3 Pro intelligence
- ✅ Dynamic global routing for model access
- ✅ Tool integration ready
- ✅ Production-ready error handling
- ✅ Lazy initialization for deployed environments

## 🔗 Links

- [Deployment guide (DEPLOYMENT_YUKI.md)](<https://github.com/Who-Visions/Yuki-Ai/blob/main/DEPLOYMENT_YUKI.md>)
- [Source Repository](<https://github.com/Who-Visions/Yuki-Ai>)

Built with 🤍 by Who Visions LLC
