
from src.view import user_interaction


class DummyAPI:
    @staticmethod
    def load_vacancies(keyword):
        _ = keyword  # подавляем предупреждение о неиспользуемой переменной
        return [
            {
                "name": "Python Developer",
                "alternate_url": "http://example.com/1",
                "salary": {"from": 100000, "to": None},
                "snippet": {"requirement": "Python, Django"}
            },
            {
                "name": "Junior Python Developer",
                "alternate_url": "http://example.com/2",
                "salary": {"from": 50000, "to": None},
                "snippet": {"requirement": "Python"}
            },
        ]


class DummySaver:
    def __init__(self):
        self.saved = []

    def add(self, vacancy):
        """
        user_interaction передаёт сюда СПИСОК Vacancy (+поддержка одиночного объекта).
        """
        if isinstance(vacancy, list):
            for v in vacancy:
                if isinstance(v, list):
                    self.saved.extend(v)
                else:
                    self.saved.append(v)
        else:
            self.saved.append(vacancy)


def test_user_interaction(monkeypatch):
    # Подготовим ответы пользователя:
    inputs = iter(["Python", "1", "Django", "json"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    exported = {}

    def _fake_export_to_json(vacancies):
        exported["json_called"] = True
        exported["count"] = len(vacancies)

    # Вариант 1 (предпочтительно): патчим именно то имя, которое использует view.py
    monkeypatch.setattr("src.view.export_to_json", _fake_export_to_json, raising=False)

    # (если вдруг выше всё равно не подхватится, можно продублировать)
    # monkeypatch.setattr("src.utils.export_to_json", _fake_export_to_json, raising=False)

    api = DummyAPI()
    saver = DummySaver()
    user_interaction(api, saver)

    filtered = [v for v in saver.saved if "django" in (v.description or "").lower()]
    assert len(filtered) == 1
    assert exported.get("json_called") is True
    assert exported.get("count") == 1


def test_user_interaction_empty_keyword(monkeypatch, capsys):
    inputs = iter([
        "",  # пустой keyword
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    api = DummyAPI()
    saver = DummySaver()

    user_interaction(api, saver)

    out = capsys.readouterr().out
    assert "Ключевое слово не может быть пустым." in out


def test_user_interaction_invalid_top_n(monkeypatch):
    inputs = iter([
        "Python",
        "abc",
        "",
        "нет"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    api = DummyAPI()
    saver = DummySaver()

    user_interaction(api, saver)

    # В saver должно лечь 2 объекта Vacancy (а не один список)
    assert len(saver.saved) == 2


def test_user_interaction_no_filter_words(monkeypatch):
    inputs = iter([
        "Python",
        "2",
        "",
        "нет"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    api = DummyAPI()
    saver = DummySaver()

    user_interaction(api, saver)

    # Должны сохранить 2 вакансии без фильтрации
    assert len(saver.saved) == 2
