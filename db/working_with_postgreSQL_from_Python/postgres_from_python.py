import psycopg2
from psycopg2 import sql
import re


class Database:
    """
    Класс для управления подключением и операциями с базой данных.
    """

    def __init__(self, dbname, user, password, host='localhost', port=5432):
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

    def insert_phone(self, client_id, phone):
        """
        Вставка данных о телефоне клиента в таблицу phones.

        :param client_id: ID клиента в таблице clients.
        :param phone: Номер телефона клиента.
        """
        try:
            query = sql.SQL("INSERT INTO phones (client_id, phone) VALUES (%s, %s)")
            self.cur.execute(query, (client_id, phone))
            self.conn.commit()
            if phone != 'No phone':
                print(f"Номер телефона успешно добавлен для клиента с ID {client_id}")
        except psycopg2.DatabaseError as e:
            print(f"Ошибка при вставке номера телефона для клиента с ID {client_id}: {e}")

    def select_data(self, table_name, columns: str = '*', condition=None, values=None):
        """
        Выполнение SELECT-запроса.

        :param table_name: Имя таблицы.
        :param columns: Список столбцов для выборки, по умолчанию '*' - все столбцы.
        :param condition: Условие WHERE для фильтрации данных, строка SQL.
        :param values: Значения для подстановки в условие WHERE, кортеж.
        :return: Список кортежей с данными.
        """
        try:
            columns_str = ', '.join(columns) if isinstance(columns, list) else columns
            query = sql.SQL(f"SELECT {columns_str} FROM {table_name}")
            if condition:
                query += sql.SQL(f" WHERE {condition}")
            self.cur.execute(query, values)
            rows = self.cur.fetchall()
            return rows
        except psycopg2.DatabaseError as e:
            print(f"Ошибка при выполнении SELECT из таблицы {table_name}: {e}")
            return []

    def update_data(self, table_name, data, condition):
        """
        Обновление данных в таблице.

        :param table_name: Имя таблицы.
        :param data: Словарь с данными для обновления
        в формате {'column1': value1, 'column2': value2, ...}.
        :param condition: Условие для фильтрации строк для обновления в формате SQL WHERE.
        """
        try:
            set_clause = ', '.join(f"{key} = %s" for key in data.keys())
            query = sql.SQL(f"UPDATE {table_name} SET {set_clause} WHERE {condition}")
            self.cur.execute(query, list(data.values()))
            self.conn.commit()
            print("Данные успешно обновлены в таблице")
        except psycopg2.DatabaseError as e:
            print(f"Ошибка при обновлении данных в таблице {table_name}: {e}")

    def delete_phone(self, client_id: str):
        """
        Удаление телефона клиента из таблицы phones.

        :param client_id: ID клиента в таблице clients.
        """
        try:
            query = sql.SQL("DELETE FROM phones WHERE client_id = %s")
            self.cur.execute(query, client_id)
            self.conn.commit()
            print(f"Телефон  успешно удален для клиента с ID {client_id}")
        except psycopg2.DatabaseError as e:
            print(f"Ошибка при удалении телефона для клиента с ID {client_id}: {e}")

    def delete_client(self, client_id):
        """
        Удаление клиента из таблицы clients и связанных телефонов из таблицы phones.

        :param client_id: ID клиента для удаления.
        """
        try:
            # Удаление телефонов клиента
            query_phones = sql.SQL("DELETE FROM phones WHERE client_id = %s")
            self.cur.execute(query_phones, (client_id,))

            # Удаление клиента
            query_client = sql.SQL("DELETE FROM clients WHERE id = %s")
            self.cur.execute(query_client, (client_id,))

            self.conn.commit()
            print(f"Клиент с ID {client_id} успешно удален")
        except psycopg2.DatabaseError as e:
            print(f"Ошибка при удалении клиента с ID {client_id}: {e}")

    def search_clients(self, search_term: str):
        """
        Поиск клиентов по имени, фамилии или email .

        :param search_term: Строка для поиска.
        :return: Список клиентов, соответствующих критериям поиска.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            print("Поисковый запрос не может быть пустым и должен быть строкой.")
            return []

        condition = 'first_name ILIKE %s OR last_name ILIKE %s OR email ILIKE %s'
        search_term_pattern = f"%{search_term}%"

        try:
            columns = ['id', 'first_name', 'last_name', 'email']
            rows = self.select_data('clients', columns, condition=condition,
                                    values=(search_term_pattern, search_term_pattern, search_term_pattern))

            if rows:
                print(f"Найдено {len(rows)} клиента(ов):")
                for row in rows:
                    print(f"ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Email: {row[3]}")
                return rows
            else:
                print("Клиенты не найдены")
                return []
        except psycopg2.DatabaseError as e:
            print(f"Ошибка при поиске клиентов: {e}")
            return []

    def _is_valid_email(self, email):
        """
        Проверка корректности email адреса.

        :param email: Email адрес.
        :return: True, если email валидный, иначе False.
        """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))

    def _is_valid_phone(self, phone):
        """
        Проверка корректности номера телефона.

        :param phone: Номер телефона.
        :return: True, если номер телефона валидный, иначе False.
        """
        phone_regex = r'^(?:\+7|8)?\s*\(?\d{3}\)?\s*\d{3}[-\s]?\d{2}[-\s]?\d{2}$'
        phone_len = len(phone) if phone[0] != '+' else len(phone[1:])
        return phone_len == 11 and bool(re.match(phone_regex, phone))


class Client(Database):
    """
    Класс для управления клиентами.
    """

    def __init__(self, dbname: str, user: str, password: str):
        """
        Инициализация клиента базы данных.

        :param dbname: Имя базы данных.
        :param user: Имя пользователя базы данных.
        :param password: Пароль пользователя базы данных.
        """
        super().__init__(dbname, user, password)

    def client_data(self, first_name: str, last_name: str, email: str, phones: str = None):
        """
        Добавление данных о клиенте и его телефоне в базу данных.

        :param first_name: Имя клиента.
        :param last_name: Фамилия клиента.
        :param email: Email клиента.
        :param phones: Номер телефона клиента (опционально).
        Форматы ввода телефона: +7 (XXX) XXX-XX-XX, 8 (XXX) XXX-XX-XX, +7XXXXXXXXXX, 8XXXXXXXXXX
        """
        valid_email = self._is_valid_email(email)

        if valid_email:
            try:
                data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email
                }

                client_id = self.insert_data('clients', data)

                if phones:
                    phones_list = re.split(r'[ ,/;]', re.sub(r'[^\+\d\s]+', '', phones))
                    for phone in phones_list:
                        valid_phone = self._is_valid_phone(phone)
                        if client_id and valid_phone:
                            self.insert_phone(client_id, phone)
                        else:
                            print(f'Телефон - {phone}, не является валидным')
                else:
                    self.insert_phone(client_id, 'No phone')

            except psycopg2.DatabaseError as e:
                print(f"Ошибка при добавлении данных клиента: {e}")
        else:
            print(f'Email - {email}, не является валидным')


if __name__ == '__main__':
    # Создание структуры таблиц
    table_client = 'clients'
    columns_client = [
        ('id', 'SERIAL PRIMARY KEY'),
        ('first_name', 'VARCHAR(255) NOT NULL'),
        ('last_name', 'VARCHAR(255) NOT NULL'),
        ('email', 'VARCHAR(255) UNIQUE NOT NULL')
    ]

    table_phone = 'phones'
    columns_phone = [
        ('id', 'SERIAL PRIMARY KEY'),
        ('client_id', 'INTEGER NOT NULL'),
        ('phone', 'VARCHAR(20) DEFAULT NULL'),
        ('FOREIGN KEY (client_id)', 'REFERENCES clients (id) ON DELETE CASCADE')
    ]

    try:
        """Подключение к базе данных"""
        client_db = Client('db_homework', 'postgres', '1234')

        """Пример использования методов"""
        # client_db.create_table(table_client, columns_client)
        # client_db.create_table(table_phone, columns_phone)
        # client_db.drop_table('clients,phones')

        """Добавление данных о клиентах"""
        # client_db.client_data('Vanya', 'Pupkin', 'vanya.pupkin@example.com', '89137468815')
        # client_db.client_data('Masha', 'Ivanova', 'masha.ivanova@example.com', '8926/123/45/67')
        # client_db.client_data('Sasha', 'Petrov', 'sasha.petrov@example.com', '8(903)123-45-67')
        # client_db.client_data('Oleg', 'Sidorov', 'oleg.sidorov@example.com', '+79161234567')
        # client_db.client_data('Anna', 'Smirnova', 'anna.smirnova@example.com', '89351234567 8935123456')

        """Поиск клиентов"""
        # print(client_db.search_clients('oleg.sidorov@example.com'))

        """Удаление клиента"""
        # client_db.delete_client(4)

        """Удаление телефона"""
        # client_db.delete_phone('2')

        """Обновляем email клиента с ID 1"""
        data = {'email': 'newemail@example.com'}
        condition = 'id = %s'
        values = (1,)

        client_db.update_data('clients', data, condition % values)

    except Exception as exc:
        print('Ошибка', exc)
