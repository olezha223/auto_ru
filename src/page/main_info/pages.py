import re
from src.base_parser import Parser
from src.settings.headers import get_headers
from src.page.main_info.page_selector import (SelectorPageMainUsed,
                                              SelectorPageMainNew,
                                              SelectorPageUsed,
                                              SelectorPageNew)


class PageParser(Parser):
    """
    Класс для парсинга страницы
    """
    def __init__(self, link, filename: str, error_path: str):
        """
        Вызывается конструктор парсера
        :param link: Ссылка на страницу
        :param filename: Путь до файла, в который идет добавление данных. Должен быть в формате json
        :param error_path: Путь до файла с ошибками. Должен быть в формате csv
        """
        super().__init__(errors_path=error_path, link=link, filename=filename)

    def get_addition_data(self, tech_1, tech_2, package: str) -> dict:
        """
        Метод собирает флаги по странице + ссылку на техническую информацию для последующего парсинга.
        В метод передаются два параметра, потому что ссылка может лежать как по первому, так и по второму селектору.
        :param tech_1: Полученный объект вариант 1, в котором возможно лежит ссылка
        :param tech_2: Полученный объект вариант 2, в котором возможно лежит ссылка
        :param package: Сюда необходимо передать то, что лежит на странице в графе <Комплектация>
        :return: возвращает полученные дополнительные данные
        """
        page_data = dict()
        page_data['captcha'] = 0
        try:
            page_data['Характеристики модели'] = tech_1['href']
        except (KeyError, AttributeError, TypeError):
            try:
                page_data['Характеристики модели'] = tech_2['href']
            except (KeyError, AttributeError, TypeError):
                self.add_error("can't get link to tech info")
                page_data['Характеристики модели'] = "No Data"
                page_data['captcha'] = 1

        page_data['has_package'] = 1 if package != "No Data" else 0
        page_data['need_selenium'] = 1 if re.match(r"\d+ опци", package) else 0
        return page_data

    def scrap_used(self) -> dict:
        """
        Собирает данные со страницы б/у машины
        :return: Полученные данные по странице
        """
        soup = self.get_soup(headers_func=get_headers)
        page_data = dict()
        page_data['link'] = self.link
        page_data['used'] = 1
        sold = 1 if self.get_text(SelectorPageMainUsed.sold_status, soup=soup) != "No Data" else 0
        page_data['sold'] = sold
        main_variables = SelectorPageMainUsed.__dict__
        for key, value in main_variables.items():
            if not key.startswith("__") and key not in ['sold_status', 'main', 'tech_link', 'tech_link_2']:
                page_data[key] = self.get_text(selector=value, soup=soup)

        variables = SelectorPageUsed.__dict__
        for key, value in variables.items():
            if not key.startswith("__"):
                page_data[key] = self.get_text(selector=value, soup=soup)
        tech_1 = soup.select_one(selector=SelectorPageMainUsed.tech_link)
        tech_2 = soup.select_one(selector=SelectorPageMainUsed.tech_link_2)
        addition: dict = self.get_addition_data(tech_1, tech_2, page_data['package'])
        page_data.update(addition)
        return page_data

    def scrap_new(self) -> dict:
        """
        Собирает данные по страницы новой машины
        :return: полученные данные
        """
        soup = self.get_soup(headers_func=get_headers)
        page_data = dict()
        page_data['link'] = self.link
        page_data['used'] = 0
        sold = 1 if self.get_text(SelectorPageMainNew.sold, soup=soup) != "No Data" else 0
        page_data['sold'] = sold
        main_variables = SelectorPageMainNew.__dict__
        for key, value in main_variables.items():
            if not key.startswith("__") and key not in ['main', 'tech_link', 'tech_link_2', 'sold']:
                page_data[key] = self.get_text(selector=value, soup=soup)
        table = soup.select_one(selector=SelectorPageMainNew.main)
        variables = SelectorPageNew.__dict__
        for key in variables.keys():
            if sold and key == 'tax':
                page_data[key] = 'No Data'
                continue
            elif sold and key == 'transmission':
                page_data['transmission'] = self.get_text(selector=variables['tax'], soup=table)
                continue
            elif sold and key == 'driver':
                page_data['driver'] = self.get_text(selector=variables['transmission'], soup=table)
                continue
            if not key.startswith("__"):
                page_data[key] = self.get_text(selector=variables[key], soup=table)
        tech_1 = soup.select_one(selector=SelectorPageMainNew.tech_link)
        tech_2 = soup.select_one(selector=SelectorPageMainNew.tech_link_2)
        addition: dict = self.get_addition_data(tech_1, tech_2, page_data['package'])
        page_data.update(addition)
        return page_data

    def run(self) -> dict:
        """
        В зависимости от ссылки запускается парсинг либо новой машины, либо б/у
        :return: полученные данные
        """
        if self.link.startswith('https://auto.ru/cars/new/'):
            data = self.scrap_new()
        else:
            data = self.scrap_used()
        return data


if __name__ == "__main__":
    # если хочется поискать ошибки
    a = PageParser(link='https://auto.ru/cars/new/group/exeed/vx/23115441/23137353/1121712442-6344b981/',
                   filename='',
                   error_path='cringe.csv').scrap_new()

    print(a)


