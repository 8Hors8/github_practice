def get_employees():
    """
    Возвращает список сотрудников в виде списка словарей.

    Returns:
        list: Список словарей, представляющих сотрудников.
    """
    employees = [
        {'id': 1, 'name': 'John Doe', 'hours_worked': 160, 'hourly_rate': 20 },
        {'id': 2, 'name': 'Jane Smith', 'hours_worked': 120, 'hourly_rate': 28 },
        {'id': 3, 'name': 'Bob Johnson', 'hours_worked': 200, 'hourly_rate': 30}
    ]

    return employees
