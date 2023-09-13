from flask import Flask, render_template, request
from datetime import datetime, timedelta
from db_handler import db, CryptoData
from data_loader import DataLoader
from candlestick_chart import generate_candlestick_chart

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'  # Ustaw bazę danych SQLite
db.init_app(app)

with app.app_context():
    db.create_all()

# Lista dostępnych symboli kryptowalut
crypto_symbols = ['BTC', 'ETH', 'LTC', 'XRP', 'SOL']


def is_data_up_to_date(symbol):
    return CryptoData.is_data_current(symbol)


@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    analysis_result = None
    candlestick_fig = None
    chart_message = None
    symbol = None
    start_datetime = None
    end_datetime = None
    if request.method == 'POST':
        symbol = request.form['symbol']
        symbol = symbol + 'USDT'
        start_date = request.form['start_date']
        start_time = request.form['start_time']
        end_date = request.form['end_date']
        end_time = request.form['end_time']

        start_datetime = datetime.strptime(start_date + " " + start_time, '%Y-%m-%d %H:%M')
        end_datetime = datetime.strptime(end_date + " " + end_time, '%Y-%m-%d %H:%M')
        first_date = datetime.strptime('2023-01-01 00:00', '%Y-%m-%d %H:%M')
        last_date = (datetime.now() - timedelta(days=2)).replace(hour=23, minute=59, second=59)
        last_date = datetime.strftime(last_date, '%Y-%m-%d %H:%M:%S')
        if start_datetime > end_datetime:
            start_datetime, end_datetime = end_datetime, start_datetime
        elif start_datetime == end_datetime:
            message = "Daty i godziny początkowa i końcowa są sobie równe. Spróbuj ponownie."
        elif start_datetime < first_date or end_datetime > last_date:
            message = f"Minimalna i maksymalna data analizy to: {first_date} - {last_date}" \
                      f"Zmień wprowadzone daty."
        else:
            if is_data_up_to_date(symbol):
                message = f"Dane w bazie danych dla {symbol} są aktualne."
            else:
                last_date_in_db = CryptoData.get_latest_date(symbol)
                if last_date_in_db is not None and end_datetime <= last_date_in_db:
                    message = f"Wczytuję dane z bazy danych dla {symbol}"
                else:
                    url = f"https://www.cryptodatadownload.com/cdd/Binance_{symbol}_2023_minute.csv"
                    data_to_add = DataLoader.download_data_from_url(url)
                    if data_to_add:
                        if last_date_in_db is None:
                            filtered_data = data_to_add
                        else:
                            filtered_data = DataLoader.filter_data_by_date(data_to_add, last_date_in_db)
                        if filtered_data:
                            CryptoData.add_data_from_list(filtered_data)
                            message = f"Dane w bazie danych dla {symbol} zostały zaktualizowane."
                        else:
                            message = f"Brak nowszych danych do zaimportowania dla {symbol}."
                    else:
                        message = "Błąd podczas pobierania danych z URL."

            analysis_result = CryptoData.analyze_data_between_dates(symbol, start_datetime, end_datetime)
            # Generowanie wykresu świeczkowego
            analysis_period = end_datetime - start_datetime
            analysis_period = analysis_period.days
            if analysis_period > 31:
                # Wyświetl informację o ograniczeniu
                chart_message = "Wykres dostępny dla interwałów nie dłuższych niż 31 dni."
                candlestick_fig = None  # wartość None, aby nie generować wykresu
            else:
                candlestick_fig = generate_candlestick_chart(CryptoData.get_data_between_dates(symbol, start_datetime,
                                                                                               end_datetime), symbol)

    return render_template('index.html', crypto_symbols=crypto_symbols, message=message,
                           analysis_result=analysis_result, chart_message=chart_message,
                           candlestick_fig=candlestick_fig, symbol=symbol, analysis_period=f"{start_datetime} - {end_datetime}")


if __name__ == '__main__':
    #with app.app_context():
    #    db.create_all()
    app.run(debug=True)

