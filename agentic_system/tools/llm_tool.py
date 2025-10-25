"""
LLM Tool for Agent Reasoning
This is what makes agents truly agentic - they use LLMs to REASON, not just match keywords
"""

import os
import json
from typing import Dict, Any, List, Optional
from agentic_system.config import Config


class LLMTool:
    """
    Tool for agents to use LLMs for reasoning
    This enables true agentic behavior - understanding, reasoning, decision-making
    """

    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or Config.LLM_PROVIDER

        # Initialize appropriate client
        if self.provider == "openai":
            try:
                import openai # type: ignore
                self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
                self.model = Config.OPENAI_MODEL
            except ImportError:
                print("⚠️  OpenAI not installed. Install: pip install openai")
                self.provider = "mock"

        elif self.provider == "anthropic":
            try:
                import anthropic # type: ignore
                self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
                self.model = Config.ANTHROPIC_MODEL
            except ImportError:
                print("⚠️  Anthropic not installed. Install: pip install anthropic")
                self.provider = "mock"

        elif self.provider == "gemini":
            try:
                import google.generativeai as genai
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.client = genai.GenerativeModel(Config.GEMINI_MODEL)
                self.model = Config.GEMINI_MODEL
                print(f"✅ Using Gemini {Config.GEMINI_MODEL} (Free tier: 1500 requests/day)")
            except ImportError:
                print("⚠️  Gemini not installed. Install: pip install google-generativeai")
                self.provider = "mock"

        if self.provider == "mock":
            print("📝 Using Mock LLM - responses will be simulated")

    def reason(self, prompt: str, system_prompt: Optional[str] = None,
               temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        Main reasoning function - agents call this to think about problems
        """
        if self.provider == "openai":
            return self._reason_openai(prompt, system_prompt, temperature, max_tokens)
        elif self.provider == "anthropic":
            return self._reason_anthropic(prompt, system_prompt, temperature, max_tokens)
        elif self.provider == "gemini":
            return self._reason_gemini(prompt, system_prompt, temperature, max_tokens)
        else:
            return self._reason_mock(prompt)

    def _reason_openai(self, prompt: str, system_prompt: Optional[str],
                       temperature: float, max_tokens: int) -> str:
        """Reason using OpenAI GPT"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=Config.LLM_TIMEOUT
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ OpenAI error: {e}")
            return f"Error in LLM reasoning: {str(e)}"

    def _reason_anthropic(self, prompt: str, system_prompt: Optional[str],
                          temperature: float, max_tokens: int) -> str:
        """Reason using Anthropic Claude"""
        try:
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}]
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            response = self.client.messages.create(**kwargs)
            return response.content[0].text
        except Exception as e:
            print(f"❌ Anthropic error: {e}")
            return f"Error in LLM reasoning: {str(e)}"

    def _reason_gemini(self, prompt: str, system_prompt: Optional[str],
                   temperature: float, max_tokens: int) -> str:
        """Reason using Google Gemini"""
        try:
            import google.generativeai as genai
            from google.generativeai.types import HarmCategory, HarmBlockThreshold

            # Combine system prompt with user prompt for Gemini
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

        # Configure generation
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
        
        # Set permissive safety settings for business/research analysis
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

            # Disable safety filters to prevent blocking on feasibility analysis prompts
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

            response = self.client.generate_content(
                full_prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )

            # Handle response with proper error checking
            if hasattr(response, 'text'):
                return response.text
            elif response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if candidate.content.parts:
                    return candidate.content.parts[0].text
                else:
                    return f"Gemini blocked response (finish_reason: {candidate.finish_reason})"
            else:
                return "Could not extract response from Gemini."

        except Exception as e:
            print(f"❌ Gemini error: {e}")
            return f"Error in LLM reasoning: {str(e)}"

    def _reason_mock(self, prompt: str) -> str:
        """Mock reasoning for testing without API keys"""
        # Extract key information from prompt
        if "technology" in prompt.lower():
            return """
Technology Analysis (Mock):
Based on the project description, the technology appears to be at a DEVELOPING maturity level.
The implementation complexity is MODERATE to HIGH due to integration requirements.
Key technologies identified: machine learning, cloud infrastructure, APIs.
Timeline estimate: 8-12 months for MVP.
Risk: Technology dependencies may cause delays.
Confidence: 70%
"""
        elif "cost" in prompt.lower():
            return """
Cost Analysis (Mock):
Estimated budget range: $200K - $800K
Budget category: MEDIUM
Main cost drivers: personnel (50%), infrastructure (25%), R&D (25%)
ROI potential: MEDIUM-HIGH based on market size
Funding sources: Venture capital, angel investors, grants
Confidence: 65%
"""
        elif "ethical" in prompt.lower():
            return """
Ethical Analysis (Mock):
Ethical risk level: MEDIUM
Key concerns: data privacy, user consent, algorithmic bias
Privacy implications: Requires GDPR/CCPA compliance
Social impact: POSITIVE - addresses real user needs
Required safeguards: encryption, access controls, audit logs
Confidence: 75%
"""
        elif "market" in prompt.lower():
            return """
Market Analysis (Mock):
Market timing: OPTIMAL - growing market with demand
Market size: $500M - $2B TAM
Competition: MODERATE - several players but room for differentiation
Adoption barriers: User education, integration complexity
Competitive advantages: Unique feature set, better UX
Confidence: 70%
"""
        else:
            return """
Analysis (Mock):
The project shows promise with moderate feasibility.
Key strengths: clear value proposition, proven technology.
Key challenges: market competition, resource requirements.
Confidence: 65%
"""

    def structured_reasoning(self, prompt: str, output_format: Dict[str, Any],
                           system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Request structured reasoning output (for parsing)
        """
        format_instruction = f"\n\nProvide your response in JSON format matching this structure: {json.dumps(output_format, indent=2)}"
        full_prompt = prompt + format_instruction

        response = self.reason(full_prompt, system_prompt, temperature=0.3)

        # Try to parse JSON response
        try:
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()

            return json.loads(json_str)
        except json.JSONDecodeError:
            print("⚠️  Could not parse structured response, returning raw text")
            return {"raw_response": response}

    def multi_step_reasoning(self, steps: List[Dict[str, str]],
                            system_prompt: Optional[str] = None) -> List[str]:
        """
        Multi-step reasoning - agent thinks through problem step by step
        """
        results = []
        context = ""

        for i, step in enumerate(steps):
            step_prompt = step["prompt"]
            if context:
                step_prompt = f"Previous reasoning: {context}\n\n{step_prompt}"

            result = self.reason(step_prompt, system_prompt)
            results.append(result)
            context += f"\nStep {i+1}: {result}\n"

        return results

    def validate_reasoning(self, reasoning: str, criteria: List[str]) -> Dict[str, Any]:
        """
        Validate reasoning against criteria (agents can self-check)
        """
        prompt = f"""
Evaluate the following reasoning against these criteria:
{chr(10).join(f"- {c}" for c in criteria)}

Reasoning to evaluate:
{reasoning}

Provide:
1. Whether reasoning meets each criterion (yes/no)
2. Overall quality score (0-100)
3. Specific issues found
4. Suggestions for improvement
"""
        return self.structured_reasoning(prompt, {
            "criteria_met": {},
            "overall_score": 0,
            "issues": [],
            "suggestions": []
        })

    def compare_analyses(self, analysis1: str, analysis2: str) -> Dict[str, Any]:
        """
        Compare two analyses to find conflicts or inconsistencies
        """
        prompt = f"""
Compare these two analyses and identify:
1. Agreements
2. Disagreements/conflicts
3. Complementary insights
4. Which analysis is more credible and why

Analysis 1:
{analysis1}

Analysis 2:
{analysis2}
"""
        return self.structured_reasoning(prompt, {
            "agreements": [],
            "conflicts": [],
            "complementary": [],
            "more_credible": "",
            "reasoning": ""
        })

    def synthesize_insights(self, insights: List[str]) -> str:
        """
        Synthesize multiple insights into coherent conclusion
        """
        prompt = f"""
Synthesize these insights into a coherent, comprehensive conclusion:

{chr(10).join(f"{i+1}. {insight}" for i, insight in enumerate(insights))}

Provide a synthesis that:
- Integrates all key points
- Resolves any contradictions
- Highlights most important findings
- Draws overall conclusion
"""
        return self.reason(prompt)


# Global LLM tool instance for agents to use
llm_tool = LLMTool()
