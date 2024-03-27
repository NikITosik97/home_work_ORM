import sqlalchemy
import json

from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
from config import CONNECTION_DRIVER, LOGIN, PASSWORD, SERVER_NAME, PORT, NAME_BD

DSN = f'{CONNECTION_DRIVER}://{LOGIN}:{PASSWORD}@{SERVER_NAME}:{PORT}/{NAME_BD}'

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# with open('tests_data.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# for record in data:
#     model = {
#         'publisher': Publisher,
#         'shop': Shop,
#         'book': Book,
#         'stock': Stock,
#         'sale': Sale,
#     }[record.get('model')]
#     session.add(model(**record.get('fields')))
# session.commit()


def find_id_by_name_publisher(name):
    result = session.query(Publisher.id_publisher).filter(Publisher.name == name).all()
    return result[0][0]


def get_data():
    data = input('Enter id or name publisher: ')
    id_publisher = int(data) if data.isdigit() else find_id_by_name_publisher(data)
    result = (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).
              join(Stock, Book.id_book == Stock.id_book).
              join(Shop, Stock.id_shop == Shop.id_shop).
              join(Sale, Stock.id_stock == Sale.id_stock).
              filter(Book.id_publisher == id_publisher)).all()

    for results in result:
        title, shop_name, price, date = results
        print(f"{title} | {shop_name} | {price} | {date}")
    session.commit()


if __name__ == '__main__':
    get_data()