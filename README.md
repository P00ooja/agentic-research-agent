# 🔍 Agentic Research Agent

An AI-powered research information gathering system using LangChain, Google Gemini API, React, and full-stack deployment.

## 🚀 Live Demo

- **Frontend:** https://agentic-research-agent.vercel.app
- **Backend API:** https://agentic-research-agent-backend.onrender.com/api

## 📋 Features

✨ **Agentic AI:**
- Multi-step autonomous research orchestration
- LangChain integration for tool calling
- Google Gemini API for reasoning
- Real-time progress tracking

🎨 **Full-Stack:**
- React 19.2.8 with Vite
- Tailwind CSS for styling
- Responsive, mobile-friendly UI
- Real-time progress updates

🔄 **CI/CD & DevOps:**
- GitHub Actions for automated testing
- Auto-deploy to Render (backend)
- Auto-deploy to Vercel (frontend)
- Production-ready configuration

## 🏗️ Architecture

```
┌─────────────────┐
│ React Frontend  │ (Vercel)
│  (Vite + TW)    │
└────────┬────────┘
         │ REST API
         ↓
┌─────────────────────┐
│  Flask Backend      │ (Render)
│  ├─ LangChain Agent │
│  ├─ Gemini API      │
│  └─ Research Tools  │
└─────────────────────┘
```

## 📁 Project Structure

```
agentic-research-agent/
├── backend/
│   ├── agent/
│   │   ├── research_agent.py   # Main agent logic
│   │   └── tools.py            # Agent tools
│   ├── api/
│   │   └── routes.py           # API endpoints
│   ├── app.py                  # Flask app
│   ├── config.py               # Configuration
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # Environment template
│
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── services/           # API services
│   │   ├── App.jsx             # Main component
│   │   └── main.jsx            # Entry point
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite config
│   ├── tailwind.config.js      # Tailwind config
│   └── .env.example            # Environment template
│
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline
│
└── README.md                   # This file
```

## 🛠️ Tech Stack

**Backend:**
- Flask 3.1.3
- LangChain 1.3.18
- Google Generative AI 0.8.6
- Python 3.11

**Frontend:**
- React 19.2.8
- Vite 8.2.2
- Tailwind CSS 4.3.3
- Axios 1.20.0

**Deployment:**
- Render (Backend)
- Vercel (Frontend)
- GitHub Actions (CI/CD)

## 🚀 Getting Started

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env
# Add your GEMINI_API_KEY to .env
python app.py
```

**Frontend (new terminal):**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Visit http://localhost:5173

### Production Deployment

- **Backend:** Automatically deploys to Render on push to main
- **Frontend:** Automatically deploys to Vercel on push to main
- **CI/CD:** GitHub Actions tests code before deployment

## 📖 How It Works

1. User enters a research topic
2. Backend research agent executes 7-step process:
   - Search for information
   - Analyze results
   - Identify key entities
   - Gather detailed information
   - Synthesize findings
   - Format report
   - Return results with citations
3. Frontend displays real-time progress
4. Results rendered with sources and links

## 🎯 Interview Talking Points

**On Agentic AI:**
> "The agent autonomously decides which tools to use and when to use them. Unlike a simple prompt, it iterates based on previous results and adapts its strategy. For example, when researching quantum computing, it searches for breakthroughs, realizes it needs company info, searches for that, then gathers market impact data—all autonomously."

**On Full-Stack:**
> "Built production-ready full-stack: Python backend with LangChain agent orchestration, React frontend with real-time updates via polling, and deployed to Render and Vercel with automated CI/CD."

**On Scalability:**
> "Currently handles sequential research. To scale: add Redis caching for results, use Celery for distributed task processing, implement batch research processing, and add user authentication with database persistence."

## 🔄 CI/CD Pipeline

On every push to main:
1. ✅ Backend tests (imports, linting)
2. ✅ Frontend tests (build check)
3. ✅ Auto-deploy to Render (backend)
4. ✅ Auto-deploy to Vercel (frontend)

## 📝 Environment Variables

**Backend (.env):**
```env
GEMINI_API_KEY=your_key_here
FLASK_ENV=production
FLASK_DEBUG=False
SERVER_PORT=10000
```

**Frontend (.env):**
```env
VITE_API_BASE_URL=https://your-backend-url/api
```

## 🐛 Known Limitations

- Mock web search (use real search API for production)
- No user authentication
- In-memory session storage (use database for scale)
- Sequential research (can parallelize with async)

## 📚 Future Enhancements

- [ ] Real web search integration (SerpAPI/Google Search)
- [ ] User authentication & history
- [ ] Database persistence (PostgreSQL)
- [ ] Parallel research steps with async
- [ ] Advanced entity extraction (NER)
- [ ] Multiple language support
- [ ] Research caching & deduplication

## 👤 Author

Built as a campus placement portfolio project.

## 📄 License

MIT
