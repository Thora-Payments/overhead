import binascii
import hashlib
from bitcoinutils.transactions import Transaction
import random


def Gen_Secret():
    """
        Replace this method with a secure random generator
    """
    rand = ''

    for i in range(0, 32):
        temp = random.randrange(0, 255)
        temp = hex(temp)[2:]
        if len(temp) == 1:
            temp = f'0{temp}'
        rand += temp

    return rand


def Hash256(hex_string: str) -> str:
    data = binascii.unhexlify(hex_string)
    h1 = hashlib.sha256(data)
    h2 = hashlib.sha256(h1.digest())
    return h2.hexdigest()


def Print_TX(tx: Transaction, name: str) -> None:
    print(f'{name}: {int(len(tx.serialize()) / 2)} Bytes')
    print(tx.serialize())
    print('----------------------------------')

