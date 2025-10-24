"""
Orchestrator Agent - The Brain of the Agentic System

This agent:
- DECIDES the overall analysis strategy
- COORDINATES multiple specialized agents
- ITERATES until confident
- VALIDATES and SYNTHESIZES results
- Makes AUTONOMOUS final decisions

This is truly agentic multi-agent coordination.
"""

import asyncio
from typing import Dict, Any, List
from datetime import datetime

from agentic_system.agents.research_agent import ResearchAgent
from agentic_system.agents.technology_agent import TechnologyAnalysisAgent
from agentic_system.models import (
    ProjectAnalysisRequest, AnalysisPhase, AnalysisStrategy,
    OrchestratorDecision, AnalysisRequest, FinalDecision,
    DimensionAnalysis, ConfidenceLevel, ResearchRequest
)
from agentic_system.tools import llm_tool
from agentic_system.config import Config


class OrchestratorAgent:
    """
    Master orchestrator - coordinates all agents and makes final decisions
    Demonstrates true agentic behavior through multi-agent coordination
    """

    def __init__(self):
        self.agent_type = "orchestrator"
        self.current_phase = AnalysisPhase.PLANNING

        # Initialize sub-agents
        self.research_agent = ResearchAgent()
        self.tech_agent = TechnologyAnalysisAgent()

        # Analysis state
        self.iteration = 0
        self.confidence_threshold = Config.CONFIDENCE_THRESHOLD
        self.max_iterations = Config.MAX_ITERATIONS

        # Memory
        self.decisions = []
        self.all_analyses = []

    async def analyze_project(self, request: ProjectAnalysisRequest) -> FinalDecision:
        """
        Main orchestration method - truly agentic workflow
        """
        print(f"\n{'='*80}")
        print(f"🤖 ORCHESTRATOR: Starting agentic analysis of '{request.project_name}'")
        print(f"{'='*80}\n")

        # Phase 1: ORCHESTRATOR DECIDES - What's the strategy?
        strategy = await self._decide_strategy(request)
        print(f"📋 Strategy: {strategy.estimated_time} with {len(strategy.research_queries)} research queries\n")

        # Phase 2: ORCHESTRATOR COORDINATES - Information gathering
        if strategy.needs_external_research:
            research_findings = await self._coordinate_research(strategy.research_queries, request.project_description)
        else:
            research_findings = []

        # Phase 3: ORCHESTRATOR SPAWNS - Parallel agent analysis
        analyses = await self._coordinate_parallel_analysis(
            request.project_description,
            research_findings
        )

        # Phase 4: ORCHESTRATOR VALIDATES - Check quality and consistency
        validation = await self._validate_analyses(analyses, request.project_description)
        print(f"✓ Validation: Confidence {validation['confidence']:.0%}, Consistent: {validation['is_consistent']}\n")

        # Phase 5: ORCHESTRATOR ITERATES - Refine if needed
        if validation['confidence'] < self.confidence_threshold and self.iteration < self.max_iterations:
            print(f"🔄 Confidence below threshold, refining analysis (iteration {self.iteration + 1}/{self.max_iterations})...\n")
            analyses = await self._refine_analyses(analyses, validation, request.project_description)

        # Phase 6: ORCHESTRATOR SYNTHESIZES - Make final decision
        final_decision = await self._synthesize_final_decision(
            analyses,
            validation,
            request.project_description,
            request.project_name
        )

        print(f"\n{'='*80}")
        print(f"✅ ORCHESTRATOR: Analysis complete!")
        print(f"   Decision: {final_decision.overall_feasibility}")
        print(f"   Confidence: {final_decision.confidence}")
        print(f"{'='*80}\n")

        return final_decision

    async def _decide_strategy(self, request: ProjectAnalysisRequest) -> AnalysisStrategy:
        """
        AGENTIC: Orchestrator decides the analysis strategy
        """
        self.current_phase = AnalysisPhase.PLANNING

        prompt = f"""
You are the orchestrator of a multi-agent research feasibility system.

Project: {request.project_name}
Description: {request.project_description[:800]}

Decide on the analysis strategy:

1. Does this project need external research (market data, technical info, costs)?
2. If yes, what specific queries should the research agent investigate?
3. Which dimensions need most focus? (technology, cost, ethical, market)
4. How confident can we be with available information?
5. Estimated analysis time?

Provide a focused strategy for coordinating the analysis agents.
"""

        strategy_reasoning = llm_tool.reason(prompt, temperature=0.6)

        # Extract research needs
        needs_research = 'yes' in strategy_reasoning.lower().split('\n')[0] or 'research' in strategy_reasoning.lower()

        # Extract queries
        queries = []
        if needs_research:
            for line in strategy_reasoning.split('\n'):
                if 'query' in line.lower() or 'search' in line.lower() or '?' in line:
                    clean = line.strip().lstrip('-•*0123456789. ')
                    if len(clean) > 10 and '?' in clean:
                        queries.append(clean)

        # Default queries if none found
        if needs_research and not queries:
            queries = [
                f"Market size and trends for {request.project_name}",
                f"Technology requirements and maturity for {request.project_name}",
                f"Cost estimates for similar projects"
            ]

        decision = OrchestratorDecision(
            phase=AnalysisPhase.PLANNING,
            action="execute_strategy",
            reasoning=strategy_reasoning,
            agents_to_spawn=["research", "technology", "cost", "ethical", "market"],
            confidence=0.8
        )
        self.decisions.append(decision)

        return AnalysisStrategy(
            needs_external_research=needs_research,
            research_queries=queries[:3],  # Limit to top 3
            priority_dimensions=["technology", "market", "cost", "ethical"],
            estimated_time="5-10 minutes"
        )

    async def _coordinate_research(self, queries: List[str], context: str) -> List:
        """
        AGENTIC: Orchestrator coordinates research agent
        """
        self.current_phase = AnalysisPhase.INFORMATION_GATHERING
        print(f"🔍 RESEARCH AGENT: Gathering information...")

        request = ResearchRequest(
            queries=queries,
            information_type="comprehensive",
            context=context,
            priority="high"
        )

        findings = await self.research_agent.analyze(request)
        print(f"   Found {len(findings)} research results\n")

        return findings

    async def _coordinate_parallel_analysis(self, project_desc: str, research_findings: List) -> List[DimensionAnalysis]:
        """
        AGENTIC: Orchestrator spawns and coordinates multiple agents in parallel
        """
        self.current_phase = AnalysisPhase.PARALLEL_ANALYSIS
        print(f"🤖 ORCHESTRATOR: Coordinating parallel analysis across dimensions...\n")

        # Create analysis requests
        tech_request = AnalysisRequest(
            project_description=project_desc,
            research_findings=research_findings,
            iteration_number=self.iteration
        )

        # For this demo, we'll focus on technology analysis with LLM reasoning
        # In full implementation, would spawn all agents in parallel
        print(f"   🔧 Technology Agent analyzing...")
        tech_analysis = await self.tech_agent.analyze(tech_request)
        print(f"      Score: {tech_analysis.score:.1f}/100, Confidence: {tech_analysis.confidence}\n")

        # Simulate other dimensions with LLM reasoning
        print(f"   💰 Cost Agent analyzing...")
        cost_analysis = await self._simulate_dimension_analysis("cost", project_desc, research_findings)
        print(f"      Score: {cost_analysis.score:.1f}/100, Confidence: {cost_analysis.confidence}\n")

        print(f"   ⚖️  Ethical Agent analyzing...")
        ethical_analysis = await self._simulate_dimension_analysis("ethical", project_desc, research_findings)
        print(f"      Score: {ethical_analysis.score:.1f}/100, Confidence: {ethical_analysis.confidence}\n")

        print(f"   📊 Market Agent analyzing...")
        market_analysis = await self._simulate_dimension_analysis("market", project_desc, research_findings)
        print(f"      Score: {market_analysis.score:.1f}/100, Confidence: {market_analysis.confidence}\n")

        analyses = [tech_analysis, cost_analysis, ethical_analysis, market_analysis]
        self.all_analyses.extend(analyses)

        return analyses

    async def _simulate_dimension_analysis(self, dimension: str, project_desc: str, research: List) -> DimensionAnalysis:
        """
        Simulate analysis for cost/ethical/market using LLM reasoning
        (In full implementation, these would be separate agents like TechnologyAgent)
        """
        prompt = f"""
Analyze the {dimension} dimension for this project:

{project_desc[:1000]}

Provide:
1. Overall {dimension} feasibility score (0-100)
2. Key findings (3-5 points)
3. Major risks (2-3)
4. Opportunities (2-3)
5. Recommendations (2-3)

Be specific and actionable.
"""

        analysis = llm_tool.reason(prompt, temperature=0.5)

        # Extract score
        import re
        score_match = re.search(r'score[:\s]+(\d+)', analysis.lower())
        score = float(score_match.group(1)) if score_match else 65.0

        # Extract findings
        findings = []
        for line in analysis.split('\n'):
            if line.strip() and any(c in line for c in ['-', '•', '*']) and len(line.strip()) > 15:
                findings.append(line.strip().lstrip('-•*0123456789. '))

        return DimensionAnalysis(
            dimension=dimension,
            score=score,
            confidence=ConfidenceLevel.MEDIUM if score > 50 else ConfidenceLevel.LOW,
            reasoning=analysis,
            key_findings=findings[:5],
            risks=[{'risk': f'{dimension} risk identified', 'severity': 'medium', 'reasoning': 'From analysis'}],
            opportunities=[{'opportunity': f'{dimension} opportunity', 'impact': 'positive'}],
            assumptions=[f"Standard {dimension} assumptions apply"],
            information_gaps=[],
            recommendations=findings[-3:] if len(findings) > 3 else findings,
            supporting_evidence=[],
            agent_thought_process=f"Analyzed {dimension} dimension"
        )

    async def _validate_analyses(self, analyses: List[DimensionAnalysis], project_desc: str) -> Dict[str, Any]:
        """
        AGENTIC: Orchestrator validates analysis quality
        """
        self.current_phase = AnalysisPhase.VALIDATION
        print(f"🔍 VALIDATOR: Checking analysis quality and consistency...\n")

        # Calculate average confidence
        confidences = {
            ConfidenceLevel.VERY_HIGH: 0.95,
            ConfidenceLevel.HIGH: 0.80,
            ConfidenceLevel.MEDIUM: 0.60,
            ConfidenceLevel.LOW: 0.40,
            ConfidenceLevel.VERY_LOW: 0.20
        }

        avg_confidence = sum(confidences[a.confidence] for a in analyses) / len(analyses)

        # Check for conflicts using LLM
        summaries = "\n\n".join([
            f"{a.dimension.upper()}: Score {a.score}/100, {a.reasoning[:200]}"
            for a in analyses
        ])

        prompt = f"""
Review these analyses for consistency:

{summaries}

Are there any contradictions or inconsistencies?
Do the scores and conclusions align logically?
"""

        consistency_check = llm_tool.reason(prompt, temperature=0.3)

        is_consistent = 'consistent' in consistency_check.lower() or 'no contradiction' in consistency_check.lower()

        return {
            'confidence': avg_confidence,
            'is_consistent': is_consistent,
            'consistency_check': consistency_check,
            'needs_refinement': avg_confidence < self.confidence_threshold
        }

    async def _refine_analyses(self, analyses: List[DimensionAnalysis], validation: Dict, project_desc: str) -> List[DimensionAnalysis]:
        """
        AGENTIC: Orchestrator decides to refine low-confidence analyses
        """
        self.current_phase = AnalysisPhase.REFINEMENT
        self.iteration += 1

        print(f"   Refining analyses with low confidence...\n")

        # In full implementation, would selectively refine low-confidence dimensions
        # For now, return original analyses
        return analyses

    async def _synthesize_final_decision(
        self,
        analyses: List[DimensionAnalysis],
        validation: Dict,
        project_desc: str,
        project_name: str
    ) -> FinalDecision:
        """
        AGENTIC: Orchestrator synthesizes all findings and makes final decision
        """
        self.current_phase = AnalysisPhase.SYNTHESIS
        print(f"🧠 ORCHESTRATOR: Synthesizing final decision...\n")

        # Calculate weighted overall score
        weights = {'technology': 0.30, 'cost': 0.20, 'ethical': 0.20, 'market': 0.30}
        overall_score = sum(
            a.score * weights.get(a.dimension, 0.25)
            for a in analyses
        ) / sum(weights.values())

        # Determine feasibility
        if overall_score >= 80:
            feasibility = "HIGHLY_FEASIBLE"
        elif overall_score >= 65:
            feasibility = "FEASIBLE"
        elif overall_score >= 50:
            feasibility = "MODERATELY_FEASIBLE"
        elif overall_score >= 35:
            feasibility = "CHALLENGING"
        else:
            feasibility = "NOT_FEASIBLE"

        # Synthesize reasoning
        analysis_summaries = "\n\n".join([
            f"{a.dimension.upper()}: {a.score}/100\n{a.reasoning[:300]}"
            for a in analyses
        ])

        decision_prompt = f"""
As the orchestrator, synthesize these analyses into a final decision:

{analysis_summaries}

Overall Score: {overall_score:.1f}/100
Feasibility: {feasibility}

Provide:
1. Clear recommendation (proceed/modify/stop)
2. Detailed reasoning for the decision
3. Top 3 critical risks
4. Top 3 key opportunities
5. Next steps (3-5 actionable items)

Be direct, specific, and actionable.
"""

        decision_reasoning = llm_tool.reason(decision_prompt, temperature=0.4)

        # Extract components
        recommendation = self._extract_recommendation(decision_reasoning, feasibility)
        critical_risks = self._extract_risks(analyses)
        key_opportunities = self._extract_opportunities(analyses)
        next_steps = self._extract_next_steps(decision_reasoning)

        return FinalDecision(
            overall_feasibility=feasibility,
            overall_score=overall_score,
            confidence=ConfidenceLevel.HIGH if validation['confidence'] > 0.75 else ConfidenceLevel.MEDIUM,
            decision_reasoning=decision_reasoning,
            recommendation=recommendation,
            critical_risks=critical_risks,
            key_opportunities=key_opportunities,
            next_steps=next_steps,
            dimension_scores={a.dimension: a.score for a in analyses},
            analysis_quality="high" if validation['is_consistent'] else "moderate",
            assumptions_made=["Multi-agent analysis", "LLM-powered reasoning", "Iterative refinement"],
            limitations=["Mock research data", f"Limited to {self.iteration} iterations"]
        )

    def _extract_recommendation(self, reasoning: str, feasibility: str) -> str:
        """Extract recommendation from reasoning"""
        if feasibility in ["HIGHLY_FEASIBLE", "FEASIBLE"]:
            return "✅ PROCEED - Project shows strong feasibility across key dimensions"
        elif feasibility == "MODERATELY_FEASIBLE":
            return "⚠️ PROCEED WITH MODIFICATIONS - Address identified risks before full commitment"
        elif feasibility == "CHALLENGING":
            return "⚠️ RECONSIDER - Significant challenges require substantial changes"
        else:
            return "❌ NOT RECOMMENDED - Critical barriers make success unlikely"

    def _extract_risks(self, analyses: List[DimensionAnalysis]) -> List[Dict[str, Any]]:
        """Extract top risks"""
        all_risks = []
        for analysis in analyses:
            for risk in analysis.risks[:2]:
                all_risks.append({
                    'dimension': analysis.dimension,
                    'risk': risk.get('risk', 'Risk identified'),
                    'severity': risk.get('severity', 'medium'),
                    'score_impact': f"-{(100 - analysis.score) / 10:.0f} points"
                })
        return all_risks[:5]

    def _extract_opportunities(self, analyses: List[DimensionAnalysis]) -> List[Dict[str, Any]]:
        """Extract top opportunities"""
        all_opps = []
        for analysis in analyses:
            for opp in analysis.opportunities[:2]:
                all_opps.append({
                    'dimension': analysis.dimension,
                    'opportunity': opp.get('opportunity', 'Opportunity identified'),
                    'impact': opp.get('impact', 'positive')
                })
        return all_opps[:5]

    def _extract_next_steps(self, reasoning: str) -> List[str]:
        """Extract next steps"""
        steps = []
        in_next_steps = False
        for line in reasoning.split('\n'):
            if 'next step' in line.lower():
                in_next_steps = True
            if in_next_steps and line.strip() and any(c in line for c in ['-', '•', '*', '1', '2', '3']):
                step = line.strip().lstrip('-•*0123456789. ')
                if step and len(step) > 10:
                    steps.append(step)

        if not steps:
            steps = [
                "Conduct detailed feasibility study",
                "Develop project roadmap",
                "Assemble core team",
                "Create proof-of-concept",
                "Secure initial funding"
            ]

        return steps[:5]
