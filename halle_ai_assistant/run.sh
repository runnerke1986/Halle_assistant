#!/usr/bin/env bashio

echo "✨ Halle Assistent Add-on start op..."

# Bashio laat ons direct met de supervisor van HA praten,
# we hoeven dus zelf geen access tokens aan te maken, het systeem injecteert ze!
export HA_URL="http://supervisor/core"
export HA_TOKEN=$SUPERVISOR_TOKEN

# Haal de configuratie die je in de UI invult op
export OLLAMA_URL=$(bashio::config 'ollama_url')
export LLM_MODEL=$(bashio::config 'llm_model')
export WHATSAPP_TOKEN=$(bashio::config 'whatsapp_token')

echo "Geladen configuratie:"
echo "LLM Model: $LLM_MODEL"

# Navigeer naar de applicatie map en start onze applicatie poort 8000
cd /app/src
exec python3 main.py
