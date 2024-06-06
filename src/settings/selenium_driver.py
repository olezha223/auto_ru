from selenium_stealth import stealth
from selenium import webdriver
from src.base_parser import Parser
from src.settings.proxy_extension import ProxyExtension


class Driver(Parser):
    """This is the base class that defines the basic parameters for creating a Chrome driver"""
    def __init__(self, errors_path,  link, filename, use_proxy=False, user_agent=False):
        """
        Инициализирует базовые поля.
        Модифицируется по желанию, в текущей версии нет доступных прокси и проверенных юзер-агентов.
        :param use_proxy: True, если хочется использовать прокси
        :param user_agent: True, если хочется подменить юзер-агент
        """
        self.use_proxy = use_proxy
        self.user_agent = user_agent
        super().__init__(errors_path=errors_path, link=link, filename=filename)

    def get_driver(self) -> webdriver.Chrome:
        """
        :return: Возвращает готовый драйвер со всеми нужными опциями для комфортного парсинга
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        if self.use_proxy:
            ip, port, login, password = [1, 1, 1, 1]
            proxy_extension = ProxyExtension(ip, int(port), login, password)
            options.add_argument(f"--load-extension={proxy_extension.directory}")

        if self.user_agent:
            def get_agent() -> str:
                return ''
            options.add_argument(f'--user-agent={get_agent()}')

        driver_stealth = webdriver.Chrome(options=options)

        stealth(driver_stealth,
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        driver_stealth.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver_stealth.implicitly_wait(100)

        return driver_stealth
