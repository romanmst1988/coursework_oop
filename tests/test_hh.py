from src.hh import HH


def test_connect():
    hh = HH()  # Передаем None, если file_worker нет
    result = hh.connect()
    # connect возвращает либо True, либо False
    assert result is True or result is False


def test_load_vacancies():
    hh = HH(None)
    vacancies = hh.load_vacancies("Python")
    # Проверяем, что вернулся список
    assert isinstance(vacancies, list)
    # Если список не пустой, проверим, что первый элемент — словарь с ключом 'name' или 'id'
    if vacancies:
        assert isinstance(vacancies[0], dict)
        assert "name" in vacancies[0] or "id" in vacancies[0]
