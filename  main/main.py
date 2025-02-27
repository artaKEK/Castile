import requests

import aiohttp

import asyncio

from fake_useragent import FakeUserAgent


async def post_request_with_headers_and_cookies(url, json_data):
    cookie_jar = aiohttp.CookieJar()

    async with aiohttp.ClientSession(cookie_jar=cookie_jar) as session:
        # Устанавливаем cookie
        cookie_jar.update_cookies({
    '_ga': 'GA1.1.2067863700.1739889339',
    '_ga_GNVVWBL3J9': 'GS1.1.1740652159.4.0.1740652167.0.0.0',
    '_ga_DV94HJBHP1': 'GS1.1.1740652136.4.1.1740652169.0.0.0',
})

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru,en;q=0.9',
            'authorization': 'Bearer null',
            'content-type': 'application/json; charset=UTF-8',
            # 'cookie': '_ga=GA1.1.2067863700.1739889339; _ga_GNVVWBL3J9=GS1.1.1740652159.4.0.1740652167.0.0.0; _ga_DV94HJBHP1=GS1.1.1740652136.4.1.1740652169.0.0.0',
            'origin': 'https://castile.world',
            'priority': 'u=1, i',
            'referer': 'https://castile.world/task',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "YaBrowser";v="25.2", "Yowser";v="2.5"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': FakeUserAgent().random,
        }

        async with session.post(url, json=json_data, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Ошибка при выполнении запроса: {response.status}, {await response.text()}")


async def register():
    json_data = {
        'email': 'zxcqweasd1234@gmail.ru',
        'code': '888888',
        'password': 'GDt-8Bw-9c7-X27',
        'password_confirm': 'GDt-8Bw-9c7-X27',
        'agree': True,
    }
    url = 'https://castile.world/api/guest/register'  # Укажите ваш URL
    response_data = await post_request_with_headers_and_cookies(url, json_data)
    print(response_data)


async def login():
    json_data = {
        'email': 'zxcqweasd1234@gmail.ru',
        'password': 'GDt-8Bw-9c7-X27',
    }
    url = 'https://castile.world/api/guest/login'
    response_data = await post_request_with_headers_and_cookies(url, json_data)
    print(response_data)

async def quantity_points():
    json_data = {}
    url = 'https://castile.world/api/task/pointsInfo'
    response_data = await post_request_with_headers_and_cookies(url, json_data)
    print(response_data['data']['points'])

if __name__ == '__main__':
    asyncio.run(login())