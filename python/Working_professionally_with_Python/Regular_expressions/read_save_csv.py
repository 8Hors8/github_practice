"""
    Этот файл предназначен для работы с данными в CSV формате, содержащими информацию о контактах.
    Функции модуля позволяют загружать данные из CSV файла и сохранять их после обработки.

    read_csv(): Функция читает данные из файла phonebook_raw.csv и возвращает
    их в виде списка списков.

    seve_csv(contacts_list): Функция сохраняет обработанные данные контактов в файл phonebook.csv.
"""

import csv
from pprint import pprint


def read_csv():
    """
        Читает данные из CSV файла и возвращает их в виде списка списков.

        Возвращает:
        list: Список списков, где каждый вложенный список представляет собой
        строку данных из CSV файла.
    """
    contacts_list = []
    with open('phonebook_raw.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            contacts_list.append(row)
    return contacts_list


def save_csv(contacts_list):
    """
        Сохраняет список контактов в CSV файл.

        Аргументы:
        contacts_list (list): Список списков, где каждый вложенный список
        представляет собой запись контакта для сохранения в CSV файл.
    """

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    pprint(read_csv())
