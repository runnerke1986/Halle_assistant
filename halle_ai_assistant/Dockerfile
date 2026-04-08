# We geven een default waarde voor amd64 (jouw NUC)
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

# Installeer systeem-afhankelijkheden die nodig zijn voor het compileren van Python packages
RUN apk add --no-cache \
  python3 \
  py3-pip \
  ffmpeg \
  gcc \
  python3-dev \
  musl-dev \
  g++ \
  make \
  libffi-dev

# Upgrade pip en installeer de packages
# We doen dit in één RUN commando om de image klein te houden
RUN pip3 install --no-cache-dir --break-system-packages \
  fastapi \
  uvicorn \
  requests \
  faster-whisper \
  pydantic

# Stel de werkmap in
WORKDIR /app

# Kopieer alles (zorg dat je mappenstructuur nu klopt op GitHub!)
COPY . .

# Zorg dat het startscript uitvoerbaar is
RUN chmod a+x run.sh

CMD [ "./run.sh" ]