from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import ask_samvidhan
from scenario_advisor import get_scenario_based_response

app = FastAPI(
    title="Samvidhan AI API",
    description="API for Constitutional Law Q&A and Scenario Analysis",
    version="1.0.0"
)

# -------------------- Request Body Models --------------------

class ChatQueryRequest(BaseModel):
    question: str

class ScenarioRequest(BaseModel):
    scenario: str

# -------------------- Home Route --------------------

@app.get("/")
def home():
    return {"message": "✅ Samvidhan AI API is running!"}

# -------------------- Chatbot Endpoint --------------------

@app.post("/chat")
def ask_constitutional_question(request: ChatQueryRequest):
    try:
        answer = ask_samvidhan(request.question)
        return {
            "question": request.question,
            "answer": answer
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to generate answer for constitutional question."
        }

# -------------------- Scenario-Based Analysis Endpoint --------------------

@app.post("/scenario")
def analyze_scenario(request: ScenarioRequest):
    try:
        response = get_scenario_based_response(request.scenario)
        return {
            "scenario": request.scenario,
            "analysis": response
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to analyze the legal scenario."
        }
    ```

---

### ✅ How to Run It

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
