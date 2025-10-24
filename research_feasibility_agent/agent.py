"""
Research Feasibility Agent - Main Agent
A truly agentic system for evaluating research project feasibility

This agent autonomously:
1. Reads and understands project descriptions
2. Coordinates multiple specialized analysis modules
3. Makes intelligent decisions about feasibility
4. Generates comprehensive reports with actionable insights
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import json

from uagents import Agent, Context, Model
from pydantic import Field

# Import analysis modules
from modules.technology_analyzer import TechnologyAnalyzer
from modules.cost_analyzer import CostAnalyzer
from modules.ethical_analyzer import EthicalAnalyzer
from modules.market_analyzer import MarketAnalyzer


# Message Models for Agent Communication
class ProjectSubmission(Model):
    """Model for submitting a project for analysis"""
    project_file_path: str = Field(description="Path to the project description file")
    requester_address: Optional[str] = Field(None, description="Address of the requester")


class FeasibilityReport(Model):
    """Model for the comprehensive feasibility report"""
    project_name: str
    overall_feasibility: str
    overall_score: float
    recommendation: str
    technology_analysis: Dict[str, Any]
    cost_analysis: Dict[str, Any]
    ethical_analysis: Dict[str, Any]
    market_analysis: Dict[str, Any]
    critical_risks: list
    key_opportunities: list
    next_steps: list


# Create the Research Feasibility Agent
agent = Agent(
    name="research_feasibility_agent",
    seed="research_feasibility_seed_phrase_2024",
    port=8001,
    endpoint=["http://localhost:8001/submit"],
)

# Initialize analysis modules (these are autonomous analyzers)
tech_analyzer = TechnologyAnalyzer()
cost_analyzer = CostAnalyzer()
ethical_analyzer = EthicalAnalyzer()
market_analyzer = MarketAnalyzer()


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
    """
    Calculate weighted overall feasibility score
    Technology and Market are weighted higher as they're critical for success
    """
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
    tech_analysis: Any,
    cost_analysis: Any,
    ethical_analysis: Any,
    market_analysis: Any
) -> str:
    """
    Autonomously generate an intelligent recommendation
    This is the "agentic" decision-making part
    """
    feasibility = determine_overall_feasibility(overall_score)

    # Decision logic based on comprehensive analysis
    if feasibility == "HIGHLY FEASIBLE":
        recommendation = (
            "✅ PROCEED WITH CONFIDENCE\n\n"
            "This project demonstrates strong feasibility across all dimensions. "
            "The technology is mature enough, market timing is favorable, costs are manageable, "
            "and ethical considerations are addressable. Recommend moving forward with detailed planning."
        )

    elif feasibility == "FEASIBLE":
        # Identify which areas need attention
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
        # Identify major blockers
        blockers = []
        if tech_analysis.feasibility_score < 50:
            blockers.append(f"Technology ({tech_analysis.feasibility_score:.0f}/100) - {tech_analysis.maturity_level} maturity")
        if cost_analysis.feasibility_score < 50:
            blockers.append(f"Cost ({cost_analysis.feasibility_score:.0f}/100) - {cost_analysis.budget_category} budget required")
        if ethical_analysis.feasibility_score < 50:
            blockers.append(f"Ethics ({ethical_analysis.feasibility_score:.0f}/100) - {ethical_analysis.ethical_risk_level} risk")
        if market_analysis.feasibility_score < 50:
            blockers.append(f"Market ({market_analysis.feasibility_score:.0f}/100) - {market_analysis.market_timing} timing")

        recommendation = (
            f"⚠️ PROCEED ONLY WITH SIGNIFICANT MODIFICATIONS\n\n"
            f"Major challenges identified:\n" +
            "\n".join(f"  • {blocker}" for blocker in blockers) +
            f"\n\nRecommend substantial redesign to address these blockers or consider alternative approaches."
        )

    elif feasibility == "CHALLENGING":
        recommendation = (
            "⚠️ HIGH RISK - RECONSIDER APPROACH\n\n"
            "This project faces significant feasibility challenges across multiple dimensions. "
            "Recommend either: (1) Substantial pivot to address core issues, "
            "(2) Extended research phase to validate assumptions, or "
            "(3) Consider alternative solutions to the underlying problem."
        )

    else:  # NOT FEASIBLE
        recommendation = (
            "❌ NOT RECOMMENDED\n\n"
            "Based on comprehensive analysis, this project is not feasible in its current form. "
            "Critical barriers exist that make success highly unlikely. "
            "Recommend exploring entirely different approaches or waiting for enabling conditions to improve."
        )

    return recommendation


def identify_critical_risks(
    tech_analysis: Any,
    cost_analysis: Any,
    ethical_analysis: Any,
    market_analysis: Any
) -> list:
    """Identify the most critical risks across all dimensions"""
    critical_risks = []

    # Technology risks
    if tech_analysis.maturity_level in ["Emerging", "Obsolete"]:
        critical_risks.append(f"🔴 Technology maturity: {tech_analysis.maturity_level} - High technical risk")
    if tech_analysis.implementation_complexity in ["Very High", "High"]:
        critical_risks.append(f"🔴 Implementation complexity: {tech_analysis.implementation_complexity}")

    # Cost risks
    if cost_analysis.budget_category in ["Very High", "High"]:
        critical_risks.append(f"🔴 Capital requirements: {cost_analysis.budget_category} budget ({cost_analysis.estimated_budget_range})")

    # Ethical risks
    if ethical_analysis.ethical_risk_level in ["Critical", "High"]:
        critical_risks.append(f"🔴 Ethical concerns: {ethical_analysis.ethical_risk_level} risk level")
    if len(ethical_analysis.ethical_concerns) > 5:
        critical_risks.append(f"🔴 Multiple ethical issues: {len(ethical_analysis.ethical_concerns)} concerns identified")

    # Market risks
    if market_analysis.market_timing in ["Too Early", "Too Late"]:
        critical_risks.append(f"🔴 Market timing: {market_analysis.market_timing}")
    if "Very High" in market_analysis.competition_level:
        critical_risks.append(f"🔴 Competition: {market_analysis.competition_level}")

    return critical_risks[:10]  # Top 10 most critical


def identify_key_opportunities(
    tech_analysis: Any,
    cost_analysis: Any,
    ethical_analysis: Any,
    market_analysis: Any
) -> list:
    """Identify key opportunities and advantages"""
    opportunities = []

    # Technology opportunities
    if tech_analysis.feasibility_score >= 75:
        opportunities.append(f"✅ Strong technology foundation: {tech_analysis.maturity_level} maturity")
    if len(tech_analysis.available_technologies) > 0:
        opportunities.append(f"✅ Leverages proven technologies: {', '.join(tech_analysis.available_technologies[:3])}")

    # Cost opportunities
    if cost_analysis.budget_category in ["Minimal", "Low"]:
        opportunities.append(f"✅ Low capital requirements: {cost_analysis.estimated_budget_range}")
    if "High" in cost_analysis.roi_potential:
        opportunities.append(f"✅ Strong ROI potential: {cost_analysis.roi_potential}")

    # Ethical opportunities
    if "Positive" in ethical_analysis.social_impact:
        opportunities.append(f"✅ Positive social impact: {ethical_analysis.social_impact}")

    # Market opportunities
    if market_analysis.market_timing in ["Optimal", "Good"]:
        opportunities.append(f"✅ Excellent market timing: {market_analysis.market_timing}")
    if "Large" in market_analysis.market_size_potential or "Very Large" in market_analysis.market_size_potential:
        opportunities.append(f"✅ Large market opportunity: {market_analysis.market_size_potential}")
    if len(market_analysis.competitive_advantages) > 0:
        opportunities.append(f"✅ Competitive advantages: {market_analysis.competitive_advantages[0]}")

    return opportunities[:10]  # Top 10 opportunities


def generate_next_steps(
    overall_feasibility: str,
    tech_analysis: Any,
    cost_analysis: Any,
    ethical_analysis: Any,
    market_analysis: Any
) -> list:
    """Generate autonomous recommendations for next steps"""
    next_steps = []

    if overall_feasibility in ["HIGHLY FEASIBLE", "FEASIBLE"]:
        next_steps.extend([
            "1. Develop detailed project roadmap with milestones",
            "2. Assemble core team with necessary expertise",
            "3. Create proof-of-concept or MVP",
            "4. Conduct customer discovery interviews",
            "5. Develop detailed budget and funding strategy"
        ])

        # Add specific technical next steps
        if tech_analysis.maturity_level == "Developing":
            next_steps.append("6. Build technical prototype to validate approach")

        # Add specific market next steps
        if market_analysis.market_timing == "Early":
            next_steps.append("7. Focus initial efforts on early adopter segment")

    elif overall_feasibility == "MODERATELY FEASIBLE":
        next_steps.extend([
            "1. Conduct deep-dive feasibility study on identified risk areas",
            "2. Explore alternative technical or business approaches",
            "3. Build quick prototypes to test riskiest assumptions",
            "4. Seek expert consultation in challenging domains",
            "5. Develop detailed risk mitigation strategies"
        ])

    else:  # CHALLENGING or NOT FEASIBLE
        next_steps.extend([
            "1. Re-examine core assumptions and problem definition",
            "2. Explore alternative solutions to the underlying problem",
            "3. Consider waiting for enabling technologies/market to mature",
            "4. Consult with domain experts before proceeding",
            "5. Conduct additional research before further investment"
        ])

    return next_steps


@agent.on_event("startup")
async def startup(ctx: Context):
    """Agent startup - announce readiness"""
    ctx.logger.info(f"Research Feasibility Agent started successfully!")
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"Ready to analyze research project feasibility")


@agent.on_message(model=ProjectSubmission)
async def handle_project_submission(ctx: Context, sender: str, msg: ProjectSubmission):
    """
    Main message handler - Autonomously analyzes project feasibility
    This is the core agentic behavior
    """
    ctx.logger.info(f"Received project analysis request from {sender}")
    ctx.logger.info(f"Project file: {msg.project_file_path}")

    try:
        # Step 1: Read the project description
        ctx.logger.info("📖 Reading project description...")
        project_description = read_project_file(msg.project_file_path)

        # Extract project name from filename
        project_name = Path(msg.project_file_path).stem.replace('_', ' ').title()

        ctx.logger.info(f"Project: {project_name}")
        ctx.logger.info(f"Description length: {len(project_description)} characters")

        # Step 2: Autonomous multi-dimensional analysis
        ctx.logger.info("\n🤖 Starting autonomous feasibility analysis...")

        ctx.logger.info("  🔧 Analyzing technology feasibility...")
        tech_analysis = tech_analyzer.analyze(project_description)

        ctx.logger.info("  💰 Analyzing cost and financial feasibility...")
        cost_analysis = cost_analyzer.analyze(project_description)

        ctx.logger.info("  ⚖️  Analyzing ethical implications...")
        ethical_analysis = ethical_analyzer.analyze(project_description)

        ctx.logger.info("  📊 Analyzing market viability...")
        market_analysis = market_analyzer.analyze(project_description)

        # Step 3: Synthesize findings and make intelligent decisions
        ctx.logger.info("\n🧠 Synthesizing analysis and making recommendations...")

        overall_score = calculate_overall_score(
            tech_analysis.feasibility_score,
            cost_analysis.feasibility_score,
            ethical_analysis.feasibility_score,
            market_analysis.feasibility_score
        )

        overall_feasibility = determine_overall_feasibility(overall_score)

        # Generate intelligent recommendation
        recommendation = generate_recommendation(
            overall_score, tech_analysis, cost_analysis, ethical_analysis, market_analysis
        )

        # Identify critical risks
        critical_risks = identify_critical_risks(
            tech_analysis, cost_analysis, ethical_analysis, market_analysis
        )

        # Identify opportunities
        key_opportunities = identify_key_opportunities(
            tech_analysis, cost_analysis, ethical_analysis, market_analysis
        )

        # Generate next steps
        next_steps = generate_next_steps(
            overall_feasibility, tech_analysis, cost_analysis, ethical_analysis, market_analysis
        )

        # Step 4: Generate comprehensive report
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
                "competitive_advantages": market_analysis.competitive_advantages,
                "go_to_market": market_analysis.go_to_market_strategy
            },
            "critical_risks": critical_risks,
            "key_opportunities": key_opportunities,
            "next_steps": next_steps
        }

        # Step 5: Display comprehensive report
        print_report(report)

        # Save report to file
        output_file = f"feasibility_report_{project_name.replace(' ', '_').lower()}.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        ctx.logger.info(f"\n✅ Analysis complete! Report saved to: {output_file}")

    except FileNotFoundError as e:
        ctx.logger.error(f"❌ Error: {str(e)}")
    except Exception as e:
        ctx.logger.error(f"❌ Unexpected error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


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
    print(f"  Technology:  {report['technology_analysis']['score']}/100 ({report['technology_analysis']['maturity']} maturity)")
    print(f"  Cost:        {report['cost_analysis']['score']}/100 ({report['cost_analysis']['category']} budget)")
    print(f"  Ethics:      {report['ethical_analysis']['score']}/100 ({report['ethical_analysis']['risk_level']} risk)")
    print(f"  Market:      {report['market_analysis']['score']}/100 ({report['market_analysis']['timing']} timing)")

    print("\n" + "-"*80)
    print("CRITICAL RISKS")
    print("-"*80)
    if report['critical_risks']:
        for risk in report['critical_risks']:
            print(f"  {risk}")
    else:
        print("  ✅ No critical risks identified")

    print("\n" + "-"*80)
    print("KEY OPPORTUNITIES")
    print("-"*80)
    if report['key_opportunities']:
        for opp in report['key_opportunities']:
            print(f"  {opp}")
    else:
        print("  ⚠️  Limited opportunities identified")

    print("\n" + "-"*80)
    print("RECOMMENDED NEXT STEPS")
    print("-"*80)
    for step in report['next_steps']:
        print(f"  {step}")

    print("\n" + "-"*80)
    print("DETAILED ANALYSIS")
    print("-"*80)

    print(f"\n📊 MARKET ANALYSIS:")
    print(f"  Market Size: {report['market_analysis']['market_size']}")
    print(f"  Competition: {report['market_analysis']['competition']}")
    print(f"  GTM Strategy: {report['market_analysis']['go_to_market']}")

    print(f"\n💰 COST ANALYSIS:")
    print(f"  Budget Range: {report['cost_analysis']['budget_range']}")
    print(f"  ROI Potential: {report['cost_analysis']['roi_potential']}")

    print(f"\n⚖️  ETHICAL ANALYSIS:")
    print(f"  Social Impact: {report['ethical_analysis']['social_impact']}")
    if report['ethical_analysis']['concerns']:
        print(f"  Key Concerns: {len(report['ethical_analysis']['concerns'])} identified")

    print(f"\n🔧 TECHNOLOGY ANALYSIS:")
    print(f"  Implementation Complexity: {report['technology_analysis']['complexity']}")
    print(f"  Estimated Timeline: {report['technology_analysis']['timeline']}")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║        RESEARCH FEASIBILITY AGENT - Fetch.AI Agent           ║
    ║                                                               ║
    ║  A truly agentic system for autonomous project evaluation    ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝

    Agent Address: {agent_address}

    To analyze a project:
    1. Create a text file with your project description
    2. Run: python test_agent.py <project_file_path>

    The agent will autonomously:
    - Analyze technology feasibility
    - Evaluate costs and ROI
    - Assess ethical implications
    - Determine market viability
    - Generate intelligent recommendations

    Starting agent...
    """.format(agent_address=agent.address))

    agent.run()
