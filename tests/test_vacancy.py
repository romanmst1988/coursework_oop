
from pathlib import Path
import json
import pytest
from src.vacancy_saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def temp_filename(tmp_path: Path) -> Path:
    """
    Даём каждому тесту свой JSON-файл.
    """
    return tmp_path / "vacancies.json"


def make_v(title: str, url: str, salary: int, desc: str) -> Vacancy:
    """Компактная фабрика Vacancy ."""
    return Vacancy(title, url, salary, desc)


def test_add_single_in_list_and_get_all(temp_filename):
    saver = JSONSaver(str(temp_filename))
    v = make_v("Python Dev", "https://hh.ru/vacancy/1", 100000, "Desc")

    # add принимает СПИСОК передаём список из одного элемента
    saver.add([v])

    # Пустые критерии и надо вернуть все записи
    got = saver.get({})
    assert len(got) == 1
    assert got[0].title == "Python Dev"
    assert got[0].url == "https://hh.ru/vacancy/1"
    assert got[0].salary == 100000
    assert got[0].description == "Desc"


def test_add_duplicates_skips_by_url(temp_filename):
    saver = JSONSaver(str(temp_filename))
    v = make_v("Python Dev", "https://hh.ru/vacancy/1", 100000, "Desc")

    saver.add([v])
    saver.add([v])  # дубль по url — не должен добавиться второй раз

    got = saver.get({})
    assert len(got) == 1


def test_get_by_single_criteria_title(temp_filename):
    saver = JSONSaver(str(temp_filename))
    v1 = make_v("Python Dev", "https://hh.ru/vacancy/1", 100000, "D1")
    v2 = make_v("Java Dev", "https://hh.ru/vacancy/2", 120000, "D2")
    saver.add([v1, v2])

    got = saver.get({"title": "Python Dev"})
    assert len(got) == 1
    assert got[0].url == "https://hh.ru/vacancy/1"


def test_get_by_multiple_criteria(temp_filename):
    saver = JSONSaver(str(temp_filename))
    v1 = make_v("Python Dev", "https://hh.ru/vacancy/1", 100000, "D1")
    v2 = make_v("Python Dev", "https://hh.ru/vacancy/2", 150000, "D2")
    saver.add([v1, v2])

    got = saver.get({"title": "Python Dev", "salary": 100000})
    assert len(got) == 1
    assert got[0].url == "https://hh.ru/vacancy/1"


def test_get_with_empty_criteria_returns_all(temp_filename):
    saver = JSONSaver(str(temp_filename))
    saver.add([make_v("A", "u1", 1, "d1"), make_v("B", "u2", 2, "d2")])

    got = saver.get({})
    assert len(got) == 2


def test_delete_existing_vacancy(temp_filename):
    saver = JSONSaver(str(temp_filename))
    v1 = make_v("Python Dev", "https://hh.ru/vacancy/1", 100000, "D1")
    v2 = make_v("Java Dev", "https://hh.ru/vacancy/2", 120000, "D2")
    saver.add([v1, v2])

    saver.delete(v1)

    got = saver.get({})
    assert len(got) == 1
    assert got[0].url == "https://hh.ru/vacancy/2"


def test_delete_nonexistent_vacancy_no_change(temp_filename):
    saver = JSONSaver(str(temp_filename))
    v1 = make_v("Python Dev", "https://hh.ru/vacancy/1", 100000, "D1")
    v2 = make_v("Java Dev", "https://hh.ru/vacancy/2", 120000, "D2")
    saver.add([v1, v2])

    ghost = make_v("Go Dev", "https://hh.ru/vacancy/999", 200000, "Ghost")
    saver.delete(ghost)  # в файле его нет — должно пройти без ошибок и без изменений

    got = saver.get({})
    assert len(got) == 2
    assert {g.url for g in got} == {"https://hh.ru/vacancy/1", "https://hh.ru/vacancy/2"}


def test_get_when_file_missing_returns_empty(temp_filename):
    """
    Файл ещё не создан _load_file() должен вернуть [] без исключений.
    """
    saver = JSONSaver(str(temp_filename))
    got = saver.get({})
    assert got == []


def test_get_when_file_has_invalid_json_returns_empty(temp_filename):
    """
    В файле некорректный JSON — _load_file() ловит JSONDecodeError и возвращает [].
    """
    # Пишем битый JSON
    temp_filename.write_text("{not valid json", encoding="utf-8")

    saver = JSONSaver(str(temp_filename))
    got = saver.get({})
    assert got == []


def test_get_when_file_has_non_list_returns_empty(temp_filename):
    """
    В файле корректный JSON, но не список (например, словарь) — функция должна вернуть [].
    """
    temp_filename.write_text(json.dumps({"not": "a list"}), encoding="utf-8")

    saver = JSONSaver(str(temp_filename))
    got = saver.get({})
    assert got == []
