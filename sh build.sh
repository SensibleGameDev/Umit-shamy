#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Деректер қорын инициализациялау (Әр жаңарту сайын тазаланады!)
flask init-db