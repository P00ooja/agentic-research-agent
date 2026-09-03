import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import json

class WebSearchTool:
    """Search the web for information"""
    
    @staticmethod
    def search(query: str, num_results: int = 5) -> List[Dict]:
        """
        Search using web (mock for MVP)
        In production, use SerpAPI or Google Search API
        """
        try:
            # Mock search results for MVP
            return [
                {
                    'title': f'Finding {i+1}: {query}',
                    'url': f'https://example.com/result-{i+1}',
                    'snippet': f'Relevant information about {query} result {i+1}'
                }
                for i in range(num_results)
            ]
        except Exception as e:
            print(f"Search error: {e}")
            return []

class ContentParserTool:
    """Parse and analyze content from URLs"""
    
    @staticmethod
    def parse(url: str) -> Dict:
        """Extract content from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                paragraphs = soup.find_all('p')
                text = ' '.join([p.get_text() for p in paragraphs])
                
                title = soup.find('h1')
                title_text = title.get_text() if title else 'Unknown'
                
                return {
                    'title': title_text,
                    'content': text[:500],
                    'url': url
                }
        except Exception as e:
            print(f"Parse error: {e}")
        
        return {
            'title': 'Unable to parse',
            'content': 'Could not extract content',
            'url': url
        }

class EntityExtractorTool:
    """Extract entities from text"""
    
    @staticmethod
    def extract_entities(text: str) -> Dict:
        """Extract key entities from text"""
        common_entities = {
            'technologies': [],
            'topics': [],
            'concepts': []
        }
        
        # Simple keyword matching
        keywords = {
            'quantum': 'Quantum Computing',
            'ai': 'Artificial Intelligence',
            'machine learning': 'Machine Learning',
            'blockchain': 'Blockchain',
            'crypto': 'Cryptocurrency'
        }
        
        text_lower = text.lower()
        for keyword, entity in keywords.items():
            if keyword in text_lower:
                common_entities['technologies'].append(entity)
        
        return common_entities

class ReportFormatterTool:
    """Format findings into structured report"""
    
    @staticmethod
    def format_report(findings: Dict, sources: List[Dict]) -> str:
        """Format findings as markdown"""
        
        report = f"# Research Report: {findings.get('topic', 'Research')}\n\n"
        report += f"## Summary\n{findings.get('summary', 'No summary')}\n\n"
        
        if 'key_findings' in findings:
            report += "## Key Findings\n"
            for i, finding in enumerate(findings['key_findings'], 1):
                report += f"{i}. {finding}\n"
        
        report += "\n## Sources\n"
        for i, source in enumerate(sources, 1):
            report += f"{i}. [{source.get('title', 'Source')}]({source.get('url', '#')})\n"
        
        return report

TOOLS = {
    'web_search': WebSearchTool.search,
    'parse_content': ContentParserTool.parse,
    'extract_entities': EntityExtractorTool.extract_entities,
    'format_report': ReportFormatterTool.format_report
}
