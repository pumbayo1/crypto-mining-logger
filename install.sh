#!/bin/bash

# Ścieżki do plików
SCRIPT_PATH="/root/scripts/calculate_average.py"
HISTORY_PATH="/root/scripts/mining_history.csv"

# Sprawdzenie, czy katalog /root/scripts istnieje
if [ ! -d "/root/scripts" ]; then
  echo "Tworzenie katalogu /root/scripts..."
  mkdir -p /root/scripts
fi

# Pobieranie skryptu Pythona z GitHub
echo "Pobieranie skryptu Pythona..."
wget -O $SCRIPT_PATH https://raw.githubusercontent.com/pumbayo1/crypto-mining-logger/main/calculate_average.py

# Nadawanie uprawnień do uruchamiania
echo "Nadawanie uprawnień skryptowi..."
chmod +x $SCRIPT_PATH

# Tworzenie pliku historii, jeśli nie istnieje
if [ ! -f "$HISTORY_PATH" ]; then
  echo "Tworzenie pliku z historią..."
  touch $HISTORY_PATH
fi

# Dodanie zadania do crona, jeśli nie istnieje
echo "Konfigurowanie cron do uruchamiania skryptu co godzinę..."
(crontab -l 2>/dev/null | grep -q "$SCRIPT_PATH") || (crontab -l 2>/dev/null; echo "0 * * * * $SCRIPT_PATH") | crontab -

echo "Instalacja zakończona pomyślnie. Skrypt będzie uruchamiany co godzinę."
