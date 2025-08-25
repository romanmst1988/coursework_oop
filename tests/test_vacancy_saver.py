
import pytest
from src.vacancy_saver import VacancySaver


def test_cannot_instantiate_abstract_class():
    with pytest.raises(TypeError):
        VacancySaver()  # Попытка создать экземпляр абстрактного класса должна вызвать TypeError


def test_abstract_methods_signature():
    # Проверяем, что у VacancySaver есть требуемые абстрактные методы
    methods = ['add', 'get', 'delete']
    for method in methods:
        assert callable(getattr(VacancySaver, method))


@pytest.fixture
def temp_filename(tmp_path):
    return tmp_path / "vacancies.json"
