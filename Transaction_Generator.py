from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence, TYPE_RELATIVE_TIMELOCK, \
    TYPE_ABSOLUTE_TIMELOCK
from bitcoinutils.script import Script
from Id_Class import Id
from Helper_Functions import Print_TX
from typing import List


def main():
    """
    Run main to print the size of the different transactions to the console
    """

    # Configuration ####################################################################################################

    id_s0 = Id(
        '72e872b404f465413a31efae3bfa9272ab2f7a37f01e395d4c6cc8d4af9451f6')  # addr: morixRGbkepJL1yioL7noKp6iMNxXXmpW7
    id_s1 = Id(
        '648bf1e63172b42bc9673f2b147de6bf8803303f73c59dbee8e9bea8db8da184')  # addr: mpQaHdvF1nKY7Ak9XrgTU8iFbkKftgoz8F
    id_r0 = Id(
        '53f7914c96e3b94edaf5ea6501cca49076631ef81c1279ca3b735c5826a53291')  # addr: mpe3bMJcJRvebotZfqLnNiGGm8bmNVjXW4
    id_r1 = Id(
        '63376bb1b98e2ae3306be70e32a3c5bdbe72c2a8921c41c136ce93dacd22e49c')  # addr: mqqMV6WPc36VQZGnU4ekL8RRgodofVEj2U

    tx_state_in = TxInput('352459366c063d1dda6a930214eb0eb70e39b9ac0e6489dc1bdb85181d7035d6',
                          0)  # 0.00009 BTC = 9000 satoshi
    tx_in = TxInput('94d009dff936a23fd37fa92cd5ba1f10c5848ee92376540c63774cc230bbc760',
                    1)  # 0.0001 BTC = 10000 satoshi
    eps = 1
    n = 2
    t = 5
    t_cd = 2
    delta = 1
    a = 1000
    balLeft = 4000
    balRight = 5000
    txin_cash = 10000
    fee = 1000

    # Generating TxIn ##################################################################################################

    txepintx = Gen_TxIn(tx_in, id_r0, [id_r0, id_s0, id_s1], n * eps, txin_cash - n * eps - fee)
    Print_TX(txepintx, 'Main: txepintx')

    # Generating TxEp ##################################################################################################
    txEp = Gen_txEp([id_r0], [id_r0], TxInput(txepintx.get_hash(), 0), eps, t_cd)
    # one signature in input / one output
    Print_TX(txEp, 'Test: tx_ep 1 output')

    txEp = Gen_txEp([id_r0], [id_r0, id_r1], TxInput(txepintx.get_hash(), 0), eps, t_cd)
    # one signature in input / two outputs
    Print_TX(txEp, 'Test: tx_ep 2 output')

    txEp = Gen_txEp([id_r0, id_s0], [id_r0], TxInput(txepintx.get_hash(), 0), eps, t_cd)
    # two signatures in input / one output
    Print_TX(txEp, 'Test: tx_ep 3 output')

    txEp = Gen_txEp([id_r0, id_s0], [id_r0, id_r1], TxInput(txepintx.get_hash(), 0), eps, t_cd)
    # two signatures in input / two outputs
    Print_TX(txEp, 'Test: tx_ep 4 output')

    txEp = Gen_txEp([id_r0, id_s0, id_s1], [id_r0], TxInput(txepintx.get_hash(), 0), eps, t_cd)
    # three signatures in input / one output
    Print_TX(txEp, 'Test: tx_ep 5 output')

    txEp = Gen_txEp([id_r0, id_s0, id_s1], [id_r0, id_r1], TxInput(txepintx.get_hash(), 0), eps, t_cd)
    # three signatures in input / two outputs
    Print_TX(txEp, 'Main: tx_ep 6 output')

    # Generating TxState ###############################################################################################
    tx_state = Gen_State(tx_state_in, id_s0, id_r0, a, balLeft, balRight, fee, t, delta)
    Print_TX(tx_state, 'Main: tx_state')

    # Generating TxP ###################################################################################################
    tx_p = Gen_TxP(TxInput(txEp.get_hash(), 0), TxInput(tx_state.get_hash(), 0), id_s0, id_r0, a, eps, t_cd, t, delta)
    Print_TX(tx_p, 'Main: tx_p')

    # Generating TxR ###################################################################################################
    tx_r = Gen_TxR(TxInput(tx_state.get_hash(), 0), id_s0, id_r0, a, t, delta)
    Print_TX(tx_r, 'Main: tx_r')

    # Generating TxTrans ###############################################################################################
    tx_trans = Gen_TxTrans(tx_state_in, id_s0, id_r0, a, balLeft, balRight)
    Print_TX(tx_trans, 'Main: tx_trans')


