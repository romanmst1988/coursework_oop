from typing import List

from src.vacancy import Vacancy


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """Фильтрация вакансий по ключевым словам."""
    if not filter_words:
        return vacancies
    return [
        v
        for v in vacancies
        if any(word.lower() in v.description.lower() for word in filter_words)
    ]


def get_vacancies_by_salary(
    vacancies: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    """Фильтрация вакансий по диапазону зарплат."""
    if not salary_range:
        return vacancies
    try:
        min_salary, max_salary = map(int, salary_range.split("-"))
        return [
            v for v in vacancies if min_salary <= v._get_salary_value() <= max_salary
        ]
    except ValueError:
        return vacancies


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка вакансий по зарплате."""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Получение топ N вакансий."""
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Вывод вакансий в консоль."""
    for vacancy in vacancies:
        print(f"Название: {vacancy.title}")
        print(f"Ссылка: {vacancy.url}")
        print(f"Зарплата: {vacancy.salary}")
        print(f"Описание: {vacancy.description}")
        print(f"Требования: {vacancy.requirements}")
        print()
