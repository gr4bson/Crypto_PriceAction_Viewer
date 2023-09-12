from db_handler import DbHandler
from datetime import datetime

def get_data_between_dates(symbol, start_date, end_date):
    db_handler = DbHandler()
    session = db_handler.create_session()

    try:
        # Ustalamy nazwę tabeli na podstawie symbolu
        table_name = db_handler.CryptoPrice.__table__.name = symbol

        # Pobieramy dane z okresu pomiędzy dwoma datami
        data = session.query(db_handler.CryptoPrice).filter(
            db_handler.CryptoPrice.date >= start_date
        ).filter(
            db_handler.CryptoPrice.date <= end_date
        ).all()

        return data
    finally:
        db_handler.close_session(session)

def calculate_data_stats(data):
    if not data:
        return None

    # Sortujemy dane względem daty
    sorted_data = sorted(data, key=lambda x: datetime.strptime(x.date, "%Y-%m-%d %H:%M:%S"))

    # Pobieramy najniższą i najwyższą wartość low_price z okresu
    low_price_values = [row.low_price for row in sorted_data]
    high_price_values = [row.high_price for row in sorted_data]

    min_low_price = min(low_price_values)
    max_high_price = max(high_price_values)

    # Obliczamy różnicę między najniższą a najwyższą ceną
    price_span = max_high_price - min_low_price
    perc_price_span = ((max_high_price - min_low_price) / max_high_price) *100
    # Pobieramy wartość open_price na początku okresu i close_price na końcu okresu
    open_price = sorted_data[0].open_price
    close_price = sorted_data[-1].close_price

    # Obliczamy procentową różnicę między close_price a open_price
    percentage_change = ((close_price - open_price) / open_price) * 100

    return {
        "min_low_price": min_low_price,
        "max_high_price": max_high_price,
        "price_span": price_span,
        "perc_price_span": perc_price_span,
        "open_price": open_price,
        "close_price": close_price,
        "percentage_change": percentage_change
    }
