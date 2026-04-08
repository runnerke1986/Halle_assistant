import os
from typing import List, Dict

class ContextManager:
    def __init__(self, ha_memory_entity: str = "input_text.user_preferences", max_history: int = 10):
        """
        Beheert het geheugen van de AI assistent.
        
        :param ha_memory_entity: De Home Assistant entiteit waar langetermijnfeiten worden opgeslagen.
        :param max_history: Het maximaal aantal berichten in het kortetermijngeheugen (geschiedenis).
        """
        self.ha_memory_entity = ha_memory_entity
        self.max_history = max_history
        self.conversation_history: List[Dict[str, str]] = []

    def get_long_term_context(self, ha_client) -> str:
        """
        Haalt het langetermijngeheugen op vanuit Home Assistant.
        In een echte applicatie praat ha_client met de HA REST API of WebSocket.
        """
        try:
            # Pseudo-code voor de aanroep naar Home Assistant via een HA Client module:
            # state = ha_client.get_state(self.ha_memory_entity)
            # return state.get("state", "")
            
            # Tijdelijke placeholder voor testen:
            return "Gebruiker houdt van warme koffie in de ochtend. Naam is demet."
        except Exception as e:
            print(f"Fout bij ophalen langetermijngeheugen: {e}")
            return ""

    def add_message(self, role: str, content: str):
        """
        Voegt een nieuw bericht ('user' of 'assistant') toe aan de kortetermijngeschiedenis.
        """
        self.conversation_history.append({"role": role, "content": content})
        
        # Voorkom dat de context-window te groot wordt
        if len(self.conversation_history) > self.max_history:
            self._trim_history()

    def _trim_history(self):
        """
        Kort de geschiedenis in. In de toekomst kan hier een AI-samenvatting (summarization)
        worden toegevoegd om geen informatie te verliezen, maar nu knippen we het gewoon af.
        """
        self.conversation_history = self.conversation_history[-self.max_history:]

    def build_full_prompt(self, ha_client, current_user_message: str) -> List[Dict[str, str]]:
        """
        Bouwt de definitieve 'messages' array die rechtstreeks naar Ollama of OpenAI gestuurd kan worden.
        """
        # 1. Haal de feiten uit de HA entiteit (Langetermijn)
        long_term_facts = self.get_long_term_context(ha_client)
        
        # 2. Construeer een robuuste System Prompt
        system_content = (
            "Jij bent een efficiënte, snelle huisassistent voor Home Assistant.\n"
            "Geef extreem beknopte, nuttige antwoorden. Geen excuses en geen lange introducties.\n"
            "--- PERSOONLIJK GEHEUGEN EN VOORKEUREN ---\n"
            f"{long_term_facts if long_term_facts else 'Geen specifieke voorkeuren opgeslagen.'}\n"
            "------------------------------------------\n"
        )
        
        full_messages = [{"role": "system", "content": system_content}]
        
        # 3. Voeg de kortetermijn geschiedenis toe
        full_messages.extend(self.conversation_history)
        
        # 4. Voeg de daadwerkelijke nieuwe vraag toe
        full_messages.append({"role": "user", "content": current_user_message})
        
        return full_messages

    def clear_history(self):
        """Wist de huidige conversatie-sessie."""
        self.conversation_history = []
