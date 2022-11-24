# Zizou Ethereum Wallet Cracker using Parallel-CPU (100%) and Blockchain as Server/Database
----
First Install The Packages :
```
pip install -r requirements.txt
```
* Download The Ethereum Wallet Addresses Containing +10M Valid Addresses HERE: [https://bit.ly/ethadresses]
* Create Folder `/DbAddresses` and put in the downloaded addresses
* Run the program Encryption/GenerateEncryptionKeys.py to generate your Public and Private Keys
* create your .env File and store your Private Data. .env File should look like the following:
```
PUBLIC_KEY=
PRIVATE_KEY=
WEB3_INFURA_PROJECT_ID=
DECRYPTION_PRIVATE_KEY=
```
After install Run The Program With This Command On Terminal or Console (`ZizouEtherWallet.py`). !Don't forget to replace the Public-Key by yours!

Windows:
```
python ZizouEtherWallet.py
```

```
python3 ZizouEtherWallet.py
```

The Result [Mnemonic + Address] will be saved into a File and logged as encrypted strings in the Blockchain Contract which is used as our Server and Database so that the programm can be run on multiple Nodes.
