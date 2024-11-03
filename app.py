# app.py
from flask import Flask, request, jsonify
from chatbot import Chatbot
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
chatbot = Chatbot()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = chatbot.get_response(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
