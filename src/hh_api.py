from typing import Any, Dict, List

import requests

from src.abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API HeadHunter."""

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params: Dict[str, Any] = {"text": "", "page": 0, "per_page": 100}
        self.vacancies: List[Dict[str, Any]] = []

    def _connect_to_api(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Приватный метод для подключения к API."""
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Ошибка подключения к API: {response.status_code}")
        return response.json()

    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """Получение вакансий с hh.ru по поисковому запросу."""
        self.params["text"] = search_query
        self.params["page"] = 0
        self.vacancies.clear()

        while self.params["page"] < 20:  # Ограничение в 2000 вакансий
            data = self._connect_to_api(self.__url, self.params)
            self.vacancies.extend(data["items"])

            # Преобразуем page в int для сравнения
            current_page = int(self.params["page"])
            total_pages = int(data["pages"])

            if total_pages <= current_page:
                break

            # Увеличиваем page как число
            self.params["page"] = current_page + 1

        return self.vacancies
