import os
import time

try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None
    print("Let op: De 'faster-whisper' library ontbreekt. Je TTS/STT zal niet werken zonder.")

class SpeechProcessor:
    def __init__(self, model_size="distil-large-v3", device="cpu", compute_type="int8"):
        """
        De "Oren en Mond" van je efficiënte slimme assistent.
        Werkt lokaal via Faster-Whisper om latentie (< 0.5s) te minimaliseren,
        precies zoals we in de strategie hadden besproken.
        
        Voor snelle hardware (GPU/NUC) kun je de 'device' naar "cuda" of "auto" zetten.
        """
        # "distil-large-v3" is extreem capabel, maar wil je nóg sneller en Engels praten,
        # dan was "tiny.en" een fantastische bliksemsnelle fallback.
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None
        
        self._load_stt_model()

    def _load_stt_model(self):
        """Laadt het model éénmalig in het geheugen in plaats van bij iedere zin."""
        if WhisperModel is None:
            return

        print(f"Laadt STT Whisper model ({self.model_size}) in het {self.device}-geheugen...")
        try:
            self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
            print("🚀 Whisper succesvol in het geheugen geladen! Klaar voor instant-verwerking.")
        except Exception as e:
            print(f"❌ Fout bij het initialiseren van STT model: {e}")

    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Dit is je 'Whisper Trick': het lokaal en bloedsnel omzetten van audio naar tekst.
        """
        if not self.model:
            return "Spraakmodel is offline."
            
        start_time = time.time()
        try:
            # We gebruiken beam_size=1 of 2 in plaats van default 5. Dit is sneller,
            # terwijl het nog steeds erg accuraat is voor algemene huis commando's.
            segments, info = self.model.transcribe(audio_file_path, beam_size=2)
            
            transcriptie = " ".join([segment.text for segment in segments])
            
            # Bereken exact hoelang we over "Time to First Text" deden
            latency = round((time.time() - start_time) * 1000, 2)
            print(f"🎤 [{latency}ms] Gehoord: {transcriptie.strip()} (taal: {info.language})")
            
            return transcriptie.strip()
        except Exception as e:
            print(f"❌ Error tijdens audiotranscriptie: {e}")
            return ""

    def generate_speech(self, ai_text_response: str, output_path: str = "output_audio.wav") -> str:
        """
        Text-to-Speech (TTS). In deze setup idealiter aangedreven door 'Piper'.
        Piper werkt direct en lokaal (perfect voor Home Assistant).
        
        In plaats van hier direct de Piper Python API te importeren (wat zwaar is) 
        kunnen we bij benadering lokaal een commando aanroepen of via de Wyoming add-on werken.
        """
        print(f"🔊 Antwoord wordt omgezet naar audio (TTS): '{ai_text_response}'")
        
        # Pseudo logica voor de daadwerkelijke TTS uitvoering:
        # os.system(f'echo "{ai_text_response}" | piper --model nl_NL-hfc_name-medium > {output_path}')
        
        # Voor nu retourneren we een pad naar de (fictieve) geluidsfile
        return output_path
