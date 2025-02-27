import aiohttp
import asyncio

async def post_data(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            # Проверяем успешность ответа
            if response.status == 200:
                data = await response.json()  # Получаем данные в формате JSON
                return data
            else:
                raise Exception(f"Ошибка при отправке данных: {response.status}")

async def main():
    url = 'https://api.example.com/data'  # Укажите ваш URL
    payload = {'key': 'value'}  # Данные, которые вы хотите отправить
    try:
        response = await post_data(url, payload)
        print(response)  # Обработка полученных данных
    except Exception as e:
        print(e)

# Запуск главной функции
if __name__ == '__main__':
    print(asyncio.run(post_data('https://api.example.com/data', )))