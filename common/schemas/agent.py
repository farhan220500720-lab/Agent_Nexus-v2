from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any



class AgentState(BaseModel):
    """
    Represents the internal state of a generic agent during execution.
    This state object is used across different agent types (e.g., StudyFlow).
    """
    request_id: str = Field(..., description="ID linking back to the original task request.")
    topic: str = Field(..., description="The main topic or query for the agent.")
    current_step: str = Field("INITIALIZING", description="The current stage of the agent execution (e.g., PLANNING, GENERATING_CONTENT, REVIEW, ANALYZING).")
    plan_data: Optional[Dict[str, Any]] = Field(None, description="The generated output data (e.g., StudyPlan or AnalysisResult data).")
    intermediate_results: List[str] = Field(default_factory=list, description="A log of key intermediate outputs or decisions.")
    error_message: Optional[str] = Field(None, description="Holds error information if the agent failed.")
