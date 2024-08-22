import datetime
import random
import application.salary as salary
import application.db.people as people


def get_current_date():
    """
    Возвращает текущую дату в формате строки.

    Returns:
        str: Текущая дата в формате 'YYYY-MM-DD'.
    """
    current_date = datetime.date.today()
    return str(current_date)


if __name__ == '__main__':
    employees = people.get_employees()
    for employee in employees:
        bonus = random.uniform(0, 1)
        salary_employee = salary.calculate_salary(hours_worked=employee['hours_worked'],
                                                  hourly_rate=employee['hourly_rate'],
                                                  bonus=bonus
                                                  )
        print(get_current_date(),employee['name'],f'salary:{salary_employee:.2f}')
