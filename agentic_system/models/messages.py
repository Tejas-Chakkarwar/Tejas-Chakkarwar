"""
Message Models for Inter-Agent Communication
Truly agentic system - agents communicate via these message types
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum


class AnalysisPhase(str, Enum):
    """Phases of analysis workflow"""
    PLANNING = "planning"
    INFORMATION_GATHERING = "information_gathering"
    PARALLEL_ANALYSIS = "parallel_analysis"
    VALIDATION = "validation"
    REFINEMENT = "refinement"
    SYNTHESIS = "synthesis"
    COMPLETE = "complete"


class ConfidenceLevel(str, Enum):
    """Confidence levels for agent decisions"""
    VERY_LOW = "very_low"  # < 30%
    LOW = "low"  # 30-50%
    MEDIUM = "medium"  # 50-70%
    HIGH = "high"  # 70-90%
    VERY_HIGH = "very_high"  # > 90%


# ============================================================================
# Orchestrator Messages
# ============================================================================

class ProjectAnalysisRequest(BaseModel):
    """Initial request to analyze a project"""
    project_description: str
    project_name: str
    requester_address: str
    analysis_depth: str = "comprehensive"  # quick, standard, comprehensive, deep


class AnalysisStrategy(BaseModel):
    """Orchestrator's strategy for analyzing the project"""
    needs_external_research: bool
    research_queries: List[str]
    priority_dimensions: List[str]  # Which dimensions to focus on
    confidence_threshold: float = 0.75
    max_iterations: int = 3
    estimated_time: str


class OrchestratorDecision(BaseModel):
    """Decision made by orchestrator about next steps"""
    phase: AnalysisPhase
    action: str
    reasoning: str
    agents_to_spawn: List[str]
    confidence: float


# ============================================================================
# Research Agent Messages
# ============================================================================

class ResearchRequest(BaseModel):
    """Request to research agent to gather information"""
    queries: List[str]
    information_type: str  # market, technical, cost, regulatory, competitor
    context: str
    priority: str = "normal"  # low, normal, high, critical


class ResearchFindings(BaseModel):
    """Findings from research agent"""
    query: str
    findings: List[Dict[str, Any]]
    sources: List[str]
    confidence: float
    relevance_score: float
    agent_reasoning: str  # Why agent thinks this is relevant


class InformationGap(BaseModel):
    """Identified gap in information"""
    gap_type: str  # missing_data, unclear, contradictory, insufficient_detail
    description: str
    priority: str
    suggested_action: str


# ============================================================================
# Analysis Agent Messages
# ============================================================================

class AnalysisRequest(BaseModel):
    """Request to specialized analysis agent"""
    project_description: str
    additional_context: Optional[Dict[str, Any]] = None
    research_findings: Optional[List[ResearchFindings]] = None
    focus_areas: Optional[List[str]] = None
    iteration_number: int = 1


class DimensionAnalysis(BaseModel):
    """Analysis result from specialized agent"""
    dimension: str  # technology, cost, ethical, market
    score: float  # 0-100
    confidence: ConfidenceLevel
    reasoning: str  # Agent's reasoning process
    key_findings: List[str]
    risks: List[Dict[str, str]]  # {risk: str, severity: str, reasoning: str}
    opportunities: List[Dict[str, str]]
    assumptions: List[str]
    information_gaps: List[InformationGap]
    recommendations: List[str]
    supporting_evidence: List[str]
    agent_thought_process: str  # Agent's internal reasoning


# ============================================================================
# Validator Messages
# ============================================================================

class ValidationRequest(BaseModel):
    """Request to validator to check analysis quality"""
    analyses: List[DimensionAnalysis]
    project_description: str
    iteration_number: int


class Conflict(BaseModel):
    """Detected conflict between analyses"""
    conflict_type: str  # contradiction, inconsistency, logic_error
    involved_dimensions: List[str]
    description: str
    severity: str  # low, medium, high, critical
    suggested_resolution: str


class ValidationResult(BaseModel):
    """Result of validation"""
    overall_confidence: float
    is_consistent: bool
    conflicts: List[Conflict]
    quality_issues: List[str]
    coverage_gaps: List[str]
    strengths: List[str]
    needs_refinement: bool
    refinement_suggestions: List[str]
    validator_reasoning: str


# ============================================================================
# Refinement Messages
# ============================================================================

class RefinementRequest(BaseModel):
    """Request to refine specific dimension analysis"""
    dimension: str
    original_analysis: DimensionAnalysis
    validation_feedback: ValidationResult
    specific_issues: List[str]
    additional_research: Optional[List[ResearchFindings]] = None


# ============================================================================
# Synthesis Messages
# ============================================================================

class SynthesisRequest(BaseModel):
    """Request to synthesize all analyses into final decision"""
    analyses: List[DimensionAnalysis]
    validation_result: ValidationResult
    project_description: str


class FinalDecision(BaseModel):
    """Final autonomous decision about project feasibility"""
    overall_feasibility: str  # HIGHLY_FEASIBLE, FEASIBLE, MODERATELY_FEASIBLE, CHALLENGING, NOT_FEASIBLE
    overall_score: float
    confidence: ConfidenceLevel
    decision_reasoning: str  # Detailed reasoning for the decision
    recommendation: str
    critical_risks: List[Dict[str, Any]]
    key_opportunities: List[Dict[str, Any]]
    next_steps: List[str]
    dimension_scores: Dict[str, float]
    analysis_quality: str
    assumptions_made: List[str]
    limitations: List[str]


# ============================================================================
# Agent Status Messages
# ============================================================================

class AgentStatus(BaseModel):
    """Status update from an agent"""
    agent_type: str
    status: str  # idle, working, completed, error
    current_task: Optional[str] = None
    progress: float  # 0-100
    message: str


class AgentQuery(BaseModel):
    """Agent asking for clarification or additional info"""
    agent_type: str
    question: str
    context: str
    priority: str
    blocking: bool  # Is agent blocked waiting for answer?


# ============================================================================
# Memory and Context
# ============================================================================

class AgentMemory(BaseModel):
    """Agent's memory of analysis process"""
    project_name: str
    phase: AnalysisPhase
    iteration: int
    decisions_made: List[Dict[str, Any]]
    findings_collected: List[Any]
    confidence_history: List[float]
    actions_taken: List[str]


class AnalysisContext(BaseModel):
    """Shared context across all agents"""
    project_description: str
    project_name: str
    current_phase: AnalysisPhase
    iteration: int
    all_research: List[ResearchFindings]
    all_analyses: List[DimensionAnalysis]
    validation_results: List[ValidationResult]
    orchestrator_decisions: List[OrchestratorDecision]
