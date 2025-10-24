"""
Market Viability and Timing Analysis Module
Evaluates market potential, timing, and commercial viability
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MarketAnalysis:
    feasibility_score: float  # 0-100
    market_timing: str  # Too Early, Early, Optimal, Late, Too Late
    market_size_potential: str
    competition_level: str
    market_readiness: str
    adoption_barriers: List[str]
    competitive_advantages: List[str]
    market_trends: List[str]
    target_segments: List[str]
    go_to_market_strategy: str
    recommendations: List[str]
    details: str


class MarketAnalyzer:
    """Analyzes market viability, timing, and commercial potential"""

    def __init__(self):
        # Emerging market indicators (may be too early)
        self.emerging_markets = [
            "quantum computing", "brain-computer interface", "fusion energy",
            "space tourism", "flying cars", "molecular nanotechnology",
            "artificial general intelligence", "neural lace"
        ]

        # Growing market indicators (good timing)
        self.growing_markets = [
            "ai", "machine learning", "electric vehicles", "renewable energy",
            "telemedicine", "remote work", "cybersecurity", "cloud",
            "cryptocurrency", "blockchain", "iot", "5g", "edge computing",
            "autonomous vehicles", "drone", "3d printing", "biotech"
        ]

        # Mature market indicators (late but stable)
        self.mature_markets = [
            "mobile apps", "e-commerce", "social media", "search engine",
            "email", "web hosting", "crm", "erp"
        ]

        # Problem-solving indicators (strong value proposition)
        self.strong_value_props = [
            "reduce cost", "save time", "increase efficiency", "automate",
            "improve health", "enhance safety", "prevent", "optimize",
            "simplify", "accelerate", "reduce risk"
        ]

        # Current year for timing analysis
        self.current_year = datetime.now().year

    def analyze(self, project_description: str) -> MarketAnalysis:
        """Perform comprehensive market analysis"""
        project_lower = project_description.lower()

        # Assess market timing
        timing, timing_score = self._assess_market_timing(project_lower)

        # Estimate market size potential
        market_size = self._estimate_market_size(project_lower)

        # Assess competition level
        competition = self._assess_competition(project_lower, timing)

        # Assess market readiness
        readiness = self._assess_market_readiness(project_lower, timing)

        # Identify adoption barriers
        barriers = self._identify_adoption_barriers(project_lower)

        # Identify competitive advantages
        advantages = self._identify_competitive_advantages(project_lower)

        # Identify relevant market trends
        trends = self._identify_market_trends(project_lower)

        # Identify target segments
        segments = self._identify_target_segments(project_lower)

        # Suggest go-to-market strategy
        gtm_strategy = self._suggest_gtm_strategy(
            project_lower, market_size, competition, segments
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            timing, market_size, competition, barriers, advantages
        )

        # Calculate overall feasibility score
        feasibility_score = self._calculate_feasibility_score(
            timing_score, market_size, competition, len(barriers), len(advantages)
        )

        # Generate detailed analysis
        details = self._generate_details(
            project_description, timing, market_size, competition, readiness
        )

        return MarketAnalysis(
            feasibility_score=round(feasibility_score, 2),
            market_timing=timing,
            market_size_potential=market_size,
            competition_level=competition,
            market_readiness=readiness,
            adoption_barriers=barriers,
            competitive_advantages=advantages,
            market_trends=trends,
            target_segments=segments,
            go_to_market_strategy=gtm_strategy,
            recommendations=recommendations,
            details=details
        )

    def _assess_market_timing(self, text: str) -> Tuple[str, float]:
        """Assess whether timing is right for this market"""
        timing_score = 0

        # Check against market categories
        is_emerging = any(market in text for market in self.emerging_markets)
        is_growing = any(market in text for market in self.growing_markets)
        is_mature = any(market in text for market in self.mature_markets)

        # Assess timing
        if is_emerging:
            timing_score = 40
            timing = "Too Early"
        elif is_growing:
            timing_score = 90
            timing = "Optimal"
        elif is_mature:
            timing_score = 60
            timing = "Late"
        else:
            # Default to early if targeting new problems
            if any(word in text for word in ["novel", "new", "innovative", "first"]):
                timing_score = 70
                timing = "Early"
            else:
                timing_score = 75
                timing = "Optimal"

        # Adjust for pandemic-accelerated trends
        if any(word in text for word in ["remote", "virtual", "telemedicine", "delivery"]):
            timing_score = min(100, timing_score + 10)

        # Adjust for sustainability trends
        if any(word in text for word in ["sustainable", "green", "climate", "carbon"]):
            timing_score = min(100, timing_score + 10)

        # Recalculate timing based on adjusted score
        if timing_score >= 85:
            timing = "Optimal"
        elif timing_score >= 65:
            timing = "Early" if timing_score < 75 else "Good"
        elif timing_score >= 45:
            timing = "Late"
        else:
            timing = "Too Early"

        return timing, timing_score

    def _estimate_market_size(self, text: str) -> str:
        """Estimate total addressable market size"""
        size_score = 0

        # Scale indicators
        scale_words = {
            "global": 30, "worldwide": 30, "international": 25,
            "national": 20, "nationwide": 20,
            "regional": 10, "local": 5,
            "enterprise": 25, "consumer": 30,
            "b2b": 20, "b2c": 25,
            "millions": 20, "billions": 30,
            "everyone": 25, "all": 15
        }

        for word, score in scale_words.items():
            if word in text:
                size_score += score

        # Industry size indicators
        large_industries = [
            "healthcare", "finance", "banking", "insurance", "retail",
            "education", "transportation", "energy", "manufacturing"
        ]
        for industry in large_industries:
            if industry in text:
                size_score += 20

        # Determine market size
        if size_score >= 60:
            return "Very Large ($10B+ TAM) - Multi-billion dollar opportunity"
        elif size_score >= 40:
            return "Large ($1B-10B TAM) - Billion dollar opportunity"
        elif size_score >= 25:
            return "Medium ($100M-1B TAM) - Hundred million dollar opportunity"
        elif size_score >= 10:
            return "Small ($10M-100M TAM) - Niche market opportunity"
        else:
            return "Very Small (<$10M TAM) - Micro market or unproven market"

    def _assess_competition(self, text: str, timing: str) -> str:
        """Assess level of competition"""
        # Timing influences competition
        competition_base = {
            "Too Early": 20,
            "Early": 40,
            "Optimal": 70,
            "Good": 70,
            "Late": 85,
            "Too Late": 95
        }
        comp_score = competition_base.get(timing, 50)

        # Adjust based on market mentions
        if any(word in text for word in ["crowded", "competitive", "saturated"]):
            comp_score += 15

        if any(word in text for word in ["blue ocean", "untapped", "underserved"]):
            comp_score -= 20

        if any(word in text for word in ["niche", "specialized", "specific"]):
            comp_score -= 10

        # Determine competition level
        if comp_score >= 80:
            return "Very High - Crowded market with established players"
        elif comp_score >= 60:
            return "High - Significant competition, differentiation critical"
        elif comp_score >= 40:
            return "Moderate - Growing market with multiple players"
        elif comp_score >= 20:
            return "Low - Early market with few competitors"
        else:
            return "Very Low - Blue ocean opportunity"

    def _assess_market_readiness(self, text: str, timing: str) -> str:
        """Assess whether market is ready for this solution"""
        readiness_score = 0

        # Problem awareness
        if any(word in text for word in ["problem", "pain point", "challenge", "issue"]):
            readiness_score += 20

        # Existing solutions
        if any(word in text for word in ["alternative", "competitor", "existing solution"]):
            readiness_score += 15

        # Demand indicators
        if any(word in text for word in ["demand", "need", "require", "want"]):
            readiness_score += 20

        # Technology readiness
        if timing in ["Optimal", "Good", "Late"]:
            readiness_score += 25
        elif timing == "Early":
            readiness_score += 15

        # Regulatory clarity
        if "regulatory" in text or "compliance" in text:
            if "unclear" in text or "evolving" in text:
                readiness_score -= 10
            else:
                readiness_score += 10

        # Determine readiness
        if readiness_score >= 70:
            return "High - Market is ready and actively seeking solutions"
        elif readiness_score >= 50:
            return "Moderate - Market exists but may need education"
        elif readiness_score >= 30:
            return "Low - Market needs significant development"
        else:
            return "Very Low - Market may not be ready for this solution"

    def _identify_adoption_barriers(self, text: str) -> List[str]:
        """Identify barriers to market adoption"""
        barriers = []

        # Technology barriers
        if any(word in text for word in ["complex", "complicated", "difficult"]):
            barriers.append("High complexity may hinder user adoption")

        if "integration" in text:
            barriers.append("Integration with existing systems may be challenging")

        # Cost barriers
        if any(word in text for word in ["expensive", "high cost", "premium"]):
            barriers.append("High cost may limit addressable market")

        # Behavioral barriers
        if "behavior change" in text or "habit" in text:
            barriers.append("Requires user behavior change - typically slow adoption")

        # Network effects
        if any(word in text for word in ["network effect", "two-sided", "marketplace"]):
            barriers.append("Chicken-and-egg problem - needs critical mass to be valuable")

        # Regulatory barriers
        if "regulatory approval" in text or "compliance" in text:
            barriers.append("Regulatory approval process may delay market entry")

        # Privacy/security concerns
        if any(word in text for word in ["privacy", "security", "data collection"]):
            barriers.append("Privacy and security concerns may create adoption resistance")

        # Switching costs
        if "switching" in text or "migration" in text:
            barriers.append("High switching costs from existing solutions")

        # Education needed
        if any(word in text for word in ["novel", "innovative", "new approach"]):
            barriers.append("Market education required - people don't know they need it yet")

        # Infrastructure dependencies
        if any(word in text for word in ["requires", "depends on", "needs"]):
            barriers.append("Dependencies on external infrastructure or platforms")

        return barriers

    def _identify_competitive_advantages(self, text: str) -> List[str]:
        """Identify potential competitive advantages"""
        advantages = []

        # Value proposition strengths
        for value_prop in self.strong_value_props:
            if value_prop in text:
                advantages.append(f"Strong value proposition: {value_prop}")
                break  # Only add once

        # Technology advantages
        if any(word in text for word in ["proprietary", "patent", "trade secret"]):
            advantages.append("Intellectual property protection")

        if any(word in text for word in ["ai", "machine learning", "automation"]):
            advantages.append("Technology-driven efficiency and scalability")

        # Network effects
        if "network effect" in text or "platform" in text:
            advantages.append("Network effects create defensible moat")

        # Data advantages
        if "data" in text and any(word in text for word in ["unique", "proprietary", "exclusive"]):
            advantages.append("Unique data assets provide competitive edge")

        # First mover
        if any(word in text for word in ["first", "pioneer", "novel"]):
            advantages.append("First-mover advantage in emerging market")

        # Better UX
        if any(word in text for word in ["simple", "easy", "intuitive", "user-friendly"]):
            advantages.append("Superior user experience")

        # Cost efficiency
        if any(word in text for word in ["cheaper", "lower cost", "affordable"]):
            advantages.append("Cost advantage enables broader market reach")

        # Partnerships
        if "partnership" in text or "strategic alliance" in text:
            advantages.append("Strategic partnerships accelerate go-to-market")

        # Specialized expertise
        if any(word in text for word in ["expertise", "specialized", "domain knowledge"]):
            advantages.append("Deep domain expertise")

        return advantages

    def _identify_market_trends(self, text: str) -> List[str]:
        """Identify relevant market trends"""
        trends = []

        # Digital transformation
        if any(word in text for word in ["digital", "online", "cloud", "saas"]):
            trends.append("Digital transformation accelerating across industries")

        # AI/ML trend
        if any(word in text for word in ["ai", "machine learning", "automation"]):
            trends.append("AI/ML adoption growing rapidly across sectors")

        # Remote/hybrid work
        if any(word in text for word in ["remote", "hybrid", "distributed"]):
            trends.append("Remote and hybrid work models becoming permanent")

        # Sustainability
        if any(word in text for word in ["sustainable", "green", "climate", "esg"]):
            trends.append("Sustainability and ESG priorities driving investment")

        # Privacy and security
        if any(word in text for word in ["privacy", "security", "cybersecurity"]):
            trends.append("Privacy and security concerns increasing regulation and spending")

        # Personalization
        if any(word in text for word in ["personalization", "customization", "tailored"]):
            trends.append("Personalization becoming expected rather than differentiator")

        # Subscription economy
        if any(word in text for word in ["subscription", "saas", "recurring revenue"]):
            trends.append("Shift from ownership to subscription models")

        # Mobile-first
        if "mobile" in text:
            trends.append("Mobile-first approach increasingly critical")

        # Healthcare innovation
        if any(word in text for word in ["health", "medical", "telemedicine"]):
            trends.append("Healthcare digitization accelerating post-pandemic")

        # Blockchain/Web3
        if any(word in text for word in ["blockchain", "web3", "decentralized"]):
            trends.append("Blockchain and decentralization gaining traction")

        return trends

    def _identify_target_segments(self, text: str) -> List[str]:
        """Identify target market segments"""
        segments = []

        # Business segments
        if "enterprise" in text or "large business" in text:
            segments.append("Enterprise (1000+ employees)")

        if "smb" in text or "small business" in text or "medium business" in text:
            segments.append("SMB (10-1000 employees)")

        if "startup" in text:
            segments.append("Startups and early-stage companies")

        # Consumer segments
        if "consumer" in text or "individual" in text or "user" in text:
            segments.append("Individual consumers")

        # Industry segments
        industries = [
            "healthcare", "finance", "education", "retail", "manufacturing",
            "technology", "government", "non-profit"
        ]
        for industry in industries:
            if industry in text:
                segments.append(f"{industry.capitalize()} sector")

        # Demographic segments
        if "millennial" in text or "gen z" in text:
            segments.append("Younger demographics (Gen Z, Millennials)")

        if "senior" in text or "elderly" in text:
            segments.append("Senior citizens")

        # Default segment
        if not segments:
            segments.append("General market - needs further segmentation analysis")

        return segments

    def _suggest_gtm_strategy(
        self, text: str, market_size: str, competition: str, segments: List[str]
    ) -> str:
        """Suggest go-to-market strategy"""
        strategies = []

        # Based on competition level
        if "Very High" in competition or "High" in competition:
            strategies.append("Focus on specific niche or vertical to avoid direct competition")
        else:
            strategies.append("Rapid expansion to capture market share before competitors emerge")

        # Based on market size
        if "Very Large" in market_size or "Large" in market_size:
            strategies.append("Land-and-expand: Start with beachhead segment, then expand")
        else:
            strategies.append("Focused approach on core segment")

        # Based on customer type
        if any("Enterprise" in seg for seg in segments):
            strategies.append("Direct sales with pilots and case studies for enterprise")
        elif any("SMB" in seg for seg in segments):
            strategies.append("Product-led growth with self-service onboarding")
        elif any("consumer" in seg.lower() for seg in segments):
            strategies.append("Digital marketing and viral growth tactics")

        # Platform approach
        if "platform" in text or "marketplace" in text:
            strategies.append("Solve chicken-and-egg by subsidizing one side initially")

        return " | ".join(strategies)

    def _generate_recommendations(
        self, timing: str, market_size: str, competition: str,
        barriers: List[str], advantages: List[str]
    ) -> List[str]:
        """Generate market recommendations"""
        recommendations = []

        # Timing-based recommendations
        if timing == "Too Early":
            recommendations.append("⚠️ Market may not be ready - consider waiting or focusing on early adopters")
            recommendations.append("Build awareness and educate market while technology matures")

        if timing == "Early":
            recommendations.append("Good timing for first-mover advantage if you can execute quickly")
            recommendations.append("Focus on innovators and early adopters willing to try new solutions")

        if timing in ["Optimal", "Good"]:
            recommendations.append("✓ Excellent market timing - move quickly to capture opportunity")

        if timing == "Late":
            recommendations.append("Market is mature - differentiation is critical for success")
            recommendations.append("Consider focusing on underserved niches or new angles")

        # Market size recommendations
        if "Very Small" in market_size or "Small" in market_size:
            recommendations.append("Small market limits growth potential - ensure low CAC or expand TAM")

        # Competition recommendations
        if "Very High" in competition:
            recommendations.append("Highly competitive - need clear differentiation and strong GTM execution")

        # Barriers recommendations
        if len(barriers) > 4:
            recommendations.append("Multiple adoption barriers - prioritize removing biggest obstacles")
            recommendations.append("Pilot programs and POCs to demonstrate value and reduce risk")

        # Advantages recommendations
        if len(advantages) < 2:
            recommendations.append("Limited competitive advantages - need to develop stronger moat")

        # General recommendations
        recommendations.append("Conduct customer discovery interviews to validate assumptions")
        recommendations.append("Build MVP to test market fit before full investment")

        return recommendations

    def _calculate_feasibility_score(
        self, timing_score: float, market_size: str, competition: str,
        barrier_count: int, advantage_count: int
    ) -> float:
        """Calculate market feasibility score"""
        score = timing_score * 0.4  # Timing is most important

        # Market size contribution
        size_scores = {
            "Very Large": 30,
            "Large": 25,
            "Medium": 20,
            "Small": 10,
            "Very Small": 5
        }
        for size_type, size_score in size_scores.items():
            if size_type in market_size:
                score += size_score * 0.3
                break

        # Competition impact (inverse - less competition is better)
        comp_scores = {
            "Very Low": 20,
            "Low": 18,
            "Moderate": 15,
            "High": 10,
            "Very High": 5
        }
        for comp_type, comp_score in comp_scores.items():
            if comp_type in competition:
                score += comp_score * 0.2
                break

        # Adjust for barriers and advantages
        score -= min(barrier_count * 2, 15)
        score += min(advantage_count * 3, 15)

        return max(0, min(100, score))

    def _generate_details(
        self, description: str, timing: str, market_size: str,
        competition: str, readiness: str
    ) -> str:
        """Generate detailed market analysis"""
        details = f"""
Market Viability Analysis:

Market Timing: {timing}
The market timing is {timing.lower()}, which {'presents excellent opportunity for market entry' if timing in ['Optimal', 'Good'] else 'may require careful consideration of entry strategy'}.

Market Size: {market_size}
Competition: {competition}
Market Readiness: {readiness}

{'The large market size provides significant growth potential.' if 'Large' in market_size or 'Very Large' in market_size else ''}
{'The competitive landscape is crowded - strong differentiation is essential.' if 'High' in competition or 'Very High' in competition else ''}
{'Limited competition provides opportunity to establish market leadership.' if 'Low' in competition or 'Very Low' in competition else ''}

Market analysis should be validated through customer discovery and market research.
Timing can shift quickly - continuous market monitoring is essential.
"""
        return details.strip()
