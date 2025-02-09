# Flask Gemini Chatbot

This project is a chatbot built using Flask and Google Gemini API. It stores conversation history in an SQLite database and dynamically updates the UI using Jinja templates.

## Features

- Integrates Google Gemini API for AI-generated responses
- Stores conversation history in a SQLite database
- Dynamically updates UI with Jinja templating

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/ultfone/Gemini_Flask.git
   cd Gemini_Flask
   ```

2. Install dependencies:

   ```sh
   pip install flask flask_sqlalchemy google-generativeai
   ```

3. Set up your Google Gemini API key in the script:

   ```python
   API_key = "Your_API_Key"
   ```

4. Run the application:

   ```sh
   python flasktest.py
   ```

5. Access the application in your browser:

   ```
   http://localhost
   ```

## Technologies Used

- **Flask** (Backend framework)
- **SQLite** (Database for storing conversation history)
- **Google Gemini API** (AI-generated responses)
- **Jinja** (Templating engine for dynamic content rendering)

## Usage

- Enter a query in the input box and submit.
- The chatbot will generate a response using the Gemini API.
- All previous conversations are stored and displayed on the webpage.

