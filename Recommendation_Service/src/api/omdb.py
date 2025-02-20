import requests
from typing import Optional, List

class OMDBApi:
    # Инициализация класса с передачей ключа API
    def init(self, api_key):
        self.api_key = api_key  # Сохранение ключа API
        self.url = "https://www.omdbapi.com"  # Базовый URL для API

    # Получение пути к постеру фильма по названию
    def _images_path(self, title: str) -> Optional[str]:
        params = {
            "apikey": self.api_key,  # Передача ключа API в параметры запроса
            "t": title,  # Название фильма для поиска
            "type": "movie"  # Тип запроса (фильм)
        }
        response = requests.get(self.url, params=params)  # Выполнение GET-запроса к API
        if response.status_code == 200:  # Проверка успешности запроса
            data = response.json()  # Преобразование ответа в JSON
            if 'Poster' in data:  # Проверка наличия постера в данных
                if data['Poster'] == 'N/A': # Проверка отсутствия данных постера
                    return None
                return data['Poster']  # Возврат URL постера
        return None

    # Получение постеров по списку названий фильмов
    def get_posters(self, titles: List[str]) -> List[str]:
        posters = []  # Список для хранения путей к постерам
        for title in titles:  # Итерация по названиям фильмов
            path = self._images_path(title)  # Получение пути к постеру
            if path:  # Если изображение существует
                posters.append(path)  # Добавление пути к постеру в список
       return posters
