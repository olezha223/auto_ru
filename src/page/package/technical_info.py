from bs4 import BeautifulSoup
from src.page.package.selectors import SelectorNames
from src.base_parser import Parser
from src.settings.headers import get_headers_2


class TechData(Parser):
    """
    Класс для парсинга технической информации
    """
    def __init__(self, url: str, tech_data_filename: str, id_car: str, errors_path: str):
        """
        :param url: ссылка на техническую информацию
        :param tech_data_filename: путь до json файла с технической информацией
        """
        super().__init__(errors_path=errors_path, link=url, filename=tech_data_filename)
        self.link = url
        self.filename = tech_data_filename
        self.id_car = id_car
        self.errors = errors_path

    def __tech_info(self, soup: BeautifulSoup) -> dict:
        """
        Данный метод вызывается в парсинге характеристик для получения информации о тех характеристиках машины
        :param soup: Суп, в котором будем искать данные
        :return: возвращает полученные данные по технической информации
        """
        try:
            first_column = soup.select_one(SelectorNames.right).find_all('div', class_=SelectorNames.column)
            second_column = soup.select_one(SelectorNames.left).find_all('div', class_=SelectorNames.column)
        except AttributeError:
            self.add_error("проблема с доступом к колонкам")
            first_column = []
            second_column = []
        tech_data = dict()
        tech_data["id"] = self.id_car  # чтобы потом понимать, с какой строкой мержить
        for block in first_column + second_column:
            values = block.find_all('span', SelectorNames.values)
            keys = block.find_all('span', SelectorNames.keys)
            for name_num in range(len(keys)):
                name = keys[name_num].text.replace('\xa0', ' ')
                var = values[name_num].text.replace('\xa0', ' ')
                tech_data[name] = var
        return tech_data

    def gather_data(self) -> dict:
        """
        Публичная обертка для парсинга технической информации
        """
        car_soup = self.get_soup(headers_func=get_headers_2)
        tech_info = self.__tech_info(car_soup)
        return tech_info
        # self.add_data_to_file(tech_info)
