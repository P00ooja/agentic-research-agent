from flask import Blueprint, request, jsonify
from agent.research_agent import ResearchAgent
import threading
import uuid

api_bp = Blueprint('api', __name__)

# Store research sessions in memory
research_sessions = {}

@api_bp.route('/research', methods=['POST'])
def start_research():
    """Start a new research task"""
    data = request.get_json()
    
    if not data or 'topic' not in data:
        return {'error': 'Missing topic in request'}, 400
    
    topic = data['topic']
    research_id = str(uuid.uuid4())
    
    # Initialize session
    research_sessions[research_id] = {
        'status': 'started',
        'topic': topic,
        'result': None,
        'progress': 0
    }
    
    # Run research in background
    def run_research():
        try:
            agent = ResearchAgent()
            result = agent.research(topic, research_id)
            research_sessions[research_id]['status'] = 'completed'
            research_sessions[research_id]['result'] = result
            research_sessions[research_id]['progress'] = 100
        except Exception as e:
            research_sessions[research_id]['status'] = 'error'
            research_sessions[research_id]['error'] = str(e)
            print(f"Research error: {e}")
    
    thread = threading.Thread(target=run_research, daemon=True)
    thread.start()
    
    return {
        'research_id': research_id,
        'status': 'started',
        'message': 'Research in progress...'
    }, 202

@api_bp.route('/research/<research_id>', methods=['GET'])
def get_research_status(research_id):
    """Get status of research task"""
    if research_id not in research_sessions:
        return {'error': 'Research not found'}, 404
    
    session = research_sessions[research_id]
    return {
        'research_id': research_id,
        'status': session['status'],
        'progress': session.get('progress', 0),
        'result': session.get('result'),
        'error': session.get('error')
    }, 200

@api_bp.route('/search-history', methods=['GET'])
def get_search_history():
    """Get research history"""
    history = [
        {
            'research_id': rid,
            'topic': session['topic'],
            'status': session['status']
        }
        for rid, session in research_sessions.items()
    ]
    return {'history': history}, 200
