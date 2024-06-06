from src.page.main_info.pages import PageParser
from src.page.package.selenium_package import SeleniumPackage
from src.page.package.requests_package import Package
from src.page.package.technical_info import TechData
from src.data_editor.data_editor import DataEditor
from src.base_parser import Parser
import re
import json
import multiprocessing
import pandas as pd
from tqdm import trange


class Wrapper(Parser):
    """
    Класс-обертка для парсинга объявления + техническая информация + комплектация
    """
    def __init__(self, link: str, filename: str):
        """
        :param link: ссылка на объявление
        :param filename: файл json, в который будут добавляться полученные данные
        """
        super().__init__(errors_path='../files/errors/wrapper.csv', link=link, filename=filename)
        self.filename: str = filename
        self.link: str = link

        # получение айди из ссылки на объявление
        match = re.search(r"\d+-\w{7}", link)
        self.id = match.group() if match else "can't get id"

        # инициализация контейнера для данных
        self.data: dict = PageParser(link=link, filename=filename, error_path='../files/errors/page_errors.csv').run()

    def run_package_parsing(self) -> dict:
        """
        Выбирает, какой способ парсинга комплектации применять
        :return: возвращает полученные данные
        """
        if self.data['captcha'] or not self.data['has_package']:
            return dict()
        if self.data['need_selenium']:
            return SeleniumPackage(link=self.link,
                                   errors_path="../files/errors/selenium_package_errors.csv",
                                   package_filename=self.filename).gather_data()
        else:
            return Package(url=self.data['Характеристики модели'],
                           errors_path='../files/errors/requests_package_errors.csv',
                           package_filename=self.filename).gather_data()

    def run_tech_data_parsing(self) -> dict:
        """
        Выбирает, применять ли парсинг технической информации.
        :return: Возвращает данные
        """
        if self.data['Характеристики модели'] != "No Data":
            return TechData(url=self.data['Характеристики модели'],
                            tech_data_filename=self.filename,
                            id_car=self.id,
                            errors_path='../files/errors/tech_data_errors.csv').gather_data()
        else:
            return {'id': self.id}

    def apply(self):
        """Добавляет агрегированные данные в файл json"""
        self.data.update(self.run_package_parsing())
        self.data.update(self.run_tech_data_parsing())
        self.add_data_to_file(variables_dict=self.data)


class Processing:
    """
    Класс-обертка для мультипроцессорного парсинга
    """
    def __init__(self, first: bool, count_processes: int):
        """
        :param first: переменная-флаг, чтобы создавать файлы
        :param count_processes: сколько процессов использовать при парсинге
        """
        self.first = first
        self.count = count_processes

    def create_json_files(self):
        """
        Создает список файлов для информации по комплектации.
        :return: Возвращает список файлов
        """
        files = [f'../data/cars/car_data_{file_num}.json'
                 for file_num in range(self.count)]
        if self.first:
            for file in files:
                with open(file, 'w') as f:
                    json.dump({'data': []}, f)
        return files

    def join(self):
        """
        Собирает данные из json файлов и сохраняет датафрейм в csv
        """
        editor = DataEditor(output_file='../data/cars/result.csv',
                            count=self.count,
                            path_to_json='../data/cars/car_data')
        editor.join_data_csv()

    def run(self):
        car_links = pd.read_csv('../data/links/result.csv')['Ссылка на объявление']
        step = self.count
        iterations_count = len(car_links) // step if len(car_links) % step == 0 else len(car_links) // step + 1
        files = self.create_json_files()
        for i in trange(iterations_count):
            left = i * step
            right = left + step
            links = car_links[left:right]
            args_tuple = tuple(zip(links, files))
            processes = []
            for link, file in args_tuple:
                p = multiprocessing.Process(target=Wrapper(link=link, filename=file).apply)
                processes.append(p)
                p.start()
            for p in processes:
                p.join()
        self.join()


if __name__ == "__main__":
    Processing(True, 5).run()
