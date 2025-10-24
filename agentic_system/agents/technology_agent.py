"""
Technology Analysis Agent - LLM-Powered Reasoning

This agent REASONS about technology feasibility using LLM intelligence,
not just keyword matching. Truly agentic.
"""

from typing import Dict, Any, List
import asyncio

from agentic_system.agents.base_agent import BaseAgenticAgent
from agentic_system.models import AnalysisRequest, DimensionAnalysis, ConfidenceLevel, InformationGap


class TechnologyAnalysisAgent(BaseAgenticAgent):
    """
    Autonomous technology analysis agent that:
    - Reasons about technical feasibility using LLM
    - Identifies technology maturity through understanding, not keywords
    - Assesses complexity with contextual reasoning
    - Makes intelligent decisions about technical viability
    """

    def __init__(self):
        super().__init__("technology_agent")

    async def analyze(self, request: AnalysisRequest) -> DimensionAnalysis:
        """
        Analyze technology feasibility using LLM reasoning
        """
        self.status = "working"
        self.current_task = "Analyzing technology feasibility"

        # Step 1: AGENT REASONS about what to analyze
        analysis_plan = self._plan_analysis(request.project_description)

        # Step 2: AGENT PERFORMS multi-step reasoning
        tech_assessment = await self._assess_technology_maturity(
            request.project_description,
            request.additional_context
        )

        complexity_assessment = await self._assess_implementation_complexity(
            request.project_description,
            tech_assessment
        )

        risk_assessment = await self._identify_technical_risks(
            request.project_description,
            tech_assessment,
            complexity_assessment
        )

        timeline_estimate = await self._estimate_development_timeline(
            request.project_description,
            complexity_assessment
        )

        # Step 3: AGENT IDENTIFIES gaps in understanding
        info_gaps = self.identify_information_gaps(
            f"{tech_assessment}\n{complexity_assessment}",
            request.project_description
        )

        # Step 4: AGENT CALCULATES confidence
        confidence = self._calculate_confidence(
            tech_assessment,
            complexity_assessment,
            len(info_gaps)
        )

        # Step 5: AGENT SYNTHESIZES and DECIDES
        final_analysis = await self._synthesize_analysis(
            tech_assessment,
            complexity_assessment,
            risk_assessment,
            timeline_estimate
        )

        # Step 6: AGENT REFLECTS on work quality
        reflection = self.reflect_on_work(final_analysis)

        # Extract structured information from reasoning
        score = self._extract_feasibility_score(final_analysis)
        maturity = self._extract_maturity_level(tech_assessment)
        complexity = self._extract_complexity_level(complexity_assessment)

        self.status = "completed"

        return DimensionAnalysis(
            dimension="technology",
            score=score,
            confidence=confidence,
            reasoning=final_analysis,
            key_findings=self._extract_key_findings(final_analysis),
            risks=self._structure_risks(risk_assessment),
            opportunities=self._extract_opportunities(final_analysis),
            assumptions=self._extract_assumptions(final_analysis),
            information_gaps=self._structure_info_gaps(info_gaps),
            recommendations=self._generate_recommendations(final_analysis, confidence),
            supporting_evidence=self._extract_evidence(tech_assessment),
            agent_thought_process=analysis_plan
        )

    def _plan_analysis(self, project_desc: str) -> str:
        """
        AGENTIC: Plan the analysis approach
        """
        prompt = f"""
You are a technology analysis agent. Plan how you will analyze this project:

{project_desc[:1000]}

Create an analysis plan covering:
1. What technical aspects need evaluation?
2. What are the most important questions to answer?
3. What information might be missing?
4. What order should you analyze things in?

Provide a clear, focused plan.
"""

        return self.tools['llm'].reason(prompt, temperature=0.6)

    async def _assess_technology_maturity(self, project_desc: str, context: Dict = None) -> str:
        """
        AGENTIC: Reason about technology maturity using LLM understanding
        """
        system_prompt = """You are an expert technology analyst. Assess technology maturity by:
1. Understanding the actual technical requirements
2. Reasoning about current state of those technologies
3. Considering real-world deployment examples
4. Evaluating ecosystem maturity (tools, libraries, talent)

Provide nuanced assessment, not just keyword matching."""

        prompt = f"""
Analyze the technology maturity for this project:

{project_desc}

Additional context: {context if context else 'None'}

Assess:
1. What technologies are required?
2. How mature is each technology? (Emerging/Developing/Mature/Obsolete)
3. What is the current state of these technologies in the real world?
4. Are there proven implementations and case studies?
5. How available are developers with these skills?
6. What is the ecosystem like (libraries, tools, documentation)?

Provide detailed, reasoned assessment.
"""

        return self.tools['llm'].reason(prompt, system_prompt, temperature=0.5)

    async def _assess_implementation_complexity(self, project_desc: str, maturity_assessment: str) -> str:
        """
        AGENTIC: Reason about implementation complexity
        """
        prompt = f"""
Given this project:
{project_desc}

And this technology maturity assessment:
{maturity_assessment}

Analyze the implementation complexity:

1. How many moving parts are there?
2. How complex is the system integration?
3. What are the hardest technical challenges?
4. How much specialized expertise is needed?
5. What could go wrong technically?

Rate complexity as: Low, Medium, High, or Very High with detailed reasoning.
"""

        return self.tools['llm'].reason(prompt, temperature=0.5)

    async def _identify_technical_risks(self, project_desc: str, maturity: str, complexity: str) -> str:
        """
        AGENTIC: Identify and reason about technical risks
        """
        prompt = f"""
Project: {project_desc}

Technology Maturity: {maturity}
Implementation Complexity: {complexity}

Identify specific technical risks:

1. What could fail technically?
2. What dependencies could cause problems?
3. What technical unknowns exist?
4. What are the scaling challenges?
5. What security/reliability concerns exist?

For each risk, assess:
- Likelihood (high/medium/low)
- Impact (critical/major/minor)
- Mitigation strategies

Be specific and realistic.
"""

        return self.tools['llm'].reason(prompt, temperature=0.6)

    async def _estimate_development_timeline(self, project_desc: str, complexity: str) -> str:
        """
        AGENTIC: Estimate realistic timeline based on reasoning
        """
        prompt = f"""
Project: {project_desc}

Complexity Assessment: {complexity}

Estimate a realistic development timeline:

1. Break down into major phases (design, MVP, beta, production)
2. Consider team ramp-up time
3. Account for unknown unknowns (add buffer)
4. Consider integration and testing time
5. Account for iterations and refinement

Provide timeline estimates with reasoning for each phase.
"""

        return self.tools['llm'].reason(prompt, temperature=0.4)

    async def _synthesize_analysis(self, maturity: str, complexity: str, risks: str, timeline: str) -> str:
        """
        AGENTIC: Synthesize all analyses into coherent conclusion
        """
        insights = [maturity, complexity, risks, timeline]
        synthesis = self.tools['llm'].synthesize_insights(insights)

        # Add feasibility conclusion
        conclusion_prompt = f"""
Based on this technology analysis:
{synthesis}

Provide:
1. Overall technology feasibility score (0-100)
2. Clear feasibility conclusion
3. Top 3 strengths
4. Top 3 concerns
5. Final recommendation

Be direct and actionable.
"""

        return self.tools['llm'].reason(conclusion_prompt, temperature=0.4)

    def _extract_feasibility_score(self, analysis: str) -> float:
        """Extract feasibility score from analysis"""
        import re

        # Look for explicit score
        match = re.search(r'score[:\s]+(\d+)', analysis.lower())
        if match:
            return float(match.group(1))

        # Look for percentage
        match = re.search(r'feasibility[:\s]+(\d+)%', analysis.lower())
        if match:
            return float(match.group(1))

        # Infer from language
        analysis_lower = analysis.lower()
        if 'highly feasible' in analysis_lower or 'excellent' in analysis_lower:
            return 85.0
        elif 'feasible' in analysis_lower and 'not' not in analysis_lower:
            return 70.0
        elif 'challenging' in analysis_lower or 'difficult' in analysis_lower:
            return 45.0
        elif 'not feasible' in analysis_lower or 'infeasible' in analysis_lower:
            return 25.0
        else:
            return 60.0  # Default moderate

    def _extract_maturity_level(self, assessment: str) -> str:
        """Extract maturity level from assessment"""
        assessment_lower = assessment.lower()
        if 'emerging' in assessment_lower or 'experimental' in assessment_lower:
            return "Emerging"
        elif 'developing' in assessment_lower or 'growing' in assessment_lower:
            return "Developing"
        elif 'mature' in assessment_lower or 'established' in assessment_lower:
            return "Mature"
        elif 'obsolete' in assessment_lower or 'outdated' in assessment_lower:
            return "Obsolete"
        else:
            return "Developing"

    def _extract_complexity_level(self, assessment: str) -> str:
        """Extract complexity level"""
        assessment_lower = assessment.lower()
        if 'very high' in assessment_lower:
            return "Very High"
        elif 'high' in assessment_lower:
            return "High"
        elif 'medium' in assessment_lower or 'moderate' in assessment_lower:
            return "Medium"
        elif 'low' in assessment_lower:
            return "Low"
        else:
            return "Medium"

    def _calculate_confidence(self, maturity: str, complexity: str, gaps_count: int) -> ConfidenceLevel:
        """Calculate confidence level"""
        # Start with base confidence
        confidence_score = 0.7

        # Adjust based on information clarity
        if 'unclear' in maturity.lower() or 'uncertain' in maturity.lower():
            confidence_score -= 0.15

        if gaps_count > 3:
            confidence_score -= gaps_count * 0.05

        # Bounded
        confidence_score = max(0.2, min(0.95, confidence_score))

        # Map to enum
        if confidence_score > 0.9:
            return ConfidenceLevel.VERY_HIGH
        elif confidence_score > 0.7:
            return ConfidenceLevel.HIGH
        elif confidence_score > 0.5:
            return ConfidenceLevel.MEDIUM
        elif confidence_score > 0.3:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW

    def _extract_key_findings(self, analysis: str) -> List[str]:
        """Extract key findings"""
        findings = []
        for line in analysis.split('\n'):
            if any(x in line.lower() for x in ['strength', 'concern', 'finding', 'key']):
                clean_line = line.strip().lstrip('-•*0123456789. ')
                if clean_line and len(clean_line) > 10:
                    findings.append(clean_line)

        return findings[:10]

    def _structure_risks(self, risk_text: str) -> List[Dict[str, str]]:
        """Structure risks from text"""
        risks = []
        for line in risk_text.split('\n'):
            if line.strip() and any(c in line for c in ['-', '•', '*', '1', '2', '3']):
                clean = line.strip().lstrip('-•*0123456789. ')
                if clean and len(clean) > 10:
                    severity = "high" if 'critical' in clean.lower() or 'major' in clean.lower() else "medium"
                    risks.append({
                        'risk': clean,
                        'severity': severity,
                        'reasoning': 'Identified through technical analysis'
                    })

        return risks[:8]

    def _extract_opportunities(self, analysis: str) -> List[Dict[str, str]]:
        """Extract opportunities"""
        opps = []
        for line in analysis.split('\n'):
            if 'opportunity' in line.lower() or 'advantage' in line.lower() or 'strength' in line.lower():
                clean = line.strip().lstrip('-•*0123456789. ')
                if clean and len(clean) > 10:
                    opps.append({
                        'opportunity': clean,
                        'impact': 'positive'
                    })

        return opps[:5]

    def _extract_assumptions(self, analysis: str) -> List[str]:
        """Extract assumptions made"""
        return [
            "Technology maturity based on current state",
            "Standard development practices followed",
            "Adequate technical expertise available",
            "Normal development velocity"
        ]

    def _structure_info_gaps(self, gaps: List[str]) -> List[InformationGap]:
        """Structure information gaps"""
        return [
            InformationGap(
                gap_type="missing_data",
                description=gap,
                priority="medium",
                suggested_action=f"Research: {gap}"
            )
            for gap in gaps[:5]
        ]

    def _generate_recommendations(self, analysis: str, confidence: ConfidenceLevel) -> List[str]:
        """Generate recommendations"""
        recs = []
        for line in analysis.split('\n'):
            if 'recommend' in line.lower() or 'should' in line.lower() or 'suggest' in line.lower():
                clean = line.strip().lstrip('-•*0123456789. ')
                if clean and len(clean) > 10:
                    recs.append(clean)

        if not recs:
            recs = [
                "Validate technical assumptions with prototype",
                "Assess team capabilities against requirements",
                "Create detailed technical architecture plan"
            ]

        return recs[:6]

    def _extract_evidence(self, assessment: str) -> List[str]:
        """Extract supporting evidence"""
        evidence = []
        for line in assessment.split('\n'):
            if 'example' in line.lower() or 'case' in line.lower() or 'proven' in line.lower():
                clean = line.strip()
                if clean and len(clean) > 15:
                    evidence.append(clean)

        return evidence[:5]

    def make_decision(self, analysis: DimensionAnalysis) -> Dict[str, Any]:
        """
        AGENTIC: Make autonomous decision about technical feasibility
        """
        if analysis.score >= 70:
            decision = "TECHNICALLY_FEASIBLE"
            action = "proceed"
        elif analysis.score >= 50:
            decision = "MODERATELY_FEASIBLE"
            action = "proceed_with_caution"
        else:
            decision = "NOT_FEASIBLE"
            action = "reconsider"

        return {
            'decision': decision,
            'recommended_action': action,
            'reasoning': f"Score: {analysis.score}/100, Confidence: {analysis.confidence}",
            'agent': self.agent_type
        }
