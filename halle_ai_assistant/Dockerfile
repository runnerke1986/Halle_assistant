ARG BUILD_FROM
FROM $BUILD_FROM

# Systeemafhankelijkheden installeren
RUN apk add --no-cache \
  python3 \
  py3-pip \
  ffmpeg \
  gcc \
  python3-dev \
  musl-dev

# Python packages installeren
# We doen dit apart zodat caching beter werkt
RUN pip3 install --no-cache-dir --break-system-packages \
  fastapi \
  uvicorn \
  requests \
  faster-whisper \
  pydantic

# Werkmap instellen
WORKDIR /app

# Kopieer de inhoud van de lokale map naar de container
COPY . .

# Zorg dat het startscript uitvoerbaar is
RUN chmod a+x run.sh

CMD [ "./run.sh" ]
