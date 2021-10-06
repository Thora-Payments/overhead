import bitcoinutils.setup as setup


def initNetwork():
    if setup.get_network() is None:
        setup.setup('testnet')

