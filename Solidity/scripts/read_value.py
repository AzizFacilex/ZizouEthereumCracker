from brownie import AddressLogs, accounts, config


def read_contract():
    address_logs = AddressLogs[-1]
    print(address_logs.retrieve())


def main():
    read_contract()
