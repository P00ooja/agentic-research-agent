import os
import json
import time
from typing import Dict, List, Any
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from tavily import TavilyClient

from agent.tools import (
    WebSearchTool,
    EntityExtractorTool,
    web_search,
    extract_entities,
    parse_url
)

load_dotenv()


# Define LangChain Tools with @tool decorator
@tool
def WebSearch(query: str) -> str:
    """Search the web for current information about a topic. Input should be a search query string."""
    return web_search(query)

@tool
def ExtractEntities(text: str) -> str:
    """Extract key entities (companies, technologies, concepts) from text."""
    return extract_entities(text)

@tool
def ParseURL(url: str) -> str:
    """Extract and parse content from a specific web URL."""
    return parse_url(url)


class ResearchAgent:
    """Autonomous Research Agent powered by LangChain and Google Gemini API"""
    
    def __init__(self):
        """Initialize the LangChain Research Agent"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.tavily_key = os.getenv('TAVILY_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")
        
        self.tools = [WebSearch, ExtractEntities, ParseURL]
        self.research_history = []
        self.sources = []

    def log_step(self, step_num: int, description: str):
        """Log research step for progress tracking"""
        self.research_history.append({
            'step': step_num,
            'description': description
        })
        print(f"[Step {step_num}] {description}")

    def _get_llm_with_fallback(self) -> ChatGoogleGenerativeAI:
        """Create ChatGoogleGenerativeAI with model fallback strategy"""
        models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        last_exception = None

        for model_name in models_to_try:
            try:
                llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=self.api_key,
                    temperature=0.7
                )
                # Test call
                llm.invoke("Test ping")
                print(f"✅ Successfully initialized LangChain model: {model_name}")
                return llm
            except Exception as e:
                last_exception = e
                print(f"⚠️ Model {model_name} failed: {e}. Trying fallback...")
                time.sleep(1)

        # Default to gemini-2.5-flash if test fails
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.7
        )

    def research(self, topic: str, research_id: str = None) -> Dict:
        """
        Execute autonomous research using LangChain agent
        
        Returns:
            Structured dictionary matching backend API and frontend contract
        """
        try:
            self.research_history = []
            self.sources = []

            # Step 1: Initial Search & Setup
            self.log_step(1, f"Searching for information about '{topic}'")
            self.sources = WebSearchTool.search(query=topic, num_results=5)

            # Step 2: Initialize LangChain LLM & Agent
            self.log_step(2, "Initializing LangChain Agent and reasoning strategy")
            llm = self._get_llm_with_fallback()
            agent = create_agent(llm, self.tools)

            # Step 3: Agent Orchestration Loop
            self.log_step(3, "LangChain Agent executing autonomous tool calling loop")
            input_prompt = (
                f"Perform comprehensive research on the topic: '{topic}'.\n\n"
                "Instructions:\n"
                "1. Use WebSearch to find current facts and news.\n"
                "2. Use ExtractEntities to identify key companies, technologies, and concepts.\n"
                "3. Synthesize your findings into a professional markdown research report with:\n"
                "   - Executive Summary (2-3 sentences)\n"
                "   - Key Findings (3-5 detailed bullet points)\n"
                "   - Future Trends & Implications\n"
                "   - Recommendations for further research"
            )

            # Step 4: Run Agent Execution
            self.log_step(4, "Gathering detailed information and analyzing entities")
            inputs = {"messages": [("user", input_prompt)]}
            agent_response = agent.invoke(inputs)

            # Extract output text
            self.log_step(5, "Synthesizing comprehensive report")
            messages = agent_response.get("messages", [])
            final_output = ""
            if messages:
                last_msg = messages[-1]
                if hasattr(last_msg, "content"):
                    final_output = last_msg.content
                    if isinstance(final_output, list):
                        final_output = "".join([item.get("text", "") if isinstance(item, dict) else str(item) for item in final_output])
                else:
                    final_output = str(last_msg)

            # Step 6: Extract Entities and Format
            self.log_step(6, "Formatting final report and collecting citations")
            entities = EntityExtractorTool.extract_entities(final_output)

            # Step 7: Final Completion
            self.log_step(7, "Research complete!")

            return {
                'topic': topic,
                'summary': final_output,
                'entities_found': entities,
                'sources': self.sources[:5],
                'research_steps': self.research_history
            }

        except Exception as e:
            print(f"Research error: {e}")
            return self._create_error_response(str(e))

    def _create_error_response(self, error_msg: str) -> Dict:
        """Create error response matching API contract"""
        return {
            'topic': 'Error',
            'summary': f"Research failed: {error_msg}",
            'error': True,
            'research_steps': self.research_history
        }
