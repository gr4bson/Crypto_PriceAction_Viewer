import os
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from datetime import datetime, timedelta
#import pandas as pd

class DbHandler:
    def __init__(self):
        instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'instance'))
        database_path = os.path.join(instance_path, 'crypto_prices.db')
        self.engine = create_engine('sqlite:///' + database_path)
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
        self.inspector = inspect(self.engine)

        class CryptoPrice(self.Base):
            __tablename__ = 'crypto_prices'

            id = Column(Integer, primary_key=True)
            symbol = Column(String)
            date = Column(String)
            open_price = Column(Float)
            high_price = Column(Float)
            low_price = Column(Float)
            close_price = Column(Float)

        self.CryptoPrice = CryptoPrice

    def check_table_exists(self, symbol):
        return self.inspector.has_table(symbol)

    def create_session(self):
        return self.Session()

    def close_session(self, session):
        session.close()

    def check_and_create_table(self, symbol):
        if not self.check_table_exists(symbol):
            print(f"Tabela o nazwie '{symbol}' nie istnieje, zostanie teraz utworzona.")
            self.CryptoPrice.__table__.name = symbol
            self.CryptoPrice.__table__.create(self.engine, checkfirst=True)
        else:
            print(f"Tabela o nazwie '{symbol}' istnieje.")

    def add_data_to_table(self, symbol, data):
        session = self.create_session()
        try:
            self.CryptoPrice.__table__.name = symbol  # Pobierz nazwę tabeli dla danego symbolu
            session.execute(self.CryptoPrice.__table__.insert(), data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.close_session(session)

    def get_most_recent_date(self, symbol):
        session = self.create_session()
        try:
            self.CryptoPrice.__table__.name = symbol
            most_recent_data = session.query(self.CryptoPrice.date).order_by(self.CryptoPrice.date.desc()).first()
            if most_recent_data:
                most_recent_date = most_recent_data[0]  # .datetime.strptime(most_recent_data.date, "%Y-%m-%d %H:%M")
                return most_recent_date
            else:
                return None
        finally:
            self.close_session(session)

    def is_data_fresh(self, symbol):
        most_recent_date = self.get_most_recent_date(symbol)
        if most_recent_date:
            day_before_yesterday = datetime.now() - timedelta(days=2)
            most_recent_date = datetime.strptime(most_recent_date, "%Y-%m-%d %H:%M:%S")
            return most_recent_date >= day_before_yesterday
        else:
            return False
