import unittest
from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):
    def test_vacancy_creation(self):
        vacancy = Vacancy("Python Developer", "https://hh.ru/vacancy/123", "100000-150000 руб.", "Описание",
                          "Опыт работы")
        self.assertEqual(vacancy.title, "Python Developer")
        self.assertEqual(vacancy.url, "https://hh.ru/vacancy/123")
        self.assertEqual(vacancy.salary, "100000-150000 руб.")
        self.assertEqual(vacancy.description, "Описание")
        self.assertEqual(vacancy.requirements, "Опыт работы")

    def test_salary_validation_unspecified(self):
        vacancy = Vacancy("Test", "url", "", "desc", "req")
        self.assertEqual(vacancy.salary, "Зарплата не указана")

    def test_salary_validation_not_specified(self):
        vacancy = Vacancy("Test", "url", "не указана", "desc", "req")
        self.assertEqual(vacancy.salary, "Зарплата не указана")

    def test_salary_comparison(self):
        v1 = Vacancy("Title1", "url1", "100000", "desc1", "req1")
        v2 = Vacancy("Title2", "url2", "150000", "desc2", "req2")
        self.assertTrue(v1 < v2)
        self.assertTrue(v2 > v1)
        self.assertTrue(v1 <= v2)
        self.assertTrue(v2 >= v1)

    def test_salary_comparison_with_unspecified(self):
        v1 = Vacancy("Title1", "url1", "не указана", "desc1", "req1")
        v2 = Vacancy("Title2", "url2", "100000", "desc2", "req2")
        self.assertTrue(v1 < v2)
        self.assertTrue(v2 > v1)

    def test_get_salary_value(self):
        v1 = Vacancy("Title1", "url1", "100000-150000 руб.", "desc1", "req1")
        self.assertEqual(v1._get_salary_value(), 150000)

        v2 = Vacancy("Title2", "url2", "не указана", "desc2", "req2")
        self.assertEqual(v2._get_salary_value(), 0)

        v3 = Vacancy("Title3", "url3", "80000 руб.", "desc3", "req3")
        self.assertEqual(v3._get_salary_value(), 80000)

    def test_cast_to_object_list(self):
        sample_data = [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123",
                "salary": {
                    "from": 100000,
                    "to": 150000,
                    "currency": "RUR"
                },
                "snippet": {
                    "responsibility": "Разработка",
                    "requirement": "Опыт работы"
                }
            },
            {
                "name": "Data Scientist",
                "alternate_url": "https://hh.ru/vacancy/456",
                "salary": None,
                "snippet": {
                    "responsibility": "Анализ данных",
                    "requirement": "Знание Python"
                }
            }
        ]

        vacancies = Vacancy.cast_to_object_list(sample_data)
        self.assertEqual(len(vacancies), 2)

        self.assertEqual(vacancies[0].title, "Python Developer")
        self.assertEqual(vacancies[0].salary, "100000-150000 RUR")
        self.assertEqual(vacancies[0].description, "Разработка")
        self.assertEqual(vacancies[0].requirements, "Опыт работы")

        self.assertEqual(vacancies[1].title, "Data Scientist")
        self.assertEqual(vacancies[1].salary, "Зарплата не указана")
        self.assertEqual(vacancies[1].description, "Анализ данных")
        self.assertEqual(vacancies[1].requirements, "Знание Python")


if __name__ == '__main__':
    unittest.main()