# Functions ############################################################################################################

def Gen_TxIn(tx_in: TxInput, id_sender: Id, id_list: List[Id], a: float, x_r: float) -> Transaction:
    # tx_in must hold at least n times eps coins plus a fee.
    r_scr = Script(['OP_3', id_list[0].pk.to_hex(), id_list[1].pk.to_hex(), id_list[2].pk.to_hex(),
                    'OP_3', 'OP_CHECKMULTISIG'])

    output_List = [TxOutput(a, r_scr.to_p2sh_script_pub_key())]
    if x_r > 0:
        output_List.append(TxOutput(x_r, id_sender.p2pkh))

    tx_ep_in = Transaction([tx_in], output_List)

    sig_sender = id_sender.sk.sign_input(tx_ep_in, 0, id_sender.p2pkh)

    tx_in.script_sig = Script([sig_sender, id_sender.pk.to_hex()])

    return tx_ep_in


def Gen_txEp(id_in: List[Id], id_out: List[Id], tx_in: TxInput, eps: float = 1, t: int = 2) -> Transaction:
    # tx_in must hold at least n times eps coins

    out_list = []
    for id in id_out:
        script = Script(['OP_IF',
                         id.pk.to_hex(), 'OP_CHECKSIGVERIFY', t, 'OP_CHECKSEQUENCEVERIFY',
                         'OP_ENDIF'])
        out_list.append(TxOutput(eps, script.to_p2sh_script_pub_key()))

    txEp = Transaction([tx_in], out_list)

    if len(id_in) == 1:
        r_scr = Script(['OP_1', id_in[0].pk.to_hex(), 'OP_1', 'OP_CHECKMULTISIG'])
    elif len(id_in) == 2:
        r_scr = Script(['OP_2', id_in[0].pk.to_hex(), id_in[1].pk.to_hex(), 'OP_2', 'OP_CHECKMULTISIG'])
    else:
        r_scr = Script(['OP_3', id_in[0].pk.to_hex(), id_in[1].pk.to_hex(), id_in[2].pk.to_hex(),
                        'OP_3', 'OP_CHECKMULTISIG'])

    unlock_script = [0x0]
    for id in id_in:
        unlock_script.append(id.sk.sign_input(txEp, 0, r_scr))
    unlock_script.append(r_scr.to_hex())

    tx_in.script_sig = Script(unlock_script)
    return txEp


def Gen_State(tx_in: TxInput, id_s: Id, id_r: Id, a: float, x_s: float, x_r: float, fee: float,
              t: int, delta: int = 0x01) -> Transaction:
    new_script = Script(['OP_IF',
                         'OP_2', id_s.pk.to_hex(), id_r.pk.to_hex(), 'OP_2', 'OP_CHECKMULTISIGVERIFY',
                         delta, 'OP_CHECKSEQUENCEVERIFY',
                         'OP_ELSE',
                         id_s.pk.to_hex(), 'OP_CHECKSIGVERIFY', t, 'OP_CHECKLOCKTIMEVERIFY',
                         'OP_ENDIF'])

    tx_out0 = TxOutput(a, new_script.to_p2sh_script_pub_key())
    tx_out1 = TxOutput(x_s - a - fee, id_s.p2pkh)
    tx_out2 = TxOutput(x_r, id_r.p2pkh)

    tx = Transaction([tx_in], [tx_out0, tx_out1, tx_out2])

    r_scr = Script(['OP_2', id_r.pk.to_hex(), id_s.pk.to_hex(), 'OP_2', 'OP_CHECKMULTISIG'])
    unlock_script = [0x00, id_r.sk.sign_input(tx, 0, r_scr), id_s.sk.sign_input(tx, 0, r_scr), r_scr.to_hex()]
    tx_in.script_sig = Script(unlock_script)

    return tx


