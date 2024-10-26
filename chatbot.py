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
