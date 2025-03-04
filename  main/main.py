import base64

import aiohttp

import asyncio

import twitter

from id_tasks import Tasks

from for_proxy import format_proxy

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
    def __init__(self, mail: str | None = None, password: str | None = None, cookies: dict | None = None, headers: dict | None = None, private_key: str | None = None, proxy: str | None = None):
        self.mail = mail
        self.password = password
        self.cookies = cookies
        self.headers = headers
        self.proxy = proxy
        self.wallet = Wallet(private_key=private_key)


    async def request(self, url: str, type_request: str, json_data: dict | None = None, params: dict | None = None, for_json: bool = False):

        async with aiohttp.ClientSession() as session:

            if type_request == 'post':
                async with session.post(url, json=json_data, headers=self.headers, proxy=self.proxy) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        raise Exception(f"Ошибка при выполнении запроса: {response.status}, {await response.text()}")

            elif type_request == 'get':
                async with session.get(url, headers=self.headers, proxy=self.proxy, params=params) as response:
                    if response.status == 200:
                        if for_json:
                            return response
                        data = await response.json()
                        return data
                    else:
                        raise Exception(f"Ошибка при выполнении запроса: {response.status}, {await response.text()}")
            else:
                print('Check type request')

    async def register(self):
        url = 'https://castile.world/api/guest/register'  # Укажите ваш URL
        json_data = {
            'email': self.mail,
            'code': '888888',
            'password': self.password,
            'password_confirm': self.password,
            'agree': True,
        }
        response_data = await self.request(url=url, type_request='post', json_data=json_data)
        authorization = f'Bearer {response_data["data"]["auth"]}'
        self.headers['authorization'] = authorization
        print(response_data)

    async def login(self):
        url = 'https://castile.world/api/guest/login'
        json_data = {
            'email': self.mail,
            'password': self.password,
        }
        response_data = await self.request(url=url, type_request='post', json_data=json_data)
        authorization = f'Bearer {response_data["data"]["auth"]}'
        self.headers['authorization'] = authorization
        print(response_data)

    async def quantity_points(self):
        url = 'https://castile.world/api/task/pointsInfo'
        json_data = {}
        response_data = await self.request(url, 'post', json_data)
        print(response_data['data']['points'])

    async def wallet_linked(self):
        url = 'https://castile.world/api/user/getWallet'
        response_data = await self.request(url=url, type_request='post')
        return response_data

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
        wallet_linked = await self.wallet_linked()
        if len(wallet_linked['data']) == 0:
            response_data = await self.request(url=url, type_request= 'post', json_data=json_data)
        else:
            print(f'Wallet for account: {self.mail} already bind')

    async def get_user_info(self) -> dict:
        url = 'https://castile.world/api/user/pullUserInfo'
        response_data = await self.request(url, 'post')
        return response_data

    async def bind_twitter(self, auth_token: str | None):

        url = 'https://www.castile.world/api/twitter/receive'

        data = await self.get_user_info()
        uid = data.get('data', {}).get('uid')

        decoded_string = f'{uid}|bind_twitter|'

        byte_string = decoded_string.encode('utf-8')

        encoded_bytes = base64.b64encode(byte_string)

        state = encoded_bytes.decode('utf-8')

        auth_code_params = {
            'response_type': 'code',
            'client_id': 'VktCa2VJcjVsdkZoSnFDLUpHanQ6MTpjaQ',
            'redirect_uri': 'https://www.castile.world/api/twitter/receive',
            'scope': 'users.read tweet.read',
            'state': state,
            'code_challenge': 'challenge',
            'code_challenge_method': 'plain',
        }

        twitter_account = twitter.Account(auth_token=auth_token)

        async with twitter.Client(twitter_account, proxy=self.proxy) as twitter_client:
            auth_code = await twitter_client.oauth2(**auth_code_params)

        params = {
            'state': state,
            'code': auth_code,
        }

        response_data = await self.request(url=url, type_request='get',params=params, for_json=True)
        print(response_data)

    async def completed_task(self):
        url = 'https://castile.world/gapi/task/v1/task'
        for good_id in Tasks.need_id:
            params = {
                'id': good_id,
                'params': '',
            }
            response_data = await self.request(url=url, type_request='get', params=params)

    async def claim_reward(self):
        url = 'https://castile.world/gapi/task/v1/reward'
        for good_id in Tasks.need_id:
            params = {
                'id': good_id,
            }
            response_data = await self.request(url=url, type_request='get', params=params)

async def main():
    account = Account('zxcqweasd000@yandex.ru', 'A12fsaiki43fj', headers=headers, proxy=format_proxy('user210578:q67d4i@212.116.242.66:7486'))
    # await account.register()
    # await account.login()
    # await account.bind_wallet()
    # await account.bind_twitter(auth_token='6173c4866966a15249685e21d800bdd281ddb15f')
    # await account.quantity_points()
    # await account.completed_task()
    # await account.claim_reward()
    # await account.quantity_points()
    # print(await account.get_user_info())

if __name__ == '__main__':
    asyncio.run(main())


