import pytest
from src.parser import Parser


def test_cannot_instantiate_abstract_parser():
    # Попытка создать экземпляр абстрактного класса должна вызвать TypeError
    with pytest.raises(TypeError):
        Parser()


class DummyParser(Parser):
    def connect(self):
        return "connected"

    def load_vacancies(self, keyword: str) -> list:
        return [{"title": "Test vacancy", "keyword": keyword}]


def test_dummy_parser_methods():
    dp = DummyParser()
    assert dp.connect() == "connected"
    vacancies = dp.load_vacancies("python")
    assert isinstance(vacancies, list)
    assert vacancies[0]["keyword"] == "python"


def test_dummy_parser_file_worker():
    dp = DummyParser(file_worker="file.txt")
    assert dp.file_worker == "file.txt"