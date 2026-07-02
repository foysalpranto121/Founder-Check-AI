# FounderCheck - Quick Start (5 Minutes)

Get the application running in 5 minutes.

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

## Step 1: Copy Environment File

```bash
cp .env.example .env
```

## Step 2: Setup Backend (Terminal 1)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python main.py
```

**Wait for:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it:**
```bash
curl http://localhost:8000/health
```

## Step 3: Setup Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

**Wait for:**
```
➜  Local:   http://localhost:5173/
```

## Step 4: Test Connection

Open browser: http://localhost:5173

Should show:
- ✅ "Backend: Connected"
- Form input
- Try submitting an idea

## That's It!

The application is running. Now you can:

1. Read `README.md` for architecture overview
2. Read `SETUP.md` for detailed configuration
3. Start building features

---

**Next:** See `SETUP.md` for PostgreSQL setup and advanced configuration
