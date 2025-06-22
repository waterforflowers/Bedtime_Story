**💤 Bedtime Storyteller Backend (Python Flask) 💤**

- This is the Python Flask backend for the "Bedtime Storyteller" web application. It acts as an API server responsible for generating personalized bedtime stories using the Google Gemini AI model. The frontend (HTML/CSS/JavaScript) communicates with this backend to get the stories.

**🔑 Key Components & Logic 🔑:**

**1.** generate_bedtime_story(adventurer_name, adventurer_sub_name, favorite_color, buddy_animal) Function:

- Purpose: The core logic for AI interaction. It constructs a detailed prompt using the provided user inputs (adventurer's name, sub-name, favorite color, and animal buddy).

- AI Interaction: Sends the crafted prompt to the Gemini API (gemini-2.0-flash model) via an HTTP POST request. It's configured with a temperature of 0.7 for balanced creativity and maxOutputTokens of 4096 to ensure complete story generation.

- Error Handling: Includes robust try-except blocks to catch network issues, API errors (e.g., rate limits, invalid responses), and general server errors.

- Returns: A dictionary containing the generated story text (e.g., {"story": "Once upon a time..."}) and a 200 HTTP status code on success. On failure, it returns an error dictionary (e.g., {"error": "message"}) and an appropriate HTTP status code (e.g., 400 for bad input, 500 for server errors).

**2.** /generate_story Flask Route (@app.route('/generate_story', methods=['POST'])):

- Purpose: This is the API endpoint that your web frontend calls.

- Request Handling: It expects a POST request with JSON data containing adventurerName, adventurerSubName, favoriteColor, and buddyAnimal.

- Delegation: It extracts these parameters and passes them to the generate_bedtime_story function.

- Response: It takes the result and status code from generate_bedtime_story and converts it into a JSON response sent back to the frontend.

- CORS: flask_cors is enabled to allow cross-origin requests from your frontend for local development.

**⚙️ Setup and Running the Backend ⚙️:**

To run this backend, you need Python installed and your Gemini API Key.

**1. Save the Code:**

- Save the Python code as app.py in a new folder (e.g., bedtime_app_backend/).

**2. Install Dependencies:**

- Open your terminal or command prompt.

- Navigate to the folder where you saved app.py:

cd path/to/your/bedtime_app_backend

- Install the required Python packages:

pip install Flask Flask-Cors requests

**3. Set Your Gemini API Key:**

- Crucial Step: The backend needs your Google Gemini API key to access the AI model. Set it as an environment variable before running the script.

- Linux/macOS:

export GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"

- Windows (Command Prompt):

set GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY_HERE

- Windows (PowerShell):

$env:GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"

- Note: Replace "YOUR_ACTUAL_GEMINI_API_KEY_HERE" with your actual key. This is the recommended secure way. Alternatively, for quick local tests, you could paste the key directly into the app.py file, but this is less secure.

**4. Run the Flask Server:**

- In the same terminal window where you set the environment variable, run:

python app.py

- You should see output similar to * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit). This indicates the backend server is running and ready to receive requests. Keep this terminal window open.

- Once the backend is running, you can open your frontend HTML file in a web browser, and it will communicate with this Python server to generate stories.

**⚙️ Why it works this way ⚙️**

- API Key Security: Crucially, it keeps your Gemini API key hidden on the server, preventing exposure in the frontend.
  
- Backend Logic & Control: It centralizes logic like validating user inputs and constructing the detailed AI prompt, ensuring data integrity before interacting with the Gemini API.
  
- Cross-Origin Communication: As a backend, it acts as a necessary intermediary to handle requests from your frontend (Canvas) due to browser security policies (CORS).
  
- Maintainability: This separation allows for cleaner development, testing, and easier updates to either the frontend or backend independently.
