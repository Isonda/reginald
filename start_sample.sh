#!/bin/sh
echo "Staring Reginald, the llama butler"
if [ -z "$PRODUCTION"]; then
    # DEV
    echo "Development API Key"
    export API_KEY="[Dev key here]"
    python bot.py
else
    # PROD
    echo "Production API Key"
    export API_KEY="[Prod key here]"
    /usr/bin/python3 /code/bot.py
fi
