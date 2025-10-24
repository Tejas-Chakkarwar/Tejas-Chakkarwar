"""
Cost Analysis Module
Evaluates the financial feasibility and cost structure of research projects
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class CostAnalysis:
    feasibility_score: float  # 0-100
    estimated_budget_range: str
    budget_category: str  # Minimal, Low, Medium, High, Very High
    cost_breakdown: Dict[str, str]
    funding_requirements: List[str]
    cost_risks: List[str]
    cost_optimization_opportunities: List[str]
    roi_potential: str
    funding_sources: List[str]
    details: str


class CostAnalyzer:
    """Analyzes financial feasibility and cost structure"""

    def __init__(self):
        # Cost indicators by category
        self.high_cost_indicators = [
            "quantum", "satellite", "space", "clinical trial", "pharmaceutical",
            "large-scale infrastructure", "data center", "fusion", "particle accelerator",
            "supercomputer", "brain-computer", "neural implant", "chip fabrication"
        ]

        self.moderate_cost_indicators = [
            "machine learning training", "cloud infrastructure", "autonomous vehicle",
            "robotics", "drone", "iot network", "blockchain network", "ar/vr",
            "biotech", "genetic", "3d printing", "pilot study"
        ]

        self.low_cost_indicators = [
            "mobile app", "web application", "software tool", "algorithm",
            "simulation", "prototype", "proof of concept", "survey", "analysis"
        ]

        # Resource cost factors
        self.resource_multipliers = {
            "team_size_small": ("1-3 people", 1.0),
            "team_size_medium": ("4-10 people", 2.5),
            "team_size_large": ("10+ people", 5.0),
            "duration_short": ("< 6 months", 1.0),
            "duration_medium": ("6-12 months", 2.0),
            "duration_long": ("> 12 months", 3.5)
        }

    def analyze(self, project_description: str) -> CostAnalysis:
        """Perform comprehensive cost analysis"""
        project_lower = project_description.lower()

        # Estimate budget category
        budget_category, base_cost = self._estimate_budget_category(project_lower)

        # Calculate detailed cost breakdown
        cost_breakdown = self._generate_cost_breakdown(project_lower, budget_category)

        # Estimate budget range
        budget_range = self._estimate_budget_range(budget_category, project_lower)

        # Identify funding requirements
        funding_reqs = self._identify_funding_requirements(budget_category, project_lower)

        # Identify cost risks
        cost_risks = self._identify_cost_risks(project_lower, budget_category)

        # Find optimization opportunities
        optimizations = self._find_optimization_opportunities(project_lower, cost_breakdown)

        # Assess ROI potential
        roi_potential = self._assess_roi_potential(project_lower, budget_category)

        # Suggest funding sources
        funding_sources = self._suggest_funding_sources(budget_category, project_lower)

        # Calculate feasibility score
        feasibility_score = self._calculate_feasibility_score(
            budget_category, len(cost_risks), len(optimizations), roi_potential
        )

        # Generate detailed analysis
        details = self._generate_details(
            project_description, budget_category, cost_breakdown, roi_potential
        )

        return CostAnalysis(
            feasibility_score=round(feasibility_score, 2),
            estimated_budget_range=budget_range,
            budget_category=budget_category,
            cost_breakdown=cost_breakdown,
            funding_requirements=funding_reqs,
            cost_risks=cost_risks,
            cost_optimization_opportunities=optimizations,
            roi_potential=roi_potential,
            funding_sources=funding_sources,
            details=details
        )

    def _estimate_budget_category(self, text: str) -> Tuple[str, float]:
        """Estimate the budget category of the project"""
        cost_score = 0

        # Check for high-cost indicators
        for indicator in self.high_cost_indicators:
            if indicator in text:
                cost_score += 40

        # Check for moderate-cost indicators
        for indicator in self.moderate_cost_indicators:
            if indicator in text:
                cost_score += 20

        # Check for low-cost indicators
        for indicator in self.low_cost_indicators:
            if indicator in text:
                cost_score += 5

        # Scale and complexity factors
        if any(word in text for word in ["large-scale", "global", "nationwide"]):
            cost_score += 30

        if any(word in text for word in ["hardware", "manufacturing", "production"]):
            cost_score += 25

        if any(word in text for word in ["hiring", "team", "staff", "employees"]):
            cost_score += 15

        if any(word in text for word in ["cloud", "infrastructure", "servers"]):
            cost_score += 10

        # Determine category
        if cost_score >= 80:
            return "Very High", 100
        elif cost_score >= 50:
            return "High", 80
        elif cost_score >= 25:
            return "Medium", 60
        elif cost_score >= 10:
            return "Low", 40
        else:
            return "Minimal", 20

    def _generate_cost_breakdown(self, text: str, category: str) -> Dict[str, str]:
        """Generate detailed cost breakdown"""
        breakdown = {}

        # Base cost multipliers by category
        multipliers = {
            "Minimal": 1,
            "Low": 5,
            "Medium": 25,
            "High": 100,
            "Very High": 500
        }
        base = multipliers.get(category, 10)

        # Personnel costs (usually largest component)
        if any(word in text for word in ["team", "developer", "researcher", "scientist"]):
            breakdown["Personnel"] = f"${base * 50}k - ${base * 100}k (40-50% of budget)"
        else:
            breakdown["Personnel"] = f"${base * 30}k - ${base * 60}k (30-40% of budget)"

        # Technology and infrastructure
        if any(word in text for word in ["hardware", "equipment", "device", "server"]):
            breakdown["Technology & Equipment"] = f"${base * 20}k - ${base * 50}k (20-30% of budget)"
        else:
            breakdown["Technology & Equipment"] = f"${base * 5}k - ${base * 15}k (10-15% of budget)"

        # Research and development
        if any(word in text for word in ["research", "development", "prototype", "testing"]):
            breakdown["R&D and Prototyping"] = f"${base * 15}k - ${base * 30}k (15-20% of budget)"

        # Data and licensing
        if any(word in text for word in ["data", "dataset", "license", "api", "third-party"]):
            breakdown["Data & Licensing"] = f"${base * 5}k - ${base * 20}k (5-15% of budget)"

        # Operational costs
        breakdown["Operational Costs"] = f"${base * 5}k - ${base * 15}k (5-10% of budget)"

        # Contingency
        breakdown["Contingency Reserve"] = f"${base * 5}k - ${base * 10}k (10-15% of budget)"

        return breakdown

    def _estimate_budget_range(self, category: str, text: str) -> str:
        """Estimate the budget range"""
        base_ranges = {
            "Minimal": (5_000, 25_000),
            "Low": (25_000, 100_000),
            "Medium": (100_000, 500_000),
            "High": (500_000, 5_000_000),
            "Very High": (5_000_000, 50_000_000)
        }

        low, high = base_ranges.get(category, (50_000, 250_000))

        # Adjust based on duration indicators
        if "year" in text or "long-term" in text:
            low *= 1.5
            high *= 2

        # Format nicely
        if high >= 1_000_000:
            return f"${low/1_000_000:.1f}M - ${high/1_000_000:.1f}M"
        else:
            return f"${low/1_000:.0f}K - ${high/1_000:.0f}K"

    def _identify_funding_requirements(self, category: str, text: str) -> List[str]:
        """Identify funding requirements and milestones"""
        requirements = []

        if category in ["Very High", "High"]:
            requirements.append("Substantial seed funding required before development can begin")
            requirements.append("Phased funding approach recommended with milestone-based releases")
            requirements.append("Detailed financial projections and risk analysis needed for investors")

        if category == "Medium":
            requirements.append("Initial funding of 20-30% needed for proof-of-concept")
            requirements.append("Additional rounds may be needed based on progress")

        if any(word in text for word in ["hardware", "equipment", "facility"]):
            requirements.append("Upfront capital expenditure for equipment and infrastructure")

        if any(word in text for word in ["hiring", "team building"]):
            requirements.append("Runway for at least 12-18 months of personnel costs")

        if "patent" in text or "intellectual property" in text:
            requirements.append("Legal and IP protection costs ($20k-$100k)")

        if not requirements:
            requirements.append("Modest initial funding sufficient to begin development")

        return requirements

    def _identify_cost_risks(self, text: str, category: str) -> List[str]:
        """Identify cost-related risks"""
        risks = []

        if category in ["Very High", "High"]:
            risks.append("High capital requirements may limit funding sources")
            risks.append("Significant financial risk if project fails or pivots")
            risks.append("Long runway to profitability increases burn rate risk")

        if any(word in text for word in ["hardware", "manufacturing"]):
            risks.append("Supply chain disruptions can cause cost overruns")
            risks.append("Prototyping costs may exceed estimates")

        if "machine learning" in text or "ai" in text:
            risks.append("Computational costs for training may be higher than expected")
            risks.append("Data acquisition costs can escalate quickly")

        if "cloud" in text or "infrastructure" in text:
            risks.append("Scaling costs may grow faster than revenue")
            risks.append("Infrastructure costs are ongoing operational expenses")

        if "regulatory" in text or "compliance" in text:
            risks.append("Regulatory compliance may require unexpected additional funding")

        if any(word in text for word in ["novel", "innovative", "first-of-its-kind"]):
            risks.append("Novel approaches have higher uncertainty in cost estimation")

        if not risks:
            risks.append("Standard project risks - recommend 15-20% contingency buffer")

        return risks

    def _find_optimization_opportunities(
        self, text: str, breakdown: Dict[str, str]
    ) -> List[str]:
        """Identify cost optimization opportunities"""
        opportunities = []

        # Cloud and infrastructure
        if "cloud" in text:
            opportunities.append("Use serverless architecture to reduce idle infrastructure costs")
            opportunities.append("Leverage free tiers and credits from cloud providers")

        # Development approach
        if any(word in text for word in ["software", "application", "platform"]):
            opportunities.append("Use open-source frameworks and tools to reduce licensing costs")
            opportunities.append("Start with MVP to validate before full investment")

        # Team structure
        if "team" in text:
            opportunities.append("Consider remote team to access global talent at lower costs")
            opportunities.append("Use contractors/freelancers for specialized short-term needs")

        # Data and AI
        if "machine learning" in text or "data" in text:
            opportunities.append("Use pre-trained models to reduce training costs")
            opportunities.append("Start with smaller datasets and scale progressively")

        # Hardware
        if "hardware" in text or "prototype" in text:
            opportunities.append("Use 3D printing and rapid prototyping to reduce initial costs")
            opportunities.append("Partner with universities for equipment access")

        # General optimizations
        opportunities.append("Phase development to spread costs over time")
        opportunities.append("Seek academic or industry partnerships for shared resources")

        if "research" in text:
            opportunities.append("Apply for research grants to offset costs")

        return opportunities

    def _assess_roi_potential(self, text: str, category: str) -> str:
        """Assess return on investment potential"""
        score = 0

        # Market indicators
        if any(word in text for word in ["market", "customer", "user", "revenue"]):
            score += 20

        # Scalability
        if any(word in text for word in ["scalable", "scale", "saas", "platform"]):
            score += 20

        # Innovation
        if any(word in text for word in ["innovative", "novel", "first", "breakthrough"]):
            score += 15

        # Problem solving
        if any(word in text for word in ["solve", "address", "improve", "optimize"]):
            score += 15

        # Commercial viability
        if any(word in text for word in ["commercial", "product", "service", "business"]):
            score += 15

        # Cost efficiency
        if category in ["Minimal", "Low"]:
            score += 15
        elif category == "Medium":
            score += 10

        # Determine ROI potential
        if score >= 70:
            return "High - Strong commercial potential with reasonable investment"
        elif score >= 50:
            return "Medium-High - Good potential if execution is solid"
        elif score >= 30:
            return "Medium - Depends on market validation and execution"
        elif score >= 15:
            return "Low-Medium - May be better suited for research than commercial venture"
        else:
            return "Low - Primarily academic/research value"

    def _suggest_funding_sources(self, category: str, text: str) -> List[str]:
        """Suggest appropriate funding sources"""
        sources = []

        if category in ["Minimal", "Low"]:
            sources.append("Bootstrapping / Personal funds")
            sources.append("Friends and family")
            sources.append("Small business grants")
            sources.append("Crowdfunding platforms")

        if category in ["Low", "Medium"]:
            sources.append("Angel investors")
            sources.append("Seed funding rounds")
            sources.append("Accelerator programs (Y Combinator, Techstars, etc.)")

        if category in ["Medium", "High", "Very High"]:
            sources.append("Venture Capital (Series A/B)")
            sources.append("Strategic corporate investors")
            sources.append("Private equity")

        if "research" in text or "academic" in text:
            sources.append("NSF/NIH/DARPA grants (for US-based research)")
            sources.append("University research funds")
            sources.append("Research foundations (Bill & Melinda Gates, etc.)")

        if "health" in text or "medical" in text:
            sources.append("Healthcare-focused VCs")
            sources.append("NIH SBIR/STTR programs")

        if "climate" in text or "environment" in text or "sustainable" in text:
            sources.append("Climate tech investors")
            sources.append("Green bonds and impact investors")

        if "government" in text or "public sector" in text:
            sources.append("Government contracts and programs")
            sources.append("SBIR/STTR programs")

        return sources

    def _calculate_feasibility_score(
        self, category: str, risk_count: int, optimization_count: int, roi: str
    ) -> float:
        """Calculate cost feasibility score"""
        # Base score by category (lower cost = higher feasibility)
        base_scores = {
            "Minimal": 95,
            "Low": 85,
            "Medium": 70,
            "High": 50,
            "Very High": 30
        }
        score = base_scores.get(category, 60)

        # Adjust for ROI potential
        if "High" in roi:
            score += 10
        elif "Medium-High" in roi:
            score += 5
        elif "Low" in roi:
            score -= 10

        # Penalty for risks
        score -= min(risk_count * 3, 20)

        # Bonus for optimizations
        score += min(optimization_count * 2, 15)

        return max(0, min(100, score))

    def _generate_details(
        self, description: str, category: str, breakdown: Dict[str, str], roi: str
    ) -> str:
        """Generate detailed cost analysis narrative"""
        details = f"""
Cost Feasibility Analysis:

The project falls into the '{category}' budget category, which has specific implications for funding and execution.

Budget Breakdown:
"""
        for item, cost in breakdown.items():
            details += f"  • {item}: {cost}\n"

        details += f"""
ROI Potential: {roi}

The financial feasibility depends on securing appropriate funding sources and managing costs effectively throughout the project lifecycle.
{'Given the high budget requirements, careful financial planning and phased funding approach is critical.' if category in ['High', 'Very High'] else ''}
{'The moderate budget makes this accessible to various funding sources.' if category == 'Medium' else ''}
{'The lower budget requirements make this project financially feasible for early-stage funding.' if category in ['Low', 'Minimal'] else ''}
"""
        return details.strip()
