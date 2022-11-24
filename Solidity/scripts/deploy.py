from brownie import accounts, config, AddressLogs, network


def deploy_address_logs():
    account = get_account()
    AddressLogs.deploy({"from": account}, publish_source=True)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_address_logs()
