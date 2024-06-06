import csv
import json
import re
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import selenium.webdriver


class Parser:
    """
    Базовый класс для парсинга
    """
    def __init__(self, errors_path: str, link: str, filename: str):
        """
        Конструктор
        :param errors_path: путь до csv файла с ошибками
        :param link: ссылка на страницу
        :param filename: путь до json файла, куда будут добавляться данные
        """
        self.errors = errors_path
        self.link = link
        self.filename = filename

    def add_error(self, error: str):
        """
        Добавляет ошибку в файл с переданным сообщением, аналог логирования
        :param error: текст ошибки
        """
        with open(self.errors, mode="a", newline="", encoding="utf-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([self.link, error])

    def add_data_to_file(self, variables_dict: dict) -> None:
        """
        Добавляет строку в указанный файл
        :param variables_dict: список данных для добавления
        """
        with open(self.filename, encoding='utf-8') as f:
            data = json.load(f)
            data['data'].append(variables_dict)
            with open(self.filename, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=2)

    def get_element(self, selector: str, driver: selenium.webdriver.Chrome, exception_list: list[str]):
        """
        Получить текст элемента
        :param selector: селектор, по которому получаем элемент
        :param driver: объект webdriver для доступа к странице
        :param exception_list: список, какие селекторы игнорировать для добавления ошибки
        :return: возвращает полученный элемент
        """
        try:
            result = driver.find_element(By.CSS_SELECTOR, selector)
        except (NoSuchElementException, AttributeError, StaleElementReferenceException):
            if selector not in exception_list:
                self.add_error(f"Can't find element : {selector}")
            result = "error"
        return result

    def get_elements(self, selector: str, driver) -> list:
        """
        Получить список элементов по селектору
        :param selector: селектор, по которому получаем элементы
        :param driver: объект webdriver для доступа к странице
        :return: возвращает все элементы на странице по данному селектору
        """
        try:
            result = driver.find_elements(By.CSS_SELECTOR, selector)
        except (NoSuchElementException, AttributeError, StaleElementReferenceException):
            self.add_error(f"Can't find elements : {selector}")
            print(f"Can't find elements: {self.link, selector}")
            result = "error"
        return result

    @staticmethod
    def get_text(selector: str, soup: BeautifulSoup) -> str:
        """
        В переданном супе найдет текста в элементе по селектору
        :param selector:  Селектор элемента
        :param soup: Суп, в котором будем искать элемент
        :return: Текст полученного элемента, если существует
        """
        try:
            result = soup.select_one(selector).text.replace('\xa0', ' ')
        except AttributeError:
            result = "No Data"
        return result

    def get_soup(self, headers_func) -> BeautifulSoup:
        """
        Проверяет наличие капчи на странице. Если получил капчу пробует снова, тесты показали,
        что хотя бы 1 из 8 раз капча не вылезает.
        :return: Возвращает soup для данной ссылки
        """
        attempt_count = 0
        while True:
            if attempt_count > 8:
                self.add_error("can't get to page")
                print(f"can't get to page : {self.link}")
                return BeautifulSoup()
            response = requests.get(self.link, headers=headers_func()[0], cookies=headers_func()[1])
            response.encoding = 'utf-8'
            captcha_regex = re.compile("Капча")
            if captcha_regex.search(response.text):
                attempt_count += 1
                continue
            soup = BeautifulSoup(response.text, "html.parser")
            return soup

