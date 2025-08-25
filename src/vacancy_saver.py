import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from src.vacancy import Vacancy

logger = logging.getLogger(__name__)  # создаём логгер для модуля


class VacancySaver(ABC):
    """
    Абстрактный класс для работы с хранилищем вакансий.
    """

    @abstractmethod
    def add(self, vacancies: list[Vacancy]) -> None:  # последовательность вакансий
        """
        Добавить вакансии в хранилище.
        """
        pass

    @abstractmethod
    def get(self, criteria: dict) -> List[Vacancy]:
        """
        Получить вакансии по заданным критериям.
        """
        pass

    @abstractmethod
    def delete(self, vacancy: Vacancy) -> None:
        """
        Удалить вакансию из хранилища.
        """
        pass


class JSONSaver(VacancySaver):
    """
    Реализация VacancySaver, использующая JSON-файл для хранения вакансий.
    """

    def __init__(self, filename: str = "vacancies.json"):
        self._filename = Path(filename)

    def _load_file(self) -> List[Dict[str, Any]]:
        """
        Метод для загрузки данных из JSON файла.
        """
        if not self._filename.exists():
            # Файл отсутствует возвращаем пустой список
            return []

        with open(self._filename, "r", encoding="utf-8") as f:
            try:
                # Загружаем JSON в список словарей
                data = json.load(f)
                # Проверяем, что данные - это список, иначе возвращаем пустой список
                if not isinstance(data, list):
                    logger.warning(f"Данные в {self._filename} не являются списком. Возвращаем пустой список.")
                    return []
                return data
            except json.JSONDecodeError:
                # При ошибке чтения JSON возвращаем пустой список
                logger.error(f"Ошибка чтения JSON из файла {self._filename}. Возвращаем пустой список.")
                return []

    def _save_file(self, data: List[Dict[str, Any]]) -> None:
        """
        Метод для сохранения списка вакансий в JSON файл.
        """
        with open(self._filename, "w", encoding="utf-8") as f:
            # Записываем данные с отступами для удобства чтения
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Файл {self._filename} успешно сохранён. Всего вакансий: {len(data)}")

    def add(self, vacancies: list[Vacancy]) -> None:
        """
        Добавление вакансии в файл (дубликаты по url не записываются).
        """
        data = self._load_file()
        have_urls = [v["url"] for v in data]  # Уже сохранённые URL
        to_save = [v for v in vacancies if v.url not in have_urls]  # Только новые

        for vacancy in to_save:
            data.append(vacancy.to_dict())  # Конвертация Vacancy в dict

        if to_save:
            self._save_file(data)
            logger.info(f"Добавлено вакансий: {len(to_save)}")

    def get(self, criteria: Dict[str, Any]) -> List[Vacancy]:
        """
        Получение списка вакансий, соответствующих заданным критериям.
        """
        data = self._load_file()
        results = []

        for v in data:
            # Проверяем, что все критерии совпадают с данными вакансии
            if all(v.get(k) == val for k, val in criteria.items()):
                # Создаем объект Vacancy из данных словаря
                results.append(Vacancy(v["title"], v["url"], v["salary"], v["description"]))
        logger.info(f"Получено {len(results)} вакансий по критериям: {criteria}")
        return results

    def delete(self, vacancy: Vacancy) -> None:
        """
        Удаление вакансии из файла по её уникальному url.
        """
        data = self._load_file()
        original_len = len(data)
        # Отфильтровываем список, исключая вакансию с заданным url
        data = [v for v in data if v["url"] != vacancy.url]
        self._save_file(data)
        logger.info(f"Удалено вакансий: {original_len - len(data)} с url: {vacancy.url}")
