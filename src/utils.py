
import json
import csv


def export_to_json(vacancies, filename="vacancies_export.json"):
    """
    Экспорт списка вакансий в JSON-файл.
    """
    data = [{
        "title": v.title,
        "url": v.url,
        "salary": v.salary,
        "description": v.description
    } for v in vacancies]

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Вакансии успешно экспортированы в {filename}")


def export_to_csv(vacancies, filename="vacancies_export.csv"):
    """
    Экспорт списка вакансий в CSV-файл.
    """
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "URL", "Salary", "Description"])
        for v in vacancies:
            writer.writerow([v.title, v.url, v.salary, v.description])
    print(f"Вакансии успешно экспортированы в {filename}")
