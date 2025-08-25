
from src.vacancy import Vacancy
from src.utils import export_to_json, export_to_csv


def extract_salary(salary_data):
    """
    Извлекает зарплату из словаря зарплаты API.
    """
    if not salary_data:
        return 0
    if isinstance(salary_data, dict):
        salary_from = salary_data.get("from")
        salary_to = salary_data.get("to")
        if salary_from is not None:
            return salary_from
        elif salary_to is not None:
            return salary_to
    return 0


def user_interaction(hh_api, saver):
    """
    Функция взаимодействия с пользователем через консоль.
    """

    # Запрос ключевого слова для поиска вакансий
    keyword = input("Введите поисковый запрос (ключевое слово): ").strip()
    if not keyword:
        print("Ключевое слово не может быть пустым.")
        return

    # Получение вакансий через API
    print(f"Загружаем вакансии по запросу '{keyword}'...")
    vacancies_data = hh_api.load_vacancies(keyword)  # Получаем список словарей с вакансиями

    # Преобразуем данные в объекты Vacancy
    vacancies = [Vacancy(
        v.get("name", "Без названия"),
        v.get("alternate_url", ""),
        extract_salary(v.get("salary")),  # Передаем числовую зарплату из extract_salary
        v.get("snippet", {}).get("requirement", "") or v.get("snippet", {}).get("responsibility", "")
    ) for v in vacancies_data]

    # Сохраняем вакансии в файл (без дублирования)
    saver.add(vacancies)

    print(f"Сохранено вакансий: {len(vacancies)}")

    # Запрос у пользователя топ-N вакансий для вывода
    try:
        top_n = int(input("Сколько вакансий показать в топ-N по зарплате? "))
    except ValueError:
        print("Неверный ввод, показываю все вакансии.")
        top_n = len(vacancies)

    # Запрос ключевых слов для фильтрации по описанию
    filter_words_input = input("Введите ключевые слова для фильтрации вакансий по описанию (через пробел, можно пропустить): ").strip()
    filter_words = filter_words_input.lower().split() if filter_words_input else []

    # Фильтрация вакансий по ключевым словам
    if filter_words:
        filtered = []
        for vac in vacancies:
            text = (vac.description or "").lower()
            if all(word in text for word in filter_words):
                filtered.append(vac)
    else:
        filtered = vacancies

    # Сортируем вакансии по зарплате по убыванию
    filtered.sort(key=lambda v: v.salary if isinstance(v.salary, int) else 0, reverse=True)

    # Выводим топ-N вакансий
    print(f"\nТоп-{top_n} вакансий по зарплате:")
    for vac in filtered[:top_n]:
        print(f"{vac}\n{'-'*40}")

    # Новый код вопрос о формате экспорта
    export_format = input("В каком формате хотите сохранить вакансии? (json/csv/нет): ").strip().lower()

    if export_format == "json":
        export_to_json(filtered[:top_n])
    elif export_format == "csv":
        export_to_csv(filtered[:top_n])
    else:
        print("Экспорт пропущен.")
