import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS # Needed for Cross-Origin Resource Sharing

app = Flask(__name__)
# Allow requests from any origin for local development.
# In production, you'd restrict this to your frontend's domain for security.
CORS(app)

# --- Configuration for Gemini API ---
# IMPORTANT: In a real application, load your API key securely from environment variables
# or a configuration management system, NOT directly in code.
# For local testing, you should set GEMINI_API_KEY as an environment variable
# before running this script.
# Example for setting environment variable:
#   Linux/macOS: export GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"
#   Windows (Command Prompt): set GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY_HERE
#   Windows (PowerShell): $env:GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# --- Core Story Generation Function ---
def generate_bedtime_story(adventurer_name: str, adventurer_sub_name: str,
                           favorite_color: str, buddy_animal: str) -> tuple:
    """
    Generates a personalized bedtime story for kids using the Gemini API.
    Returns: (dict, status_code)
    """
    # Problem 1: API key validation
    if not GEMINI_API_KEY:
        return {"error": "Gemini API key is not set. Please set GEMINI_API_KEY environment variable."}, 500

    if not all([adventurer_name, adventurer_sub_name, favorite_color, buddy_animal]):
        return {"error": "All story parameters must be provided."}, 400

    prompt = f"""Generate a short, adventurous bedtime story for kids.
The main character's full name is \"{adventurer_name} {adventurer_sub_name}\".
Their traveling companion is a \"{buddy_animal}\".
Their favorite color, \"{favorite_color}\", should be incorporated into the story in a natural and interesting way.
The story should have a clear beginning, middle, and end.
Include a simple obstacle or challenge that the adventurer and their buddy need to overcome.
Use small, easy-to-understand words suitable for young children (ages 4-8).
The story must include a simple moral lesson that kids can learn from, stated clearly at the end or subtly woven throughout.
Make sure the adventure is exciting but not scary."""

    chat_history = [{"role": "user", "parts": [{"text": prompt}]}]

    payload = {
        "contents": chat_history,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096,
        },
    }

    try:
        full_api_url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        response = requests.post(
            full_api_url,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        print(f"Gemini API Raw Response: {json.dumps(result, indent=2)}")
        if result.get("candidates") and len(result["candidates"]) > 0 and \
           result["candidates"][0].get("content") and \
           result["candidates"][0]["content"].get("parts") and \
           len(result["candidates"][0]["content"]["parts"]) > 0:
            story_text = result["candidates"][0]["content"]["parts"][0].get("text")
            if story_text:
                return {"story": story_text}, 200
            else:
                return {"error": "Generated content is empty or malformed from AI."}, 500
        else:
            return {"error": "AI generation failed or response structure unexpected.", "details": result}, 500
    except requests.exceptions.RequestException as e:
        print(f"Network or API request error: {e}")
        return {"error": f"Failed to connect to AI story generator: {str(e)}"}, 500
    except json.JSONDecodeError as e:
        print(f"JSON decode error from API response: {e}")
        return {"error": f"Invalid response format from AI: {str(e)}"}, 500
    except Exception as e:
        print(f"An unexpected error occurred in story generation: {e}")
        return {"error": f"An internal server error occurred: {str(e)}"}, 500

# --- Flask Routes ---
@app.route('/generate_story', methods=['POST'])
def api_generate_story():
    """
    API endpoint to receive story parameters from the frontend (via POST request)
    and return a generated story.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    # Problem 3: Input validation for required fields
    required_fields = ['adventurerName', 'adventurerSubName', 'favoriteColor', 'buddyAnimal']
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    adventurer_name = data.get('adventurerName')
    adventurer_sub_name = data.get('adventurerSubName')
    favorite_color = data.get('favoriteColor')
    buddy_animal = data.get('buddyAnimal')

    # Call the core story generation function
    story_result, status_code = generate_bedtime_story(adventurer_name, adventurer_sub_name,
                                                      favorite_color, buddy_animal)
    return jsonify(story_result), status_code

if __name__ == '__main__':
    # This block executes when you run 'python app.py'
    # It starts the Flask development server.
    # For local development, debug=True is useful as it provides hot-reloading
    # and detailed error messages. Do NOT use debug=True in production.
    app.run(debug=True, port=5000)
