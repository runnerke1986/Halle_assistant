import os
import requests
from fastapi import FastAPI, Request
from agents.llm_orchestrator import LLMOrchestrator
from tools.ha_client import HomeAssistantClient

# 1. API Setup
app = FastAPI(title="WhatsApp Bridge for Home Assistant")

# 2. Initialiseer Core Componenten
# In een grote productie-app doe je dit in de main.py, maar voor een compacte bridge kan het direct hier.
ha_client = HomeAssistantClient()
orchestrator = LLMOrchestrator(ha_client)

WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "http://jouw_lokale_wa_bridge:3000/send")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "optionele_api_token")

@app.post("/webhook")
async def handle_incoming_message(request: Request):
    """
    Deze webhook luistert naar inkomende JSON-berichten van je WhatsApp-koppeling
    (zoals de WhatsApp Business API, of een lokale tool zoals Baileys API).
    """
    data = await request.json()
    
    # We extraheren het nummer van de afzender en de verstuurde tekst.
    # Note: dit format varieert licht afhankelijk van je exacte WhatsApp koppeling (e.g. Meta API vs lokaal).
    sender = data.get("from")
    text_message = data.get("text", {}).get("body", "")
    
    if not text_message:
        # Als er geen tekst is (bijv. een 'read receipt' of image), negeren we het voor nu.
        return {"status": "geen actie vereist"}

    print(f"📲 Nieuw bericht van {sender}: {text_message}")

    # 3. Het "Brein" activeren: stuur de tekst naar je lokale LLM met Home Assistant context
    ai_response = orchestrator.process_message(text_message)
    
    # 4. Het antwoord onmiddellijk terugsturen naar WhatsApp
    send_reply(sender, ai_response)
    
    return {"status": "succesvol verwerkt"}

def send_reply(to_number: str, message: str):
    """
    Stuurt de door de AI gegenereerde tekst terug naar de gebruiker in WhatsApp.
    """
    payload = {
        "to": to_number,
        "text": message
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    if WHATSAPP_TOKEN:
        headers["Authorization"] = f"Bearer {WHATSAPP_TOKEN}"
        
    try:
        response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"✅ Antwoord verstuurd: {message}")
    except Exception as e:
        print(f"❌ Fout bij versturen bericht naar WhatsApp: {e}")

# Je kunt dit script als een webserver lokaal draaien via je terminal met het volgende commando:
# uvicorn bridges.whatsapp_bridge:app --host 0.0.0.0 --port 8000
