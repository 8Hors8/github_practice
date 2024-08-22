def calculate_salary(hours_worked, hourly_rate, bonus=0):
    """
    Рассчитывает заработную плату сотрудника на основе отработанных часов,
    почасовой ставки и бонуса.

    Args:
        hours_worked (float): Количество отработанных часов.
        hourly_rate (float): Почасовая ставка сотрудника.
        bonus (float, optional): Бонус, который будет добавлен к зарплате. По умолчанию 0.

    Returns:
        float: Рассчитанная заработная плата.
    """
    base_salary = hours_worked * hourly_rate
    total_salary = base_salary + (base_salary * bonus)
    return total_salary
