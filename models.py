import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publishers'

    id_publisher = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)

    def __str__(self):
        return f'{self.id_publisher}: {self.name}'


class Book(Base):
    __tablename__ = 'books'

    id_book = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publishers.id_publisher'), nullable=False)
    publishers = relationship('Publisher', backref='publishers')

    def __str__(self):
        return f'{self.title}'


class Shop(Base):
    __tablename__ = 'shops'

    id_shop = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)


class Stock(Base):
    __tablename__ = 'stocks'

    id_stock = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('books.id_book'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shops.id_shop'), nullable=False)
    count = sq.Column(sq.Integer)
    books = relationship(Book, backref='books')
    shops = relationship(Shop, backref='shops')


class Sale(Base):
    __tablename__ = 'sales'

    id_sale = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stocks.id_stock'), nullable=False)
    count = sq.Column(sq.Integer)
    stocks = relationship(Stock, backref='stocks')


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
