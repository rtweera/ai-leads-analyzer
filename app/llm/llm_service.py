from app.llm.llm_client import ask_openai

def classify_lead(lead_payload: dict) -> str:
    """
    Classify the lead using OpenAI's GPT-4 model.
    """
    prompt = f"Classify the following lead information: {lead_payload}"
    classification = ask_openai(prompt)
    return classification

