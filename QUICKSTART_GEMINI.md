# Quick Start: Gemini API (FREE!)

Get your truly agentic system running with real LLM reasoning in **5 minutes** using Google's free Gemini API!

## Step 1: Get API Key (2 minutes)

1. Go to: **https://aistudio.google.com/app/apikey**
2. Sign in with Google
3. Click "Get API Key" → "Create API Key"
4. Copy your key

## Step 2: Install SDK (1 minute)

```bash
pip install google-generativeai
```

## Step 3: Set API Key (30 seconds)

```bash
export GEMINI_API_KEY='paste-your-key-here'
```

## Step 4: Run! (1 minute)

```bash
python run_agentic_system.py research_feasibility_agent/examples/mobile_app.txt
```

## That's It! 🎉

You should see:

```
✅ Using Gemini gemini-1.5-flash (Free tier: 1500 requests/day)

================================================================================
🤖 ORCHESTRATOR: Starting agentic analysis of 'Mobile App'
================================================================================

📋 Strategy: Comprehensive analysis with external research
...
```

## What You Get

✅ **Real LLM reasoning** (not keyword matching!)
✅ **Multi-agent coordination**
✅ **Autonomous decision-making**
✅ **Iterative refinement**
✅ **1,500 free requests per day**
✅ **No credit card required**

## Try More Examples

```bash
# AI Healthcare project
python run_agentic_system.py research_feasibility_agent/examples/ai_healthcare.txt

# Quantum Computing project
python run_agentic_system.py research_feasibility_agent/examples/quantum_computing.txt

# Brain-Computer Interface
python run_agentic_system.py research_feasibility_agent/examples/brain_computer_interface.txt
```

## Analyze Your Own Project

1. Create a text file with your project description:
```bash
nano my_project.txt
```

2. Describe your project (include goals, technology, market, budget, etc.)

3. Run analysis:
```bash
python run_agentic_system.py my_project.txt
```

## Free Tier Limits

**Gemini 1.5 Flash (Default):**
- 1,500 requests per day
- 15 requests per minute
- Perfect for analyzing 50-100 projects daily!

**Each analysis uses ~10-20 requests**, so you can analyze 75-150 projects per day on the free tier!

## Troubleshooting

**Error: "GEMINI_API_KEY not set"**
```bash
# Make sure you exported it:
export GEMINI_API_KEY='your-key'

# Verify it's set:
echo $GEMINI_API_KEY
```

**Want to use a different model?**
```bash
# Use Gemini 1.5 Pro (more powerful, fewer requests):
export GEMINI_MODEL='gemini-1.5-pro'
```

## Why Gemini?

| Feature | Gemini Free | OpenAI | Anthropic |
|---------|-------------|--------|-----------|
| Cost | **FREE** | $$ | $$ |
| Requests/Day | **1,500** | Pay per use | Pay per use |
| Credit Card | **Not needed** | Required | Required |
| Setup Time | **2 minutes** | 10 minutes | 10 minutes |
| Quality | **Excellent** | Excellent | Excellent |

## Next Steps

- **Full docs:** See [GEMINI_SETUP.md](GEMINI_SETUP.md)
- **Agentic details:** See [AGENTIC_SYSTEM.md](AGENTIC_SYSTEM.md)
- **Compare systems:** See [README_AGENTIC.md](README_AGENTIC.md)

---

**You now have a truly agentic multi-agent system with real LLM reasoning, powered by free Gemini API!** 🤖✨

No more keyword matching - your agents can actually THINK and REASON about projects!
