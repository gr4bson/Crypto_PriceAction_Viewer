import requests
import csv
from io import StringIO

class DataLoader:
    @classmethod
    def download_data_from_url(cls, url):
        response = requests.get(url)
        if response.status_code == 200:
            csv_data = response.text
            csv_data = csv_data.splitlines()
            csv_reader = csv.reader(StringIO('\n'.join(csv_data[2:])), delimiter=',')
            data_to_add = []
            for row in csv_reader:
                if len(row) >= 7:  # Sprawdzam, czy wiersz ma wystarczającą liczbę kolumn
                    data_to_add.append({
                        'date': row[1],  # Pozycja 2 (indeks 1) to Date
                        'symbol': row[2],  # Pozycja 3 (indeks 2) to Symbol
                        'open_price': float(row[3]),  # Pozycja 4 (indeks 3) to Open
                        'high_price': float(row[4]),  # Pozycja 5 (indeks 4) to High
                        'low_price': float(row[5]),  # Pozycja 6 (indeks 5) to Low
                        'close_price': float(row[6])  # Pozycja 7 (indeks 6) to Close
                    })
            return data_to_add
        else:
            return None
