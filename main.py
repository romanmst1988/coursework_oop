
from src.hh import HH
from src.vacancy_saver import JSONSaver
from src.view import user_interaction
import logging


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[logging.StreamHandler()]  # Логи выводятся в консоль
    )

    # Инициализация объектов API и сохранения
    hh_api = HH()  # Пока file_worker=None, можно доработать
    saver = JSONSaver("data/vacancies.json")

    print("Подключение к HH API...")
    connected = hh_api.connect()
    if connected:
        print("Подключение к HH API успешно.")
    else:
        print("Не удалось подключиться к HH API. Проверьте соединение.")

    # Запускаем взаимодействие с пользователем
    user_interaction(hh_api, saver)


if __name__ == "__main__":
    main()
