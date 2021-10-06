from bitcoinutils.keys import P2pkhAddress, PrivateKey
import Network_Initiator as Init
from Helper_Functions import Gen_Secret

Init.initNetwork()


class Id:
    """
    Helper class for handling identity related keys and addresses easily
    """

    def __init__(self):
        rand = Gen_Secret()
        self.sk = PrivateKey(secret_exponent=int(rand, 16))
        self.pk = self.sk.get_public_key()
        self.addr = self.pk.get_address().to_string()
        self.p2pkh = P2pkhAddress(self.addr).to_script_pub_key()
