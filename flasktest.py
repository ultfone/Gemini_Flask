from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_history.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

API_key = "Your_API_Key"
genai.configure(api_key=API_key)

# Define the Conversation History Model
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_query = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(2000), nullable=False)

# Create DB (only runs once) 
with app.app_context():
    db.create_all()

    def ask_gemini(query):
        model = genai.GenerativeModel("gemini-1.5-flash")

    # Retrieve convo history from  db
        history = Conversation.query.all()

                    # Build the context from the history
        context = "\n".join([f"User: {item.user_query}\nGemini: {item.answer}" for item in history])
        full_prompt = f"{context}\n\nUser: {query}"
        response = model.generate_content(full_prompt)
        return response.text if response else "No response from Gemini."
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("search")
        if not query:
            return "Query is required.", 400

        answer = ask_gemini(query)


        try:
            conversation = Conversation(user_query=query, answer=answer)
            db.session.add(conversation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}", 500

        return redirect(url_for("index"))
    # Retrieve all conversation history from the database
    try:
        history = Conversation.query.all()  
    except Exception as e:
        return f" error: {str(e)}", 500

    return render_template("index.html", history=reversed(history)) #to show the convo history from the bottom up and update it in HTML with jinja
if __name__ == "__main__":
    app.run(debug=True)     #you canuse your own port and host too 

   
