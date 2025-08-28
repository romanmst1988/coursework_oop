import json
from typing import List, Dict, Any
from src.abstract_file_handler import AbstractFileHandler
from src.vacancy import Vacancy


class JSONFileHandler(AbstractFileHandler):
    """Класс для работы с JSON-файлами."""

    def __init__(self, filename: str = "vacancies.json") -> None:
        self.__filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в файл."""
        data = self._load_data()
        vacancy_dict = {
            "title": vacancy.title,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description,
            "requirements": vacancy.requirements,
        }
        if vacancy_dict not in data:
            data.append(vacancy_dict)
            self._save_data(data)

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Vacancy]:
        """Получение вакансий по критериям."""
        data = self._load_data()
        filtered_data = [
            item for item in data if all(item.get(k) == v for k, v in criteria.items())
        ]
        return [Vacancy(**item) for item in filtered_data]

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из файла."""
        data = self._load_data()
        vacancy_dict = {
            "title": vacancy.title,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description,
            "requirements": vacancy.requirements,
        }
        if vacancy_dict in data:
            data.remove(vacancy_dict)
            self._save_data(data)

    def _load_data(self) -> List[Dict[str, Any]]:
        """Загрузка данных из файла."""
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self, data: List[Dict[str, Any]]) -> None:
        """Сохранение данных в файл."""
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
