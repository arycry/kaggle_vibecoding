"""
P.L.A.T.E. (Predictive Logistics Agent for Triage & Edibles)
Main Application orchestrating the ADK multi-agent system.
"""

import os
import sys
from google import genai
from mcp_server import find_local_charity

# --- SECURITY FIRST ---
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("CRITICAL SECURITY ALERT: GEMINI_API_KEY environment variable is missing.")
    print("Please set the API key to proceed safely. Exiting.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

class TriageAgent:
    """
    Agent 1: Triage Classifier
    Responsible for categorizing the food donation into 'cooked' or 'raw'.
    Demonstrates ADK separation of concerns.
    """
    def __init__(self):
        # Using Gemini 2.5 Flash for quick classification tasks
        self.model_name = 'gemini-2.5-flash'
        
    def classify(self, user_input: str) -> str:
        prompt = f"""
        Act as a strict food triage classifier. 
        Read the following user input and determine if it is a food or beverage donation.
        If it is a valid food/beverage donation, classify it and output ONLY the word "cooked" or "raw".
        If the input is NOT related to food/beverage donations (e.g., general questions, math, casual chat, spam), output ONLY the word "invalid".
        Do not include punctuation, explanations, or any other words.
        
        Input: "{user_input}"
        """
        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            classification = response.text.strip().lower()
            
            # Resilience: Fallback and sanitization
            if "invalid" in classification:
                return "invalid"
            elif "cooked" in classification:
                return "cooked"
            elif "raw" in classification:
                return "raw"
            else:
                # Programmatic fallback if the LLM hallucinates
                print("[TriageAgent] Warning: LLM returned invalid category. Defaulting to 'raw' for safety.")
                return "raw"
        except Exception as e:
            print(f"[TriageAgent] System error during classification: {e}")
            return "raw"

class LogisticsAgent:
    """
    Agent 2: Logistics Planner
    Responsible for taking the food type, querying the MCP tool, and generating a delivery plan.
    Demonstrates ADK tool usage and sequential agent handoff.
    """
    def __init__(self):
        # Using Gemini 2.5 Flash as it is supported by the free tier quota
        self.model_name = 'gemini-2.5-flash'
        
    def generate_plan(self, original_input: str, food_type: str) -> str:
        # Programmatic call to MCP Server Tool
        print(f"[LogisticsAgent] Querying MCP Server tool 'find_local_charity' for '{food_type}' food...")
        mcp_data = find_local_charity(food_type)
        
        prompt = f"""
        Act as a polite, professional logistics planner for P.L.A.T.E.
        
        The user wants to donate: "{original_input}"
        The food was classified as: {food_type}
        
        Here is the data retrieved from our local charity database (MCP Tool Output):
        {mcp_data}
        
        Based on this data, please write a clear, actionable logistical delivery plan for the restaurant.
        Be concise, helpful, and polite. If no charities are found or an error occurred, explain the next steps gracefully.
        """
        
        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"Failed to generate logistics plan due to an internal error: {e}"

def main():
    """
    CLI Loop: Interactive terminal interface for P.L.A.T.E.
    """
    # Stylized welcome banner
    print("=" * 60)
    print("   Welcome to P.L.A.T.E. CLI Interface")
    print("   Predictive Logistics Agent for Triage & Edibles")
    print("   Track: Agents for Good (Food Insecurity)")
    print("=" * 60)
    print("Type 'exit' or 'quit' to close the application.\n")
    
    triage_agent = TriageAgent()
    logistics_agent = LogisticsAgent()
    
    while True:
        try:
            user_input = input("\n[Restaurant User] Enter leftover food description: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("\nShutting down P.L.A.T.E. Thank you for helping reduce food waste!")
                break
                
            print("\n--- Agent Workflow Started ---")
            
            # Step 1: Triage Agent
            print(f"[TriageAgent] Analyzing input: '{user_input}'...")
            food_type = triage_agent.classify(user_input)
            print(f"[TriageAgent] Output Classification -> {food_type.upper()}")
            
            # Step 2: Logistics Agent
            plan = logistics_agent.generate_plan(user_input, food_type)
            print("\n[LogisticsAgent] Generated Delivery Plan:")
            print("-" * 40)
            print(plan)
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\n\nProcess interrupted by user. Shutting down P.L.A.T.E. safely.")
            sys.exit(0)
        except Exception as e:
            print(f"\n[System] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
