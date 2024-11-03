<<<<<<< HEAD
# app.py
from flask import Flask, request, jsonify
from chatbot import Chatbot

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
=======
from flask import Flask, request, jsonify
from chatbot import send_message_to_ai

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
    """Ruta para enviar un mensaje a la IA."""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided."}), 400
    
    response_message = send_message_to_ai(user_message)
    return jsonify({"response": response_message})
>>>>>>> b9d35ff92409a4e05986110027f789fc8e60814f

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
