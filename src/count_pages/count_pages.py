from src.count_pages.selector import SelectorMainPage
from src.settings.selenium_driver import Driver


class ParseCount(Driver):
    """
    Парсинг количества объявлений по данной модели/марке в данном регионе
    """

    def __init__(self, bad_outputs_path: str, link: str, use_proxy=False, user_agent=False):
        """
        :param bad_outputs_path: Путь к файлу, в который будут отправляться ошибки
        :param link: Ссылка на страницу
        :param use_proxy: True, если хочется использовать прокси
        :param user_agent: True, если хочется подменить юзер-агент
        """
        super().__init__(use_proxy=use_proxy, user_agent=user_agent,
                         errors_path=bad_outputs_path,
                         link=link,
                         filename='')
        self.chrome = super().get_driver()

    def get_count(self) -> list:
        """
        Заходит на страницу с помощью Selenium и по селекторам выбирает данные
        :return: Формат вывода: [[название машину, количество объявлений, ссылка на машину], [], ...]
        """
        with self.chrome as driver:
            driver.implicitly_wait(60)
            driver.get(self.link)
            driver.execute_script("window.scrollBy(0,100)")

            columns_area = self.get_element(selector=SelectorMainPage.items_area,
                                            driver=driver,
                                            exception_list=[SelectorMainPage.button])
            if columns_area == "error":
                self.add_error("captcha")
                return ['captcha']
            columns = self.get_elements(selector=SelectorMainPage.column, driver=columns_area)

            for column in columns:
                driver.implicitly_wait(0.01)
                button = self.get_element(selector=SelectorMainPage.button,
                                          driver=column,
                                          exception_list=[SelectorMainPage.button])
                # кнопки может и не быть из-за маленького количества объявлений
                if button != "error":
                    button.click()
            result = []

            # нам снова надо получить доступ ко всем колонкам, страница могла измениться после нажатия кнопки
            columns_area = self.get_element(selector=SelectorMainPage.items_area, driver=driver,
                                            exception_list=[SelectorMainPage.button])
            columns = self.get_elements(selector=SelectorMainPage.column, driver=columns_area)
            for column in columns:
                cars = self.get_elements(selector=SelectorMainPage.car, driver=column)
                for car in cars:
                    car_name = self.get_element(selector=SelectorMainPage.car_name, driver=car,
                                                exception_list=[SelectorMainPage.button]).text
                    car_link = self.get_element(selector=SelectorMainPage.car_name, driver=car,
                                                exception_list=[SelectorMainPage.button]).get_attribute("href")
                    car_quantity = self.get_element(selector=SelectorMainPage.count, driver=car,
                                                    exception_list=[SelectorMainPage.button]).text
                    result.append([car_name, car_quantity, car_link])

            return result
