def get_headers():
    cookies = {'_yasc': 'R2APlF2D/HxxLiO3CY+ozAihHEtQsz8fE5cyGCJy8I7KlFwrDbjhaPS3HTNoCP2elABp',
               'Session_id': 'noauth:1717062121',
               'sso_status': 'sso.passport.yandex.ru:synchronized'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://sso.auto.ru/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=1',
    }

    return headers, cookies


def get_headers_3():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://sso.auto.ru/',
        'Connection': 'keep-alive',
        'Cookie': '_yasc=R2APlF2D/HxxLiO3CY+ozAihHEtQsz8fE5cyGCJy8I7KlFwrDbjhaPS3HTNoCP2elABp; '
                  'Session_id=noauth:1717062121; '
                  'sso_status=sso.passport.yandex.ru:synchronized;',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=1',
    }
    return headers


def get_headers_2():
    cookies = {
        'suid': '335aba9d667dd78ff3de11772ca702ea.49452dff846a7969160f8cc81fbc1781',
        'autoru_sid': 'a%3Ag6617f93b2nekpa2iu1v0i5c2ub85gtv.05b9698f7e9bcde5017ff76e53cc8cc7%'
                      '7C1715381550956.604800.PhDDbtu42AtlCOkrjB_DPw.XhvCBktxUXvIa8idYuZNPcSBVxlSmQH_bdE9ukNC8hE',
        '_yasc': '2aQEkQWSsL/iHo5hDEGbfFFp4Crdvj/wvnW8wNpuWwY3YsmPt8ApcwzVtKTWOu/zuWbK',
        'i': 'tvxjrBixP+NanmJFqdYMqSPMujpkT/f2DvmCArYzxwzfwWUhbYlIbY8q1RrjsUhZDptidETM93C+Gx/PQ95FWxrH1a0=',
        'yandexuid': '2899243411712847163',
        'mda2_beacon': '1715278617329',
        'layout-config': '{"screen_height":864,"screen_width":1536,"win_width":1536,"win_height":558.4000244140625}',
        'fp': '2bcbd34333ba388b7c7875eaee6b450d%7C1712847167380',
        'cycada': 'Q07O1q0Jq5fOc5uCHeVGXmhXfxOp+c2hXUzI7c3OjsQ=',
        'autoru-visits-count': '28',
        '_ym_uid': '1712847166133907112',
        'listing_view': '%7B%22output_type%22%3Anull%2C%22version%22%3A1%7D',
        'gids': '213',
        'mindboxDeviceUUID': '684ab371-c2a8-4951-934e-39fdec217096',
        'directCrm-session': '%7B%22deviceGuid%22%3A%22684ab371-c2a8-4951-934e-39fdec217096%22%7D',
        'autoruuid': 'g6617f93b2nekpa2iu1v0i5c2ub85gtv.05b9698f7e9bcde5017ff76e53cc8cc7',
        'gradius': '200',
        '_csrf_token': 'e3e0023fa25a5757065b8a7b9efa6488ca3c3d2aa500dcb4',
        'from': 'direct',
        'ys': 'c_chck.3598606168',
        'autoru_sso_blocked': '1',
        'Session_id': 'noauth:1715278617',
        'sessar': '1.1189.CiA9pvW9xAe4QMpa_ka97JjtotTMbRQ_nNb04-lV-HrjAQ.qey7xHFhCl2tHSMFtrw-bsEwIL6kj99f0E0oYmKcgoQ',
        'sso_status': 'sso.passport.yandex.ru:synchronized',
        '_ym_isad': '2',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://sso.auto.ru/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-User': '?1'
    }
    return headers, cookies
