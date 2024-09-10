from typing import List, Union, Dict
from statistics import mode


def discriminant(a: int, b: int, c: int) -> int:
    """
    Вычисляет дискриминант квадратного уравнения.

    Дискриминант вычисляется по формуле D = b^2 - 4ac. Это значение помогает определить
    количество и тип корней квадратного уравнения.

    :param a: Коэффициент при x^2 в квадратном уравнении.
    :param b: Коэффициент при x в квадратном уравнении.
    :param c: Свободный член в квадратном уравнении.
    :return: Значение дискриминанта уравнения.
    """
    D = b ** 2 - 4 * a * c
    return D


def solution(a: int, b: int, c: int) -> Union[str, float, tuple]:
    """
    Находит корни квадратного уравнения.

    Использует дискриминант для определения корней уравнения ax^2 + bx + c = 0.
    Возвращает строку, если корней нет, либо одно число, если есть один корень,
    либо кортеж из двух чисел, если есть два корня.

    :param a: Коэффициент при x^2 в квадратном уравнении.
    :param b: Коэффициент при x в квадратном уравнении.
    :param c: Свободный член в квадратном уравнении.
    :return: Корень уравнения или сообщение о том, что корней нет.
    """
    d = discriminant(a, b, c)
    if d < 0:
        return 'корней нет'
    elif d == 0:
        return -b / (2 * a)
    else:
        x1 = (-b + d ** 0.5) / (2 * a)
        x2 = (-b - d ** 0.5) / (2 * a)
        return x1, x2


def vote(votes: List[int]) -> int:
    """
    Находит наиболее частое значение в списке голосов.

    Использует функцию mode для определения наиболее часто встречающегося элемента
    в списке.

    :param votes: Список голосов, каждый из которых является целым числом.
    :return: Наиболее часто встречающееся целое число.
    """
    return mode(votes)


# Примеры документов и полок
documents: List[Dict[str, str]] = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
    {"type": "driver license", "number": "5455 028765", "name": "Василий Иванов"},
]

directories: Dict[str, List[str]] = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': []
}


def get_name(doc_number: str) -> str:
    """
    Ищет имя владельца документа по его номеру.

    :param doc_number: Номер документа.
    :return: Имя владельца документа, если документ найден; иначе сообщение об ошибке.
    """
    for doc in documents:
        if doc['number'] == doc_number:
            return doc['name']
    return 'Документ не найден'


def get_directory(doc_number: str) -> str:
    """
    Находит номер полки, на которой хранится документ по его номеру.

    :param doc_number: Номер документа.
    :return: Номер полки, где хранится документ, если документ найден; иначе сообщение об ошибке.
    """
    for key, vals in directories.items():
        if doc_number in vals:
            return f'Полка под номером {key}'
    return 'Полки с таким документом не найдено'


def add(document_type: str, number: str, name: str, shelf_number: int) -> str:
    """
    Добавляет новый документ в систему и помещает его на указанную полку.

    :param document_type: Тип документа (например, паспорт, страховка и т.д.).
    :param number: Номер документа.
    :param name: Имя владельца документа.
    :param shelf_number: Номер полки, на которую помещается документ.
    :return: Сообщение о том, что данные были успешно добавлены.
    """
    doc = {
        "type": document_type,
        "number": number,
        "name": name
    }
    documents.append(doc)
    if str(shelf_number) in directories:
        directories[str(shelf_number)].append(number)
    else:
        directories[str(shelf_number)] = [number]
    return 'Данные добавлены успешны'


if __name__ == '__main__':
    print(solution(1, 8, 15))
    print(solution(1, -13, 12))
    print(solution(-4, 28, -49))
    print(solution(1, 1, 1))

    print('-----')

    print(vote([1, 1, 1, 2, 3]))
    print(vote([1, 2, 3, 2, 2]))
    print(vote([1, 2, 3, 4, 5]))

    print('-----')

    print(get_name("10006"))
    print(get_directory("11-2"))
    print(get_name("101"))
    add('international passport', '311 020203', 'Александр Пушкин', 3)
    print(get_directory("311 020203"))
    print(get_name("311 020203"))
    print(get_directory("311 020204"))
