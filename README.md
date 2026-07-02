# FounderCheck - Bangladesh Startup Validator

An AI-powered platform for validating startup ideas in Bangladesh context using regulatory knowledge, competitor data, and investor insights.

## 📋 Project Status: Phase 0 - Setup & Scoping

### 🏗️ Architecture

```
FounderCheck/
├── frontend/          # React + Vite SPA
├── backend/           # FastAPI REST API
├── data/              # Knowledge base (regulations, competitors, embeddings)
└── docs/              # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Setup

1. **Clone & Navigate**
   ```bash
   git clone https://github.com/foysalpranto121/FounderCheck.git
   cd FounderCheck
   ```

2. **Copy Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/Scripts/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

4. **Frontend Setup** (in new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

Visit `http://localhost:5173` — frontend should call backend at `http://localhost:8000`

## 📅 Build Phases

### Phase 0: Setup & Scoping ✅ (IN PROGRESS)
- [x] Monorepo structure
- [x] .env configuration
- [ ] Hello World end-to-end
- [ ] Deploy to Vercel + Railway

### Phase 1: Knowledge Base (Days 2–4)
- [ ] Collect BD regulatory data (NBR, RJSC, trade licenses, BIDA, BTRC, BSTI, Bangladesh Bank)
- [ ] Competitor dataset (200–300 BD startups)
- [ ] Vector embeddings (Chroma/pgvector)
- [ ] Retrieval testing

### Phase 2: Analysis Pipeline (Days 5–8)
- [ ] Idea intake endpoint (language detection, field extraction)
- [ ] Retrieval integration
- [ ] 5 parallel analysis modules
- [ ] Hallucination guard (verification badges)

### Phase 3: Investor Q&A (Days 9–11)
- [ ] Question generation & storage
- [ ] Chat interface
- [ ] Scoring & scoring logic
- [ ] Readiness recalculation

### Phase 4: Frontend & Reports (Days 12–14)
- [ ] Input screen with examples
- [ ] Results dashboard
- [ ] Investor mode chat
- [ ] PDF export (WeasyPrint)

### Phase 5: Voice + Polish (Days 15–16)
- [ ] Whisper integration
- [ ] Audio recording UI
- [ ] Fallback to text

### Phase 6: Demo Hardening (Final 2 days)
- [ ] Test demo ideas 10+ times
- [ ] Cache fallback
- [ ] Rate limiting
- [ ] Q&A prep

## 🔑 Key Features

1. **RAG-based Analysis** - Regulatory data + competitor intelligence
2. **Hallucination Guard** - Citations with verification badges
3. **Investor Q&A** - Interactive readiness scoring
4. **Multi-language** - Bangla, English, Banglish support
5. **PDF Reports** - Bangla-compatible export

## 📝 Demo Ideas (for testing)
- "Cloud kitchen in Mirpur"
- "Agri-tech for Bogura farmers"
- "Fintech lending platform"

## 🛠️ Tech Stack

**Frontend:** React 18, Vite, TypeScript, Tailwind CSS
**Backend:** FastAPI, Python 3.10+
**LLM:** Anthropic Claude / OpenAI
**Vector DB:** Chroma or pgvector
**PDF:** WeasyPrint
**Deployment:** Vercel (frontend), Railway/Render (backend)

## 📚 Docs

See `/docs` for detailed architecture and phase guidelines.

---

**Next Step:** Create Hello World backend + frontend
