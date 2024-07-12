"""
Задача №1
Задача №2
Нужно написать функцию, которая на вход принимает список блюд из cook_book и количество персон
для кого мы будем готовить

get_shop_list_by_dishes(dishes, person_count)
На выходе мы должны получить словарь с названием ингредиентов и его количества для блюда. Например,
для такого вызова

get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2)
Должен быть следующий результат:

{
  'Картофель': {'measure': 'кг', 'quantity': 2},
  'Молоко': {'measure': 'мл', 'quantity': 200},
  'Помидор': {'measure': 'шт', 'quantity': 4},
  'Сыр гауда': {'measure': 'г', 'quantity': 200},
  'Яйцо': {'measure': 'шт', 'quantity': 4},
  'Чеснок': {'measure': 'зубч', 'quantity': 6}
}
Обратите внимание, что ингредиенты могут повторяться
"""
from pprint import pprint


def reading_recipes() -> dict:
    """
    Считывает рецепты из файла и добавляет в словарь
    """
    cook_book = {}

    with open('recipes.txt', encoding='UTF-8') as file:
        dish_name = None
        for line in file:
            line = line.strip().split('|')
            if not line[0].isdigit() and line[0]:

                if len(line) == 1:
                    dish_name = line[0]
                    cook_book[dish_name] = []
                else:
                    ingredient, quantity, measure = line
                    cook_book[dish_name].append({
                        'ingredient_name': ingredient.strip(),
                        'quantity': int(quantity),
                        'measure': measure.strip()
                    })

    return cook_book


def get_shop_list_by_dishes(dishes: list, person_count: int):
    """
    Подготавливает количество ингредиентов для приготовления заказа
    :param dishes:
    :param person_count:
    """
    cook_book = reading_recipes()
    order = {}

    for name in dishes:
        ingredient_list = cook_book[name]
        for dict_ing in ingredient_list:
            ingredient_name = dict_ing['ingredient_name']
            measure = dict_ing['measure']
            quantity = dict_ing['quantity']
            if ingredient_name not in order:
                order[ingredient_name] = {'measure': measure, 'quantity': quantity * person_count}
            else:
                update_quantity = quantity * person_count + order[ingredient_name]['quantity']
                order[ingredient_name]['quantity'] = update_quantity
    pprint(order)


if __name__ == '__main__':
    get_shop_list_by_dishes(['Фахитос', 'Омлет'], 3)
