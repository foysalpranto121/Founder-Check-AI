# FounderCheck - Bangladesh Startup Validator

An AI-powered platform for validating startup ideas in Bangladesh context using regulatory knowledge, competitor data, and investor insights.

## 🏗️ Architecture

```
FounderCheck/
├── frontend/          # React + Vite SPA
├── backend/           # FastAPI REST API
├── database/          # PostgreSQL schema & migrations
└── data/              # Knowledge base (regulations, competitors)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Git

### Setup

1. **Clone and navigate:**

```bash
git clone https://github.com/foysalpranto121/FounderCheck.git
cd FounderCheck
```

2. **Copy environment file:**

```bash
cp .env.example .env
```

3. **Backend setup:**

```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

4. **Frontend setup** (new terminal):

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` — frontend will connect to backend at `http://localhost:8000`

## 💾 Database Setup

1. **Create PostgreSQL database:**

```sql
CREATE DATABASE foundercheck;
```

2. **Update .env with connection string:**

```
DATABASE_URL=postgresql://user:password@localhost:5432/foundercheck
```

3. **Run migrations:**

```bash
cd backend
alembic upgrade head
```

## 📚 Development Workflow

### Backend

- API runs on `http://localhost:8000`
- Health check: `http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`

### Frontend

- App runs on `http://localhost:5173`
- Hot reload enabled

## 🛠️ Tech Stack

- **Frontend:** React 18, Vite, TypeScript
- **Backend:** FastAPI, Python 3.10+
- **Database:** PostgreSQL with SQLAlchemy ORM
- **LLM:** Anthropic Claude or OpenAI
- **Deployment:** Vercel (frontend), Railway/Render (backend)

## 📝 Environment Variables

See `.env.example` for all required variables. Key ones:

- `ANTHROPIC_API_KEY` - Claude API key
- `DATABASE_URL` - PostgreSQL connection string
- `BACKEND_PORT` - Backend server port (default: 8000)

## 🐛 Troubleshooting

**Port in use:**

```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Database connection error:**

- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Ensure database exists

**Module not found:**

```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

---

**Next:** Follow the step-by-step implementation guide in `SETUP.md`
