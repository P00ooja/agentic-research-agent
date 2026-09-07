from google import genai
from agent.tools import WebSearchTool, EntityExtractorTool, ReportFormatterTool
import os
import json
import time
from typing import Dict
from dotenv import load_dotenv

load_dotenv()        


class ResearchAgent:
    """Main research agent using Gemini API with automatic model fallback & retries"""
    
    def __init__(self):
        """Initialize the agent"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")

        self.client = genai.Client(api_key=self.api_key)
        self.research_history = []
        self.sources = []
    
    def log_step(self, step_num: int, description: str):
        """Log research step"""
        self.research_history.append({
            'step': step_num,
            'description': description
        })
        print(f"[Step {step_num}] {description}")

    def _call_gemini_with_fallback(self, prompt: str) -> str:
        """Call Gemini API with model fallback and retries for high availability"""
        models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        last_exception = None

        for model_name in models_to_try:
            for attempt in range(3):
                try:
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    if response and response.text:
                        return response.text
                except Exception as e:
                    last_exception = e
                    err_str = str(e)
                    if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str:
                        print(f"Model {model_name} (attempt {attempt+1}) temporarily busy. Retrying...")
                        time.sleep(2)
                    else:
                        break  # Try next fallback model if error is persistent

        raise RuntimeError(f"All Gemini model attempts failed. Details: {last_exception}")
    
    def research(self, topic: str, research_id: str = None) -> Dict:
        """
        Orchestrate multi-step research process
        
        Args:
            topic: The research topic
            research_id: ID for this research session
        
        Returns:
            Comprehensive research findings
        """
        try:
            # Step 1: Initial Search
            self.log_step(1, f"Searching for information about '{topic}'")
            search_results = WebSearchTool.search(query=topic, num_results=5)
            
            if not search_results:
                return self._create_error_response("No search results found")
            
            self.sources = search_results
            
            # Step 2: Analyze Findings
            self.log_step(2, "Analyzing search results")
            results_text = json.dumps(search_results, indent=2)
            
            analysis_prompt = f"""
Analyze these search results about '{topic}':

{results_text}

Provide:
1. Key findings (2-3 main points)
2. Important entities (companies, technologies)
3. What additional information is needed

Be concise and factual.
"""
            
            analysis = self._call_gemini_with_fallback(analysis_prompt)
            
            # Step 3: Extract Entities
            self.log_step(3, "Identifying key entities")
            entities = EntityExtractorTool.extract_entities(analysis)
            
            # Step 4: Deep Dive
            self.log_step(4, "Gathering detailed information")
            
            for entity in entities.get('technologies', [])[:2]:
                entity_query = f"{topic} {entity}"
                entity_results = WebSearchTool.search(query=entity_query, num_results=2)
                self.sources.extend(entity_results)
            
            # Step 5: Synthesize
            self.log_step(5, "Synthesizing comprehensive report")
            
            synthesis_prompt = f"""
Create a research report about '{topic}'.

Initial Analysis:
{analysis}

Entities Found:
{json.dumps(entities, indent=2)}

Provide:
1. Executive Summary (2-3 sentences)
2. Key Findings (3-5 bullet points)
3. Implications and Trends
4. Recommendations for Further Research

Be clear and professional.
"""
            
            synthesis = self._call_gemini_with_fallback(synthesis_prompt)

            # Step 6: Format Report
            self.log_step(6, "Formatting final report")
            
            result = {
                'topic': topic,
                'summary': synthesis,
                'entities_found': entities,
                'sources': self.sources[:5],  # Top 5 sources
                'research_steps': self.research_history
            }
            
            self.log_step(7, "Research complete!")
            return result
            
        except Exception as e:
            print(f"Research error: {e}")
            return self._create_error_response(str(e))
    
    def _create_error_response(self, error_msg: str) -> Dict:
        """Create error response"""
        return {
            'topic': 'Error',
            'summary': f"Research failed: {error_msg}",
            'error': True
        }
