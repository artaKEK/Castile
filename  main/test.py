import asyncio
import base64
from main import Account

account = Account()

async def fun():

    decoded_string = f'{uid}|bind_twitter|'


    byte_string = decoded_string.encode('utf-8')

    # Кодируем байты в формат Base64
    encoded_bytes = base64.b64encode(byte_string)

    # Преобразуем обратно в строку для удобства
    encoded_string = encoded_bytes.decode('utf-8')

    # Вывод результата
    print(decoded_string)
    print(encoded_string)

if __name__ == '__main__':
    asyncio.run(fun())