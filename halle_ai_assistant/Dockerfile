ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

# 1. Installeer systeem-afhankelijkheden die nodig zijn voor PyAV/Faster-Whisper
RUN apk add --no-cache \
  python3 \
  py3-pip \
  ffmpeg \
  ffmpeg-dev \
  pkgconfig \
  gcc \
  g++ \
  make \
  libc-dev \
  linux-headers \
  python3-dev \
  musl-dev \
  libffi-dev

# 2. Forceer de installatie van PyAV via de HA Wheels om compilatie te voorkomen
# En installeer daarna de rest van de benodigdheden
RUN pip3 install --no-cache-dir --break-system-packages \
  --find-links https://wheels.home-assistant.io/musllinux/ \
  av==12.1.0

RUN pip3 install --no-cache-dir --break-system-packages \
  --find-links https://wheels.home-assistant.io/musllinux/ \
  fastapi \
  uvicorn \
  requests \
  faster-whisper \
  pydantic

WORKDIR /app

# 3. Kopieer je bestanden (met de mappenstructuur die in orde is!)
COPY . .

# 4. Startscript uitvoerbaar maken
RUN chmod a+x run.sh

CMD [ "./run.sh" ]