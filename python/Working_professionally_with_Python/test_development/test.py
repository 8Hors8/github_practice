import unittest
import requests

from unittest.mock import patch, MagicMock
from python.Working_professionally_with_Python.test_development.task_1 import discriminant, \
    solution, vote, get_name, get_directory, add
from python.Working_professionally_with_Python.test_development.task_2 import YandexDiskApi


class TestDiscriminant(unittest.TestCase):
    """Тесты для функции discriminant"""

    def test_discriminant_values(self):
        """Тест дискриминанта для различных значений"""
        self.assertEqual(discriminant(1, 8, 15), 4)
        self.assertEqual(discriminant(1, -13, 12), 121)
        self.assertEqual(discriminant(-4, 28, -49), 0)
        self.assertEqual(discriminant(1, 1, 1), -3)


class TestSolution(unittest.TestCase):
    """Тесты для функции solution"""

    def test_solution_two_roots(self):
        """Тест решения уравнения с двумя корнями"""
        self.assertEqual(solution(1, 8, 15), (-3.0, -5.0))
        self.assertEqual(solution(1, -13, 12), (12.0, 1.0))

    def test_solution_one_root(self):
        """Тест решения уравнения с одним корнем"""
        self.assertEqual(solution(-4, 28, -49), 3.5)

    def test_solution_no_roots(self):
        """Тест решения уравнения без корней"""
        self.assertEqual(solution(1, 1, 1), 'корней нет')


class TestVote(unittest.TestCase):
    """Тесты для функции vote"""

    def test_vote_most_frequent_number(self):
        """Тест на нахождение наиболее частого числа"""
        self.assertEqual(vote([1, 1, 1, 2, 3]), 1)
        self.assertEqual(vote([1, 2, 3, 2, 2]), 2)
        self.assertEqual(vote([1, 2, 3, 3, 3]), 3)


class TestDocuments(unittest.TestCase):
    """Тесты для функций работы с документами"""

    def test_get_name_existing_document(self):
        """Тест на успешный поиск имени по номеру документа"""
        self.assertEqual(get_name("10006"), 'Аристарх Павлов')
        self.assertEqual(get_name("11-2"), 'Геннадий Покемонов')
        self.assertEqual(get_name("2207 876234"), 'Василий Гупкин')

    def test_get_name_non_existing_document(self):
        """Тест на неуспешный поиск имени по номеру документа"""
        self.assertEqual(get_name("11"), 'Документ не найден')


class TestDirectories(unittest.TestCase):
    """Тесты для функций работы с полками"""

    def test_get_directory_existing_document(self):
        """Тест на успешное нахождение полки по номеру документа"""
        self.assertEqual(get_directory("11-2"), 'Полка под номером 1')
        self.assertEqual(get_directory("10006"), 'Полка под номером 2')

    def test_get_directory_non_existing_document(self):
        """Тест на неуспешное нахождение полки по номеру документа"""
        self.assertEqual(get_directory("15"), 'Полки с таким документом не найдено')


class TestAddDocument(unittest.TestCase):
    """Тесты для функции add"""

    def test_add_document_success(self):
        """Тест на успешное добавление нового документа"""
        add('international passport', '311 020203', 'Александр Пушкин', 3)
        self.assertEqual(get_name("311 020203"), 'Александр Пушкин')
        self.assertEqual(get_directory("311 020203"), 'Полка под номером 3')


# Задание №2

class TestYandexDiskApi(unittest.TestCase):
    """Тесты для класса YandexDiskApi"""

    def setUp(self):
        """Подготовка к тестам, создание объекта API с тестовым токеном."""
        self.api = YandexDiskApi("test_token")

    def test_initialization(self):
        """Тест: проверка корректной инициализации объекта."""
        self.assertEqual(self.api.token, "test_token")
        self.assertIsNone(self.api.name_folder)

    def test_common_headers(self):
        """Тест: проверка правильности заголовков для запроса."""
        expected_headers = {"Authorization": "OAuth test_token"}
        self.assertEqual(self.api._common_headers(), expected_headers)

    @patch('builtins.input', return_value="test_folder")
    def test_request_folder_name(self, mock_input):
        """Тест: проверка запроса имени папки у пользователя."""
        folder_name = self.api._request_folder_name()
        self.assertEqual(folder_name, "test_folder")
        self.assertEqual(self.api.name_folder, "test_folder")

    @patch('builtins.input', return_value="")
    def test_request_folder_name_default(self, mock_input):
        """Тест: проверка использования имени по умолчанию, если имя не введено."""
        folder_name = self.api._request_folder_name()
        self.assertEqual(folder_name, "image")
        self.assertEqual(self.api.name_folder, "image")

    @patch('requests.put')
    @patch('builtins.input', return_value="test_folder")
    def test_creating_folder_success(self, mock_input, mock_put):
        """Тест: проверка успешного создания папки."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_put.return_value = mock_response

        result = self.api.creating_folder()
        self.assertEqual(result, "Папка 'test_folder' успешно создана.")

    @patch('requests.put')
    @patch('builtins.input', return_value="test_folder")
    def test_creating_folder_already_exists(self, mock_input, mock_put):
        """Тест: проверка случая, когда папка уже существует."""
        mock_response = MagicMock()
        mock_response.status_code = 409
        mock_put.return_value = mock_response

        result = self.api.creating_folder()
        self.assertEqual(result, "Папка 'test_folder' уже существует.")

    @patch('requests.put')
    @patch('builtins.input', return_value="test_folder")
    def test_creating_folder_unexpected_status(self, mock_input, mock_put):
        """Тест: проверка случая с неожиданным статусом ответа."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_put.return_value = mock_response

        result = self.api.creating_folder()
        self.assertEqual(result, "Неожиданный код состояния: 500")
