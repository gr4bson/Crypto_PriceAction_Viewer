from db_handler import DbHandler
from data_loader import DataLoader
from show_data import get_data_between_dates, calculate_data_stats
from datetime import datetime, timedelta

# Inicjalizacja handlera bazy danych
db_handler = DbHandler()

# Rozpoczęcie sesji SQLAlchemy
session = db_handler.create_session()

# Zapytanie użytkownika o symbol kryptowaluty
symbol = input("Podaj symbol kryptowaluty: ") or 'ETH'
# Zapytanie użytkownika o datę początkową i końcową analizy
start_date_str = input("Podaj datę początkową analizy (RRRR-MM-DD HH:MM): ") or '2023-09-01 12:00'
end_date_str = input("Podaj datę końcową analizy (RRRR-MM-DD HH:MM): ") or '2023-09-07 14:00'

try:
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")
except ValueError:
    print("Błąd w formacie daty. Upewnij się, że podajesz datę w formacie RRRR-MM-DD HH:MM")
else:
    # Sprawdzenie, czy tabela o nazwie symbol istnieje i tworzenie jej, jeśli nie istnieje
    db_handler.check_and_create_table(symbol)
    # Sprawdzenie, czy dane są aktualne
    if db_handler.is_data_fresh(symbol):
        print("Dane w tabeli są aktualne.")
    else:
        # Pobieranie danych z URL
        csv_url = f"https://www.cryptodatadownload.com/cdd/Binance_{symbol}USDT_2023_minute.csv"
        data_to_add = DataLoader.download_data_from_url(csv_url)

        if data_to_add:
            # Dodawanie danych do tabeli
            db_handler.add_data_to_table(symbol, data_to_add)
            print(f"Dane zostały pobrane i dodane do tabeli '{symbol}'.")
        else:
            print("Błąd podczas pobierania danych z URL.")

    # Zakończenie sesji SQLAlchemy
    db_handler.close_session(session)

    # Prezentacja skalkulowanych danych:
    data = get_data_between_dates(symbol, start_date, end_date)
    if data:
        stats = calculate_data_stats(data)
        if stats:
            print("\nStatystyki danych:")
            print(f"Najniższa cena (Low Price): {stats['min_low_price']}")
            print(f"Najwyższa cena (High Price): {stats['max_high_price']}")
            print(f"Rozpiętość ceny (Price Span): {stats['price_span']}")
            print(f"Procentowa rozpiętość ceny (% Price Span:): {stats['perc_price_span']:.2f}%")
            print(f"Open Price na początku okresu: {stats['open_price']}")
            print(f"Close Price na końcu okresu: {stats['close_price']}")
            print(f"Procentowa zmiana w okresie (Percentage Change): {stats['percentage_change']:.2f}%")
    else:
        print("Brak danych w podanym okresie.")


