import json
from src.data_editor.data_editor import DataEditor
import multiprocessing
from src.page_links.links import LinksParser
import os
import pandas as pd


class Processing:
    """
    Класс-обертка для мультипроцессорного парсинга ссылок на объявления
    """
    def __init__(self, count: int):
        """
        :param count: сколько процессов использовать при парсинге
        """
        self.count = count

    def create_json_files(self, init: bool):
        """
        Создает список файлов для информации по комплектации.
        :return: Возвращает список файлов
        """
        files = [f'../data/links/links_data_{file_num}.json'
                 for file_num in range(self.count)]
        if init:
            for file in files:
                with open(file, 'w') as f:
                    json.dump({'data': []}, f)
        return files

    def join(self):
        """
        Собирает данные из json файлов и сохраняет датафрейм в csv
        """
        editor = DataEditor(output_file='../data/links/result.csv',
                            count=self.count,
                            path_to_json='../data/links/links_data')
        editor.join_data_csv()

    def multi_run(self):
        """
        Запуск парсинга
        """
        model_links = pd.read_csv("../data/counting/result.csv")['Ссылка на модель']
        step = self.count
        iterations_count = len(model_links) // step if len(model_links) % step == 0 else len(model_links) // step + 1
        for i in range(iterations_count):
            left = i * step
            right = left + step
            files = self.create_json_files(init=(left == 0))
            tmp = model_links[left: right]
            args_tuple = tuple(zip(tmp, files))
            processes = []
            for link, filename in args_tuple:

                p = multiprocessing.Process(target=LinksParser(model_link=link,
                                                               errors_path="../files/errors/links_errors.csv",
                                                               filename=filename).run)
                processes.append(p)
                p.start()
            for p in processes:
                p.join()
        self.join()


def run_links_parser(count):
    proc = Processing(count=count)
    proc.multi_run()
    proc.join()


if __name__ == '__main__':
    run_links_parser(count=5)
