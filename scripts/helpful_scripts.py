from os import link
from brownie import accounts, network, config, MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken


LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local","mainnet-fork","mainnet-fork-dev"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

BREED_MAPPING = {0: "PUG", 1: "INU", 2: "BERNARD"}
def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
 
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator, "vrf_coordinator": VRFCoordinatorMock, "link_token": LinkToken}

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type)<=0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        #address 
        #abi
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)

    return contract

def deploy_mocks():
    account = get_account()
    
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print ("Mocks Deployed!")


def fund_with_link(contract_address, account = None, link_token = None, ammount=100000000000000000): #0.1 link 
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, ammount, {"from":account})
    tx.wait(1)
    print(f"funded contract: {contract_address}")
    return tx