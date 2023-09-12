from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()


class CryptoData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    open_price = db.Column(db.Float, nullable=False)
    low_price = db.Column(db.Float, nullable=False)
    high_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)

    @classmethod
    def get_latest_date(cls, symbol):
        latest_date = cls.query.filter_by(symbol=symbol).order_by(cls.date.desc()).first()
        return latest_date.date if latest_date else None

    @classmethod
    def is_data_current(cls, symbol):
        latest_date = cls.get_latest_date(symbol)

        if latest_date:
            # Oblicz datę i godzinę dniu przedwczorajszemu o 23:59
            day_before_yesterday = datetime.now() - timedelta(days=2)
            day_before_yesterday = day_before_yesterday.replace(hour=23, minute=59, second=59)

            return latest_date >= day_before_yesterday
        else:
            return False

    @classmethod
    def add_data_from_list(cls, data_list):
        for item in data_list:
            symbol = item['symbol']
            date = datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S')
            open_price = item['open_price']
            low_price = item['low_price']
            high_price = item['high_price']
            close_price = item['close_price']

            crypto_data = cls(
                symbol=symbol,
                date=date,
                open_price=open_price,
                low_price=low_price,
                high_price=high_price,
                close_price=close_price
            )
            db.session.add(crypto_data)

        db.session.commit()

    @classmethod
    def get_data_between_dates(cls, symbol, start_date, end_date):
        data = cls.query.filter_by(symbol=symbol).filter(
            cls.date >= start_date
        ).filter(
            cls.date <= end_date
        ).order_by(cls.date.asc()).all()
        # print(data)
        return data

    @classmethod
    def analyze_data_between_dates(cls, symbol, start_date, end_date):
        data = cls.get_data_between_dates(symbol=symbol, start_date=start_date, end_date=end_date)
        if not data:
            return None
        # data = sorted(data, key=lambda x: datetime.strptime(x.date, "%Y-%m-%d %H:%M:%S"))
        min_low_price = min(item.low_price for item in data)
        max_high_price = max(item.high_price for item in data)
        price_span = max_high_price - min_low_price

        open_price = data[0].open_price
        close_price = data[-1].close_price

        percentage_price_span = (price_span / min_low_price) * 100
        percentage_change = ((close_price - open_price) / open_price) * 100

        return {
            'min_low_price': min_low_price,
            'max_high_price': max_high_price,
            'price_span': price_span,
            'percentage_price_span': percentage_price_span,
            'open_price': open_price,
            'close_price': close_price,
            'percentage_change': percentage_change
        }
