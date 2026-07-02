from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# ============================================================================
# Request Models
# ============================================================================

class AnalyzeIdeaRequest(BaseModel):
    idea: str
    language: Optional[str] = "english"  # english, bangla, banglish


# ============================================================================
# Response Models
# ============================================================================

class IdeaExtraction(BaseModel):
    title: str
    description: str
    sector: str
    target_customer: str
    revenue_model: str
    location: str


class DemandAnalysis(BaseModel):
    score: float
    market_size: str
    competition: str
    opportunities: List[str]
    threats: List[str]


class RegulatoryAnalysis(BaseModel):
    risk_score: float
    key_regulators: List[str]
    critical_approvals: Any  # Can be str or list
    estimated_timeline: int
    cost_estimate: Any  # Can be int or str
    warnings: Any  # Can be str or list


class BusinessCanvas(BaseModel):
    key_partners: Any
    key_activities: Any
    key_resources: Any
    value_proposition: Any
    customer_segments: Any
    channels: Any
    customer_relationships: Any
    revenue_streams: Any
    cost_structure: Any


class InvestorQuestion(BaseModel):
    question: str
    category: str


class AnalysisResult(BaseModel):
    idea_extraction: IdeaExtraction
    demand_analysis: DemandAnalysis
    regulatory_analysis: RegulatoryAnalysis
    business_canvas: BusinessCanvas
    investor_questions: List[InvestorQuestion]
    overall_readiness_score: float
    analysis_status: str


class VerifiedClaim(BaseModel):
    claim: str
    status: str
    source: Optional[str]


class UnverifiedClaim(BaseModel):
    claim: str
    reason: str


class VerificationResult(BaseModel):
    verified_claims: List[VerifiedClaim]
    unverified_claims: List[UnverifiedClaim]
    corrections: str
