"""
MCP Server Mock implementation for P.L.A.T.E.
Provides a local tool to simulate external data retrieval for local charities.
"""

import json
import os
from typing import List, Dict, Any

def find_local_charity(food_type: str) -> str:
    """
    Reads charities.json, filters by food_type (case-insensitive), 
    and returns a sorted list of charities by distance.
    
    Args:
        food_type (str): The type of food accepted ("cooked" or "raw").
        
    Returns:
        str: A neatly formatted string of matched charities or an error message.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'charities.json')
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Filter and sort
        matched = [c for c in data if c.get('accepted_food_type', '').lower() == food_type.lower()]
        matched.sort(key=lambda x: x.get('distance_km', float('inf')))
        
        if not matched:
            return f"No charities found accepting '{food_type}' food within range."
            
        # Format the output
        result = [f"Found {len(matched)} local charities accepting {food_type} food:"]
        for charity in matched:
            result.append(
                f"- {charity['name']} (ID: {charity['id']}) | Distance: {charity['distance_km']}km"
            )
            
        return "\n".join(result)
        
    except FileNotFoundError:
        return "SECURITY LOG: Error 404 - Database file 'charities.json' not found or inaccessible."
    except json.JSONDecodeError:
        return "SECURITY LOG: Error 500 - Database file is malformed. Failed to parse JSON."
    except Exception as e:
        # Catch-all to prevent exposing internal stack traces as per requirements
        return "SECURITY LOG: Error 500 - An unexpected system error occurred during data retrieval."
