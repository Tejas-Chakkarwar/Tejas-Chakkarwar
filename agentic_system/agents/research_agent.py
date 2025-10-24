"""
Research Agent - Autonomous Information Gathering

This agent DECIDES what information to search for, WHERE to search,
and HOW to interpret findings. True agentic behavior.
"""

from typing import List, Dict, Any
import asyncio

from agentic_system.agents.base_agent import BaseAgenticAgent
from agentic_system.models import ResearchRequest, ResearchFindings, InformationGap


class ResearchAgent(BaseAgenticAgent):
    """
    Autonomous research agent that:
    - Decides what information is needed
    - Chooses where to search
    - Evaluates relevance of findings
    - Synthesizes information
    """

    def __init__(self):
        super().__init__("research_agent")
        self.findings_cache = {}

    async def analyze(self, request: ResearchRequest) -> List[ResearchFindings]:
        """
        Main research method - agent autonomously gathers information
        """
        self.status = "working"
        self.current_task = f"Researching: {', '.join(request.queries[:2])}"

        all_findings = []

        for query in request.queries:
            # AGENT DECIDES: Should I search for this or use cached info?
            if query in self.findings_cache:
                self.log_action(f"Using cached results for: {query}", "cache_hit")
                all_findings.append(self.findings_cache[query])
                continue

            # AGENT EXECUTES: Perform research
            findings = await self._research_query(query, request.information_type, request.context)
            all_findings.append(findings)

            # Cache results
            self.findings_cache[query] = findings

            self.log_action(f"Researched: {query}", findings)

        self.status = "completed"
        return all_findings

    async def _research_query(self, query: str, info_type: str, context: str) -> ResearchFindings:
        """
        Research a specific query - agent decides how to approach it
        """
        # AGENT DECIDES: What's the best search strategy?
        strategy = self._decide_search_strategy(query, info_type, context)

        # AGENT EXECUTES: Perform web search
        search_results = self.tools['web_search'].search(query, num_results=5)

        # AGENT REASONS: Analyze and interpret results
        analysis = self._analyze_search_results(search_results, query, context)

        # AGENT EVALUATES: How relevant and confident am I?
        relevance = self._assess_relevance(search_results, context)
        confidence = self._assess_research_confidence(search_results, analysis)

        return ResearchFindings(
            query=query,
            findings=search_results,
            sources=[r['source'] for r in search_results],
            confidence=confidence,
            relevance_score=relevance,
            agent_reasoning=analysis
        )

    def _decide_search_strategy(self, query: str, info_type: str, context: str) -> Dict[str, Any]:
        """
        AGENTIC: Decide how to approach this search
        """
        prompt = f"""
You need to research: "{query}"
Information type: {info_type}
Context: {context}

Decide on the best search strategy:
1. Should you search broadly or specifically?
2. What specific aspects should you focus on?
3. What sources would be most credible?
4. What related queries might be helpful?

Provide a focused search strategy.
"""

        strategy_reasoning = self.tools['llm'].reason(prompt, temperature=0.6)

        return {
            'approach': 'specific' if 'specific' in strategy_reasoning.lower() else 'broad',
            'focus_areas': self._extract_focus_areas(strategy_reasoning),
            'reasoning': strategy_reasoning
        }

    def _analyze_search_results(self, results: List[Dict], query: str, context: str) -> str:
        """
        AGENTIC: Analyze what the search results mean
        """
        results_summary = "\n".join([
            f"- {r['title']}: {r['snippet']}" for r in results[:3]
        ])

        prompt = f"""
You searched for: "{query}"
Context: {context}

Top search results:
{results_summary}

Analyze these results:
1. What are the key insights?
2. What patterns or trends do you see?
3. How reliable is this information?
4. What's missing or unclear?
5. What conclusions can you draw?

Provide a concise analysis.
"""

        return self.tools['llm'].reason(prompt, temperature=0.5)

    def _assess_relevance(self, results: List[Dict], context: str) -> float:
        """
        AGENTIC: Assess how relevant results are to the context
        """
        if not results:
            return 0.0

        # Agent reasons about relevance
        results_text = " ".join([r.get('snippet', '') for r in results[:3]])

        prompt = f"""
Context: {context}

Search results: {results_text[:500]}

How relevant are these results to the context?
Rate from 0-100 where:
- 90-100: Highly relevant, directly answers questions
- 70-89: Relevant, provides useful information
- 50-69: Moderately relevant, some useful info
- 30-49: Somewhat relevant, limited usefulness
- 0-29: Not relevant

Provide just the numeric score and brief reasoning.
"""

        response = self.tools['llm'].reason(prompt, temperature=0.3)
        score = self._extract_score(response)

        return score

    def _assess_research_confidence(self, results: List[Dict], analysis: str) -> float:
        """
        AGENTIC: Agent assesses its own confidence in the research
        """
        if not results:
            return 0.1

        # Multiple sources increase confidence
        num_sources = len(set(r['source'] for r in results))
        source_confidence = min(num_sources * 0.15, 0.35)

        # Quality of analysis affects confidence
        if 'unclear' in analysis.lower() or 'missing' in analysis.lower():
            analysis_confidence = 0.4
        elif 'consistent' in analysis.lower() or 'clear' in analysis.lower():
            analysis_confidence = 0.75
        else:
            analysis_confidence = 0.6

        # Combine factors
        total_confidence = (source_confidence + analysis_confidence) / 2 + 0.2

        return min(total_confidence, 0.95)

    def _extract_focus_areas(self, text: str) -> List[str]:
        """Extract focus areas from reasoning"""
        areas = []
        for line in text.split('\n'):
            if 'focus' in line.lower() or 'aspect' in line.lower():
                areas.append(line.strip())

        return areas if areas else ['general research']

    def make_decision(self, analysis_results: List[ResearchFindings]) -> Dict[str, Any]:
        """
        AGENTIC: Decide if more research is needed
        """
        avg_confidence = sum(f.confidence for f in analysis_results) / len(analysis_results) if analysis_results else 0
        avg_relevance = sum(f.relevance_score for f in analysis_results) / len(analysis_results) if analysis_results else 0

        # AGENT DECIDES: Is this enough or do I need more?
        if avg_confidence < 0.6 or avg_relevance < 0.6:
            decision = "need_more_research"
            reasoning = f"Confidence ({avg_confidence:.2f}) or relevance ({avg_relevance:.2f}) is too low"
        else:
            decision = "sufficient"
            reasoning = f"Research is sufficient with confidence {avg_confidence:.2f}"

        return {
            'decision': decision,
            'reasoning': reasoning,
            'average_confidence': avg_confidence,
            'average_relevance': avg_relevance,
            'findings_count': len(analysis_results)
        }

    async def deep_dive(self, topic: str, context: str) -> ResearchFindings:
        """
        AGENTIC: Agent decides to do deeper research on a topic
        """
        # Agent generates multiple related queries
        prompt = f"""
You need to deeply research: {topic}
Context: {context}

Generate 5 specific search queries that would give comprehensive information about this topic.
Focus on different aspects: technical, market, cost, competition, trends.
"""

        queries_response = self.tools['llm'].reason(prompt)

        # Extract queries
        queries = []
        for line in queries_response.split('\n'):
            if any(c.isdigit() and '.' in line for c in line[:5]):
                query = line.split('.', 1)[-1].strip().strip('"\'')
                if query:
                    queries.append(query)

        # Research all queries
        request = ResearchRequest(
            queries=queries[:5],
            information_type="comprehensive",
            context=context,
            priority="high"
        )

        findings_list = await self.analyze(request)

        # Synthesize all findings
        all_insights = []
        all_sources = []
        for f in findings_list:
            all_insights.append(f.agent_reasoning)
            all_sources.extend(f.sources)

        synthesized = self.tools['llm'].synthesize_insights(all_insights)

        return ResearchFindings(
            query=f"Deep dive: {topic}",
            findings=[{'synthesis': synthesized}],
            sources=list(set(all_sources)),
            confidence=max(f.confidence for f in findings_list),
            relevance_score=max(f.relevance_score for f in findings_list),
            agent_reasoning=synthesized
        )
