"""
    Этот модуль предназначен для форматирования и объединения контактных данных,
    загруженных из CSV файла.
    Он обеспечивает обработку строк, разделение полных имен, приведение телефонных
    номеров к единому формату, а также объединение данных для устранения дубликатов.

    format_data(): Основная функция для форматирования данных и их сохранения обратно в CSV файл.

    format_phone(phone): Функция для форматирования телефонного номера в стандартный вид.

    merge_contacts(data): Функция для объединения контактов на основе совпадения фамилии и имени,
    при этом дополняя данные, если они присутствуют в других записях.
"""
import re
import read_save_csv


def format_data():
    """
        Форматирует и объединяет контактные данные, загруженные из CSV файла,
        приводя их к единому виду и удаляя дубликаты.

        Функция:
        1. Загружает данные из CSV файла с помощью функции `read_csv`.
        2. Форматирует каждый контакт:
           - Разделяет полное имя на составляющие (фамилия, имя, отчество).
           - Приводит номер телефона к единому формату.
        3. Удаляет дубликаты контактов, объединяя данные для записей с
        одинаковыми фамилией и именем.
        4. Сохраняет отформатированные данные обратно в CSV файл с помощью функции `seve_csv`.
    """

    contact_list = read_save_csv.read_csv()
    correct_contacts = []
    for cotat in contact_list[1:]:
        format_correct_contacts = []
        full_name_flag = 0
        for index, el in enumerate(cotat):

            if index <= 2:
                list_text = el.split()
                full_name_flag += len(list_text)
                if full_name_flag <= index and not el:
                    format_correct_contacts.append(el)
                else:
                    format_correct_contacts.extend(list_text)

            elif index == 3:
                format_correct_contacts.append(el)

            elif index == 4:
                format_correct_contacts.append(el)

            elif index == 5:
                result = format_phone(el)
                format_correct_contacts.append(result)

            elif index == 6:
                format_correct_contacts.append(el)
            else:
                pass

        correct_contacts.append(format_correct_contacts)

    data_to_write = merge_contacts(correct_contacts)
    data_to_write = contact_list[:1] + data_to_write
    read_save_csv.save_csv(data_to_write)


def format_phone(phone):
    """
        Приводит номер телефона к единому формату.

        Форматы:
        - 11 цифр: +7 (999) 999-99-99
        - 15 цифр: +7 (999) 999-99-99 доб.9999

        Аргументы:
        phone (str): Телефонный номер в произвольном формате.

        Возвращает:
        str: Отформатированный телефонный номер или сообщение об ошибке в случае неверного формата.
    """
    digits = re.sub(r'\D', '', phone)
    if digits:
        if len(digits) == 11:
            formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        elif len(digits) == 15:
            formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]} доб.{digits[11:]}"
        else:
            return "Неверный формат номера"
    else:
        return ''
    return formatted


def merge_contacts(data):
    """
        Объединяет записи контактов на основе совпадения фамилии и имени.

        Аргументы:
        data (list): Список списков, где каждый вложенный список представляет собой запись контакта.

        Возвращает:
        list: Список объединенных и уникальных записей контактов.
    """
    merged_data = {}

    for row in data:
        # Ключ состоит из фамилии и имени
        key = (row[0], row[1])

        if key not in merged_data:
            # Если такой записи еще нет, добавляем её
            merged_data[key] = row
        else:
            # Объединение данных: если элемент пустой, заменяем его на непустой из текущей строки
            for i in range(2, len(row)):
                if not merged_data[key][i]:
                    merged_data[key][i] = row[i]

    # Преобразование словаря обратно в список
    return list(merged_data.values())


if __name__ == '__main__':
    format_data()
