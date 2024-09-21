#!/usr/bin/env python3

import csv
from datetime import datetime

# Ścieżka do pliku balance_log.csv
csv_file_path = '/root/scripts/balance_log.csv'

# Ścieżka do pliku z historią wydobycia
history_file_path = '/root/scripts/mining_history.csv'

def parse_csv(file_path):
    # Wczytanie pliku CSV i wyciągnięcie dwóch ostatnich linijek
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        # Wyciągnięcie dwóch ostatnich linijek
        if len(rows) < 2:
            print("Za mało danych w pliku do obliczenia średniej.")
            return None
        
        last_row = rows[-1]
        second_last_row = rows[-2]
        
        return second_last_row, last_row

def calculate_average_coins_per_hour(row1, row2):
    # Parsowanie daty i ilości coinów z linijek
    time1 = datetime.strptime(row1[0], '%d/%m/%Y %H:%M')
    time2 = datetime.strptime(row2[0], '%d/%m/%Y %H:%M')
    
    # Zamiana przecinków na kropki, aby Python mógł parsować liczby
    balance1 = float(row1[1].replace(',', '.'))
    balance2 = float(row2[1].replace(',', '.'))
    
    # Obliczenie różnicy w czasie (w godzinach)
    time_diff_hours = (time2 - time1).total_seconds() / 3600
    
    # Obliczenie różnicy w ilości coinów
    coins_diff = balance2 - balance1
    
    # Obliczenie średniej ilości coinów na godzinę
    if time_diff_hours > 0:
        average_coins_per_hour = coins_diff / time_diff_hours
        return average_coins_per_hour
    else:
        print("Brak różnicy w czasie pomiędzy logami.")
        return None

def log_mining_history(average_coins_per_hour):
    # Zapisz aktualny czas
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    # Otwórz plik z historią w trybie do dopisywania
    with open(history_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        
        # Zapisz czas i średnią ilość wydobywanych coinów
        writer.writerow([current_time, f"{average_coins_per_hour:.2f}"])

def main():
    # Parsowanie pliku CSV
    rows = parse_csv(csv_file_path)
    
    if rows:
        row1, row2 = rows
        # Obliczenie średniej ilości coinów na godzinę
        average_coins_per_hour = calculate_average_coins_per_hour(row1, row2)
        
        if average_coins_per_hour is not None:
            print(f"Średnia ilość wydobywanych coinów na godzinę: {average_coins_per_hour:.2f}")
            
            # Zaloguj wynik do pliku historii
            log_mining_history(average_coins_per_hour)

if __name__ == '__main__':
    main()
