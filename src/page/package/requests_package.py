from src.page.package.selectors import SelectorPackage
from src.base_parser import Parser
from src.settings.headers import get_headers_2


class Package(Parser):
    """
    Класс для парсинга комплектации с помощью requests
    """
    def __init__(self, url: str, package_filename: str, errors_path: str):
        """
        :param url: ссылка на техническую информацию
        :param package_filename: путь до json файла с информацией по комплектации
        """
        self.filename = package_filename
        self.link = url.replace("specifications", "equipment")
        self.errors = errors_path
        super().__init__(errors_path=errors_path, link=self.link, filename=package_filename)

    def __parse_package(self) -> dict:
        """
        Парсинг комплектации
        :return: возвращает полученные данные по комплектации
        """
        package_data = {'captcha_package': 0}
        package_soup = self.get_soup(headers_func=get_headers_2)
        try:
            blocks = package_soup.select_one(SelectorPackage.head).find_all('div', class_=SelectorPackage.options)
        except AttributeError:
            self.add_error("error while block parsing")
            print(f"error while block parsing: {self.link}")
            return {'captcha_package': 1}
        for block in blocks:
            options = block.find('ul', class_=SelectorPackage.opt_parent).find_all('li', SelectorPackage.option_value)
            for option in options:
                option_text = option.text.replace('\xa0', ' ')
                if "₽" not in option_text:  # платные опции нам не нужны
                    package_data[option_text] = 1
        return package_data

    def gather_data(self) -> dict:
        """
        Метод собирает данные по комплектации и тех. характеристикам и добавляет их в данные
        """
        pack: dict = self.__parse_package()
        return pack
