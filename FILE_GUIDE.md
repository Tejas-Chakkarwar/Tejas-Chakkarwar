# 📁 File Structure Guide - What Each File Does

## ✅ ESSENTIAL FILES (Keep These!)

### 🚀 **Main Entry Points** (How to Run)

| File | Purpose | How to Use |
|------|---------|------------|
| **`run_agentic_system.py`** | **⭐ MAIN FILE** - Run the truly agentic system with LLM reasoning | `python run_agentic_system.py research_feasibility_agent/examples/mobile_app.txt` |
| **`test_agent.py`** | Run the rule-based system (keyword matching, no LLM needed) | `python test_agent.py research_feasibility_agent/examples/mobile_app.txt` |

**Which one to use?**
- **Use `run_agentic_system.py`** if you have Gemini/OpenAI/Anthropic API key (RECOMMENDED!)
- **Use `test_agent.py`** if you want quick results without API key

---

### 📖 **Documentation** (Read These!)

| File | What It Explains | Read When |
|------|------------------|-----------|
| **`QUICKSTART_GEMINI.md`** | ⚡ **START HERE!** 5-minute setup with free Gemini API | First time setup |
| **`GEMINI_SETUP.md`** | Detailed Gemini setup, troubleshooting, configuration | Need more details |
| **`AGENTIC_SYSTEM.md`** | Deep dive: Why it's agentic, architecture, comparison | Want to understand how it works |
| **`README_AGENTIC.md`** | Comparison of both systems (rule-based vs agentic) | Deciding which to use |
| **`README.md`** | Original documentation for rule-based system | Using rule-based system |

**Reading Order:**
1. `QUICKSTART_GEMINI.md` - Get started fast
2. `README_AGENTIC.md` - Understand the two systems
3. `AGENTIC_SYSTEM.md` - Deep technical dive (if interested)

---

### 🤖 **Agentic System** (Truly Agentic - LLM Powered)

```
agentic_system/                      ⭐ THE GOOD STUFF - Multi-agent system
├── orchestrator.py                  Main brain - coordinates all agents
├── config.py                        Configuration (API keys, models)
├── agents/
│   ├── base_agent.py               Core agentic capabilities (all agents inherit)
│   ├── research_agent.py           Autonomous information gathering
│   └── technology_agent.py         LLM-powered tech analysis
├── models/
│   └── messages.py                 Inter-agent communication
└── tools/
    ├── llm_tool.py                 ⭐ LLM reasoning (Gemini/OpenAI/Anthropic)
    └── web_search_tool.py          Web search capabilities
```

**This is the MAIN system** - Uses real LLM reasoning, not keyword matching!

---

### 🔧 **Rule-Based System** (Old System - Keyword Matching)

```
research_feasibility_agent/          Original rule-based system
├── agent.py                         Fetch.AI uAgent wrapper
├── modules/
│   ├── technology_analyzer.py      Keyword-based tech analysis
│   ├── cost_analyzer.py            Keyword-based cost analysis
│   ├── ethical_analyzer.py         Keyword-based ethical analysis
│   └── market_analyzer.py          Keyword-based market analysis
└── examples/                        ⭐ Example projects (KEEP THESE!)
    ├── ai_healthcare.txt
    ├── mobile_app.txt
    ├── quantum_computing.txt
    └── brain_computer_interface.txt
```

**Still useful for:**
- Quick analysis without API key
- When you want deterministic results
- Comparing with agentic system

---

### 🗂️ **Configuration Files**

| File | Purpose | Keep? |
|------|---------|-------|
| **`requirements.txt`** | Python dependencies to install | ✅ YES |
| **`.gitignore`** | Git ignore rules | ✅ YES |

---

## ❌ NOT ESSENTIAL (Can Delete)

### 📊 **Generated Reports** (Output Files)

These are just example outputs - safe to delete:

| File | What It Is | Delete? |
|------|------------|---------|
| `agentic_report_mobile_app.json` | Sample output from agentic system | ✅ Safe to delete |
| `feasibility_report_mobile_app.json` | Sample output from rule-based system | ✅ Safe to delete |
| `feasibility_report_ai_healthcare.json` | Sample output from rule-based system | ✅ Safe to delete |

**Note:** New reports are generated each time you run analysis

---

### 🗑️ **Unused Files**

| File | What It Is | Delete? |
|------|------------|---------|
| `names.txt` | Empty placeholder file | ✅ DELETE - Not used |

---

## 📋 Summary: What to Keep vs Delete

### ✅ **KEEP (Essential):**

**For Running:**
- `run_agentic_system.py` ⭐ Main entry point for agentic system
- `test_agent.py` - Entry point for rule-based system
- `agentic_system/` folder - The actual agentic system
- `research_feasibility_agent/` folder - Rule-based system + examples
- `requirements.txt` - Dependencies

**For Setup/Docs:**
- `QUICKSTART_GEMINI.md` ⭐ Start here!
- `GEMINI_SETUP.md` - Setup details
- `AGENTIC_SYSTEM.md` - Deep dive
- `README_AGENTIC.md` - Comparison
- `README.md` - Original docs

**Configuration:**
- `.gitignore` - Git configuration

### ❌ **CAN DELETE (Non-Essential):**

**Generated Output:**
- `agentic_report_mobile_app.json` - Sample output
- `feasibility_report_mobile_app.json` - Sample output
- `feasibility_report_ai_healthcare.json` - Sample output

**Unused:**
- `names.txt` - Empty placeholder

---

## 🎯 Quick Decision Guide

**Want to analyze a project?**
1. With API key: `python run_agentic_system.py your_project.txt`
2. Without API key: `python test_agent.py your_project.txt`

**Want to set up Gemini (FREE)?**
- Read: `QUICKSTART_GEMINI.md`

**Want to understand the system?**
- Read: `README_AGENTIC.md` then `AGENTIC_SYSTEM.md`

**Want to customize?**
- Edit: `agentic_system/config.py`

---

## 🔄 Recommended Cleanup

```bash
# Delete generated reports (they'll be recreated)
rm agentic_report_*.json
rm feasibility_report_*.json

# Delete unused file
rm names.txt
```

After cleanup, you'll have a clean, organized repository with only essential files!

---

## 📊 File Count by Type

| Type | Count | Purpose |
|------|-------|---------|
| 🚀 Entry Points | 2 | `run_agentic_system.py`, `test_agent.py` |
| 📖 Documentation | 5 | Setup guides and explanations |
| 🤖 Agentic System | 10+ | The truly agentic multi-agent system |
| 🔧 Rule-Based System | 8+ | Original keyword-matching system |
| 📄 Examples | 4 | Sample projects to analyze |
| ⚙️ Config | 2 | `requirements.txt`, `.gitignore` |
| 🗑️ Deletable | 4 | Generated reports + empty file |

**Total Essential Files:** ~31
**Total Deletable Files:** ~4
