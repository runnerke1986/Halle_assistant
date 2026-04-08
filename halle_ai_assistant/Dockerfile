ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.12
FROM $BUILD_FROM

# Installeer systeem-afhankelijkheden en zorg dat pip aanwezig is
RUN apk add --no-cache \
  python3 \
  py3-pip \
  ffmpeg \
  ffmpeg-libs \
  libffi \
  openssl

# We installeren met 'python3 -m pip' om de 'not found' error te voorkomen
RUN python3 -m pip install --no-cache-dir --break-system-packages \
  --prefer-binary \
  --find-links https://wheels.home-assistant.io/musllinux/ \
  av==12.1.0 \
  faster-whisper

RUN python3 -m pip install --no-cache-dir --break-system-packages \
  fastapi \
  uvicorn \
  requests \
  pydantic

WORKDIR /app
COPY . .
RUN chmod a+x run.sh

CMD [ "./run.sh" ]