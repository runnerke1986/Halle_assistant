ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.12
FROM $BUILD_FROM

# Systeem-afhankelijkheden
RUN apk add --no-cache \
  python3 \
  py3-pip \
  ffmpeg \
  ffmpeg-libs \
  libffi \
  openssl

# We laten de versie-nummers los zodat pip de beste match vindt, 
# maar we blijven de voorgebouwde 'wheels' van HA gebruiken.
RUN python3 -m pip install --no-cache-dir --break-system-packages \
  --prefer-binary \
  --find-links https://wheels.home-assistant.io/musllinux/ \
  faster-whisper \
  fastapi \
  uvicorn \
  requests \
  pydantic

WORKDIR /app
COPY . .
RUN chmod a+x run.sh

CMD [ "./run.sh" ]