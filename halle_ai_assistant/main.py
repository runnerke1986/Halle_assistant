import uvicorn
from fastapi import FastAPI

# Importeer onze zelfgebouwde modules
from tools.ha_client import HomeAssistantClient
from agents.llm_orchestrator import LLMOrchestrator
from processors.speech_processor import SpeechProcessor

# In een modulaire setup halen we de router direct uit ons whatsapp script.
# We hebben whatsapp_bridge zojuist een eigen 'app' gegeven, dus we kunnen 
# die FastAPI app uitbreiden, of we maken hier de 'Main Application' die alles insluit.
from bridges.whatsapp_bridge import app as whatsapp_app

print("🚀 Systeem 'Halle' (Home Assistant Local Engine) aan het opstarten...")

# 1. DE KERN INITIALISEREN
# Zorg dat de engine centraal geladen wordt zodra het script start.
ha_global = HomeAssistantClient()
brein_global = LLMOrchestrator(ha_global)

# Laad Faster-Whisper met STT stilletjes in het geheugen in de achtergrond
oren_en_mond = SpeechProcessor()

# 2. DE HOOFD APPLICATIE
# We herbruiken de app uit de WhatsApp bridge, of monteren die in een grotere app.
main_app = whatsapp_app
main_app.title = "Halle Centrale Server"

# 3. EXTRA FUNCTIES KOPPELEN (b.v. een test endpoint voor spraak)
@main_app.get("/system/status")
async def get_status():
    """Een simpele heartbeat om te checken of je assistent vrolijk draait."""
    return {
        "status": "online",
        "modules": {
            "ha_bridge": "verbonden",
            "llm": brein_global.model_name,
            "stt_engine": "geladen" if oren_en_mond.model else "offline"
        }
    }

# Simuleer hoe een Voice-Speaker via het netwerk zou communiceren
@main_app.post("/system/voice_trigger")
async def handle_voice_api():
    """
    Dit endpoint zou je M5Stack of Home Assistant speaker kunnen aanroepen.
    Het ontvangt een audio bestand, zet het bliksemsnel om, en stuurt tekst of
    spraak terug.
    """
    fake_audio_path = "voorbeeld_audio.wav"
    
    # 1. Spraak naar Tekst
    tekst_gehoord = oren_en_mond.transcribe_audio(fake_audio_path)
    if not tekst_gehoord:
         return {"error": "Niks gehoord"}
         
    # 2. Denken (Met de Home Assistant context)
    antwoord = brein_global.process_message(tekst_gehoord)
    
    # 3. Tekst naar Spraak
    oren_en_mond.generate_speech(antwoord)
    
    return {"status": "uitgevoerd", "tekst": antwoord}

# 4. DE SERVER DRAAIEN
if __name__ == "__main__":
    print("✅ Architectuur succesvol ingeladen!")
    print("🌐 Typ het volgende lokaal of in je container: ")
    print("   uvicorn main:main_app --host 0.0.0.0 --port 8000 --reload")
    
    # Werkt ook direct als je `python main.py` uitvoert:
    uvicorn.run("main:main_app", host="0.0.0.0", port=8000, reload=True)
