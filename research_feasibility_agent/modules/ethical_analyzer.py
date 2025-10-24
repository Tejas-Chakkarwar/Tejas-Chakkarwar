"""
Ethical Analysis Module
Evaluates ethical implications and social responsibility of research projects
"""

import re
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class EthicalAnalysis:
    feasibility_score: float  # 0-100
    ethical_risk_level: str  # Low, Medium, High, Critical
    ethical_concerns: List[str]
    privacy_implications: List[str]
    social_impact: str
    regulatory_compliance: List[str]
    bias_and_fairness_risks: List[str]
    environmental_impact: str
    recommendations: List[str]
    required_safeguards: List[str]
    details: str


class EthicalAnalyzer:
    """Analyzes ethical implications and social responsibility"""

    def __init__(self):
        # High-risk ethical domains
        self.critical_domains = [
            "human subjects", "clinical trial", "genetic manipulation", "gene editing",
            "crispr", "embryo", "human enhancement", "weaponization", "autonomous weapons",
            "surveillance", "facial recognition", "biometric", "social credit",
            "manipulation", "addiction", "children", "minors", "vulnerable populations"
        ]

        self.high_risk_domains = [
            "medical", "healthcare", "diagnosis", "treatment", "pharmaceutical",
            "personal data", "health data", "financial data", "location tracking",
            "behavioral analysis", "predictive policing", "hiring decision",
            "credit scoring", "insurance", "autonomous vehicle", "deepfake",
            "synthetic media", "ai-generated content", "nuclear", "dual-use"
        ]

        self.moderate_risk_domains = [
            "machine learning", "artificial intelligence", "algorithm",
            "user data", "privacy", "social media", "content moderation",
            "recommendation system", "personalization", "iot", "smart home",
            "drone", "facial detection", "emotion recognition"
        ]

        # Privacy concern indicators
        self.privacy_indicators = [
            "personal data", "user data", "tracking", "monitoring", "surveillance",
            "biometric", "location", "behavioral", "profile", "identity",
            "medical records", "health information", "financial data", "children's data"
        ]

        # Bias and fairness indicators
        self.bias_indicators = [
            "machine learning", "ai", "algorithm", "decision", "classification",
            "prediction", "recommendation", "scoring", "ranking", "filtering",
            "hiring", "lending", "criminal justice", "facial recognition"
        ]

        # Environmental impact indicators
        self.environmental_indicators = [
            "data center", "training", "computation", "mining", "blockchain",
            "manufacturing", "hardware production", "energy consumption",
            "carbon footprint", "emissions", "waste", "resource extraction"
        ]

    def analyze(self, project_description: str) -> EthicalAnalysis:
        """Perform comprehensive ethical analysis"""
        project_lower = project_description.lower()

        # Assess ethical risk level
        risk_level, base_score = self._assess_risk_level(project_lower)

        # Identify specific ethical concerns
        concerns = self._identify_ethical_concerns(project_lower)

        # Analyze privacy implications
        privacy_issues = self._analyze_privacy(project_lower)

        # Assess social impact
        social_impact = self._assess_social_impact(project_lower)

        # Identify regulatory requirements
        regulatory_reqs = self._identify_regulatory_requirements(project_lower)

        # Analyze bias and fairness risks
        bias_risks = self._analyze_bias_fairness(project_lower)

        # Assess environmental impact
        env_impact = self._assess_environmental_impact(project_lower)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            risk_level, concerns, privacy_issues, bias_risks
        )

        # Identify required safeguards
        safeguards = self._identify_safeguards(
            risk_level, concerns, privacy_issues, regulatory_reqs
        )

        # Calculate overall feasibility score
        feasibility_score = self._calculate_feasibility_score(
            base_score, len(concerns), len(privacy_issues),
            len(bias_risks), risk_level
        )

        # Generate detailed analysis
        details = self._generate_details(
            project_description, risk_level, concerns, social_impact
        )

        return EthicalAnalysis(
            feasibility_score=round(feasibility_score, 2),
            ethical_risk_level=risk_level,
            ethical_concerns=concerns,
            privacy_implications=privacy_issues,
            social_impact=social_impact,
            regulatory_compliance=regulatory_reqs,
            bias_and_fairness_risks=bias_risks,
            environmental_impact=env_impact,
            recommendations=recommendations,
            required_safeguards=safeguards,
            details=details
        )

    def _assess_risk_level(self, text: str) -> tuple:
        """Assess the ethical risk level"""
        risk_score = 0

        # Check for critical domains
        for domain in self.critical_domains:
            if domain in text:
                risk_score += 50

        # Check for high-risk domains
        for domain in self.high_risk_domains:
            if domain in text:
                risk_score += 25

        # Check for moderate-risk domains
        for domain in self.moderate_risk_domains:
            if domain in text:
                risk_score += 10

        # Determine risk level
        if risk_score >= 50:
            return "Critical", 30
        elif risk_score >= 25:
            return "High", 50
        elif risk_score >= 10:
            return "Medium", 70
        else:
            return "Low", 90

    def _identify_ethical_concerns(self, text: str) -> List[str]:
        """Identify specific ethical concerns"""
        concerns = []

        # Human subjects and medical research
        if any(word in text for word in ["human subjects", "clinical trial", "patients"]):
            concerns.append("Human subjects research requires IRB approval and informed consent")
            concerns.append("Patient safety and wellbeing must be paramount concern")

        # Genetic manipulation
        if any(word in text for word in ["gene editing", "crispr", "genetic manipulation", "germline"]):
            concerns.append("Genetic manipulation raises profound ethical questions about human enhancement")
            concerns.append("Potential for unintended genetic consequences across generations")
            concerns.append("Ethical concerns about 'designer babies' and genetic inequality")

        # AI and automation
        if any(word in text for word in ["artificial intelligence", "machine learning", "automation"]):
            concerns.append("AI systems may perpetuate or amplify existing societal biases")
            concerns.append("Automation may cause job displacement and economic disruption")
            concerns.append("Lack of transparency in AI decision-making ('black box' problem)")

        # Surveillance and privacy
        if any(word in text for word in ["surveillance", "tracking", "monitoring", "facial recognition"]):
            concerns.append("Mass surveillance threatens fundamental privacy rights")
            concerns.append("Potential for authoritarian misuse and social control")
            concerns.append("Chilling effect on free speech and assembly")

        # Autonomous systems
        if any(word in text for word in ["autonomous", "self-driving", "unmanned"]):
            concerns.append("Ethical responsibility for autonomous system decisions")
            concerns.append("Trolley problem and moral decision-making in edge cases")

        # Dual-use technology
        if any(word in text for word in ["dual-use", "military", "weapon", "defense"]):
            concerns.append("Potential for misuse in weapons or harmful applications")
            concerns.append("Ethical obligations around dual-use research")

        # Vulnerable populations
        if any(word in text for word in ["children", "minors", "vulnerable", "elderly", "disabled"]):
            concerns.append("Special protections needed for vulnerable populations")
            concerns.append("Power imbalances and exploitation risks")

        # Manipulation and addiction
        if any(word in text for word in ["engagement", "retention", "addictive", "persuasive"]):
            concerns.append("Ethical concerns about manipulative design and addiction")
            concerns.append("User autonomy vs. commercial interests")

        # Data and consent
        if "data collection" in text or "user data" in text:
            concerns.append("Informed consent for data collection may be inadequate")
            concerns.append("Secondary use of data beyond original consent")

        # Deepfakes and misinformation
        if any(word in text for word in ["deepfake", "synthetic media", "generated content"]):
            concerns.append("Potential for misinformation and erosion of trust")
            concerns.append("Nonconsensual synthetic media and identity theft")

        return concerns

    def _analyze_privacy(self, text: str) -> List[str]:
        """Analyze privacy implications"""
        privacy_issues = []

        # Check for privacy indicators
        matches = sum(1 for indicator in self.privacy_indicators if indicator in text)

        if matches > 0:
            if "personal data" in text or "user data" in text:
                privacy_issues.append("Collection and processing of personal data requires GDPR/CCPA compliance")
                privacy_issues.append("Data minimization - only collect what's necessary")
                privacy_issues.append("Right to deletion and data portability must be supported")

            if "health" in text or "medical" in text:
                privacy_issues.append("Health data is highly sensitive - HIPAA compliance required (US)")
                privacy_issues.append("Extra security measures needed for health information")

            if "location" in text or "tracking" in text:
                privacy_issues.append("Location tracking requires explicit user consent")
                privacy_issues.append("Historical location data can reveal sensitive patterns")

            if "biometric" in text or "facial" in text:
                privacy_issues.append("Biometric data is irreversible - cannot be changed if compromised")
                privacy_issues.append("Strict regulations on biometric data in many jurisdictions")

            if "children" in text or "minors" in text:
                privacy_issues.append("COPPA compliance required for children under 13 (US)")
                privacy_issues.append("Parental consent mechanisms needed")

            if "behavioral" in text or "profiling" in text:
                privacy_issues.append("Behavioral profiling raises privacy and manipulation concerns")
                privacy_issues.append("Users should be able to opt-out of profiling")

            # General privacy issues
            if not privacy_issues:
                privacy_issues.append("User privacy rights must be respected throughout data lifecycle")
                privacy_issues.append("Transparent privacy policy and user controls needed")

        return privacy_issues

    def _assess_social_impact(self, text: str) -> str:
        """Assess potential social impact"""
        positive_score = 0
        negative_score = 0

        # Positive indicators
        positive_words = [
            "improve", "benefit", "help", "assist", "enhance", "empower",
            "accessibility", "education", "health", "environment", "sustainability",
            "equality", "inclusion", "democratize"
        ]
        positive_score = sum(5 for word in positive_words if word in text)

        # Negative/risk indicators
        negative_words = [
            "replace", "eliminate", "surveillance", "control", "manipulation",
            "exploitation", "discrimination", "bias", "inequality", "harm"
        ]
        negative_score = sum(5 for word in negative_words if word in text)

        # Calculate net impact
        net_score = positive_score - negative_score

        if net_score > 15:
            return "Highly Positive - Project addresses important social needs with minimal downsides"
        elif net_score > 5:
            return "Positive - Benefits likely outweigh risks with proper safeguards"
        elif net_score > -5:
            return "Neutral/Mixed - Both benefits and risks present, careful design needed"
        elif net_score > -15:
            return "Concerning - Significant risks that must be carefully mitigated"
        else:
            return "High Risk - Potential for substantial social harm without major redesign"

    def _identify_regulatory_requirements(self, text: str) -> List[str]:
        """Identify regulatory compliance requirements"""
        requirements = []

        # Data protection regulations
        if any(word in text for word in ["personal data", "user data", "privacy"]):
            requirements.append("GDPR compliance (EU) - data protection and privacy")
            requirements.append("CCPA/CPRA compliance (California) - consumer privacy rights")
            requirements.append("Privacy impact assessment recommended")

        # Healthcare regulations
        if any(word in text for word in ["medical", "health", "patient", "clinical"]):
            requirements.append("HIPAA compliance (US) - health information privacy")
            requirements.append("FDA approval may be required for medical devices/software")
            requirements.append("IRB approval for human subjects research")

        # Financial regulations
        if any(word in text for word in ["financial", "banking", "payment", "credit"]):
            requirements.append("PCI DSS compliance for payment data")
            requirements.append("Financial services regulations (varies by jurisdiction)")

        # AI and automated decision-making
        if any(word in text for word in ["ai", "machine learning", "automated decision"]):
            requirements.append("EU AI Act compliance (risk-based regulation)")
            requirements.append("Algorithmic accountability and transparency requirements")
            requirements.append("Right to explanation for automated decisions")

        # Children's data
        if "children" in text or "minors" in text:
            requirements.append("COPPA compliance (US) - children's online privacy")
            requirements.append("Age verification mechanisms")

        # Biometrics
        if "biometric" in text or "facial recognition" in text:
            requirements.append("Illinois BIPA and similar biometric privacy laws")
            requirements.append("Explicit consent for biometric collection")

        # Accessibility
        if "public" in text or "government" in text or "website" in text:
            requirements.append("ADA/WCAG accessibility compliance")

        # Environmental
        if any(word in text for word in ["environmental", "emissions", "waste"]):
            requirements.append("Environmental impact assessment")
            requirements.append("EPA or equivalent environmental regulations")

        return requirements

    def _analyze_bias_fairness(self, text: str) -> List[str]:
        """Analyze bias and fairness risks"""
        risks = []

        # Check if project involves decision-making
        has_bias_risk = any(indicator in text for indicator in self.bias_indicators)

        if has_bias_risk:
            if "machine learning" in text or "ai" in text:
                risks.append("Training data may contain historical biases that will be learned")
                risks.append("Model may perform differently across demographic groups")
                risks.append("Regular bias audits and fairness testing required")

            if any(word in text for word in ["hiring", "recruitment", "employment"]):
                risks.append("AI hiring tools have shown gender and racial bias")
                risks.append("EEOC compliance required - cannot discriminate in hiring")

            if any(word in text for word in ["lending", "credit", "loan"]):
                risks.append("Fair lending laws prohibit discrimination")
                risks.append("Proxy discrimination through seemingly neutral variables")

            if "facial recognition" in text:
                risks.append("Facial recognition has higher error rates for people of color")
                risks.append("Gender and age bias in facial analysis systems")

            if "criminal justice" in text or "policing" in text:
                risks.append("Predictive policing may reinforce discriminatory patterns")
                risks.append("High stakes decisions require human oversight")

            if "recommendation" in text or "content" in text:
                risks.append("Recommendation algorithms may create filter bubbles")
                risks.append("Potential for amplifying harmful or extreme content")

            # General bias risks
            if not risks:
                risks.append("Algorithmic bias can arise from data, design, or deployment")
                risks.append("Disparate impact on protected groups must be monitored")

        return risks

    def _assess_environmental_impact(self, text: str) -> str:
        """Assess environmental impact"""
        impact_score = 0

        # Negative environmental factors
        if any(word in text for word in ["data center", "cloud computing", "large-scale computation"]):
            impact_score += 10

        if "machine learning training" in text or "deep learning" in text:
            impact_score += 15

        if "blockchain" in text or "cryptocurrency" in text or "mining" in text:
            impact_score += 20

        if "hardware" in text or "manufacturing" in text:
            impact_score += 10

        # Positive environmental factors
        if any(word in text for word in ["sustainable", "green", "renewable", "climate"]):
            impact_score -= 20

        if "optimization" in text or "efficiency" in text:
            impact_score -= 5

        # Determine impact level
        if impact_score >= 30:
            return "High Negative - Significant carbon footprint and energy consumption"
        elif impact_score >= 15:
            return "Moderate Negative - Notable energy consumption, carbon offsets recommended"
        elif impact_score >= 5:
            return "Low Negative - Standard environmental considerations apply"
        elif impact_score <= -10:
            return "Positive - Project contributes to environmental sustainability"
        else:
            return "Neutral - Minimal environmental impact expected"

    def _generate_recommendations(
        self, risk_level: str, concerns: List[str],
        privacy_issues: List[str], bias_risks: List[str]
    ) -> List[str]:
        """Generate ethical recommendations"""
        recommendations = []

        if risk_level == "Critical":
            recommendations.append("⚠️ CRITICAL: Extensive ethical review required before proceeding")
            recommendations.append("Consult with bioethics or AI ethics experts")
            recommendations.append("Consider if project should proceed at all given ethical risks")

        if risk_level in ["Critical", "High"]:
            recommendations.append("Establish ethics advisory board for ongoing oversight")
            recommendations.append("Conduct formal ethical impact assessment")
            recommendations.append("Implement robust harm mitigation strategies")

        if len(privacy_issues) > 0:
            recommendations.append("Implement privacy-by-design principles from the start")
            recommendations.append("Conduct privacy impact assessment (PIA)")
            recommendations.append("Consider privacy-enhancing technologies (differential privacy, etc.)")

        if len(bias_risks) > 0:
            recommendations.append("Ensure diverse, representative datasets")
            recommendations.append("Implement fairness metrics and regular bias audits")
            recommendations.append("Include diverse perspectives in design and testing")

        if len(concerns) > 5:
            recommendations.append("Phased rollout with continuous monitoring for unintended consequences")

        # Universal recommendations
        recommendations.append("Engage stakeholders, especially affected communities")
        recommendations.append("Maintain transparency about capabilities and limitations")
        recommendations.append("Establish clear accountability mechanisms")

        return recommendations

    def _identify_safeguards(
        self, risk_level: str, concerns: List[str],
        privacy_issues: List[str], regulatory: List[str]
    ) -> List[str]:
        """Identify required safeguards"""
        safeguards = []

        # High-risk safeguards
        if risk_level in ["Critical", "High"]:
            safeguards.append("Human-in-the-loop for high-stakes decisions")
            safeguards.append("Kill switch or ability to quickly disable system")
            safeguards.append("Comprehensive audit logs and monitoring")
            safeguards.append("Regular third-party ethical audits")

        # Privacy safeguards
        if len(privacy_issues) > 0:
            safeguards.append("End-to-end encryption for sensitive data")
            safeguards.append("Data anonymization and de-identification")
            safeguards.append("Access controls and authentication")
            safeguards.append("Regular security audits and penetration testing")

        # AI/ML safeguards
        if any("ai" in c.lower() or "machine learning" in c.lower() for c in concerns):
            safeguards.append("Model explainability and interpretability")
            safeguards.append("Continuous monitoring for model drift and degradation")
            safeguards.append("Fallback mechanisms for model failures")

        # Regulatory safeguards
        if len(regulatory) > 0:
            safeguards.append("Compliance management system")
            safeguards.append("Regular compliance audits")
            safeguards.append("Documentation and record-keeping")

        # Universal safeguards
        safeguards.append("Clear terms of service and user agreements")
        safeguards.append("Incident response and breach notification procedures")
        safeguards.append("Ethics training for all team members")

        return safeguards

    def _calculate_feasibility_score(
        self, base_score: float, concern_count: int,
        privacy_count: int, bias_count: int, risk_level: str
    ) -> float:
        """Calculate ethical feasibility score"""
        score = base_score

        # Penalties for ethical issues
        score -= min(concern_count * 4, 25)
        score -= min(privacy_count * 3, 15)
        score -= min(bias_count * 3, 15)

        # Additional penalty for critical risk
        if risk_level == "Critical":
            score -= 20

        return max(0, min(100, score))

    def _generate_details(
        self, description: str, risk_level: str,
        concerns: List[str], social_impact: str
    ) -> str:
        """Generate detailed ethical analysis"""
        details = f"""
Ethical Feasibility Analysis:

The project presents '{risk_level}' ethical risk level with the following social impact assessment:
{social_impact}

Number of Ethical Concerns Identified: {len(concerns)}

{'⚠️ CRITICAL ETHICAL ISSUES DETECTED - This project requires extensive ethical review and may face significant regulatory hurdles or public opposition.' if risk_level == 'Critical' else ''}
{'⚠️ HIGH ETHICAL RISKS - Careful consideration of ethical implications and robust safeguards are essential.' if risk_level == 'High' else ''}
{'Moderate ethical considerations present - standard ethical practices and compliance needed.' if risk_level == 'Medium' else ''}
{'Low ethical risk - project can proceed with standard ethical practices.' if risk_level == 'Low' else ''}

Ethical considerations should be integrated throughout the project lifecycle, not treated as an afterthought.
Engaging with affected communities and stakeholders is essential for responsible development.
"""
        return details.strip()
