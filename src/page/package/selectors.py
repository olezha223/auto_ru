class SelectorNames:
    """Селекторы для перехода по элементам страницы для парсинга технической информации"""
    left = 'div.ModificationInfo__column-F3xzT:nth-child(1)'
    right = 'div.ModificationInfo__column-F3xzT:nth-child(2)'

    column = 'ModificationInfo__group-lR6NU'

    block_name = 'ModificationInfo__groupName-axo8d'
    values = 'ModificationInfo__optionValue-V_utP'
    keys = 'ModificationInfo__optionName-iuJYq'


class SelectorPackage:
    """Селекторы для перехода по элементам страницы для парсинга комплектации"""
    head = '.Equipment__options-4ZPvN'
    options = 'CardOptionsGroup'
    header = 'CardOptionsGroup__headerTitle'

    opt_parent = 'CardOptionsGroupList-REq1U CardOptionsGroupList_columns_2-KbJJL'

    option_value = 'CardOptionsGroupList__item-BHX6o'


class SelectorSelenium:
    """Селекторы для парсинга комплектации с помощью Selenium"""
    captcha_tracker = '.CardHead__title'

    tech_data_link = ".CardInfo__link-LIbAF > a:nth-child(1)"
    button = ".ComplectationGroupsDesktop__cutLink"

    title = '.CardComplectation__titleWrap'

    package_parent = '.ComplectationGroupsDesktop__row'
    blocks = '.ComplectationGroupsDesktop__group'

    header = ".ComplectationGroupsDesktop__groupTitle"
    item = '.ComplectationGroupsDesktop__item'
