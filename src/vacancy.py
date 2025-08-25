class Vacancy:
    """
    Класс для представления вакансии.
    """

    __slots__ = ("title", "url", "salary", "description")  # Оптимизация памяти

    def __init__(self, title: str, url: str, salary, description: str):
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    @staticmethod
    def _validate_salary(salary):
        """
        Валидация зарплаты. Если зарплата не указана, возвращаем 0.
        """
        if salary is None or salary == "" or (isinstance(salary, str) and salary.lower() == "зарплата не указана"):
            return 0
        try:
            return int(salary)
        except (ValueError, TypeError):
            return 0

    def __lt__(self, other):
        """
        Сравнение вакансий по зарплате (меньше).
        """
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def __eq__(self, other):
        """
        Проверка равенства вакансий по зарплате и названию (title).
        """
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary and self.title == other.title  # исправлено с name на title

    def __repr__(self) -> str:
        """
        Строковое представление вакансии для отладки.
        """
        return (
            f"Vacancy(title={self.title!r}, url={self.url!r}, "
            f"salary={self.salary}, description={self.description!r})"
        )  # исправлено с name на title

    def __str__(self):
        """
        Представление вакансии (учим вакансию саму себя выводить).
        """
        return f"Название: {self.title}\nСсылка: {self.url}\nЗарплата: {self.salary}\nОписание: {self.description}"

    def to_dict(self):
        """
        Преобразует объект Vacancy в словарь (возможность класса самому себя выводить).
        """

        return {"title": self.title, "url": self.url, "salary": self.salary, "description": self.description}
