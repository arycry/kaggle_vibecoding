# P.L.A.T.E. - Predictive Logistics Agent for Triage & Edibles

## Overview
P.L.A.T.E. is a sequential multi-agent system designed to eliminate the friction in routing restaurant food surplus to local charities. By utilizing natural language processing, the system instantly classifies leftover food and generates a secure, actionable logistics plan.

## Architecture
This project utilizes a Separation of Concerns pattern with two primary agents:
*   **TriageAgent**: Acts as a strict binary classifier to determine if the described food is 'cooked' or 'raw', preventing LLM hallucinations.
*   **LogisticsAgent**: The core reasoning engine. It takes the classification, queries a local **MCP Server**, and synthesizes a delivery plan.

The backend is built with **FastAPI**, serving a clean Glassmorphism UI through static HTML/CSS/JS.

## Prerequisites
*   Python 3.9+
*   A valid Google Gemini API Key

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/arycry/kaggle_vibecoding
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your API Key:**
   Set your Google Gemini API key as an environment variable to ensure security.
   Windows (CMD):
   ```bash
   set GEMINI_API_KEY=your_api_key_here
   ```
   Windows (PowerShell):
   ```bash
   $env:GEMINI_API_KEY=  "your_api_key_here"
   ```
   
   Mac/Linux:
   ```bash
   export GEMINI_API_KEY= "your_api_key_here"
   ```

5. Running the Application
   Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
   Once the server is running, open your browser and navigate to http://127.0.0.1:8000 to interact with the P.L.A.T.E. web interface.
