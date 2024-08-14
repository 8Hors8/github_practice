"""
Модуль для подключение к бд
"""

import re
import psycopg2
from psycopg2 import sql
from config import DB_PATH


class Database:
    """
    Класс для управления подключением и операциями с базой данных.
    """

    def __init__(self, dbname=DB_PATH['dbname'], user=DB_PATH['user'], password=DB_PATH['password'], host='localhost',
                 port=5432):
        """
        Инициализация соединения с базой данных.

        :param dbname: Имя базы данных.
        :param user: Имя пользователя базы данных.
        :param password: Пароль пользователя базы данных.
        :param host: Хост базы данных (по умолчанию 'localhost').
        :param port: Порт базы данных (по умолчанию 5432).
        """
        self.conn = None
        self.cur = None
        try:
            self.conn = psycopg2.connect(dbname=dbname, user=user,
                                         password=password, host=host, port=port)
            self.cur = self.conn.cursor()
            print(f"Соединение с {dbname} успешно")
        except psycopg2.OperationalError:
            print(f"Ошибка подключения к {dbname}")

    def __del__(self):
        """Закрытие соединения и курсора при уничтожении объекта."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def create_table(self, table_name: str, columns: list):
        """
        Создание таблицы в базе данных.

        :param table_name: Имя таблицы.
        :param columns: Список столбцов и их типов
        в формате [('название_столбца', 'тип_данных'), ...].
        """
        try:
            columns_str = ', '.join(f'{col[0]} {col[1]}' for col in columns)
            query = sql.SQL(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
            self.cur.execute(query)
            self.conn.commit()
            print(f"Таблица {table_name} успешно создана")
        except psycopg2.DatabaseError as e:
            print(f"Ошибка при создании таблицы {table_name}: {e}")

    def drop_table(self, table_name: str):
        """
        Удаление таблицы из базы данных.

        :param table_name: Имя таблицы.
        """
        try:
            query = sql.SQL(f"DROP TABLE IF EXISTS {table_name}")
            self.cur.execute(query)
            self.conn.commit()
            print(f'Таблица успешно удалена {table_name}')
        except psycopg2.DatabaseError as e:
            print(f"Ошибка при удалении таблицы {table_name}: {e}")

    def insert_data(self, table_name, data):
        """
        Вставка данных в таблицу.

        :param table_name: Имя таблицы.
        :param data: Словарь с данными для вставки
        в формате {'column1': value1, 'column2': value2, ...}.
        :return: ID вставленной записи.
        """
        try:
            columns = data.keys()
            values = data.values()
            query = sql.SQL(
                f"INSERT INTO {table_name} ({', '.join(columns)})"
                f" VALUES ({', '.join(['%s'] * len(values))}) RETURNING id"
            )
            self.cur.execute(query, list(values))
            inserted_id = self.cur.fetchone()[0]
            self.conn.commit()
            return inserted_id
        except psycopg2.DatabaseError as e:
            print(f"Ошибка при вставке данных в таблицу {table_name}: {e}")
            return None


if __name__ == '__main__':
    r = Database()