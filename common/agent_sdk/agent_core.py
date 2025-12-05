import json
from typing import Callable, List, Dict, Any

from langchain_core.runnables import Runnable, RunnableLambda
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END

from common.ai_sdk.llm_client import AIClient
from common.agent_sdk.schemas import AgentState, ToolCall
from common.agent_sdk.tools import create_vector_search_tool

def create_agent_executor(
    llm_client: AIClient, 
    tools: List[Callable], 
    system_prompt: str
) -> Runnable:
    """
    Creates and compiles the core LangGraph state machine for a single agent lobe.
    """
    
    tool_names = [t.__name__ for t in tools]
    
    llm = llm_client.get_chat_model(temperature=0.0).bind(
        tools=tools, 
        tool_choice="auto"
    )
    
    llm_chain = (
        RunnableLambda(lambda state: [SystemMessage(content=system_prompt)])
        + RunnableLambda(lambda state: [HumanMessage(content=state["user_query"])])
        + llm
    )

    def call_llm(state: AgentState) -> Dict[str, Any]:
        """
        Invokes the LLM to decide on the next action (ToolCall) or the final response.
        """
        result = llm_chain.invoke(state)
        
        if result.tool_calls:
            tool_call_data = result.tool_calls[0]
            action = ToolCall(
                tool_name=tool_call_data['name'],
                tool_input=json.dumps(tool_call_data['args'])
            )
            return {"agent_action": action, "run_count": state["run_count"] + 1}
        else:
            return {"final_response": result.content}


    def execute_tool(state: AgentState) -> Dict[str, Any]:
        """
        Executes the tool function specified by the AgentAction.
        """
        action: ToolCall = state['agent_action']
        tool_map = {t.__name__: t for t in tools}
        
        if action.tool_name not in tool_map:
            raise ValueError(f"Unknown tool: {action.tool_name}")

        try:
            tool_args = json.loads(action.tool_input)
            
            tool_result = tool_map[action.tool_name](**tool_args)
            
            return {"tool_output": tool_result}
        except Exception as e:
            return {"tool_output": f"Tool execution failed with error: {e}. Please try a different approach."}

    def route_to_next_step(state: AgentState) -> str:
        """
        Determines the next node in the graph based on the LLM's output.
        """
        if state.get("final_response"):
            return "end"
        
        if state.get("agent_action"):
            return "execute_tool"
            
        return "call_llm"
        
    workflow = StateGraph(AgentState)

    workflow.add_node("call_llm", call_llm)
    workflow.add_node("execute_tool", execute_tool)

    workflow.set_entry_point("call_llm")
    
    workflow.add_conditional_edges(
        "call_llm", 
        route_to_next_step,
        {"execute_tool": "execute_tool", "end": END}
    )
    
    workflow.add_edge("execute_tool", "call_llm")

    app = workflow.compile()
    
    return app

# --- Example Usage: Simulate InsightMate Agent ---

if __name__ == "__main__":
    from common.data_sdk.vector_client import VectorClient
    
    llm_client = AIClient(model_name="gpt-4o-mini")
    vector_client = VectorClient(llm_client)

    INSIGHT_MATE_COLLECTION = "insight_mate_v1"
    
    INSIGHT_MATE_PROMPT = (
        "You are InsightMate, a world-class AI meeting summary and action item tracker. "
        "Your goal is to be concise, helpful, and grounded in facts from your memory. "
        "ALWAYS use the vector_memory_search tool if the user asks about past meetings, "
        "tasks, or decisions. If you cannot find relevant information, state that clearly."
    )
    
    tools = [
        create_vector_search_tool(vector_client, INSIGHT_MATE_COLLECTION),
    ]

    vector_client.upsert_documents(
        INSIGHT_MATE_COLLECTION,
        ["Kakarot must finalize the Qdrant connection setup by EOD Friday."],
        [{"source": "meeting_01"}]
    )
    
    insight_mate_executor = create_agent_executor(llm_client, tools, INSIGHT_MATE_PROMPT)
    
    user_query = "What is the action item I was assigned from the last meeting?"
    initial_state = AgentState(user_query=user_query, chat_history=[], tool_output="", agent_action=None, final_response="", run_count=0)
    
    print(f"\n--- Running InsightMate Agent for Query: '{user_query}' ---")
    
    for step in insight_mate_executor.stream(initial_state):
        if "__end__" in step:
            final_state = step['__end__']
            print("\n--- FINAL AGENT RESPONSE ---")
            print(final_state['final_response'])
            break
        
        node_name = list(step.keys())[0]
        print(f"[{node_name}] -> State Updated: {list(step[node_name].keys())}")