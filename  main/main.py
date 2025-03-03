import aiohttp

import asyncio


from fake_useragent import FakeUserAgent

from wallet import Wallet

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


class Account:
    def __init__(self, mail: str, password: str, cookies: dict | None = None, headers: dict | None = None, private_key: str | None = None):
        self.mail = mail
        self.password = password
        self.cookies = cookies
        self.headers = headers
        self.wallet = Wallet(private_key=private_key)

    async def post_request_with_headers_and_cookies(self, url: str, json_data: dict):

        async with aiohttp.ClientSession() as session:

            async with session.post(url, json=json_data, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    raise Exception(f"Ошибка при выполнении запроса: {response.status}, {await response.text()}")


    async def register(self):
        url = 'https://castile.world/api/guest/register'  # Укажите ваш URL
        json_data = {
            'email': self.mail,
            'code': '888888',
            'password': self.password,
            'password_confirm': self.password,
            'agree': True,
        }
        response_data = await self.post_request_with_headers_and_cookies(url, json_data)
        authorization = f'Bearer {response_data["data"]["auth"]}'
        self.headers['authorization'] = authorization
        print(response_data)


    async def login(self):
        url = 'https://castile.world/api/guest/login'
        json_data = {
            'email': self.mail,
            'password': self.password,
        }
        response_data = await self.post_request_with_headers_and_cookies(url, json_data)
        authorization =f'Bearer {response_data["data"]["auth"]}'
        self.headers['authorization'] = authorization
        print(response_data)

    async def quantity_points(self):
        url = 'https://castile.world/api/task/pointsInfo'
        json_data = {}
        response_data = await self.post_request_with_headers_and_cookies(url, json_data)
        print(response_data['data']['points'])

    async def bind_wallet(self):
        url = 'https://castile.world/api/user/bindWallet'
        json_data = {
            'sign': self.wallet.signa(self.wallet.generate_massage()),
            'publicKey': str(self.wallet.account.public_key()),
            'address': str(self.wallet.account.address()),
            'wallet': 'Petra',
            'message': self.wallet.generate_massage(),
            'type': 'Aptos',
        }
        response_data = await self.post_request_with_headers_and_cookies(url, json_data)
        print(response_data)

async def main():
    account = Account('zxcqweasd123456789@yandex.ru', 'A12fsaiki43fj', headers=headers)
    await account.login()
    # await account.bind_wallet()

if __name__ == '__main__':
    asyncio.run(main())


