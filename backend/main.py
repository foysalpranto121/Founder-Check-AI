from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="FounderCheck API",
    description="Bangladesh Startup Validator API",
    version="0.1.0"
)

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Models
# ============================================================================

class HealthCheck(BaseModel):
    status: str
    message: str

class HelloRequest(BaseModel):
    idea: str

class HelloResponse(BaseModel):
    message: str
    idea_received: str
    backend_status: str

# ============================================================================
# Routes
# ============================================================================

@app.get("/", response_model=HealthCheck)
async def root():
    """Health check endpoint"""
    return {
        "status": "operational",
        "message": "FounderCheck API is running ✓"
    }

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check with API key status"""
    anthropic_key = "✓" if os.getenv("ANTHROPIC_API_KEY") else "✗"
    return {
        "status": "operational",
        "message": f"API Keys: Anthropic={anthropic_key}"
    }

@app.post("/api/v1/hello", response_model=HelloResponse)
async def hello_endpoint(request: HelloRequest):
    """Hello World endpoint - receives idea and echoes back"""
    return {
        "message": "FounderCheck backend is connected!",
        "idea_received": request.idea,
        "backend_status": "ready_for_analysis"
    }

# ============================================================================
# Placeholder for Phase 2 endpoints
# ============================================================================
# @app.post("/api/v1/analyze")      # Full analysis pipeline
# @app.post("/api/v1/retrieve")     # RAG retrieval
# @app.post("/api/v1/investor-qa")  # Q&A endpoint

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
