# app.py
from datetime import datetime
from time import time
import uuid
from flask import Flask, request, jsonify
from chatbot import Chatbot
from flask_cors import CORS
import os
from handler import Handler

app = Flask(__name__)
CORS(app)

chatbot = Chatbot()
handler = Handler(chatbot)

@app.route('/user', methods = ["GET"])
def get_user():
    id = request.args.get("id")

    user = handler.get_user(id)
    if user is None:
        return jsonify({"error": "El usuario no existe"}), 401
    else:
        return jsonify(user)

@app.route('/login', methods = ["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    user = handler.authenticate(username, password)
    if user is None:
        return jsonify({"error": "Credenciales incorrectas"}), 401
    else:
        return jsonify(user)
    
@app.route('/register', methods = ["GET"])
def register():
    username = request.args.get("username")
    password = request.args.get("password")
    name = request.args.get("name")
    lastname = request.args.get("lastname")

    user = handler.register_user(username, password, name, lastname)
    if user is None:
        return jsonify({"error": "El usuario ya existe"}), 401
    else:
        return jsonify(user)

# Endpoint para enviar mensaje
@app.route("/chat", methods=["POST"])
def send_message():
    username = request.args.get("username")
    password = request.args.get("password")

    user = handler.authenticate(username, password)
    if user is None:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    data = request.get_json()
    chat_id = request.args.get("chat_id") 
    message = data.get("message")
    ia_author = chatbot.author

    chat_data = handler.load_chat_history(chat_id, user["id"])

    response = chatbot.get_response(message["text"])
    handler.save_message(chat_data, message)

    ia_message = {
        "author": ia_author,
        "createdAt": int(time() * 1000),
        "id": f"M-{str(uuid.uuid4())}",
        "text": response
    }
    handler.save_message(chat_data, ia_message)
    return jsonify({ "response": response })

@app.route("/chats", methods=["GET"])
def get_user_chats():
    # Obtener parámetros de autenticación
    username = request.args.get("username")
    password = request.args.get("password")

    # Validar credenciales
    user = handler.authenticate(username, password)
    if user is None:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    # Cargar historial de chat
    chats = handler.get_user_chats(user["id"])
    return jsonify(chats)

@app.route("/messages", methods=["GET"])
def get_messages():
    # Obtener parámetros de autenticación
    username = request.args.get("username")
    password = request.args.get("password")
    chat_id = request.args.get("chat_id")

    # Validar credenciales
    user = handler.authenticate(username, password)
    if user is None:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    # Cargar historial de chat
    chat_data = handler.load_chat_history(chat_id, user["id"])
    return jsonify(chat_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
