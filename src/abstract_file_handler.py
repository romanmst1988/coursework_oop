from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.vacancy import Vacancy


class AbstractFileHandler(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Vacancy]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass
