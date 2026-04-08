import os
import requests

class HomeAssistantClient:
    def __init__(self, url: str = None, token: str = None):
        """
        De 'Handen en Ogen' van je AI: de API client voor Home Assistant.
        """
        # Je haalt deze best uit een .env bestand of configuratie
        self.url = url or os.getenv("HA_URL", "http://homeassistant.local:8123")
        self.token = token or os.getenv("HA_TOKEN", "JOUW_LONG_LIVED_ACCESS_TOKEN_HIER")
        
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def get_state(self, entity_id: str) -> dict:
        """Haalt de huidige status (en evt attributen) van een specifieke entiteit op."""
        try:
            response = requests.get(
                f"{self.url}/api/states/{entity_id}",
                headers=self.headers,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Fout bij ophalen van {entity_id}: {e}")
            return {}

    def call_service(self, domain: str, service: str, service_data: dict = None) -> bool:
        """
        Roept een actie aan in Home Assistant.
        Voorbeeld: call_service("light", "turn_on", {"entity_id": "light.woonkamer_plafond_1"})
        """
        service_data = service_data or {}
        try:
            response = requests.post(
                f"{self.url}/api/services/{domain}/{service}",
                headers=self.headers,
                json=service_data,
                timeout=5
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Fout bij uitvoeren van {domain}.{service}: {e}")
            return False

    def update_memory(self, memory_entity_id: str, new_memory_text: str) -> bool:
        """
        Een specifieke wrapper om je langetermijngeheugen up te daten 
        (mits opgeslagen in een input_text of iets dergelijks binnen HA).
        """
        return self.call_service("input_text", "set_value", {
            "entity_id": memory_entity_id,
            "value": new_memory_text
        })
