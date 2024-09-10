import os
from dotenv import load_dotenv
import requests

load_dotenv()

token = os.getenv("TOKEN_YND")

if token:
    print("Токен успешно загружен:", token)
else:
    print("Токен не найден!")


class YandexDiskApi:
    """
    Класс для работы с API Яндекс.Диска для загрузки фотографий.
    Attributes:
        token (str): Токен OAuth для доступа к API Яндекс.Диска.
        name_folder (str or None): Название папки на Яндекс.Диске,
         куда будут загружаться фотографии.
    """

    def __init__(self, token_yandex: str):
        """
        Инициализация объекта класса YandexDiskApi.

        Args:
            token_yandex (str): Токен OAuth для доступа к API Яндекс.Диска.
        """
        self.token = token_yandex
        self.name_folder = None

    def _common_headers(self):
        """
        Формирует общие заголовки для запросов к API Яндекс.Диска.

        Returns:
            dict: Словарь с заголовками HTTP запроса.
        """

        headers = {
            "Authorization": f'OAuth {self.token}'
        }
        return headers

    def _request_folder_name(self):
        """
        Запрашивает у пользователя название папки для создания на Яндекс.Диске.

        Returns:
            str: Название папки, введенное пользователем или значение по умолчанию "image".
        """
        reply = input('Ведите название папки ---> ')
        self.name_folder = reply if reply else "image"
        return self.name_folder

    def creating_folder(self):
        """
        Создает папку на Яндекс.Диске с указанным именем или использует имя по умолчанию.

        Raises:
            ValueError: Если возникает ошибка создания папки.

        Notes:
            Использует API endpoint для создания ресурсов на Яндекс.Диске.
        """
        print("Введите имя папки, которую вы хотите создать, "
              "или нажмите Enter для использования имени по умолчанию 'image'.")

        url = "https://cloud-api.yandex.net/v1/disk/resources"
        name_folder = self.name_folder if self.name_folder is not None \
            else self._request_folder_name()
        params = {
            "path": f'{name_folder}'
        }
        response = requests.put(url, headers=self._common_headers(), params=params, timeout=5)

        if response.status_code == 201:
            answer = f"Папка '{self.name_folder}' успешно создана."
        elif response.status_code == 409:
            answer = f"Папка '{self.name_folder}' уже существует."
        else:
            answer = f"Неожиданный код состояния: {response.status_code}"
        return answer


if __name__ == '__main__':
    r = YandexDiskApi(token)
    print(r.creating_folder())
