# Research Feasibility Analysis - Two Implementations

This repository contains TWO implementations of a research feasibility analysis system:

## 1. Rule-Based System (v1.0)

**Location:** `research_feasibility_agent/`

**How it works:** Keyword matching and predefined rules

**Run:** `python test_agent.py research_feasibility_agent/examples/mobile_app.txt`

**Pros:**
- Fast and predictable
- No API keys needed
- Deterministic results
- Good for quick assessments

**Cons:**
- ❌ Just keyword matching - no real understanding
- ❌ Fixed rules - can't adapt
- ❌ No reasoning about context
- ❌ Not truly agentic

## 2. Truly Agentic System (v2.0) ⭐ NEW!

**Location:** `agentic_system/`

**How it works:** Multi-agent coordination with LLM-powered reasoning

**Run:** `python run_agentic_system.py research_feasibility_agent/examples/mobile_app.txt`

**What makes it TRULY agentic:**
✅ **Autonomous Decision-Making** - Agents decide strategy, not just execute
✅ **Multi-Agent Coordination** - Orchestrator coordinates specialized agents
✅ **LLM Reasoning** - Actually understands and reasons, not keyword matching
✅ **Tool Selection** - Agents choose which tools to use
✅ **Iterative Refinement** - Agents iterate until confident
✅ **Self-Validation** - Agents check their own work

### Quick Comparison

| Feature | Rule-Based (v1) | Agentic (v2) |
|---------|-----------------|--------------|
| Understanding | Keywords only | LLM reasoning |
| Decision-making | Fixed rules | Autonomous |
| Workflow | Fixed | Adaptive |
| Agents | Single | Multiple coordinated |
| Tool use | Hardcoded | Agent selects |
| Iteration | No | Yes |
| Learning | No | LLM-powered |

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# For agentic system with real LLM (optional but recommended):
pip install openai anthropic

# Set API key (choose one):
export OPENAI_API_KEY=your_key        # For OpenAI GPT
export ANTHROPIC_API_KEY=your_key     # For Anthropic Claude
```

## Usage

### Rule-Based System:
```bash
python test_agent.py research_feasibility_agent/examples/ai_healthcare.txt
```

### Agentic System (Mock Mode):
```bash
python run_agentic_system.py research_feasibility_agent/examples/mobile_app.txt
```

### Agentic System (With Real LLM):
```bash
export OPENAI_API_KEY=your_key
export LLM_PROVIDER=openai
python run_agentic_system.py research_feasibility_agent/examples/quantum_computing.txt
```

## Example Projects Included

Both systems can analyze these example projects:

1. **AI Healthcare Platform** - Medical imaging AI
2. **Mobile App** - Local marketplace app
3. **Quantum Computing** - Drug discovery platform
4. **Brain-Computer Interface** - Accessibility device

## Output Comparison

### Rule-Based Output:
```
Technology: 65/100 (keyword matching)
- Found keywords: "mobile", "app", "cloud"
- Complexity: HIGH (found "integration")
- Maturity: MATURE (found "mobile")
```

### Agentic Output:
```
Technology: 72/100 (LLM reasoning)
- Agent reasoning: "The mobile app stack is mature with
  proven frameworks like React Native. However, the
  real-time features and marketplace dynamics add
  significant complexity. Integration challenges stem
  from needing to coordinate payment processing,
  location services, and user matching..."
- Confidence: HIGH
- Self-assessment: "This analysis considers real-world
  deployment patterns and team capabilities"
```

## Which Should You Use?

**Use Rule-Based System if:**
- You want quick, consistent results
- You don't have API keys
- You need deterministic output
- Speed is more important than depth

**Use Agentic System if:**
- You want deep, contextual analysis
- You have LLM API access
- You need adaptive reasoning
- Quality is more important than speed

## Documentation

- **Rule-Based System:** See `README.md` (main documentation)
- **Agentic System:** See `AGENTIC_SYSTEM.md` (detailed architecture)

## Architecture

### Rule-Based System:
```
Input → Analysis Modules → Scoring → Report
        (keyword matching)
```

### Agentic System:
```
                Orchestrator Agent
                       ↓
      ┌────────────────┼────────────────┐
      ↓                ↓                ↓
Research Agent  Specialized Agents  Validator
      ↓                ↓                ↓
      └────────────────┼────────────────┘
                       ↓
              Synthesis & Decision
```

## Key Innovation: True Agency

The agentic system is NOT just an API wrapper. It demonstrates:

1. **Orchestration** - Master agent coordinates sub-agents
2. **Autonomy** - Agents decide their own actions
3. **Collaboration** - Agents communicate and validate
4. **Adaptation** - Workflow changes based on findings
5. **Reflection** - Agents evaluate their own work

### Code Example - Agentic Decision Making:

```python
# Orchestrator DECIDES strategy
strategy = await self._decide_strategy(request)
# → Agent reasons about approach

# Research agent DECIDES what to search
queries = self._decide_search_strategy(topic)
# → Agent determines information needs

# Validator DECIDES if refinement needed
if validation['confidence'] < threshold:
    analyses = await self._refine_analyses(analyses)
# → Agent determines quality, decides to iterate
```

## Requirements

### Basic (Both Systems):
```
Python 3.8+
pydantic
```

### Agentic System (Optional for real LLM):
```
openai (for GPT-4)
anthropic (for Claude)
```

## Future Work

**Rule-Based System:**
- More sophisticated keyword databases
- Better scoring algorithms
- Domain-specific rules

**Agentic System:**
- More specialized agents
- Real web search integration
- Interactive refinement
- Learning from feedback
- Agent performance metrics

## Contributing

Both systems are open for contributions:
- Improve analysis modules
- Add new dimensions
- Enhance agent capabilities
- Better LLM prompts
- Documentation improvements

## Author

Created by Tejas Chakkarwar
Built with Fetch.AI uAgents framework

## License

Educational and research purposes

---

**For detailed agentic system documentation, see [AGENTIC_SYSTEM.md](AGENTIC_SYSTEM.md)**
