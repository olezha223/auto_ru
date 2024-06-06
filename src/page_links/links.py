import csv
from requests_html import HTMLSession
from src.settings.headers import get_headers_3
from src.base_parser import Parser


class LinksParser(Parser):
    """
    Класс для парсинга ссылок на объявления
    """
    def __init__(self, model_link: str, errors_path: str, filename: str):
        """
        Конструктор парсера
        :param model_link: ссылка на страницу
        :param errors_path: путь до csv файла с ошибками
        :param filename: путь до json файла, куда будут добавляться данные
        """
        self.url = model_link
        super().__init__(errors_path=errors_path, link=model_link, filename=filename)

    def get_link(self, page: int) -> str:
        """
        Конструктор ссылки на страницу, чтоб проще всего получать ссылки + пагинация
        :param page: номер страницы
        :return:
        """
        return f'{self.url}?output_type=table&page={page}'

    def run(self):
        """Запуск парсинга ссылок"""
        with HTMLSession() as session:
            session.headers = get_headers_3()

            r = session.get(self.url)
            if 'X-Yandex-Captcha' in r.headers.keys() and r.headers['X-Yandex-Captcha'] == 'captcha':
                # эта штука проверяет, что ты получил капчу
                self.add_error(error='captcha')
                return
            parent = r.html.find('.ListingPagination', first=True)
            try:
                pages_count = int(parent.find('span')[2].find('span')[-1].text)
            except AttributeError:  # если на странице нет пагинации, то в parent будет лежать None
                pages_count = 1
            for page in list(r.html.absolute_links):
                if page.startswith('https://auto.ru/cars/new/') or page.startswith('https://auto.ru/cars/used/sale/'):
                    self.add_data_to_file(variables_dict={"Ссылка на модель": self.url,
                                                          "Ссылка на объявление": page})
        if pages_count > 1:  # если больше одной страницы в пагинации, то надо все собрать
            for i in range(2, pages_count + 1):
                with HTMLSession() as session:
                    session.headers = get_headers_3()
                    car_link = self.get_link(page=i)
                    r = session.get(car_link)
                    if 'X-Yandex-Captcha' in r.headers.keys() and r.headers['X-Yandex-Captcha'] == 'captcha':
                        self.add_error(error='captcha')
                        return
                    for page in list(r.html.absolute_links):
                        if page.startswith('https://auto.ru/cars/new/') or page.startswith('https://auto.ru/cars/used/sale/'):
                            self.add_data_to_file(variables_dict={"Ссылка на модель": self.url,
                                                                  "Ссылка на объявление": page})


if __name__ == "__main__":
    LinksParser(model_link='https://auto.ru/adygeya/cars/tank/300/new/?output_type=table',
                errors_path='cringe.csv',
                filename="../../data/links/links_data_0.json").run()
