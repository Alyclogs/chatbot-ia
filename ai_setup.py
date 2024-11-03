import vertexai
from vertexai.preview.generative_models import GenerativeModel, Tool
from vertexai.preview.generative_models import grounding

def initialize_ai(project_id, location, system_instruction):
    vertexai.init(project=project_id, location=location)
    
    tools = [
        Tool.from_google_search_retrieval(
            google_search_retrieval=grounding.GoogleSearchRetrieval()
        ),
    ]
    
    model = GenerativeModel(
        "gemini-1.5-flash-002",
        tools=tools,
        system_instruction=[system_instruction]
    )
    
    return model.start_chat()
