import base64

from aptos_sdk.account import Account
from aptos_sdk.ed25519 import Signature

private_key = '0x16bd6732fbd8344dafc7398bd075ca17edb1c1eb29db5787574d528eabfa06b5'

account = Account.load_key(private_key)

print(type(str(account.public_key())))