import os
import random
from typing import List, Dict, Any

from common.ai_sdk import AIClient, EmbeddingProvider
from common.data_sdk import VectorClient
from common.agent_sdk.schemas import MeetingSummary

INSIGHT_MATE_COLLECTION = "insight_mate_knowledge_base"

def run_insight_mate_test():
    """
    Initial entry point for the InsightMate Agent.
    
    This function demonstrates the basic initialization and use of the SDK 
    components (AI Client and Vector Client) to perform a RAG task.
    """
    print("--- InsightMate Agent Lobe Initializing ---")

    try:
        ai_client = AIClient(model_name="gpt-4o-mini")
        vector_client = VectorClient(ai_client=ai_client)
    except Exception as e:
        print(f"FATAL ERROR: Could not initialize core SDK clients. Ensure Qdrant is running and API keys are set. Error details: {e}")
        return

    documents_to_ingest = [
        "The Q3 sales meeting concluded that the new Gemini-powered analysis feature resulted in a 45% efficiency gain in the data pipeline.",
        "Team lead Kakarot suggested standardizing the agent communication protocol using Redis streams for Phase 3 integration.",
        "InsightMate's primary function is to summarize meeting transcripts and extract actionable intelligence.",
        "The deadline for the StudyFlow prototype feature freeze is next Tuesday."
    ]
    metadatas_to_ingest = [
        {"source": "Q3_Review", "date": "2024-10-15"},
        {"source": "Architecture_Meeting", "date": "2024-11-29"},
        {"source": "Project_Scope_V1", "date": "2024-09-01"},
        {"source": "Roadmap_2025", "date": "2024-12-05"}
    ]
    
    print(f"\n[Memory] Ingesting {len(documents_to_ingest)} documents into {INSIGHT_MATE_COLLECTION}...")
    vector_client.upsert_documents(INSIGHT_MATE_COLLECTION, documents_to_ingest, metadatas_to_ingest)

    test_query = "What did Kakarot propose for the agent communication protocol?"
    print(f"\n[User Query] -> {test_query}")
    
    retrieved_knowledge = vector_client.search(INSIGHT_MATE_COLLECTION, test_query, top_k=2)

    context = "\n---\n".join([f"Source ({r['metadata'].get('source')}): {r['text']}" for r in retrieved_knowledge])
    
    llm_prompt = f"""
    You are the InsightMate Agent, an expert in meeting analysis.
    Answer the following question based ONLY on the provided context. If the context 
    is insufficient, state clearly that you cannot answer.

    Question: {test_query}

    Context:
    {context}
    """
    
    print("[Brain] Invoking LLM for final answer...")
    chat_model = ai_client.get_chat_model(temperature=0.0)
    
    llm_response = chat_model.invoke(llm_prompt)
    
    print("\n--- FINAL AGENT RESPONSE ---")
    print(llm_response.content)
    print("-----------------------------\n")

    print("InsightMate Test Complete. Base SDK functionality verified.")
    


if __name__ == "__main__":
    run_insight_mate_test()