"""
Base Agent Class - Foundation for Truly Agentic Behavior

This base class provides core agentic capabilities:
- Decision-making
- Tool selection and use
- Memory and context
- Self-reflection
- Confidence assessment
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import asyncio
from datetime import datetime

from agentic_system.tools import llm_tool, web_search_tool
from agentic_system.models import AgentStatus, ConfidenceLevel


class BaseAgenticAgent(ABC):
    """
    Base class for all agentic agents
    Provides core agentic capabilities
    """

    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.memory = []  # Agent's memory of actions and decisions
        self.tools = {
            'llm': llm_tool,
            'web_search': web_search_tool
        }
        self.status = "idle"
        self.confidence = 0.0

    # ========================================================================
    # Core Agentic Capabilities
    # ========================================================================

    def decide(self, situation: str, options: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        AGENTIC: Make a decision based on situation
        Agent reasons about options and chooses best action
        """
        prompt = f"""
You are a {self.agent_type} agent. Analyze this situation and decide what to do next.

Situation: {situation}

Available options:
{chr(10).join(f"{i+1}. {opt}" for i, opt in enumerate(options))}

Context: {context}

Think through:
1. What information do I have?
2. What information do I need?
3. What are the risks of each option?
4. Which option best achieves my goal?

Provide your decision with clear reasoning.
"""

        reasoning = self.tools['llm'].reason(prompt)

        # Agent reflects on its decision
        confidence = self._assess_confidence(reasoning)

        decision = {
            'agent': self.agent_type,
            'situation': situation,
            'chosen_action': self._extract_choice(reasoning, options),
            'reasoning': reasoning,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }

        # Store in memory
        self.memory.append(decision)

        return decision

    def select_tool(self, task: str, context: Dict[str, Any]) -> str:
        """
        AGENTIC: Decide which tool to use for a task
        """
        prompt = f"""
You need to complete this task: {task}

Available tools:
- llm: For reasoning, analysis, and decision-making
- web_search: For finding external information

Context: {context}

Which tool should you use and why?
"""

        reasoning = self.tools['llm'].reason(prompt, temperature=0.3)

        if 'web_search' in reasoning.lower() or 'search' in reasoning.lower():
            return 'web_search'
        else:
            return 'llm'

    def assess_situation(self, situation_desc: str) -> Dict[str, Any]:
        """
        AGENTIC: Assess a situation and determine what's needed
        """
        prompt = f"""
Assess this situation:
{situation_desc}

Provide:
1. What information is present?
2. What information is missing?
3. What are the key challenges?
4. What should be done next?
5. Your confidence in this assessment (0-100)
"""

        assessment = self.tools['llm'].reason(prompt)

        return {
            'assessment': assessment,
            'confidence': self._extract_confidence(assessment),
            'agent': self.agent_type
        }

    def reflect_on_work(self, work_done: str) -> Dict[str, Any]:
        """
        AGENTIC: Self-reflect on work quality
        Agents can evaluate their own work
        """
        prompt = f"""
You just completed this work:
{work_done}

Reflect on:
1. Quality of the work (0-100)
2. What was done well?
3. What could be improved?
4. Are there any gaps or errors?
5. Should this work be refined further?
"""

        reflection = self.tools['llm'].reason(prompt, temperature=0.5)

        return {
            'reflection': reflection,
            'quality_score': self._extract_score(reflection),
            'needs_refinement': 'refin' in reflection.lower() or 'improv' in reflection.lower(),
            'agent': self.agent_type
        }

    def identify_information_gaps(self, analysis: str, context: str) -> List[str]:
        """
        AGENTIC: Identify what information is missing
        """
        prompt = f"""
Given this analysis:
{analysis}

And this context:
{context}

What critical information is missing or unclear?
List specific gaps that need to be filled for a complete analysis.
"""

        response = self.tools['llm'].reason(prompt)

        # Extract list items
        gaps = []
        for line in response.split('\n'):
            if line.strip().startswith(('-', '•', '*')) or any(c.isdigit() and '.' in line for c in line[:3]):
                gaps.append(line.strip().lstrip('-•*0123456789. '))

        return [g for g in gaps if g]

    def _assess_confidence(self, reasoning: str) -> float:
        """Assess confidence level from reasoning"""
        # Look for confidence indicators
        if 'high confidence' in reasoning.lower() or 'confident' in reasoning.lower():
            return 0.85
        elif 'moderate' in reasoning.lower() or 'fairly' in reasoning.lower():
            return 0.65
        elif 'low confidence' in reasoning.lower() or 'uncertain' in reasoning.lower():
            return 0.40
        else:
            return 0.70  # Default

    def _extract_confidence(self, text: str) -> float:
        """Extract numeric confidence from text"""
        import re
        # Look for patterns like "confidence: 75" or "75%"
        match = re.search(r'confidence[:\s]+(\d+)', text.lower())
        if match:
            return float(match.group(1)) / 100.0

        match = re.search(r'(\d+)%', text)
        if match:
            return float(match.group(1)) / 100.0

        return self._assess_confidence(text)

    def _extract_score(self, text: str) -> float:
        """Extract numeric score from text"""
        import re
        match = re.search(r'(\d+)/100', text)
        if match:
            return float(match.group(1)) / 100.0

        match = re.search(r'score[:\s]+(\d+)', text.lower())
        if match:
            return float(match.group(1)) / 100.0

        return 0.70  # Default

    def _extract_choice(self, reasoning: str, options: List[str]) -> str:
        """Extract chosen option from reasoning"""
        reasoning_lower = reasoning.lower()
        for opt in options:
            if opt.lower() in reasoning_lower:
                return opt
        return options[0]  # Default to first option

    def get_status(self) -> AgentStatus:
        """Get current agent status"""
        return AgentStatus(
            agent_type=self.agent_type,
            status=self.status,
            current_task=getattr(self, 'current_task', None),
            progress=getattr(self, 'progress', 0.0),
            message=f"{self.agent_type} is {self.status}"
        )

    # ========================================================================
    # Abstract Methods - Must be implemented by subclasses
    # ========================================================================

    @abstractmethod
    async def analyze(self, request: Any) -> Any:
        """
        Main analysis method - each agent implements its own logic
        """
        pass

    @abstractmethod
    def make_decision(self, analysis_results: Any) -> Dict[str, Any]:
        """
        Make an autonomous decision based on analysis
        """
        pass

    # ========================================================================
    # Helper Methods
    # ========================================================================

    def log_action(self, action: str, result: Any):
        """Log an action to memory"""
        self.memory.append({
            'action': action,
            'result': result,
            'timestamp': datetime.now().isoformat(),
            'agent': self.agent_type
        })

    def get_memory_summary(self) -> str:
        """Get summary of agent's memory/actions"""
        if not self.memory:
            return "No previous actions"

        recent = self.memory[-5:]  # Last 5 actions
        summary = f"Recent actions by {self.agent_type}:\n"
        for i, mem in enumerate(recent, 1):
            action = mem.get('action', 'unknown')
            summary += f"{i}. {action}\n"

        return summary
