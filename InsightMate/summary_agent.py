import os
import json
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from InsightMate.db_setup import get_db, Analysis

load_dotenv()

class Summary(BaseModel):
    meeting_title: str = Field(description="The original title of the meeting transcript.")
    summary: str = Field(description="A concise summary of the key discussion points, no more than 100 words.")
    key_decisions: list[str] = Field(description="A list of all explicit decisions made during the meeting.")
    action_items: list[str] = Field(description="A list of action items assigned, including the responsible party if mentioned.")
    sentiment: str = Field(description="Overall meeting sentiment (e.g., 'Positive', 'Mixed', 'Negative').")

async def run_summary_agent(transcript: str, title: str):
    print("--- Running LLM Analysis ---")

    llm = ChatOpenAI(
        model="mistralai/mistral-7b-instruct",
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_API_BASE"),
        temperature=0.0
    )

    parser = PydanticOutputParser(pydantic_object=Summary)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert financial analyst AI specialized in extracting precise, structured information from meeting transcripts. Your primary goal is to structure the analysis into the exact JSON format provided by the user. The original meeting title is: {title}\n\n{format_instructions}"),
        ("user", "Analyze the following transcript and extract the required fields, ensuring the output is perfectly clean JSON that conforms to the schema. TRANSCRIPT: {transcript}"),
    ]).partial(format_instructions=parser.get_format_instructions())

    chain = prompt | llm | parser

    try:
        summary_data = chain.invoke({
            "transcript": transcript, 
            "title": title
        })

        db = next(get_db())
        
        analysis_record = Analysis(
            title=summary_data.meeting_title,
            data=json.loads(summary_data.json()), 
            raw_text=transcript,
            status="COMPLETED"
        )
        db.add(analysis_record)
        db.commit()

        print("--- Analysis Saved to Database ---")

    except Exception as e:
        print(f"--- FAILED TO PROCESS TASK ---")
        print(f"Error during LLM or DB operation: {e}")
        raise e