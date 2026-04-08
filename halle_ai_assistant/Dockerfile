ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

# Alleen de noodzakelijke runtime bibliotheken installeren (geen compilers meer nodig!)
RUN apk add --no-cache \
  python3 \
  py3-pip \
  ffmpeg \
  libffi \
  openssl

# Gebruik de Home Assistant wheels-index om compilatie-fouten te voorkomen
RUN pip3 install --no-cache-dir --break-system-packages \
  --find-links https://wheels.home-assistant.io/musllinux/ \
  fastapi \
  uvicorn \
  requests \
  faster-whisper \
  pydantic

WORKDIR /app
COPY . .
RUN chmod a+x run.sh

CMD [ "./run.sh" ]