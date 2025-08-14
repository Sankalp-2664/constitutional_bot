from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scenario_advisor import get_scenario_based_response
from chatbot import ask_samvidhan

app = FastAPI()

class ScenarioRequest(BaseModel):
    scenario: str

class ChatbotRequest(BaseModel):
    question: str

@app.get("/")
async def home():
    return {
        "message": "Welcome to the Samvidhan AI API!",
        "endpoints": {
            "POST /ask-chatbot": {"question": "string"},
            "POST /analyze-scenario": {"scenario": "string"}
        }
    }

@app.post("/analyze-scenario")
async def analyze_scenario(request: ScenarioRequest):
    scenario = request.scenario.strip()
    if not scenario:
        raise HTTPException(status_code=400, detail="Scenario cannot be empty.")

    try:
        response = get_scenario_based_response(scenario)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing scenario: {str(e)}")

@app.post("/ask-chatbot")
async def ask_chatbot(request: ChatbotRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        answer = ask_samvidhan(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting chatbot answer: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
