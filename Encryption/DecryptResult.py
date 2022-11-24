import rsa
from dotenv import load_dotenv, find_dotenv
import os
from web3 import Web3

load_dotenv(find_dotenv())

decryptionPrivateKey = os.getenv(
    'DECRYPTION_PRIVATE_KEY').replace(' ', '').split(',')
decryption_private_key = rsa.PrivateKey(
    int(decryptionPrivateKey[0]), int(decryptionPrivateKey[1]), int(decryptionPrivateKey[2]), int(decryptionPrivateKey[3]), int(decryptionPrivateKey[4]))

web3 = Web3(Web3.HTTPProvider(
    'https://goerli.infura.io/v3/'+os.getenv('WEB3_INFURA_PROJECT_ID')))

contract_instance = web3.eth.contract(
    address="0x09BdA56F59A692464673b265f4BFDCFCc59b29d1", abi='[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"string","name":"_add","type":"string"},{"internalType":"string","name":"_mnem","type":"string"}],"name":"addElement","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"retrieve","outputs":[{"components":[{"internalType":"string","name":"addr","type":"string"},{"internalType":"string","name":"mnem","type":"string"}],"internalType":"struct SimpleStorage.FoundAddr[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}]')

results = contract_instance.functions.retrieve().call()

for result in results:
    address = rsa.decrypt(bytes.fromhex(
        result[0]), decryption_private_key).decode()
    mnemo = rsa.decrypt(bytes.fromhex(
        result[1]), decryption_private_key).decode()

    f = open("ResultFromBlockchain.txt", "a")
    f.write("\nAddress = " + str(address))
    f.write("\nMnemonic = " + str(mnemo))
    f.write(
        "\n=========================================================\n"
    )
    f.flush()
    f.close()
