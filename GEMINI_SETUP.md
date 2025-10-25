# Using Gemini API (Free Tier) with the Agentic System

Google's Gemini API has a **generous free tier** that's perfect for this agentic system!

## Why Gemini?

✅ **Free Tier:** 1,500 requests per day (Gemini 1.5 Flash)
✅ **Fast:** Gemini 1.5 Flash is optimized for speed
✅ **Good Quality:** Strong reasoning capabilities
✅ **No Credit Card:** Free tier doesn't require payment info

## Step 1: Get Your Gemini API Key

1. **Go to Google AI Studio:**
   - Visit: https://aistudio.google.com/app/apikey

2. **Sign in** with your Google account

3. **Create API Key:**
   - Click "Get API Key"
   - Click "Create API Key"
   - Copy your API key

## Step 2: Install Gemini SDK

```bash
pip install google-generativeai
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

## Step 3: Set Your API Key

### Option A: Environment Variable (Recommended)

**Linux/Mac:**
```bash
export GEMINI_API_KEY='AIzaSyDFAQQNtbgUVUe38uaC69PwWtBWi9R_PLQ'
export LLM_PROVIDER='gemini'
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY='your-api-key-here'
$env:LLM_PROVIDER='gemini'
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your-api-key-here
set LLM_PROVIDER=gemini
```

### Option B: .env File

Create a file named `.env` in the project root:

```bash
GEMINI_API_KEY=your-api-key-here
LLM_PROVIDER=gemini
GEMINI_MODEL=gemini-1.5-flash
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

## Step 4: Run the Agentic System

```bash
python run_agentic_system.py research_feasibility_agent/examples/mobile_app.txt
```

You should see:
```
✅ Using Gemini gemini-1.5-flash (Free tier: 1500 requests/day)

╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        TRULY AGENTIC RESEARCH FEASIBILITY SYSTEM             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## Usage Examples

### Basic Analysis:
```bash
python run_agentic_system.py research_feasibility_agent/examples/ai_healthcare.txt
```

### Different Models:

**Gemini 1.5 Flash (Default - Free, Fast):**
```bash
export GEMINI_MODEL=gemini-1.5-flash
python run_agentic_system.py research_feasibility_agent/examples/quantum_computing.txt
```

**Gemini 1.5 Pro (More powerful, still free tier):**
```bash
export GEMINI_MODEL=gemini-1.5-pro
python run_agentic_system.py research_feasibility_agent/examples/brain_computer_interface.txt
```

## Free Tier Limits

**Gemini 1.5 Flash:**
- 15 requests per minute
- 1 million tokens per minute
- 1,500 requests per day

**Gemini 1.5 Pro:**
- 2 requests per minute
- 32,000 tokens per minute
- 50 requests per day

For most analyses, you'll use about 10-20 requests per project, so the free tier is very generous!

## Configuration Options

Set these environment variables to customize:

```bash
# Required
export GEMINI_API_KEY='your-key'
export LLM_PROVIDER='gemini'

# Optional
export GEMINI_MODEL='gemini-1.5-flash'  # or 'gemini-1.5-pro'
export CONFIDENCE_THRESHOLD=0.75        # Confidence threshold
export MAX_ITERATIONS=3                 # Max refinement iterations
```

## Troubleshooting

### Error: "GEMINI_API_KEY not set"
**Solution:** Make sure you've exported the environment variable or created a .env file

### Error: "pip install google-generativeai"
**Solution:** Install the Gemini SDK:
```bash
pip install google-generativeai
```

### Error: "API key not valid"
**Solution:**
1. Go back to https://aistudio.google.com/app/apikey
2. Generate a new API key
3. Make sure you copied it correctly (no extra spaces)

### Rate Limit Error
**Solution:** You've hit the free tier limit. Wait a minute or switch to a less frequent model:
- Use `gemini-1.5-flash` (15 req/min) instead of `gemini-1.5-pro` (2 req/min)
- Wait 1 minute between analyses

## Comparison: Gemini vs Others

| Provider | Free Tier | Speed | Setup |
|----------|-----------|-------|-------|
| **Gemini 1.5 Flash** | 1,500/day | ⚡ Fast | ✅ Easy |
| Gemini 1.5 Pro | 50/day | Medium | ✅ Easy |
| OpenAI GPT-4 | ❌ No free tier | Fast | Credit card required |
| Anthropic Claude | ❌ No free tier | Fast | Credit card required |

**Winner for free tier: Gemini 1.5 Flash** 🏆

## Example Output

```bash
$ export GEMINI_API_KEY='your-key'
$ python run_agentic_system.py research_feasibility_agent/examples/mobile_app.txt

✅ Using Gemini gemini-1.5-flash (Free tier: 1500 requests/day)

================================================================================
🤖 ORCHESTRATOR: Starting agentic analysis of 'Mobile App'
================================================================================

📋 Strategy: Comprehensive analysis with external research

🔍 RESEARCH AGENT: Gathering information...
   Found 3 research results

🤖 ORCHESTRATOR: Coordinating parallel analysis across dimensions...

   🔧 Technology Agent analyzing...
      [Gemini reasoning about tech stack, complexity, risks...]
      Score: 74.5/100, Confidence: HIGH

   💰 Cost Agent analyzing...
      [Gemini analyzing budget, ROI, funding...]
      Score: 68.0/100, Confidence: MEDIUM
...
```

## Next Steps

Once you have Gemini working:

1. **Try all example projects:**
   ```bash
   python run_agentic_system.py research_feasibility_agent/examples/ai_healthcare.txt
   python run_agentic_system.py research_feasibility_agent/examples/quantum_computing.txt
   python run_agentic_system.py research_feasibility_agent/examples/brain_computer_interface.txt
   ```

2. **Analyze your own projects:**
   - Create a .txt file with your project description
   - Run: `python run_agentic_system.py your_project.txt`

3. **Experiment with models:**
   - Try both `gemini-1.5-flash` (fast) and `gemini-1.5-pro` (powerful)
   - Compare results

## Resources

- **Google AI Studio:** https://aistudio.google.com
- **Gemini API Docs:** https://ai.google.dev/docs
- **Gemini Pricing:** https://ai.google.dev/pricing
- **Get API Key:** https://aistudio.google.com/app/apikey

---

**Pro Tip:** Gemini 1.5 Flash is perfect for this agentic system because:
- Fast enough for real-time analysis
- Smart enough for complex reasoning
- Free tier is very generous
- No credit card needed!

Enjoy your truly agentic research feasibility system powered by Gemini! 🤖✨
