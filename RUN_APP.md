# FounderCheck - How to Run the Application

Your Anthropic API key is already configured. Here's how to run the complete app with Claude AI analysis.

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+ (optional for now - backend will create tables automatically)
- API key already in `.env` ✓

## Setup (First Time Only)

### 1. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
venv\Scripts\activate  # Windows
python main.py
```

**Expected Output:**
```
INFO:     Started server process [1234]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

**Expected Output:**
```
  VITE v5.0.8  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### Open Browser

Visit: **http://localhost:5173**

## Using the Application

### 1. See Backend Status
- Should show "✅ Backend: Connected"
- If not, check backend is running

### 2. Enter Your Idea
- Type in the textarea: "Cloud kitchen in Mirpur"
- Or any startup idea

### 3. Click "Analyze My Idea"
- Processing takes **30-40 seconds** (first time longer)
- Claude AI is analyzing your idea

### 4. See Complete Analysis
You'll get:
- **Readiness Score** (1-10) with visual gauge
- **Idea Summary** (sector, target customer, revenue model, location)
- **Market Demand** (score, competition, opportunities, threats)
- **Regulatory Landscape** (regulators, approvals needed, timeline, costs in BDT)
- **Business Model Canvas** (9 blocks: partners, activities, value prop, etc.)
- **Investor Questions** (10 tough questions to prepare for)

## What Each Analysis Does

### 📋 Idea Extraction
Claude analyzes your raw idea text and extracts:
- Title
- Sector (fintech, food delivery, agritech, etc.)
- Target customer
- Revenue model
- Location

### 📊 Demand Analysis
- Market size estimation
- Competition analysis
- 3+ opportunities
- 2+ threats
- Score 1-10

### ⚖️ Regulatory Analysis
- BD-specific regulators (NBR, RJSC, BIDA, BTRC, BSTI, Bangladesh Bank)
- Critical approvals needed
- Timeline in days
- Estimated cost in BDT
- Regulatory warnings

### 🎨 Business Model Canvas
- Key Partners
- Key Activities
- Value Proposition
- Customer Segments
- Channels to market
- Customer relationships
- Revenue streams (in BDT)
- Cost structure (in BDT)

### ❓ Investor Questions
- 10 tough questions for your pitch
- Categorized by: market, execution, financials, team
- Real questions investors ask in Bangladesh

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is free
netstat -ano | findstr :8000

# Kill the process using it
taskkill /PID <PID> /F

# Try again
python main.py
```

### Frontend won't start
```bash
# Make sure dependencies are installed
npm install

# Try a different port if 5173 is in use
# Edit frontend/vite.config.ts, change port: 5174
npm run dev
```

### "Backend not reachable" error
- Verify backend is running on http://localhost:8000
- Check firewall isn't blocking port 8000
- Try: `curl http://localhost:8000/health`

### API analysis fails
- Check Anthropic API key in `.env`
- Verify you have API credits at https://console.anthropic.com
- Check backend logs for detailed error message

### Analysis takes too long
- First run takes longer (30-40 seconds)
- Subsequent calls should be faster (20-30 seconds)
- Normal - Claude is analyzing multiple aspects

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

Returns:
```json
{"status":"operational","message":"API Keys: Anthropic=✓"}
```

### Full Analysis
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"idea":"Cloud kitchen in Mirpur"}'
```

Returns:
```json
{
  "idea_extraction": {...},
  "demand_analysis": {...},
  "regulatory_analysis": {...},
  "business_canvas": {...},
  "investor_questions": [...],
  "overall_readiness_score": 7.5,
  "analysis_status": "completed"
}
```

## Development Notes

### Backend Structure
```
backend/
├── main.py              # FastAPI app with /api/v1/analyze endpoint
├── llm.py              # Claude API integration functions
├── database.py         # SQLAlchemy models (PostgreSQL)
├── schemas.py          # Pydantic request/response models
└── requirements.txt    # Python dependencies
```

### Frontend Structure
```
frontend/
├── src/App.tsx         # Main React component with analysis logic
├── src/App.css         # Styling for dashboard
└── src/main.tsx        # Entry point
```

## Database (Optional)

If you want to persist data to PostgreSQL:

```bash
# Create database
psql -U postgres
CREATE DATABASE foundercheck;
\q

# Update .env
DATABASE_URL=postgresql://postgres:password@localhost:5432/foundercheck
```

Currently data is logged but not persisted if you skip this.

## Next Steps

1. **Test with different ideas**
   - "Agri-tech for Bogura farmers"
   - "Fintech lending platform"
   - "EdTech for rural schools"

2. **Iterate on your idea**
   - See what regulatory issues come up
   - Check the investor questions
   - Refine your business model

3. **Extend the app** (coming next)
   - Voice input (Whisper)
   - Interactive investor Q&A chat
   - PDF export of results
   - Admin dashboard for knowledge base

## Support

### Check logs
- **Backend logs:** Terminal where you ran `python main.py`
- **Frontend logs:** Browser console (F12)

### Common error messages

| Error | Solution |
|-------|----------|
| `CONNECTION_ERROR` | Backend not running - start it in Terminal 1 |
| `API_KEY_ERROR` | Check `.env` has correct Anthropic key |
| `JSON_DECODE_ERROR` | Claude returned invalid JSON - try shorter idea text |
| `TIMEOUT` | Analysis taking too long - check internet connection |

---

**Everything is configured and ready to go!**

Just run the backend and frontend as shown above, then visit http://localhost:5173

Enjoy analyzing startup ideas! 🚀
