from brownie import SimpleStorage, accounts, config
import brownie.network as network


def test_updating_storage():
    account = accounts.add(config["wallets"]["from_key"])
    simple_storage = SimpleStorage.deploy({"from": account})

    expected = [("0", "0")]
    txn = simple_storage.addElement(expected, {"from": account})
    txn.wait(1)

    assert [("0", "0")] == SimpleStorage.retrieve()
