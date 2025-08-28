import re
from typing import List, Dict, Any


class Vacancy:
    """Класс для представления вакансии."""

    __slots__ = ("title", "url", "salary", "description", "requirements")

    def __init__(
        self, title: str, url: str, salary: str, description: str, requirements: str
    ):
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description
        self.requirements = requirements

    def _validate_salary(self, salary: str) -> str:
        """Валидация зарплаты."""
        if not salary or salary.lower() == "не указана":
            return "Зарплата не указана"
        return salary

    def __lt__(self, other: "Vacancy") -> bool:
        return self._get_salary_value() < other._get_salary_value()

    def __le__(self, other: "Vacancy") -> bool:
        return self._get_salary_value() <= other._get_salary_value()

    def __gt__(self, other: "Vacancy") -> bool:
        return self._get_salary_value() > other._get_salary_value()

    def __ge__(self, other: "Vacancy") -> bool:
        return self._get_salary_value() >= other._get_salary_value()

    def _get_salary_value(self) -> int:
        """Получение числового значения зарплаты для сравнения."""
        if self.salary == "Зарплата не указана":
            return 0

        # Используем регулярное выражение для поиска всех чисел в строке
        numbers = re.findall(r"\d+", self.salary)
        if numbers:
            return max(map(int, numbers))
        return 0

    @staticmethod
    def cast_to_object_list(vacancies_data: List[Dict[str, Any]]) -> List["Vacancy"]:
        """Преобразование JSON-данных в список объектов Vacancy."""
        vacancies = []
        for item in vacancies_data:
            title = item.get("name", "")
            url = item.get("alternate_url", "")
            salary = item.get("salary")
            if salary:
                from_salary = salary.get("from", "")
                to_salary = salary.get("to", "")
                currency = salary.get("currency", "")

                if from_salary and to_salary:
                    salary_str = f"{from_salary}-{to_salary} {currency}"
                elif from_salary:
                    salary_str = f"{from_salary} {currency}"
                elif to_salary:
                    salary_str = f"{to_salary} {currency}"
                else:
                    salary_str = "Зарплата не указана"
            else:
                salary_str = "Зарплата не указана"

            description = item.get("snippet", {}).get("responsibility", "")
            requirements = item.get("snippet", {}).get("requirement", "")
            vacancies.append(Vacancy(title, url, salary_str, description, requirements))
        return vacancies
