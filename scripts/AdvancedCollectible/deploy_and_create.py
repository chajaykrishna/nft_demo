from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import AdvancedCollectible, config, network
from scripts.helpful_scripts import OPENSEA_URL

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

def deploy_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(get_contract("vrf_coordinator"),get_contract("link_token"),
    config["networks"]["rinkeby"]["keyhash"], config["networks"]["rinkeby"]["fee"],
    {"from":account})

    fund_with_link(advanced_collectible.address)
    token_id = advanced_collectible.tokenCounter()
    tx = advanced_collectible.createCollectible({"from":account})
    tx.wait(1)
    print("token created !")
    return advanced_collectible, tx
    # print(
    #     "Awesome! You can view your NFT at {}".format(
    #         OPENSEA_URL.format(advanced_collectible.address, token_id)
    #     )
    # )
    # print('Please give up to 20 minutes, and hit the "refresh metadata" button')
    # return advanced_collectible

def main():
    deploy_create() 