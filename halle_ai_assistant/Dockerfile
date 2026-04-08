ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

# Installeer Python en benodigdheden
RUN \
  apk add --no-cache \
    python3 \
    py3-pip \
    ffmpeg \
    && pip3 install --no-cache-dir --break-system-packages \
       fastapi \
       uvicorn \
       requests \
       faster-whisper \
       pydantic

# Kopieer de code die we hebben gebouwd naar de image
COPY src/ /app/src/
COPY run.sh /

# Zorg dat HA het start script kan uitvoeren
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
