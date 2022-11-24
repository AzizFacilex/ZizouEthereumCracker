from hdwallet.symbols import ETH as SYMBOL
from colorama import Fore, Style
import pickle
from hdwallet.utils import generate_mnemonic
from typing import Optional
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet import BIP44HDWallet
from mnemonic import Mnemonic
from multiprocessing import Pool
import os
import rsa
from web3 import Web3
from dotenv import load_dotenv, find_dotenv


def sendTransaction(address, mnemo, contract_instance, account, private_key1):
    nonce = web3.eth.getTransactionCount(account)
    # replace by your generated public key
    encryptionPublicKey = os.getenv(
        'ENCRYPTION_PUBLIC_KEY').replace(' ', '').split(',')
    pub = rsa.PublicKey(
        encryptionPublicKey[0], encryptionPublicKey[1])
    encAddress = rsa.encrypt(address.encode(),
                             pub).hex()
    encMnemp = rsa.encrypt(mnemo.encode(),
                           pub).hex()
    transaction = contract_instance.functions.addElement(
        encAddress,
        encMnemp).buildTransaction({
            'type': '0x2',
            'maxFeePerGas': web3.toWei('250', 'gwei'),
            'maxPriorityFeePerGas': 1,
            'from': '0x18061f6B7D6E5B9C2eF34441c3C094eFcaA8e0Fc',
            'nonce': nonce,
            'chainId': 5
        })
    signed_txn = web3.eth.account.signTransaction(
        transaction, private_key=private_key1)
    web3.eth.send_raw_transaction(signed_txn.rawTransaction)


def main(*i):
    z = 1
    toReturn = {}
    mnemo = Mnemonic("english")
    PASSPHRASE: Optional[str] = None
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
        cryptocurrency=EthereumMainnet)
    while True:
        MNEMONIC: str = generate_mnemonic(language="english", strength=128)
        while not mnemo.check(MNEMONIC):
            MNEMONIC = generate_mnemonic(language="english", strength=128)
        bip44_hdwallet.from_mnemonic(
            mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
        )
        addr = bip44_hdwallet.p2pkh_address()
        toReturn[addr] = MNEMONIC
        z += 1
        if z > 10000:
            return toReturn


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    account = os.getenv('PUBLIC_KEY')
    private_key = os.getenv('PRIVATE_KEY')
    web3 = Web3(Web3.HTTPProvider(
        'https://goerli.infura.io/v3/'+os.getenv('WEB3_INFURA_PROJECT_ID')))
    contract_instance = web3.eth.contract(
        address="0x09BdA56F59A692464673b265f4BFDCFCc59b29d1", abi='[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"string","name":"_add","type":"string"},{"internalType":"string","name":"_mnem","type":"string"}],"name":"addElement","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"retrieve","outputs":[{"components":[{"internalType":"string","name":"addr","type":"string"},{"internalType":"string","name":"mnem","type":"string"}],"internalType":"struct SimpleStorage.FoundAddr[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}]')

    zizou = """
//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
//   ____ _  ____ ___  _ _                                                     @
//  |_  /| ||_  /| . || | |    ==> Keep work up                                @
//   / / | | / / | | || ' |    ==> Donate ETH at: 0x0000000000000000000000000  @
//  /___||_|/___|`___'`___'    ==> GitHub: @AzizFacilex                        @
//                                                                             @
//   ___  ___  _ _  ___  ___  ___  _ _  __ __   _ _ _  ___  _    _    ___  ___ @
//  | __>|_ _|| | || __>| . \| __>| | ||  \  \ | | | || . || |  | |  | __>|_ _|@
//  | _>  | | |   || _> |   /| _> | ' ||     | | | | ||   || |_ | |_ | _>  | | @
//  |___> |_| |_|_||___>|_\_\|___>`___'|_|_|_| |__/_/ |_|_||___||___||___> |_| @ 
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                                                                                
    """

    binaryFiles = "DbAddresses/Adresses"
    print("\n", Fore.RED,
          str(zizou), Style.RESET_ALL)
    numberOfResults = 0
    numberOfCalculations = 0
    itemlist = []
    for i in range(1, 71):
        with open(binaryFiles + str(i), "rb") as fp:
            itemlist += pickle.load(fp)
    with open(binaryFiles + "X", "rb") as fp:
        itemlist += pickle.load(fp)
    add = set(itemlist)
    itemlist = None
    cpuCount = os.cpu_count()
    with Pool(cpuCount) as processes_pool:
        while True:
            resultList = processes_pool.map(main, range(cpuCount))
            for element in resultList:
                for resultAdress in add.intersection(element.keys()):
                    mnemo = element.get(resultAdress)
                    f = open("EthereumWinnerWallet.txt", "a")
                    f.write("\nAddress = " + str(resultAdress))
                    f.write("\nMnemonic = " + str(mnemo))
                    f.write(
                        "\n=========================================================\n"
                    )
                    f.flush()
                    f.close()
                    print("Winner information Saved On text file")
                    numberOfResults += 1
                    sendTransaction(resultAdress, mnemo,
                                    contract_instance, account, private_key)

            numberOfCalculations += 10000 * cpuCount
            print(
                Fore.GREEN,
                str(numberOfResults),
                Fore.WHITE,
                str(numberOfCalculations),
                Fore.YELLOW,
                "Total Scan Checking",
                end="\r",
            )
