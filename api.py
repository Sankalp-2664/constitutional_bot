from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import asyncio
from dotenv import load_dotenv

# Import your existing modules
try:
    from chatbot import ask_samvidhan
    from scenario_advisor import get_scenario_based_response
except ImportError as e:
    raise ImportError(f"Failed to import required modules: {e}")

# Load environment variables
load_dotenv()

# Ensure event loop for async operations
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Initialize FastAPI app
app = FastAPI(
    title="Samvidhan AI API",
    description="API for Constitutional law assistance and scenario analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ChatQuery(BaseModel):
    question: str
    
class ChatResponse(BaseModel):
    answer: str
    success: bool
    error: Optional[str] = None

class ScenarioQuery(BaseModel):
    scenario: str
    
class ScenarioResponse(BaseModel):
    analysis: str
    success: bool
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify API is running."""
    return HealthResponse(
        status="healthy",
        message="Samvidhan AI API is running successfully"
    )

# Constitutional chatbot endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_with_samvidhan(query: ChatQuery):
    """
    Ask questions about the Constitution of India.
    
    Args:
        query: ChatQuery object containing the question
        
    Returns:
        ChatResponse with the constitutional answer
    """
    try:
        if not query.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Get response from chatbot
        answer = ask_samvidhan(query.question)
        
        return ChatResponse(
            answer=answer,
            success=True
        )
    
    except Exception as e:
        return ChatResponse(
            answer="",
            success=False,
            error=f"Error processing question: {str(e)}"
        )

# Scenario analysis endpoint
@app.post("/analyze-scenario", response_model=ScenarioResponse)
async def analyze_scenario(scenario_query: ScenarioQuery):
    """
    Analyze legal scenarios based on Constitutional law.
    
    Args:
        scenario_query: ScenarioQuery object containing the scenario description
        
    Returns:
        ScenarioResponse with constitutional analysis
    """
    try:
        if not scenario_query.scenario.strip():
            raise HTTPException(status_code=400, detail="Scenario description cannot be empty")
        
        # Get analysis from scenario advisor
        analysis = get_scenario_based_response(scenario_query.scenario)
        
        return ScenarioResponse(
            analysis=analysis,
            success=True
        )
    
    except Exception as e:
        return ScenarioResponse(
            analysis="",
            success=False,
            error=f"Error analyzing scenario: {str(e)}"
        )

# Get API information
@app.get("/info")
async def get_api_info():
    """Get information about the API and its capabilities."""
    return {
        "name": "Samvidhan AI API",
        "version": "1.0.0",
        "description": "API for Constitutional law assistance and scenario analysis",
        "endpoints": {
            "/health": "Health check",
            "/chat": "Ask constitutional questions",
            "/analyze-scenario": "Analyze legal scenarios",
            "/info": "API information",
            "/docs": "API documentation (Swagger UI)",
            "/redoc": "Alternative API documentation"
        },
        "features": [
            "Constitutional Q&A with FAISS vector search",
            "Scenario-based legal analysis using Gemini AI",
            "Article and Schedule references",
            "Source citations"
        ]
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with welcome message."""
    return {
        "message": "Welcome to Samvidhan AI API",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0"
    }

# Example usage endpoint
@app.get("/examples")
async def get_examples():
    """Get example queries and scenarios for testing."""
    return {
        "chat_examples": [
            "What are the fundamental rights in the Constitution?",
            "Explain Article 19 of the Constitution",
            "What is the procedure for constitutional amendments?",
            "What are the directive principles of state policy?"
        ],
        "scenario_examples": [
            "A state government passes a law restricting online speech criticizing its ministers, citing maintenance of public order. Is this constitutional?",
            "A private school refuses admission based on religion. What does the Constitution say?",
            "Government wants to acquire private land for highway. What are the constitutional provisions?",
            "A citizen wants to challenge a law in court. What are their constitutional rights?"
        ]
    }

# Error handler for validation errors
@app.exception_handler(422)
async def validation_exception_handler(request, exc):
    return {
        "error": "Validation Error",
        "message": "Please check your input format",
        "details": str(exc)
    }

# Global exception handler
@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "details": str(exc)
    }

if __name__ == "__main__":
    import uvicorn
    
    # Check if required files exist
    required_files = ["vector_store/faiss_index_constitution/index.faiss"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"Warning: Missing required files: {missing_files}")
        print("Please ensure FAISS index is built before running the API.")
    
    # Check environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not found in environment variables.")
        print("Please set your Google API key in .env file.")
    
    print("Starting Samvidhan AI API...")
    print("API Documentation will be available at: http://localhost:8000/docs")
    print("Alternative docs at: http://localhost:8000/redoc")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
