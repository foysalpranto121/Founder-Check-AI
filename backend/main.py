from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from database import init_db, get_db, engine, Base, StartupIdea, Analysis
from sqlalchemy.orm import Session
from schemas import AnalyzeIdeaRequest, AnalysisResult, DemandAnalysis, RegulatoryAnalysis, BusinessCanvas, InvestorQuestion, IdeaExtraction
from llm import extract_idea_fields, analyze_demand, analyze_regulatory_risks, generate_business_canvas, generate_investor_questions
import os
import json

load_dotenv()

# Initialize database tables
Base.metadata.create_all(bind=engine)

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
# Analysis Endpoints
# ============================================================================

@app.post("/api/v1/analyze", response_model=AnalysisResult)
async def analyze_startup_idea(request: AnalyzeIdeaRequest, db: Session = Depends(get_db)):
    """Full startup idea analysis pipeline"""

    if not request.idea or len(request.idea.strip()) < 10:
        raise HTTPException(status_code=400, detail="Idea must be at least 10 characters")

    try:
        # Step 1: Extract structured fields
        print("📋 Extracting idea fields...")
        idea_data = extract_idea_fields(request.idea)

        # Step 2: Analyze demand
        print("📊 Analyzing market demand...")
        demand_data = analyze_demand(request.idea, idea_data.get("target_customer", "Unknown"))

        # Step 3: Analyze regulatory risks
        print("⚖️ Analyzing regulatory risks...")
        regulatory_data = analyze_regulatory_risks(request.idea, idea_data.get("sector", "unknown"))

        # Step 4: Generate business canvas
        print("🎨 Generating business model canvas...")
        canvas_data = generate_business_canvas(request.idea, idea_data.get("sector", "unknown"))

        # Step 5: Generate investor questions
        print("❓ Generating investor questions...")
        questions_data = generate_investor_questions(request.idea, idea_data.get("sector", "unknown"))

        # Calculate overall readiness score (average of key scores)
        overall_score = (
            demand_data.get("score", 5) +
            (10 - regulatory_data.get("risk_score", 5)) +
            6.5  # Default for business model
        ) / 3

        # Create response
        response = AnalysisResult(
            idea_extraction=IdeaExtraction(**idea_data),
            demand_analysis=DemandAnalysis(**demand_data),
            regulatory_analysis=RegulatoryAnalysis(**regulatory_data),
            business_canvas=BusinessCanvas(**canvas_data),
            investor_questions=[InvestorQuestion(**q) for q in questions_data],
            overall_readiness_score=round(overall_score, 1),
            analysis_status="completed"
        )

        # Store in database
        print("💾 Saving to database...")
        db_idea = StartupIdea(
            title=idea_data.get("title", "Untitled"),
            description=request.idea,
            sector=idea_data.get("sector"),
            target_customer=idea_data.get("target_customer"),
            revenue_model=idea_data.get("revenue_model"),
            location=idea_data.get("location"),
            language=request.language
        )
        db.add(db_idea)
        db.commit()
        db.refresh(db_idea)

        # Store analysis results
        db_analysis = Analysis(
            idea_id=db_idea.id,
            demand_score=demand_data.get("score"),
            regulatory_score=10 - regulatory_data.get("risk_score", 5),
            business_model_score=6.5,
            overall_readiness=response.overall_readiness_score,
            demand_validation=demand_data,
            regulatory_risks=regulatory_data,
            business_canvas=canvas_data,
            investor_questions=questions_data
        )
        db.add(db_analysis)
        db.commit()

        print("✅ Analysis complete!")
        return response

    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# ============================================================================
# Placeholder for future endpoints
# ============================================================================
# @app.post("/api/v1/retrieve")     # RAG retrieval
# @app.post("/api/v1/investor-qa")  # Q&A endpoint

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
