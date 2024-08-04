import json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Publisher(Base):
    """
    Класс Publisher представляет модель таблицы 'publisher' в базе данных.
    Атрибуты:
        id (int): Уникальный идентификатор издателя.
        name (str): Название издательства.
        books (relationship): Связь с таблицей 'book'.

    """
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship('Book', back_populates='publisher')


class Book(Base):
    """
    Класс Book представляет модель таблицы 'book' в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор книги.
        title (str): Название книги.
        id_publisher (int): Идентификатор издателя, связанного с книгой.
        publisher (relationship): Связь с таблицей 'publisher'.
        stocks (relationship): Связь с таблицей 'stock'.
    """
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)

    publisher = relationship('Publisher', back_populates='books')
    stocks = relationship('Stock', back_populates='book')


class Shop(Base):
    """
    Класс Shop представляет модель таблицы 'shop' в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор магазина.
        name (str): Название магазина.
        stocks (relationship): Связь с таблицей 'stock'.
    """
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    stocks = relationship('Stock', back_populates='shop')


class Stock(Base):
    """
    Класс Stock представляет модель таблицы 'stock' в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор записи на складе.
        id_book (int): Идентификатор книги.
        id_shop (int): Идентификатор магазина.
        count (int): Количество книг на складе.
        book (relationship): Связь с таблицей 'book'.
        shop (relationship): Связь с таблицей 'shop'.
        sales (relationship): Связь с таблицей 'sale'.
    """
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False)

    book = relationship('Book', back_populates='stocks')
    shop = relationship('Shop', back_populates='stocks')
    sales = relationship('Sale', back_populates='stock')


class Sale(Base):
    """
    Класс Sale представляет модель таблицы 'sale' в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор продажи.
        price (float): Стоимость продажи.
        date_sale (date): Дата продажи.
        id_stock (int): Идентификатор записи на складе.
        count (int): Количество проданных книг.
        stock (relationship): Связь с таблицей 'stock'.
    """
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    date_sale = Column(Date, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=False)

    stock = relationship('Stock', back_populates='sales')


login = 'postgres'
password = '1234'
db_name = 'db_homework'
DSN = f'postgresql://{login}:{password}@localhost:5432/{db_name}'
engine = create_engine(DSN)


def create_table(engine_db):
    """
    Создает таблицы в БД
    :param engine_db: Экземпляр движка базы данных.
    """
    Base.metadata.create_all(engine_db)


def drop_table(engine_db):
    """
    Удаляет таблицы в БД
    :param engine_db: Экземпляр движка базы данных.
    """
    Base.metadata.drop_all(engine_db)


Session = sessionmaker(bind=engine)
session = Session()


def data_recording(path: str, session_db):
    """
    Загружает данные из JSON файла и сохраняет их в базе данных.

    :param path: Путь к JSON файлу с данными.
    :param session_db: Сессия базы данных для записи данных.
    """
    with open(path, 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session_db.add(model(id=record.get('pk'), **record.get('fields')))
    session_db.commit()


def search(param):
    """
    Поиск и вывод информации о покупках книг издателя по имени или идентификатору.

    :param param: Имя или идентификатор издателя.
    """
    try:

        param = int(param)
        publisher = session.query(Publisher).filter(Publisher.id == param).first()

    except ValueError:
        publisher = session.query(Publisher).filter(Publisher.name == param).first()

    if publisher:
        books = session.query(Book).filter(Book.id_publisher == publisher.id).all()

        for book in books:
            stocks = session.query(Stock).filter(Stock.id_book == book.id).all()

            for stock in stocks:
                sales = session.query(Sale).filter(Sale.id_stock == stock.id).all()

                for sale in sales:
                    shop = session.query(Shop).filter(Shop.id == stock.id_shop).first()
                    print(
                        f"Книга: {book.title} | Магазин: {shop.name} | Цена: {sale.price} | Дата продажи: {sale.date_sale}")
    else:
        print(f"Издатель с параметром '{param}' не найден.")


# data_recording('tests_data.json', session)


search('1')
