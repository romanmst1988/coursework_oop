from abc import ABC, abstractmethod


class Parser(ABC):
    """
    Абстрактный родительский класс для работы с API сервисов вакансий.
    """

    def __init__(self, file_worker=None):
        """
        Добавляем параметр file_worker для возможности разделения ответственности:
            - file_worker отвечает за сохранение и загрузку данных в файлы JSON, CSV и т.д.
            - если не нужен, можно передать None (как в нашей курсовой).
        """
        self.file_worker = file_worker

    @abstractmethod
    def connect(self):
        """
        Метод для подключения к API сервиса.
        """
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str) -> list:
        """
        Метод для получения вакансий по ключевому слову.
        """
        pass
