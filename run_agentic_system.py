"""
Run the Truly Agentic Research Feasibility System

This demonstrates REAL agentic behavior:
- Autonomous decision-making
- Multi-agent coordination
- Tool selection and use
- Iterative refinement
- LLM-powered reasoning (not just keyword matching)
"""

import asyncio
import sys
import os
from pathlib import Path

# Add agentic_system to path
sys.path.insert(0, str(Path(__file__).parent))

from agentic_system.orchestrator import OrchestratorAgent
from agentic_system.models import ProjectAnalysisRequest
from agentic_system.config import Config


def print_final_report(decision):
    """Print beautiful final report"""
    print("\n" + "="*80)
    print("AGENTIC RESEARCH FEASIBILITY ANALYSIS - FINAL REPORT")
    print("="*80)

    print(f"\nOVERALL FEASIBILITY: {decision.overall_feasibility}")
    print(f"Overall Score: {decision.overall_score:.1f}/100")
    print(f"Confidence: {decision.confidence}")
    print(f"Analysis Quality: {decision.analysis_quality}")

    print("\n" + "-"*80)
    print("ORCHESTRATOR'S DECISION")
    print("-"*80)
    print(decision.recommendation)

    print("\n" + "-"*80)
    print("AGENT REASONING")
    print("-"*80)
    print(decision.decision_reasoning[:800])
    if len(decision.decision_reasoning) > 800:
        print("   [... full reasoning in JSON output]")

    print("\n" + "-"*80)
    print("DIMENSION SCORES (Weighted: Tech 30%, Market 30%, Cost 20%, Ethics 20%)")
    print("-"*80)
    for dim, score in decision.dimension_scores.items():
        print(f"  {dim.capitalize():12} {score:>5.1f}/100")

    print("\n" + "-"*80)
    print("CRITICAL RISKS IDENTIFIED BY AGENTS")
    print("-"*80)
    if decision.critical_risks:
        for i, risk in enumerate(decision.critical_risks, 1):
            print(f"  {i}. [{risk['dimension'].upper()}] {risk['risk'][:100]}")
            print(f"     Severity: {risk['severity']}, Impact: {risk['score_impact']}")
    else:
        print("  No critical risks identified")

    print("\n" + "-"*80)
    print("KEY OPPORTUNITIES IDENTIFIED BY AGENTS")
    print("-"*80)
    if decision.key_opportunities:
        for i, opp in enumerate(decision.key_opportunities, 1):
            print(f"  {i}. [{opp['dimension'].upper()}] {opp['opportunity'][:100]}")
    else:
        print("  Limited opportunities identified")

    print("\n" + "-"*80)
    print("ORCHESTRATOR'S RECOMMENDED NEXT STEPS")
    print("-"*80)
    for i, step in enumerate(decision.next_steps, 1):
        print(f"  {i}. {step}")

    print("\n" + "="*80)
    print("END OF AGENTIC ANALYSIS")
    print("="*80 + "\n")


async def analyze_project_file(file_path: str):
    """Analyze a project from a file"""
    # Read project file
    try:
        with open(file_path, 'r') as f:
            project_description = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        return

    project_name = Path(file_path).stem.replace('_', ' ').title()

    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        TRULY AGENTIC RESEARCH FEASIBILITY SYSTEM             ║
║                                                               ║
║  Multi-Agent Coordination • LLM Reasoning • Autonomous       ║
║  Decision-Making • Iterative Refinement • Tool Selection     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Project: {project_name}
File: {file_path}
LLM Provider: {Config.LLM_PROVIDER}
Confidence Threshold: {Config.CONFIDENCE_THRESHOLD}
Max Iterations: {Config.MAX_ITERATIONS}
    """)

    # Create orchestrator
    orchestrator = OrchestratorAgent()

    # Create analysis request
    request = ProjectAnalysisRequest(
        project_description=project_description,
        project_name=project_name,
        requester_address="user",
        analysis_depth="comprehensive"
    )

    # Run agentic analysis
    decision = await orchestrator.analyze_project(request)

    # Print results
    print_final_report(decision)

    # Save detailed JSON report
    import json
    output_file = f"agentic_report_{project_name.replace(' ', '_').lower()}.json"
    with open(output_file, 'w') as f:
        json.dump({
            'project_name': project_name,
            'overall_feasibility': decision.overall_feasibility,
            'overall_score': decision.overall_score,
            'confidence': decision.confidence,
            'recommendation': decision.recommendation,
            'reasoning': decision.decision_reasoning,
            'dimension_scores': decision.dimension_scores,
            'critical_risks': decision.critical_risks,
            'key_opportunities': decision.key_opportunities,
            'next_steps': decision.next_steps,
            'analysis_quality': decision.analysis_quality,
            'assumptions': decision.assumptions_made,
            'limitations': decision.limitations
        }, f, indent=2)

    print(f"📄 Detailed report saved to: {output_file}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        TRULY AGENTIC RESEARCH FEASIBILITY SYSTEM             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

This is NOT just keyword matching - it's REAL agentic behavior!

Features:
✓ LLM-powered reasoning (not keyword matching)
✓ Autonomous decision-making
✓ Multi-agent coordination
✓ Iterative refinement
✓ Tool selection and use
✓ Self-reflection and validation

Usage:
  python run_agentic_system.py <project_file>

Examples:
  python run_agentic_system.py research_feasibility_agent/examples/ai_healthcare.txt
  python run_agentic_system.py research_feasibility_agent/examples/mobile_app.txt
  python run_agentic_system.py research_feasibility_agent/examples/quantum_computing.txt

Configuration (via environment variables):
  LLM_PROVIDER=openai|anthropic|mock (default: mock)
  OPENAI_API_KEY=your_key (for OpenAI)
  ANTHROPIC_API_KEY=your_key (for Claude)
  CONFIDENCE_THRESHOLD=0.75 (default: 0.75)
  MAX_ITERATIONS=3 (default: 3)

Note: Without API keys, system runs in mock mode with simulated LLM responses.
      For TRUE agentic reasoning, provide API keys for OpenAI or Anthropic.
        """)
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)

    # Run async analysis
    asyncio.run(analyze_project_file(file_path))


if __name__ == "__main__":
    main()
