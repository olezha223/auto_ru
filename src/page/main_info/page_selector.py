class SelectorPageMainUsed:
    """Селекторы для парсинга основной части страницы б/у машины"""
    sold_status = 'div.CardSold__title:nth-child(1)'
    main = '.CardInfo__list-MZpc1'
    title = '.CardHead__title'
    price = '.OfferPriceCaption__price'
    place = '.MetroListPlace__regionName'
    tech_link = ".Button_width_full"
    tech_link_2 = '.CardInfo__link-LIbAF > a:nth-child(1)'


class SelectorPageUsed:
    """Селекторы для парсинг дополнительной информации со страницы б/у машины"""
    can_by = '.CardInfoRow_availability > div:nth-child(2) > a:nth-child(1)'
    generation = '.CardInfoRow_superGen > div:nth-child(2)'
    year = '.CardInfoRow_year > div:nth-child(2) > a:nth-child(1)'
    km = '.CardInfoRow_kmAge > div:nth-child(2)'
    body = '.CardInfoRow_bodytype > div:nth-child(2) > a:nth-child(1)'
    color = '.CardInfoRow_color > div:nth-child(2) > a:nth-child(1)'
    engine = '.CardInfoRow_engine > div:nth-child(2) > div:nth-child(1)'
    package = '.CardInfoRow_complectationOrEquipmentCount > div:nth-child(2)'
    tax = '.CardInfoRow_transportTax > div:nth-child(2)'
    transmission = '.CardInfoRow_transmission > div:nth-child(2)'
    driver = '.CardInfoRow_drive > div:nth-child(2)'
    wheel = '.CardInfoRow_wheel > div:nth-child(2)'
    state = '.CardInfoRow_state > div:nth-child(2)'
    owners_count = '.CardInfoRow_ownersCount > div:nth-child(2)'
    pts = '.CardInfoRow_pts > div:nth-child(2)'
    customs = '.CardInfoRow_customs > div:nth-child(2)'


class SelectorPageMainNew:
    """Селекторы для парсинга основной части страницы новой машины"""
    sold = '.CardSold__infoCol'
    main = '.CardInfoGrouped__list'
    title = '.CardHead__title'
    price = '.OfferPriceCaption__price'
    place = '.MetroListPlace__regionName'
    tech_link = 'a.Button:nth-child(3)'
    tech_link_2 = 'a.Button_color_gray:nth-child(2)'


class SelectorPageNew:
    """Селекторы для парсинга дополнительной информации со страницы новой машины"""
    generation = 'a.CardInfoGroupedRow__cellValue_complectationName'
    year = 'li.CardInfoGroupedRow:nth-child(2) > div:nth-child(2) > div:nth-child(2)'
    body = 'li.CardInfoGroupedRow:nth-child(3) > div:nth-child(2) > a:nth-child(2)'
    color = 'li.CardInfoGroupedRow:nth-child(9) > div:nth-child(2) > a:nth-child(2)'
    engine = 'li.CardInfoGroupedRow:nth-child(5) > div:nth-child(2) > div:nth-child(2)'
    package = 'span.Link:nth-child(2)'
    tax = 'li.CardInfoGroupedRow:nth-child(6) > div:nth-child(2) > div:nth-child(2)'
    transmission = 'li.CardInfoGroupedRow:nth-child(7) > div:nth-child(2) > div:nth-child(2)'
    driver = 'li.CardInfoGroupedRow:nth-child(8) > div:nth-child(2) > div:nth-child(2)'
