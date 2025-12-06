from common.schemas import StudyAgentState
from langgraph.graph import StateGraph, END

def initialize_study_plan(state):
    print("Agent Node: Initializing Study Plan State")
    return {"next_step": "plan_generation"}

def generate_study_plan(state):
    print("Agent Node: Generating Study Plan via LLM")
    return {"next_step": "plan_refinement"}

def refine_and_format_plan(state):
    print("Agent Node: Refining and Formatting Plan")
    return {"next_step": "save_to_db"}

def save_plan_to_db(state):
    print("Agent Node: Saving Plan to DB")
    return {"next_step": "complete"}

def build_studyflow_graph(llm_client):
    graph = StateGraph(StudyAgentState)

    graph.add_node("initialize", initialize_study_plan)
    graph.add_node("generate_plan", generate_study_plan)
    graph.add_node("refine_plan", refine_and_format_plan)
    graph.add_node("save_plan", save_plan_to_db)

    graph.set_entry_point("initialize")

    graph.add_edge("initialize", "generate_plan")
    graph.add_edge("generate_plan", "refine_plan")
    graph.add_edge("refine_plan", "save_plan")
    graph.add_edge("save_plan", END)

    return graph.compile()