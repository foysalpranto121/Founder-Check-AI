# FounderCheck - Step-by-Step Setup

Follow these steps in order to build and run the application.

## Step 1: Environment Setup

### Install Python and Node.js

- Python 3.10+: https://www.python.org/downloads/
- Node.js 18+: https://nodejs.org/
- PostgreSQL 14+: https://www.postgresql.org/download/

### Verify installations

```bash
python --version
node --version
psql --version
```

## Step 2: Database Setup

### Create PostgreSQL Database

```bash
psql -U postgres
CREATE DATABASE foundercheck;
\q
```

### Update .env with Database URL

Edit `.env`:

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/foundercheck
```

## Step 3: Backend Installation

### Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Database Tables

```bash
alembic upgrade head
```

### Start Backend Server

```bash
python main.py
```

**Expected output:**
```
INFO:     Started server process [1234]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Verify it works:**
```bash
curl http://localhost:8000/health
```

Should return:
```json
{"status":"operational","message":"API Keys: Anthropic=✓"}
```

## Step 4: Frontend Installation

### Open New Terminal and Navigate

```bash
cd frontend
```

### Install Dependencies

```bash
npm install
```

### Start Development Server

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.0.8  ready in 234 ms
  ➜  Local:   http://localhost:5173/
```

## Step 5: Test End-to-End Connection

1. Open browser to http://localhost:5173
2. Should see:
   - ✅ "Backend: Connected"
   - Text area for startup idea
3. Type: "Cloud kitchen in Dhaka"
4. Click "Send to Backend"
5. See response displayed

**Success:** Frontend and backend are communicating ✓

## Step 6: API Keys

### Get Anthropic API Key

1. Go to https://console.anthropic.com
2. Create account or login
3. Create API key
4. Copy key to `.env`:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Verify API Key Works

```bash
cd backend
python -c "
from anthropic import Anthropic
client = Anthropic(api_key='YOUR_KEY_HERE')
print('✓ API key is valid')
"
```

## Step 7: Database Operations

### Check Database Connection

```bash
python -c "
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:password@localhost:5432/foundercheck')
with engine.connect() as conn:
    print('✓ Database connected')
"
```

### Run Migrations

```bash
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### Check Tables

```bash
psql -U postgres -d foundercheck -c "\dt"
```

## Step 8: Common Issues

### Port 8000 Already in Use

```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Port 5173 Already in Use

Change in `frontend/vite.config.ts`:
```typescript
server: {
  port: 5174,  // or another free port
}
```

### PostgreSQL Connection Refused

- Check PostgreSQL is running: `pg_isready`
- Check credentials in `.env`
- Create user if needed: `createuser -U postgres youruser`

### Module Not Found

```bash
# Backend
pip install -r requirements.txt --upgrade

# Frontend
npm install
```

### Frontend Can't Reach Backend

- Check backend is running on http://localhost:8000
- Check `vite.config.ts` proxy settings
- Check CORS is enabled in `backend/main.py`

## Step 9: Project Structure

After setup, your project should look like:

```
FounderCheck/
├── .env                    (local config)
├── README.md               (main docs)
├── SETUP.md                (this file)
│
├── backend/
│   ├── venv/               (virtual environment)
│   ├── main.py             (API entry point)
│   ├── requirements.txt
│   └── migrations/         (alembic)
│
├── frontend/
│   ├── node_modules/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── index.html
│
└── data/
    └── (knowledge base files - created next)
```

## Step 10: Verify Everything Works

Run all health checks:

```bash
# Terminal 1: Backend
curl http://localhost:8000/health

# Terminal 2: Frontend - should show:
# "Backend: ✓ Connected"

# Terminal 3: Database
psql -U postgres -d foundercheck -c "SELECT version();"
```

All three should work without errors.

## Next Steps

Once setup is complete:

1. Collect regulatory data for knowledge base
2. Build competitor dataset
3. Create database schema for regulations/competitors
4. Implement analysis endpoints
5. Build frontend results dashboard

---

**Status:** ✓ Setup complete
