import json
import os
from time import time
import uuid
from chatbot import AI_AUTHOR

# Ruta para los archivos de historial de chat
CHAT_HISTORY_PATH = "./data/chat_history"

# Ruta para los archivos de usuarios
USER_FILE = "./data/users.json"

class Handler:
    initial_message = {
        "author": AI_AUTHOR,
        "createdAt": int(time() * 1000),
        "id": str(uuid.uuid4()),
        "text": "¡Hola! soy Julian, ¿En qué puedo ayudarte hoy?"
    }

    def __init__(self, chatbot):
        try:
            if not os.path.exists(CHAT_HISTORY_PATH):
                print(f"Directory {CHAT_HISTORY_PATH} not exists, creating it...")
                os.mkdir(CHAT_HISTORY_PATH)
            print(f"Directory {CHAT_HISTORY_PATH} created successfully")
        except OSError as error:
            print(f"Directory {CHAT_HISTORY_PATH} can not be created: {error}")
        self.chatbot = chatbot

    # Función para autenticar usuario
    def get_user(self, id):
        with open(USER_FILE, "r") as file:
            users = json.load(file)
        for user in users:
            if user["id"] == id:
                return user
        return None

    # Función para autenticar usuario
    def authenticate(self, username, password):
        with open(USER_FILE, "r") as file:
            users = json.load(file)
        for user in users:
            if user["username"] == username and user["password"] == password:
                return user
        return None
  
    def register_user(self, username, password, name, lastname):
        user = self.authenticate(username, password)

        if user is None:
            with open(USER_FILE, "r") as file:
                users = json.load(file)

            new_user = {
                "username": username,
                "password": password,
                "firstName": name,
                "lastName": lastname,
                "fotoUrl": "",
                "id": f"U-{str(uuid.uuid4())}"
            }
            users.append(new_user)

            with open(USER_FILE, "w") as file:
                json.dump(users, file)
            return new_user
        
        else: return None

    def load_chat_history(self, chat_id, user_id):
        user_chat_file = f"{CHAT_HISTORY_PATH}/chat_{chat_id}_{user_id}.json"
        if os.path.exists(user_chat_file):
            print(f"Chat history found at {user_chat_file}")

            with open(user_chat_file, 'r') as file:
                chat_data = json.load(file)
                self.load_ai_messages(chat_data)
                return chat_data
        
        chat_data = {
            "id": chat_id,
            "title": "",
            "user_id": user_id,
            "messages": [self.initial_message]
        }
        # print(f"Chat history not found, creating one at {user_chat_file}")
        # self.save_chat_history(chat_data)
        self.load_ai_messages(chat_data)
        return chat_data
    
    # Función para obtener los chats existentes de un usuario
    def get_user_chats(self, user_id):
        chats = []

        for file_name in os.listdir(CHAT_HISTORY_PATH):
            if file_name.endswith(f"_{user_id}.json"):
                chat_file = os.path.join(CHAT_HISTORY_PATH, file_name)

                with open(chat_file, "r") as file:
                    chat_data = json.load(file)
                    chats.append({
                        "id": chat_data["id"],
                        "title": chat_data["title"],
                        "user_id": chat_data["user_id"]
                    })
        
        return chats
    
    def save_message(self, chat_data, message):
        if not chat_data["title"]:
            chat_data["title"] = self.generate_chat_title(message["text"])

        chat_data["messages"].append(message)
        self.load_ai_messages(chat_data)
        self.save_chat_history(chat_data)

    def save_chat_history(self, chat_data):
        user_chat_file = f"{CHAT_HISTORY_PATH}/chat_{chat_data["id"]}_{chat_data["user_id"]}.json"
        print(f"Saving chat history in {user_chat_file}")

        with open(user_chat_file, 'w') as file:
            json.dump(chat_data, file)
    
    def load_ai_messages(self, chat_data):
        self.chatbot.chat_history.clear()

        messages = chat_data["messages"]
        for message in messages:
            self.chatbot.chat_history.append({
                "role": "assistant" if message["author"]["id"] == AI_AUTHOR["id"] else "user",
                "content": message["text"]
            })

    def generate_chat_title(self, first_message_text):
        return f"{first_message_text[:30]}..."