def Gen_TxP(tx_in_txEp: TxInput, tx_in_state: TxInput, id_s: Id, id_r: Id,
            a: float, eps: float = 1, t_cd: int = 2, t: int = 5, delta: int = 0x01) -> Transaction:
    tx_out0 = TxOutput(a + eps, id_r.p2pkh)
    tx = Transaction([tx_in_txEp, tx_in_state], [tx_out0])

    r_scr = Script(['OP_IF',
                    id_r.pk.to_hex(), 'OP_CHECKSIGVERIFY', t_cd, 'OP_CHECKSEQUENCEVERIFY',
                    'OP_ENDIF'])

    tx_in_txEp.script_sig = Script([id_r.sk.sign_input(tx, 0, r_scr), r_scr.to_hex()])

    r_scr = Script(['OP_IF',
                    'OP_2', id_s.pk.to_hex(), id_r.pk.to_hex(), 'OP_2', 'OP_CHECKMULTISIGVERIFY',
                    delta, 'OP_CHECKSEQUENCEVERIFY',
                    'OP_ELSE',
                    id_r.pk.to_hex(), 'OP_CHECKSIGVERIFY', t, 'OP_CHECKLOCKTIMEVERIFY',
                    'OP_ENDIF'])
    unlock_script = [0x00, id_r.sk.sign_input(tx, 0, r_scr), id_s.sk.sign_input(tx, 0, r_scr), r_scr.to_hex()]
    tx_in_state.script_sig = Script(unlock_script)

    return tx


def Gen_TxR(tx_in_state: TxInput, id_s: Id, id_r: Id, a: float, t: int = 5, delta: int = 0x01) -> Transaction:
    tx_out0 = TxOutput(a, id_s.p2pkh)
    tx = Transaction([tx_in_state], [tx_out0])

    r_scr = Script(['OP_IF',
                    'OP_2', id_s.pk.to_hex(), id_r.pk.to_hex(), 'OP_2', 'OP_CHECKMULTISIGVERIFY',
                    delta, 'OP_CHECKSEQUENCEVERIFY',
                    'OP_ELSE',
                    id_r.pk.to_hex(), 'OP_CHECKSIGVERIFY', t, 'OP_CHECKLOCKTIMEVERIFY',
                    'OP_ENDIF'])

    unlock_script = [id_s.sk.sign_input(tx, 0, r_scr), r_scr.to_hex()]
    tx_in_state.script_sig = Script(unlock_script)

    return tx


def Gen_TxTrans(tx_in: TxInput, id_s: Id, id_r: Id, a: float, x_s: float, x_r: float) -> Transaction:
    tx_out0 = TxOutput(x_s - a, id_s.p2pkh)
    tx_out1 = TxOutput(x_r + a, id_r.p2pkh)

    tx = Transaction([tx_in], [tx_out0, tx_out1])

    r_scr = Script(['OP_2', id_r.pk.to_hex(), id_s.pk.to_hex(), 'OP_2', 'OP_CHECKMULTISIG'])
    unlock_script = [0x00, id_r.sk.sign_input(tx, 0, r_scr), id_s.sk.sign_input(tx, 0, r_scr), r_scr.to_hex()]

    tx_in.script_sig = Script(unlock_script)

    return tx


if __name__ == "__main__":
    main()
