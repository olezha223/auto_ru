import csv
import json
import pandas as pd
import os
from src.count_pages.link import Link
from src.count_pages.count_pages import ParseCount
from src.data_editor.data_editor import DataEditor
import multiprocessing


class CountingProcess:
    """
    Класс-обертка для создания топа машин и добавления данных
    """
    def __init__(self, region: str, errors_path: str):
        self.region = region
        self.errors_path = errors_path
        self.region_link = Link(region).create_link()

    def add_error(self, error: str):
        """
        Метод обрабатывает ошибку и кидает ее в файл для дальнейшей обработки.
        :param error: Текст ошибки
        """
        with open(self.errors_path, mode="a", newline="", encoding="utf-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([self.region_link, error])

    @staticmethod
    def add_data_to_file(variables_dict: dict, filename: str) -> None:
        """
        Добавляет строку в указанный файл
        :param filename: путь до json
        :param variables_dict: список данных для добавления
        """
        with open(filename, encoding='utf-8') as f:
            data = json.load(f)
            data['data'].append(variables_dict)
            with open(filename, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=2)

    def get_cars_count(self, k: int) -> list[list[str]]:
        """
        Здесь мы выделяем топ-k машин по количеству объявлений
        :param k: кол-во машин, которое идет в топ
        :return: отсортированный по убыванию количества машин массив длины k
        """
        not_sorted_cars = ParseCount(bad_outputs_path=self.errors_path,
                                     link=self.region_link).get_count()
        try:
            cars = sorted(not_sorted_cars, key=lambda x: int(x[1]))[::-1][:k]
        except ValueError:
            self.add_error(f"что-то не так со списком машин: {not_sorted_cars}")
            cars = [['AA', '0', 'AA']]
        return cars

    def get_model_counts(self, car_link: str, k: int) -> list[list[str]]:
        """
        Здесь мы выделяем топ-k по количеству объявлений моделей машины со ссылкой car_link
        :param car_link: ссылка на модель машины
        :param k: кол-во моделей, которое идет в топ
        :return: отсортированный по убыванию количества моделей массив длины k
        """
        not_sorted_models = ParseCount(bad_outputs_path=self.errors_path,
                                       link=car_link).get_count()
        try:
            models = sorted(not_sorted_models, key=lambda x: int(x[1]))[::-1][:k]
        except ValueError:
            self.add_error(f"что-то не так со списком моделей: {not_sorted_models}")
            models = [['AAA', '0', 'AAA']]
        return models

    def apply(self, k: int, filename: str, car: list[str]):
        """
        Метод добавляет по переданному filename данные
        :param k: количество машин, которое идет в топ
        :param filename: путь до json файла, в который добавляются данные
        :param car: массив, откуда мы вытаскиваем ссылку и потом остальные данные по машине
        :return:
        """
        models = self.get_model_counts(car_link=car[2], k=k)
        for model in models:
            data = {'Регион': self.region,
                    'Марка': car[0], 'Кол-во об. марки': car[1], 'Ссылка на марку': car[2],
                    'Модель': model[0], 'Кол-во об. модели': model[1], 'Ссылка на модель': model[2]}
            self.add_data_to_file(variables_dict=data, filename=filename)


class Wrapper:
    """
    Класс-обертка для реализации мультипроцессинга
    """
    def __init__(self, region: str, count_processes: int, first: bool):
        """
        Конструктор
        :param region: регион, в котором ведется парсинг
        :param count_processes: сколько процессов задействовать. Эквивалентно тому, сколько моделей машин будет в топе
        для каждого региона
        :param first: параметр-флаг того, что нужно заново создать json файлы для добавления данных
        """
        self.region = region
        self.count_processes = count_processes
        self.first = first

    def create_json_files(self):
        """
        Создает список файлов для информации по комплектации.
        :return: Возвращает список файлов
        """
        files = [f'../data/counting/counting_data_{file_num}.json'
                 for file_num in range(self.count_processes)]
        if self.first:
            for file in files:
                with open(file, 'w') as f:
                    json.dump({'data': []}, f)
        return files

    def one_region(self, boarder: int):
        """Мы реализуем мультипроцессорный парсинг для одного региона. Дальше в цикле мы будем идти по регионам"""
        cars = CountingProcess(region=self.region, errors_path='../files/errors/counting_errors.csv')
        cars_list = cars.get_cars_count(k=self.count_processes)
        arg_tuple = tuple(zip(cars_list, self.create_json_files()))
        processes = []
        for car, filename in arg_tuple:
            p = multiprocessing.Process(target=cars.apply, args=(boarder, filename, car))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()

    def join(self):
        """Соединяет все файлы json в датафрейм и сохраняет все в csv"""
        editor = DataEditor(output_file='../data/counting/result.csv',
                            count=self.count_processes,
                            path_to_json='../data/counting/counting_data')
        editor.join_data_csv()


def run_count_parsing(count_processes, count_models):
    """
    Итоговый цикл с проходом по всем регионам
    :param count_processes: сколько процессов будет использоваться
    :param count_models: сколько моделей будет в топе
    """
    regions = pd.read_csv('../files/regions.csv')['Name']
    for region in regions:
        wrapper = Wrapper(region=region, count_processes=count_processes, first=(region == regions[0]))
        wrapper.one_region(count_models)
        wrapper.join()


if __name__ == "__main__":
    import time
    start = time.perf_counter()
    run_count_parsing(count_models=5, count_processes=5)
    end = time.perf_counter()
    print(f"Время парсинга {round(100 * 2 / 86, 2)}"
          f"% данных составляет: {round(end - start, 2)} секунд")


