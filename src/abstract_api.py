from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями."""

    @abstractmethod
    def get_vacancies(self, search_query: str) -> list[Dict[str, Any]]:
        pass

    @abstractmethod
    def _connect_to_api(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Приватный метод для подключения к API."""
        pass
