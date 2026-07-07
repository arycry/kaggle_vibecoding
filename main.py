import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from plate_app import TriageAgent, LogisticsAgent

app = FastAPI(title="P.L.A.T.E. Web API")

# Mount the static directory to serve HTML/CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Agents
try:
    triage_agent = TriageAgent()
    logistics_agent = LogisticsAgent()
except Exception as e:
    print(f"Error initializing agents: {e}")

class FoodRequest(BaseModel):
    description: str

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/process_food")
async def process_food(request: FoodRequest):
    if not request.description.strip():
        raise HTTPException(status_code=400, detail="Description cannot be empty.")
        
    try:
        # Step 1: Triage
        food_type = triage_agent.classify(request.description)
        
        if food_type == "invalid":
            raise HTTPException(status_code=400, detail="Invalid input. This application only accepts food or beverage donation descriptions.")
        
        # Step 2: Logistics Plan
        plan = logistics_agent.generate_plan(request.description, food_type)
        
        return {
            "status": "success",
            "food_type": food_type.upper(),
            "plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
