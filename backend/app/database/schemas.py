"""
MongoDB schemas and data models for BiasScope
Designed by Tejas - Schema design and data consistency lead
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr


class SyntheticInput(BaseModel):
    """Schema for synthetic input data"""
    input_id: str
    features: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ModelOutput(BaseModel):
    """Schema for model output"""
    input_id: str
    output: Any
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class BiasScore(BaseModel):
    """Schema for bias score metrics"""
    metric_name: str
    value: float
    threshold: Optional[float] = None
    passed: bool


class FairnessMetric(BaseModel):
    """Schema for fairness metrics"""
    metric: str
    value: float
    group: Optional[str] = None


class FeatureInfluence(BaseModel):
    """Schema for feature influence on bias"""
    feature: str
    influence: float
    importance: float


class AnalysisResults(BaseModel):
    """Schema for complete analysis results"""
    overall_bias_score: float
    fairness_metrics: List[FairnessMetric]
    feature_influence: List[FeatureInfluence]
    demographic_parity: List[Dict[str, Any]]
    explainability_insights: Optional[Dict[str, Any]] = None


class AnalysisDocument(BaseModel):
    """Schema for analysis document in MongoDB"""
    analysis_id: str
    model_url: str
    status: str  # "started", "in_progress", "completed", "failed"
    progress: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # Test data
    synthetic_inputs: List[SyntheticInput] = []
    model_outputs: List[ModelOutput] = []
    
    # Results
    bias_scores: List[BiasScore] = []
    results: Optional[AnalysisResults] = None
    
    # Report metadata
    report_generated: bool = False
    report_path: Optional[str] = None
    
    # User reference
    user_id: Optional[str] = None
    
    # Error handling
    error_message: Optional[str] = None


# User-related schemas
class UserProfile(BaseModel):
    """Schema for user profile"""
    user_id: str
    email: str
    username: str
    profession: str
    full_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    analysis_history: List[str] = []  # List of analysis IDs


class UserDocument(BaseModel):
    """Schema for user document in MongoDB"""
    user_id: str
    email: str
    username: str
    password_hash: str
    profession: str
    full_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    analysis_history: List[Dict[str, Any]] = []  # List of analysis with URLs
    is_active: bool = True
