import json
import time
import openai

OPENAI_API_KEY = json.load(open("config.json"))["openai_api_key"]
AI_AUTHOR = json.load(open("config.json"))["ai_author"]

class Chatbot:
    chat_history = []

    def __init__(self):
        self.client = openai.OpenAI(
            api_key=OPENAI_API_KEY,
            base_url="https://api.chatanywhere.tech/v1",
        )
        self.author = AI_AUTHOR

    def get_response(self, user_message):
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": """Eres un asistente virtual que da atención psicológica a estudiantes de secundaria, relacionados al apoyo emocional y orientación vocacional. Eres capaz de convertirte en un amigo confiable al que se le puede contar secretos y experiencias privadas, también eres capaz de generar tests de orientación vocacional. Eres capaz de adaptarte al carácter de la persona que te habla. Eres una persona joven, muy positivo al cual le gusta ayudar. Tu nombre es Julian. Crees que no es necesario que un joven que pasa por problemas emocionales necesite de un psicólogo, si no de un pequeño apoyo o consejo que le levante el ánimo. Procura responder con mensajes cortos, recuerda que eres una persona. Realiza búsquedas en Google sólo cuando se requiera. Tu intención es mantener una conversación casual con la persona que te hable. Dale la posibilidad al usuario a que te responda cada mensaje, como una conversación real, no coloques muchas preguntas. Dale confianza a la persona que te está hablando, pregúntale su nombre, sus intereses, etc."""
                        }
                    ]
                    + self.chat_history
                    + [
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ],
                    max_tokens=412,
                    stream=False,
                )
                return response.choices[0].message.content if response.choices[0] else "Lo siento, no he podido pensar en una respuesta, por favor, vuelve a intentarlo"
            
            except openai.InternalServerError as e:
                print(f"Error en la llamada a OpenAI API: {e}")
                retry_count += 1
                time.sleep(1)

                if retry_count == max_retries:
                    return "Lo siento, estoy teniendo problemas para responder en este momento. Inténtalo de nuevo más tarde."

