import os
import requests
import json
from agents.context_manager import ContextManager
from tools.ha_client import HomeAssistantClient

class LLMOrchestrator:
    def __init__(self, ha_client: HomeAssistantClient):
        """
        De 'Hersenen': Regelt het nadenken en uitvoeren.
        """
        self.ha_client = ha_client
        self.context_manager = ContextManager()
        
        # We gaan uit van een snelle lokale API zoals Ollama of Llama.cpp
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
        
        # Bij voorkeur een klein model voor snelheid (bijv. Llama-3-8B of Mistral)
        self.model_name = os.getenv("LLM_MODEL", "llama3")

    def process_message(self, user_text: str) -> str:
        """
        De centrale event-loop voor ieder bericht dat binnenkomt (van WhatsApp of Voice).
        """
        # 1. Haal alle verzamelde context (lange & kortetermijn) en bouw de prompt
        full_prompt_messages = self.context_manager.build_full_prompt(self.ha_client, user_text)
        
        payload = {
            "model": self.model_name,
            "messages": full_prompt_messages,
            "stream": False
        }
        
        try:
            # 2. Vraag het model om na te denken
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            ai_message = result.get("message", {}).get("content", "")
            
            # 3. Voeg daadwerkelijk toe aan het kortetermijngeheugen van de conversatie
            self.context_manager.add_message("user", user_text)
            self.context_manager.add_message("assistant", ai_message)
            
            # 4. Check of het model 'Tool Use' / Home Assistant Acties wil uitvoeren.
            # Dit vereist normaal gesproken json/function-calling logica, 
            # maar hier implementeren we een versimpelde router voor de leesbaarheid.
            return self._handle_actions_and_response(ai_message)

        except Exception as e:
            print(f"Fout tijdens LLM processing: {e}")
            return "Oeps, er is een probleem in mijn neuraal netwerk."

    def _handle_actions_and_response(self, raw_ai_response: str) -> str:
        """
        In een echte 'Tool Calling' flow geeft het LLM JSON-data strak terug. 
        Hier simuleren we dat de tekst parsed wordt op acties.
        """
        # Voorbeeld: Als de AI reageert met `{"action": "light.turn_on", "entity_id": "light.woonkamer"}`
        # Parse dit uit.
        
        # TODO: Implementeer robuuste JSON parsen of instructie parsing hier.
        # Voor nu sturen we de (hopelijk) menselijke antwoord-tekst terug naar WhatsApp of Spraak
        
        return raw_ai_response
