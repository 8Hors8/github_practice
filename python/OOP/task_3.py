"""
Задача №3
В папке лежит некоторое количество файлов. Считайте, что их количество и имена вам заранее
известны, пример для выполнения домашней работы можно взять тут

Необходимо объединить их в один по следующим правилам:

Содержимое исходных файлов в результирующем файле должно быть отсортировано по количеству
строк в них (то есть первым нужно записать файл с наименьшим количеством строк,
 а последним - с наибольшим)
Содержимое файла должно предваряться служебной информацией на 2-х строках:
имя файла и количество строк в нем
"""


def open_faile(failes: list):
    """
    Собирает информацию о фале и сортирует по количеству строк
    :param failes:
    :return:
    """
    file_data = []
    for name in failes:
        with open(name, encoding='UTF-8') as file:
            data = file.read()
            number_lines = len(data.strip().split('\n'))
            file_data.append([name, number_lines, data])

    sorted_list = sorted(file_data, key=lambda x: x[1])
    return sorted_list


def merging_into_file(list_sorted: list):
    """
    Формирует текст и записывает в файл
    :param list_sorted:
    """
    text = ''
    for el in list_sorted:
        text += ''.join(f'\n{el[0]}\n{el[1]}\n{el[2]}\n')

    with open('output.txt', 'w', encoding='UTF-8') as file:
        file.write(text)


if __name__ == '__main__':
    list_ = open_faile(['1.txt', '2.txt', '3.txt'])
    merging_into_file(list_)
