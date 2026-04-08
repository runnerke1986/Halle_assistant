ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.12
FROM $BUILD_FROM

# Alleen de runtime bibliotheken, geen compilers
RUN apk add --no-cache \
  ffmpeg \
  ffmpeg-libs \
  libffi \
  openssl

# We installeren eerst AV en Faster-Whisper met een strikte regel:
# NIET compileren. Als er geen wheel is, moet hij stoppen.
RUN pip3 install --no-cache-dir --break-system-packages \
  --prefer-binary \
  --find-links https://wheels.home-assistant.io/musllinux/ \
  av==12.1.0 \
  faster-whisper

# De rest van de benodigdheden
RUN pip3 install --no-cache-dir --break-system-packages \
  fastapi \
  uvicorn \
  requests \
  pydantic

WORKDIR /app
COPY . .
RUN chmod a+x run.sh

CMD [ "./run.sh" ]