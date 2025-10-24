"""
Technology Feasibility Analyzer Module
Evaluates the technological feasibility of research projects
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class TechnologyAnalysis:
    feasibility_score: float  # 0-100
    maturity_level: str  # Emerging, Developing, Mature, Obsolete
    required_technologies: List[str]
    available_technologies: List[str]
    technology_gaps: List[str]
    implementation_complexity: str  # Low, Medium, High, Very High
    estimated_development_time: str
    risks: List[str]
    recommendations: List[str]
    details: str


class TechnologyAnalyzer:
    """Analyzes technological feasibility of research projects"""

    def __init__(self):
        # Technology maturity database
        self.emerging_tech = [
            "quantum computing", "quantum", "brain-computer interface", "bci",
            "fusion energy", "nuclear fusion", "agi", "artificial general intelligence",
            "molecular nanotechnology", "carbon nanotubes", "graphene computing",
            "room temperature superconductor", "space elevator", "neural lace"
        ]

        self.developing_tech = [
            "autonomous vehicles", "self-driving", "augmented reality", "ar glasses",
            "virtual reality", "vr", "blockchain", "cryptocurrency", "gene editing",
            "crispr", "5g", "6g", "edge computing", "neuromorphic computing",
            "synthetic biology", "bioprinting", "drone delivery", "flying cars"
        ]

        self.mature_tech = [
            "machine learning", "deep learning", "neural networks", "cloud computing",
            "mobile applications", "web applications", "iot", "internet of things",
            "computer vision", "natural language processing", "nlp", "robotics",
            "3d printing", "additive manufacturing", "solar panels", "wind turbines",
            "electric vehicles", "ev", "gps", "satellite", "fiber optics"
        ]

        self.obsolete_tech = [
            "floppy disk", "cassette tape", "cd-rom only", "dial-up", "flash player",
            "internet explorer specific", "windows xp", "32-bit only",
            "non-quantum resistant cryptography", "sha-1", "md5 hashing"
        ]

        # Complexity indicators
        self.high_complexity_indicators = [
            "real-time", "large-scale", "distributed system", "blockchain",
            "quantum", "brain", "neural interface", "autonomous", "self-learning",
            "multi-agent", "federated", "zero-knowledge", "homomorphic encryption"
        ]

    def analyze(self, project_description: str) -> TechnologyAnalysis:
        """
        Perform comprehensive technology feasibility analysis
        """
        project_lower = project_description.lower()

        # Identify mentioned technologies
        tech_mentions = self._identify_technologies(project_lower)

        # Assess technology maturity
        maturity_level, maturity_score = self._assess_maturity(tech_mentions, project_lower)

        # Identify technology gaps
        gaps = self._identify_gaps(project_lower, tech_mentions)

        # Assess complexity
        complexity, complexity_score = self._assess_complexity(project_lower)

        # Estimate development time
        dev_time = self._estimate_development_time(complexity, maturity_level)

        # Identify risks
        risks = self._identify_risks(project_lower, maturity_level, complexity)

        # Calculate overall feasibility score
        feasibility_score = self._calculate_feasibility_score(
            maturity_score, complexity_score, len(gaps), len(risks)
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            feasibility_score, maturity_level, complexity, gaps
        )

        # Generate detailed analysis
        details = self._generate_details(
            project_description, tech_mentions, maturity_level, complexity
        )

        return TechnologyAnalysis(
            feasibility_score=round(feasibility_score, 2),
            maturity_level=maturity_level,
            required_technologies=tech_mentions["required"],
            available_technologies=tech_mentions["available"],
            technology_gaps=gaps,
            implementation_complexity=complexity,
            estimated_development_time=dev_time,
            risks=risks,
            recommendations=recommendations,
            details=details
        )

    def _identify_technologies(self, text: str) -> Dict[str, List[str]]:
        """Identify technologies mentioned in the project"""
        required = []
        available = []

        all_tech_lists = [
            self.emerging_tech, self.developing_tech,
            self.mature_tech, self.obsolete_tech
        ]

        for tech_list in all_tech_lists:
            for tech in tech_list:
                if tech in text:
                    if tech_list == self.mature_tech:
                        available.append(tech)
                    else:
                        required.append(tech)

        # Additional pattern matching for technologies
        patterns = [
            r'\b(ai|ml|dl|cnn|rnn|lstm|gpt|transformer|llm)\b',
            r'\b(api|rest|graphql|grpc)\b',
            r'\b(database|sql|nosql|mongodb|postgresql)\b',
            r'\b(sensor|actuator|microcontroller|raspberry pi|arduino)\b',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if match not in required and match not in available:
                    available.append(match.upper())

        return {
            "required": list(set(required)),
            "available": list(set(available))
        }

    def _assess_maturity(self, tech_mentions: Dict, text: str) -> Tuple[str, float]:
        """Assess the maturity level of technologies"""
        scores = {
            "Emerging": 0,
            "Developing": 0,
            "Mature": 0,
            "Obsolete": 0
        }

        # Check against known tech lists
        for tech in tech_mentions["required"] + tech_mentions["available"]:
            tech_lower = tech.lower()
            if any(t in tech_lower for t in self.emerging_tech):
                scores["Emerging"] += 2
            elif any(t in tech_lower for t in self.developing_tech):
                scores["Developing"] += 2
            elif any(t in tech_lower for t in self.mature_tech):
                scores["Mature"] += 2
            elif any(t in tech_lower for t in self.obsolete_tech):
                scores["Obsolete"] += 2

        # Default to mature if no specific tech identified
        if sum(scores.values()) == 0:
            scores["Mature"] = 1

        # Determine primary maturity level
        max_level = max(scores, key=scores.get)

        # Calculate maturity score (higher is better for feasibility)
        maturity_score = (
            scores["Mature"] * 100 +
            scores["Developing"] * 70 +
            scores["Emerging"] * 40 +
            scores["Obsolete"] * 10
        ) / max(sum(scores.values()), 1)

        return max_level, maturity_score

    def _identify_gaps(self, text: str, tech_mentions: Dict) -> List[str]:
        """Identify technology gaps"""
        gaps = []

        # Check for emerging tech without supporting infrastructure
        for tech in tech_mentions["required"]:
            if any(t in tech.lower() for t in self.emerging_tech):
                gaps.append(f"{tech} - Still in experimental phase, limited infrastructure")

        # Check for data requirements
        if any(word in text for word in ["dataset", "training data", "data collection"]):
            if "large-scale" in text or "big data" in text:
                gaps.append("Large-scale data collection and storage infrastructure")

        # Check for computational requirements
        if any(word in text for word in ["deep learning", "training", "simulation", "modeling"]):
            gaps.append("High-performance computing resources may be required")

        # Check for specialized hardware
        if any(word in text for word in ["quantum", "neuromorphic", "fpga", "asic"]):
            gaps.append("Specialized hardware procurement and expertise")

        # Check for integration challenges
        if len(tech_mentions["required"]) > 3:
            gaps.append("Complex system integration across multiple technologies")

        return gaps

    def _assess_complexity(self, text: str) -> Tuple[str, float]:
        """Assess implementation complexity"""
        complexity_score = 0

        # Check for complexity indicators
        for indicator in self.high_complexity_indicators:
            if indicator in text:
                complexity_score += 20

        # Check for scale indicators
        scale_words = ["large-scale", "global", "millions", "billions", "worldwide"]
        complexity_score += sum(10 for word in scale_words if word in text)

        # Check for integration requirements
        integration_words = ["integrate", "interoperable", "cross-platform", "multi-system"]
        complexity_score += sum(5 for word in integration_words if word in text)

        # Check for real-time requirements
        if "real-time" in text or "low latency" in text:
            complexity_score += 15

        # Determine complexity level
        if complexity_score >= 60:
            return "Very High", 40
        elif complexity_score >= 40:
            return "High", 60
        elif complexity_score >= 20:
            return "Medium", 80
        else:
            return "Low", 95

    def _estimate_development_time(self, complexity: str, maturity: str) -> str:
        """Estimate development timeline"""
        base_times = {
            "Low": 3,
            "Medium": 6,
            "High": 12,
            "Very High": 24
        }

        maturity_multipliers = {
            "Mature": 1.0,
            "Developing": 1.5,
            "Emerging": 2.5,
            "Obsolete": 1.2
        }

        months = base_times.get(complexity, 12) * maturity_multipliers.get(maturity, 1.5)

        if months <= 6:
            return f"{int(months)} months (Prototype in {int(months/2)} months)"
        elif months <= 12:
            return f"{int(months)} months (MVP in {int(months*0.6)} months)"
        else:
            years = months / 12
            return f"{years:.1f} years (Phased development recommended)"

    def _identify_risks(self, text: str, maturity: str, complexity: str) -> List[str]:
        """Identify technological risks"""
        risks = []

        if maturity == "Emerging":
            risks.append("Technology not yet proven at scale - high risk of technical failure")
            risks.append("Limited vendor support and ecosystem")
            risks.append("Rapid obsolescence as technology evolves")

        if maturity == "Obsolete":
            risks.append("Using outdated technology - security and maintenance concerns")
            risks.append("Difficulty finding skilled developers")

        if complexity in ["High", "Very High"]:
            risks.append("High integration complexity may lead to delays and cost overruns")
            risks.append("Difficult to debug and maintain")

        if "quantum" in text:
            risks.append("Quantum hardware still limited and expensive")

        if "ai" in text or "machine learning" in text:
            risks.append("Model training requires significant computational resources")
            risks.append("Potential bias and fairness issues in AI models")

        if "blockchain" in text:
            risks.append("Scalability limitations in current blockchain technology")
            risks.append("High energy consumption concerns")

        if "real-time" in text:
            risks.append("Real-time performance constraints may be difficult to guarantee")

        return risks

    def _calculate_feasibility_score(
        self, maturity_score: float, complexity_score: float,
        gap_count: int, risk_count: int
    ) -> float:
        """Calculate overall technology feasibility score"""
        # Base score from maturity and complexity
        base_score = (maturity_score * 0.4) + (complexity_score * 0.3)

        # Penalties for gaps and risks
        gap_penalty = min(gap_count * 5, 20)
        risk_penalty = min(risk_count * 3, 15)

        final_score = base_score - gap_penalty - risk_penalty

        return max(0, min(100, final_score))

    def _generate_recommendations(
        self, score: float, maturity: str, complexity: str, gaps: List[str]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        if score < 40:
            recommendations.append("⚠️ HIGH RISK: Consider alternative approaches or wait for technology to mature")
        elif score < 60:
            recommendations.append("⚠️ MODERATE RISK: Proceed with caution and extensive prototyping")
        else:
            recommendations.append("✓ Technology appears feasible with proper planning")

        if maturity == "Emerging":
            recommendations.append("Build proof-of-concept first before full development")
            recommendations.append("Maintain flexibility to pivot as technology evolves")

        if complexity in ["High", "Very High"]:
            recommendations.append("Use agile/iterative development methodology")
            recommendations.append("Break project into smaller, manageable modules")
            recommendations.append("Invest in experienced technical leadership")

        if len(gaps) > 3:
            recommendations.append("Conduct detailed technical feasibility study before proceeding")
            recommendations.append("Identify strategic partners with complementary expertise")

        recommendations.append("Establish clear technical milestones and go/no-go decision points")

        return recommendations

    def _generate_details(
        self, description: str, tech_mentions: Dict, maturity: str, complexity: str
    ) -> str:
        """Generate detailed analysis narrative"""
        details = f"""
Technology Feasibility Analysis:

The project involves technologies at the '{maturity}' maturity level with '{complexity}' implementation complexity.

Identified Technologies:
- Core Requirements: {', '.join(tech_mentions['required']) if tech_mentions['required'] else 'General purpose technologies'}
- Available/Mature Tech: {', '.join(tech_mentions['available']) if tech_mentions['available'] else 'Standard development stack'}

The technological landscape for this project presents {'significant challenges' if maturity == 'Emerging' else 'moderate challenges' if maturity == 'Developing' else 'well-established pathways'}
for implementation. {'The complexity level requires careful architectural planning and experienced technical team.' if complexity in ['High', 'Very High'] else 'The complexity is manageable with standard development practices.'}
"""
        return details.strip()
