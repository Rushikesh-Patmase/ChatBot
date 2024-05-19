from flask import Flask, request, jsonify
from transformers import pipeline
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3

app = Flask(__name__)

# Load a small language model
chatbot = pipeline("text-generation", model="gpt2")

# Initialize SQLite Database
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (email text, password text)''')
conn.commit()

user_sessions = {}

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    from_number = request.values.get('From', '')
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()
    msg = response.message()

    if from_number not in user_sessions:
        user_sessions[from_number] = {'stage': None}

    if user_sessions[from_number]['stage'] is None:
        if "i want to log in" in incoming_msg:
            user_sessions[from_number]['stage'] = 'email'
            msg.body("Please enter your email:")
        else:
            msg.body("I'm a simple chatbot. Type 'i want to log in' to start.")
    elif user_sessions[from_number]['stage'] == 'email':
        user_sessions[from_number]['email'] = incoming_msg
        user_sessions[from_number]['stage'] = 'password'
        msg.body("Please enter your password:")
    elif user_sessions[from_number]['stage'] == 'password':
        user_sessions[from_number]['password'] = incoming_msg
        email = user_sessions[from_number]['email']
        password = incoming_msg
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        user_sessions[from_number]['stage'] = None
        msg.body("Your account has been registered.")
    
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
