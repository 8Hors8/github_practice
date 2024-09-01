

"""Задание 1"""
class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.main_list_index = 0
        self.nested_list_index = 0


    def __iter__(self):
        return self

    def __next__(self):
        while self.main_list_index < len(self.list_of_list):
            current_elem = self.list_of_list[self.main_list_index]

            if isinstance(current_elem, list):

                if self.nested_list_index < len(current_elem):
                    item = current_elem[self.nested_list_index]
                    self.nested_list_index += 1
                    return item

                else:
                    self.main_list_index += 1
                    self.nested_list_index = 0

            else:
                item = current_elem
                self.main_list_index += 1
                self.nested_list_index = 0
                return item

        raise StopIteration


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f',
                                                   'h', False, 1, 2, None]
    print("Тест 1 выполнен успешно")

"""Задание 2"""

import types


def flat_generator(list_of_lists):

    for sublist in list_of_lists:
        for item in sublist:
            yield item


def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)
    print("Тест 2 выполнен успешно")

"""Задание 3"""
def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    print("Тест 3 выполнен успешно")


if __name__ == '__main__':
    test_1()
    test_2()
    # test_3()