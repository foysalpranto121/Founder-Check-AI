# PHASE 0: Setup & Scoping - Complete Guide

## ✅ What's Been Created

### Project Structure
```
FounderCheck/
├── .env                    # Environment variables (LOCAL ONLY)
├── .env.example            # Template for .env
├── .gitignore              # Git exclusions
├── README.md               # Main project README
├── PHASE_0_GUIDE.md        # This file
│
├── frontend/               # React + Vite SPA
│   ├── src/
│   │   ├── App.tsx        # Main component with API call
│   │   ├── App.css        # Styling
│   │   └── main.tsx       # Entry point
│   ├── index.html         # HTML template
│   ├── package.json       # Dependencies
│   ├── tsconfig.json      # TypeScript config
│   └── vite.config.ts     # Vite configuration
│
├── backend/                # FastAPI REST API
│   ├── main.py            # Hello World API
│   └── requirements.txt    # Python dependencies
│
└── data/                   # Knowledge base (Phase 1)
    └── (empty for now)
```

### What Works Now
✅ FastAPI backend with CORS enabled
✅ React frontend with Vite
✅ End-to-end connection test (React → FastAPI → Response)
✅ Health check endpoints
✅ Basic error handling
✅ TypeScript type safety

---

## 🚀 Running the Hello World App

### 1️⃣ Install Backend Dependencies

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2️⃣ Start Backend

```bash
python main.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Visit `http://localhost:8000/health` to verify → should return:
```json
{
  "status": "operational",
  "message": "API Keys: Anthropic=✓"
}
```

### 3️⃣ Install Frontend Dependencies (new terminal)

```bash
cd frontend
npm install
```

### 4️⃣ Start Frontend

```bash
npm run dev
```

**Expected Output:**
```
  VITE v5.0.8  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### 5️⃣ Test End-to-End

1. Open `http://localhost:5173` in browser
2. Should show:
   - ✅ "Backend: ✓ Connected"
   - Form to enter startup idea
3. Type: "Cloud kitchen in Dhaka"
4. Click "Send to Backend"
5. Should see response:
   ```
   Message: FounderCheck backend is connected!
   Idea Received: Cloud kitchen in Dhaka
   Status: ready_for_analysis
   ```

---

## 📋 API Endpoints (Ready)

### Health Checks
- `GET /` → Returns status
- `GET /health` → Returns API key status

### Hello World (Test)
- `POST /api/v1/hello` 
  - Input: `{ "idea": "string" }`
  - Output: `{ "message": "...", "idea_received": "...", "backend_status": "..." }`

---

## 🔑 Next Steps

### Before Phase 1 (Knowledge Base):
1. Get Anthropic API key from https://console.anthropic.com
2. Add to `.env` as `ANTHROPIC_API_KEY=sk-ant-...`
3. Verify it works: `python -c "from anthropic import Anthropic; print('API Key works!')"`

### Phase 1 Prep:
- [ ] Collect BD regulatory data (5 core regulators)
- [ ] Build 200–300 startup dataset
- [ ] Create vector embeddings schema
- [ ] Test retrieval pipeline

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F
```

### CORS Error
- Check backend is running on `http://localhost:8000`
- Check frontend proxy in `vite.config.ts`

### Module Not Found
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### API Keys Not Loading
```bash
# Verify .env exists and is in root
cat .env | grep ANTHROPIC_API_KEY
```

---

## 📝 Phase 0 Deliverables Checklist

- [x] Monorepo structure created
- [x] `.env` template and local `.env`
- [x] Backend: FastAPI app with CORS
- [x] Frontend: React + Vite + TypeScript
- [x] End-to-end "hello world" working
- [ ] Deploy to Vercel (frontend)
- [ ] Deploy to Railway (backend)

---

## 🎯 Success Criteria

Phase 0 is complete when:
1. Backend runs on port 8000 without errors ✓
2. Frontend runs on port 5173 without errors ✓
3. Frontend displays "Backend: ✓ Connected" ✓
4. Submitting a form sends data to backend ✓
5. Backend returns response and frontend displays it ✓

**Status: 80% complete** (need deployment links in next step)

---

## 📚 Files Modified/Created This Phase

**Created:**
- `backend/main.py` (FastAPI hello world)
- `backend/requirements.txt` (dependencies)
- `frontend/src/App.tsx` (React component)
- `frontend/src/App.css` (styling)
- `frontend/src/main.tsx` (entry)
- `frontend/index.html` (template)
- `frontend/package.json` (npm config)
- `frontend/vite.config.ts` (build config)
- `frontend/tsconfig.json` (TS config)
- `.env` (local config)
- `.env.example` (template)
- `.gitignore` (git exclusions)
- `README.md` (main docs)
- `PHASE_0_GUIDE.md` (this file)

---

**Next:** After confirming hello world works → Move to Phase 1: Knowledge Base Build
