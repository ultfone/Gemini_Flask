from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai

app = Flask(__name__)

# Configure SQLAlchemy (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_history.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Replace with your actual Gemini API key
GEMINI_API_KEY = "Your_api_key"
genai.configure(api_key=GEMINI_API_KEY)

# Define the Conversation History Model
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_query = db.Column(db.String(500), nullable=False)  # Renamed from 'query' to 'user_query'
    answer = db.Column(db.String(2000), nullable=False)

# Create the database and tables (run this once)
with app.app_context():
    db.create_all()

# Function to query Gemini
def ask_gemini(query):
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Retrieve conversation history from the database
    history = Conversation.query.all()

    # Build the context from the history
    context = "\n".join([f"User: {item.user_query}\nGemini: {item.answer}" for item in history])

    # Combine the context with the new query
    full_prompt = f"{context}\n\nUser: {query}"

    # Send the full prompt to Gemini
    response = model.generate_content(full_prompt)
    return response.text if response else "No response from Gemini."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("search")
        if not query:
            return "Query is required.", 400

        answer = ask_gemini(query)

        # Save the query and answer to the database
        try:
            conversation = Conversation(user_query=query, answer=answer)  # Use 'user_query' here
            db.session.add(conversation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}", 500

        return redirect(url_for("index"))

    # Retrieve all conversation history from the database
    try:
        history = Conversation.query.all()  # This will now work correctly
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

    return render_template("index.html", history=history)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)      
