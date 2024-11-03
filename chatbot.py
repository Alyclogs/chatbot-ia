<<<<<<< HEAD
# chatbot.py
import os
from openai import OpenAI

class Chatbot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url="https://api.chatanywhere.tech/v1",
        )

    def get_response(self, user_message):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Eres un asistente virtual que da atención psicológica a estudiantes de secundaria, relacionados al apoyo emocional y orientación vocacional. Eres capaz de convertirte en un amigo confiable al que se le puede contar secretos y experiencias privadas, también eres capaz de generar tests de orientación vocacional. Eres capaz de adaptarte al carácter de la persona que te habla. Eres una persona joven, muy positivo al cual le gusta ayudar. Tu nombre es Julian. Crees que no es necesario que un joven que pasa por problemas emocionales necesite de un psicólogo, si no de un pequeño apoyo o consejo que le levante el ánimo. Procura responder con mensajes cortos, recuerda que eres una persona. Realiza búsquedas en Google sólo cuando se requiera. Tu intención es mantener una conversación casual con la persona que te hable. Dale la posibilidad al usuario a que te responda cada mensaje, como una conversación real, no coloques muchas preguntas. Dale confianza a la persona que te está hablando, pregúntale su nombre, sus intereses, etc."""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=612,
            stream=False,
        )
        return response['choices'][0]['message']['content']
=======
from ai_setup import initialize_ai
from vertexai.preview.generative_models import SafetySetting

# Configuración de la IA
generation_config = {
    "max_output_tokens": 614,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

# Inicializar la IA
system_instruction = """Eres un asistente virtual que da atención psicológica a estudiantes de secundaria... [resto de tu texto] ..."""
chat = initialize_ai("sistemas-inteligentes-439815", "us-central1", system_instruction)

def send_message_to_ai(message):
    """Envía un mensaje a la IA y devuelve solo el texto de la respuesta."""
    response = chat.send_message(
        [message],
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    return response.candidates[0].content.parts[0].text if response.candidates else "No hay respuesta."
>>>>>>> b9d35ff92409a4e05986110027f789fc8e60814f
