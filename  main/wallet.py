import base64
import time

from aptos_sdk.account import Account


class Wallet:
    def __init__(self, private_key: str | None = None):
        if private_key:
            self.account = Account.load_key(private_key)
        else:
            self.account = Account.generate()
        if private_key:
            self.private_key = private_key
        else:
            self.private_key = self.account.private_key

    def signa(self, massage: str):
        byte_message = massage.encode()

        signature_hex = self.account.sign(byte_message)

        signature_bytes = bytes.fromhex(str(signature_hex)[2:])

        signature_base64 = base64.b64encode(signature_bytes).decode('utf-8')
        return signature_base64

    @staticmethod
    def generate_massage():
        current_time = int(time.time())
        rounded_time = int(current_time - current_time % 3600)
        massage = f'APTOS\nmessage: Welcome to the Castile platform’s wallet management process. By clicking to sign in, you are initiating the linking of your wallet address to your Castile account as a deposit wallet. This request will not trigger a blockchain transaction or cost any gas fees.\nnonce: {rounded_time}'
        return massage


if __name__ == '__main__':
    wallet = Wallet
