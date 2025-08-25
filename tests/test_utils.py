import json
import csv
import pytest
from src.utils import export_to_json, export_to_csv
from src.vacancy import Vacancy


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Dev 1", "http://url1", 100000, "desc 1"),
        Vacancy("Dev 2", "http://url2", 200000, "desc 2"),
    ]


def test_export_to_json(tmp_path, sample_vacancies):
    file = tmp_path / "vacancies.json"
    export_to_json(sample_vacancies, filename=str(file))
    assert file.exists()

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert data[0]["title"] == "Dev 1"
    assert data[1]["salary"] == 200000


def test_export_to_csv(tmp_path, sample_vacancies):
    file = tmp_path / "vacancies.csv"
    export_to_csv(sample_vacancies, filename=str(file))
    assert file.exists()

    with open(file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    # Первая строка - заголовки
    assert rows[0] == ["Title", "URL", "Salary", "Description"]
    # Проверяем данные первой вакансии
    assert "Dev 1" in rows[1]
    assert "100000" in rows[1] or "100000" in rows[1][2]