"""
Test script for Research Feasibility Agent
This script allows you to test the agent with project idea files
"""

import sys
import os
import asyncio
from pathlib import Path

# Add the research_feasibility_agent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'research_feasibility_agent'))

from modules.technology_analyzer import TechnologyAnalyzer
from modules.cost_analyzer import CostAnalyzer
from modules.ethical_analyzer import EthicalAnalyzer
from modules.market_analyzer import MarketAnalyzer
import json


def read_project_file(file_path: str) -> str:
    """Read project description from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Project file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading project file: {str(e)}")


def calculate_overall_score(
    tech_score: float,
    cost_score: float,
    ethical_score: float,
    market_score: float
) -> float:
    """Calculate weighted overall feasibility score"""
    weights = {
        'technology': 0.30,
        'market': 0.30,
        'cost': 0.20,
        'ethical': 0.20
    }

    overall = (
        tech_score * weights['technology'] +
        market_score * weights['market'] +
        cost_score * weights['cost'] +
        ethical_score * weights['ethical']
    )

    return round(overall, 2)


def determine_overall_feasibility(score: float) -> str:
    """Determine overall feasibility category"""
    if score >= 80:
        return "HIGHLY FEASIBLE"
    elif score >= 65:
        return "FEASIBLE"
    elif score >= 50:
        return "MODERATELY FEASIBLE"
    elif score >= 35:
        return "CHALLENGING"
    else:
        return "NOT FEASIBLE"


def generate_recommendation(
    overall_score: float,
    tech_analysis,
    cost_analysis,
    ethical_analysis,
    market_analysis
) -> str:
    """Generate intelligent recommendation"""
    feasibility = determine_overall_feasibility(overall_score)

    if feasibility == "HIGHLY FEASIBLE":
        recommendation = (
            "✅ PROCEED WITH CONFIDENCE\n\n"
            "This project demonstrates strong feasibility across all dimensions. "
            "The technology is mature enough, market timing is favorable, costs are manageable, "
            "and ethical considerations are addressable. Recommend moving forward with detailed planning."
        )

    elif feasibility == "FEASIBLE":
        weak_areas = []
        if tech_analysis.feasibility_score < 70:
            weak_areas.append("technology")
        if cost_analysis.feasibility_score < 70:
            weak_areas.append("cost")
        if ethical_analysis.feasibility_score < 70:
            weak_areas.append("ethics")
        if market_analysis.feasibility_score < 70:
            weak_areas.append("market")

        recommendation = (
            f"✅ PROCEED WITH CAUTION\n\n"
            f"This project is feasible but requires attention to: {', '.join(weak_areas)}. "
            f"Develop detailed mitigation strategies for identified risks before full commitment. "
            f"Consider starting with a proof-of-concept or pilot program."
        )

    elif feasibility == "MODERATELY FEASIBLE":
        blockers = []
        if tech_analysis.feasibility_score < 50:
            blockers.append(f"Technology ({tech_analysis.feasibility_score:.0f}/100)")
        if cost_analysis.feasibility_score < 50:
            blockers.append(f"Cost ({cost_analysis.feasibility_score:.0f}/100)")
        if ethical_analysis.feasibility_score < 50:
            blockers.append(f"Ethics ({ethical_analysis.feasibility_score:.0f}/100)")
        if market_analysis.feasibility_score < 50:
            blockers.append(f"Market ({market_analysis.feasibility_score:.0f}/100)")

        recommendation = (
            f"⚠️ PROCEED ONLY WITH SIGNIFICANT MODIFICATIONS\n\n"
            f"Major challenges identified:\n" +
            "\n".join(f"  • {blocker}" for blocker in blockers) +
            f"\n\nRecommend substantial redesign to address these blockers."
        )

    elif feasibility == "CHALLENGING":
        recommendation = (
            "⚠️ HIGH RISK - RECONSIDER APPROACH\n\n"
            "This project faces significant feasibility challenges. "
            "Recommend either substantial pivot or extended research phase."
        )

    else:
        recommendation = (
            "❌ NOT RECOMMENDED\n\n"
            "Based on comprehensive analysis, this project is not feasible in its current form."
        )

    return recommendation


def print_report(report: dict):
    """Print a beautifully formatted report"""
    print("\n" + "="*80)
    print("RESEARCH PROJECT FEASIBILITY ANALYSIS REPORT")
    print("="*80)
    print(f"\nProject: {report['project_name']}")
    print(f"\nOVERALL FEASIBILITY: {report['overall_feasibility']}")
    print(f"Overall Score: {report['overall_score']}/100")
    print("\n" + "-"*80)
    print("RECOMMENDATION")
    print("-"*80)
    print(report['recommendation'])

    print("\n" + "-"*80)
    print("FEASIBILITY SCORES BY DIMENSION")
    print("-"*80)
    print(f"  Technology:  {report['technology_analysis']['score']:.1f}/100 ({report['technology_analysis']['maturity']} maturity)")
    print(f"  Cost:        {report['cost_analysis']['score']:.1f}/100 ({report['cost_analysis']['category']} budget)")
    print(f"  Ethics:      {report['ethical_analysis']['score']:.1f}/100 ({report['ethical_analysis']['risk_level']} risk)")
    print(f"  Market:      {report['market_analysis']['score']:.1f}/100 ({report['market_analysis']['timing']} timing)")

    print("\n" + "-"*80)
    print("CRITICAL RISKS")
    print("-"*80)
    if report.get('critical_risks'):
        for risk in report['critical_risks']:
            print(f"  {risk}")
    else:
        print("  ✅ No critical risks identified")

    print("\n" + "-"*80)
    print("KEY OPPORTUNITIES")
    print("-"*80)
    if report.get('key_opportunities'):
        for opp in report['key_opportunities']:
            print(f"  {opp}")
    else:
        print("  ⚠️  Limited opportunities identified")

    print("\n" + "-"*80)
    print("DETAILED ANALYSIS")
    print("-"*80)

    print(f"\n📊 MARKET ANALYSIS:")
    print(f"  Market Size: {report['market_analysis']['market_size']}")
    print(f"  Competition: {report['market_analysis']['competition']}")
    if report['market_analysis'].get('adoption_barriers'):
        print(f"  Adoption Barriers: {len(report['market_analysis']['adoption_barriers'])} identified")

    print(f"\n💰 COST ANALYSIS:")
    print(f"  Budget Range: {report['cost_analysis']['budget_range']}")
    print(f"  ROI Potential: {report['cost_analysis']['roi_potential']}")

    print(f"\n⚖️  ETHICAL ANALYSIS:")
    print(f"  Social Impact: {report['ethical_analysis']['social_impact']}")
    if report['ethical_analysis'].get('concerns'):
        print(f"  Ethical Concerns: {len(report['ethical_analysis']['concerns'])} identified")

    print(f"\n🔧 TECHNOLOGY ANALYSIS:")
    print(f"  Implementation Complexity: {report['technology_analysis']['complexity']}")
    print(f"  Estimated Timeline: {report['technology_analysis']['timeline']}")

    print("\n" + "="*80 + "\n")


def analyze_project(file_path: str):
    """Main analysis function"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║        RESEARCH FEASIBILITY AGENT - Analysis Starting        ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

    # Initialize analyzers
    tech_analyzer = TechnologyAnalyzer()
    cost_analyzer = CostAnalyzer()
    ethical_analyzer = EthicalAnalyzer()
    market_analyzer = MarketAnalyzer()

    # Read project file
    print(f"📖 Reading project file: {file_path}")
    project_description = read_project_file(file_path)
    project_name = Path(file_path).stem.replace('_', ' ').title()

    print(f"Project: {project_name}")
    print(f"Description length: {len(project_description)} characters\n")

    # Perform analysis
    print("🤖 Starting autonomous feasibility analysis...\n")

    print("  🔧 Analyzing technology feasibility...")
    tech_analysis = tech_analyzer.analyze(project_description)

    print("  💰 Analyzing cost and financial feasibility...")
    cost_analysis = cost_analyzer.analyze(project_description)

    print("  ⚖️  Analyzing ethical implications...")
    ethical_analysis = ethical_analyzer.analyze(project_description)

    print("  📊 Analyzing market viability...")
    market_analysis = market_analyzer.analyze(project_description)

    print("\n🧠 Synthesizing analysis and generating recommendations...\n")

    # Calculate overall score
    overall_score = calculate_overall_score(
        tech_analysis.feasibility_score,
        cost_analysis.feasibility_score,
        ethical_analysis.feasibility_score,
        market_analysis.feasibility_score
    )

    overall_feasibility = determine_overall_feasibility(overall_score)

    # Generate recommendation
    recommendation = generate_recommendation(
        overall_score, tech_analysis, cost_analysis, ethical_analysis, market_analysis
    )

    # Identify critical risks
    critical_risks = []
    if tech_analysis.maturity_level in ["Emerging", "Obsolete"]:
        critical_risks.append(f"🔴 Technology maturity: {tech_analysis.maturity_level}")
    if cost_analysis.budget_category in ["Very High", "High"]:
        critical_risks.append(f"🔴 High capital requirements: {cost_analysis.estimated_budget_range}")
    if ethical_analysis.ethical_risk_level in ["Critical", "High"]:
        critical_risks.append(f"🔴 Ethical concerns: {ethical_analysis.ethical_risk_level} risk")
    if market_analysis.market_timing in ["Too Early", "Too Late"]:
        critical_risks.append(f"🔴 Market timing: {market_analysis.market_timing}")

    # Identify opportunities
    key_opportunities = []
    if tech_analysis.feasibility_score >= 75:
        key_opportunities.append(f"✅ Strong technology foundation")
    if "High" in cost_analysis.roi_potential:
        key_opportunities.append(f"✅ Strong ROI potential")
    if "Positive" in ethical_analysis.social_impact:
        key_opportunities.append(f"✅ Positive social impact")
    if market_analysis.market_timing in ["Optimal", "Good"]:
        key_opportunities.append(f"✅ Excellent market timing")

    # Create report
    report = {
        "project_name": project_name,
        "overall_feasibility": overall_feasibility,
        "overall_score": overall_score,
        "recommendation": recommendation,
        "technology_analysis": {
            "score": tech_analysis.feasibility_score,
            "maturity": tech_analysis.maturity_level,
            "complexity": tech_analysis.implementation_complexity,
            "timeline": tech_analysis.estimated_development_time,
            "risks": tech_analysis.risks,
            "recommendations": tech_analysis.recommendations
        },
        "cost_analysis": {
            "score": cost_analysis.feasibility_score,
            "budget_range": cost_analysis.estimated_budget_range,
            "category": cost_analysis.budget_category,
            "roi_potential": cost_analysis.roi_potential,
            "breakdown": cost_analysis.cost_breakdown,
            "funding_sources": cost_analysis.funding_sources
        },
        "ethical_analysis": {
            "score": ethical_analysis.feasibility_score,
            "risk_level": ethical_analysis.ethical_risk_level,
            "concerns": ethical_analysis.ethical_concerns,
            "social_impact": ethical_analysis.social_impact,
            "privacy_implications": ethical_analysis.privacy_implications,
            "required_safeguards": ethical_analysis.required_safeguards
        },
        "market_analysis": {
            "score": market_analysis.feasibility_score,
            "timing": market_analysis.market_timing,
            "market_size": market_analysis.market_size_potential,
            "competition": market_analysis.competition_level,
            "adoption_barriers": market_analysis.adoption_barriers,
            "competitive_advantages": market_analysis.competitive_advantages
        },
        "critical_risks": critical_risks,
        "key_opportunities": key_opportunities
    }

    # Print report
    print_report(report)

    # Save report
    output_file = f"feasibility_report_{project_name.replace(' ', '_').lower()}.json"
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"✅ Analysis complete! Report saved to: {output_file}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
Usage: python test_agent.py <project_file_path>

Example:
  python test_agent.py research_feasibility_agent/examples/ai_healthcare.txt

Available example projects:
  - research_feasibility_agent/examples/ai_healthcare.txt
  - research_feasibility_agent/examples/quantum_computing.txt
  - research_feasibility_agent/examples/mobile_app.txt
        """)
        sys.exit(1)

    project_file = sys.argv[1]

    if not os.path.exists(project_file):
        print(f"❌ Error: File not found: {project_file}")
        sys.exit(1)

    try:
        analyze_project(project_file)
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
