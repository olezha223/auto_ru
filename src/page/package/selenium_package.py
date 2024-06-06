from selenium.webdriver.common.by import By
from src.settings.selenium_driver import Driver
from src.page.package.selectors import SelectorSelenium


class SeleniumPackage(Driver):
    """
    Дочка базового класса Driver для парсинга комплектации через библиотеку Selenium
    """
    def __init__(self,  link: str, errors_path: str,
                 package_filename: str,
                 use_proxy: bool = False,
                 user_agent: bool = False):
        """
        :param link: ссылка на объявление
        :param errors_path: путь до csv файла с ошибками
        :param package_filename: путь до json файла с информацией по комплектации
        :param use_proxy: принимает True, если хочется использовать прокси (временно недоступно)
        :param user_agent: принимает True, если хочется выбрать рандомный user-agent, не рекомендуется использовать,
        так как при изменении агента может выдать другую версию сайта
        """
        super().__init__(use_proxy=use_proxy, user_agent=user_agent,
                         errors_path=errors_path, link=link, filename=package_filename)
        self.chrome = super().get_driver()

    def get_package(self) -> dict:
        """
        Парсинг комплектации
        :return: возвращает полученные данные по комплектации
        """
        with self.chrome as driver:
            driver.implicitly_wait(1)
            driver.get(self.link)
            flag = self.get_element(SelectorSelenium.captcha_tracker, driver,
                                    exception_list=[SelectorSelenium.button, SelectorSelenium.title])
            if flag == "error":
                print(f"something went wrong: {self.link}")
                self.add_error("captcha_package")
                return {'captcha_package': 1}

            button = self.get_element(SelectorSelenium.button, driver,
                                      exception_list=[SelectorSelenium.button, SelectorSelenium.title])

            if button != "error":
                button.click()  # у нас может просто не быть кнопки из-за малого количества опций в комплектации

            # так же может комплектации просто не быть, тогда мы должны передать пустой package data
            if self.get_element(SelectorSelenium.title, driver,
                                exception_list=[SelectorSelenium.button, SelectorSelenium.title]) == "error":
                return {'captcha_package': 0}

            package_parent = self.get_element(SelectorSelenium.package_parent, driver,
                                              exception_list=[SelectorSelenium.button, SelectorSelenium.title])
            blocks = self.get_elements(SelectorSelenium.blocks, package_parent)
            package_data = {'captcha_package': 0}
            for block in blocks:
                content = self.get_elements(SelectorSelenium.item, block)
                for item in content:
                    option = item.find_elements(By.TAG_NAME, 'span')[1].text
                    if "₽" not in option:  # платные опции нам не нужны
                        package_data[option] = 1
            return package_data

    def gather_data(self) -> dict:
        """Метод собирает данные по комплектации"""
        package: dict = self.get_package()
        return package
