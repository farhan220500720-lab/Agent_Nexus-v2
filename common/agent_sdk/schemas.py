from typing import List, Annotated, TypedDict
from datetime import datetime

from pydantic import BaseModel, Field

from langgraph.graph.message import AnyMessage, add_messages

class ActionItem(BaseModel):
    """
    Defines the structure for a single, actionable item extracted from a transcript.
    This schema is used for Structured Output generation by the LLM.
    """
    action_item_id: str = Field(description="A unique UUID for the action item.")
    assignee: str = Field(description="The person or team responsible for the action.")
    task_description: str = Field(description="A concise summary of the task to be completed.")
    due_date: str = Field(description="The date the task is due (e.g., 'EOD Tuesday' or '2024-12-31').")

class MeetingSummary(BaseModel):
    """
    Defines the complete structured output for the InsightMate Lobe.
    """
    meeting_title: str = Field(description="The final title of the meeting.")
    key_decisions: List[str] = Field(description="A list of 3-5 critical decisions made during the meeting.")
    key_metrics: List[str] = Field(description="A list of any numbers, percentages, or key data points mentioned.")
    action_items: List[ActionItem] = Field(description="The list of structured action items extracted from the transcript.")
    summary_date: datetime = Field(description="The date the summary was generated, set to the current UTC timestamp.")


class AgentState(TypedDict):
    """
    Represents the state of the agent in the LangGraph pipeline.
    """
    messages: Annotated[List[AnyMessage], add_messages]
    
    retrieved_context: str
    
    query: str
    
    final_output: MeetingSummary


if __name__ == "__main__":
    
    print("--- Pydantic Schema Validation Test ---")
    
    sample_action_item = ActionItem(
        action_item_id="a1b2c3d4-e5f6-7890-abcd-ef0123456789",
        assignee="Jane Doe",
        task_description="Update the public shareholder report.",
        due_date="Tuesday"
    )
    
    sample_summary = MeetingSummary(
        meeting_title="Q4 Revenue Review",
        key_decisions=["Exceeded Q4 target by 5%", "Increased Q1 marketing budget by 15%"],
        key_metrics=["45%", "5%", "15%"],
        action_items=[sample_action_item],
        summary_date=datetime.now()
    )
    
    print(f"Validated Action Item: {sample_action_item.model_dump_json(indent=2)}")
    print(f"\nValidated Meeting Summary: {sample_summary.model_dump_json(indent=2)}")

    print("\n--- LangGraph State Initialization Test ---")
    initial_state: AgentState = {
        "messages": [("user", "Analyze this meeting transcript.")],
        "retrieved_context": "None yet.",
        "query": "The Q4 budget was approved.",
        "final_output": None
    }
    
    print(f"Initial Agent State Keys: {list(initial_state.keys())}")
    