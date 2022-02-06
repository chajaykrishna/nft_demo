from scripts.helpful_scripts import get_account
from brownie import SimpleCollectible

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"
def deploy_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from":account})
    token_id = simple_collectible.tokenCounter()
    tx = simple_collectible.createCollectible(sample_token_uri)
    tx.wait(1)
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(simple_collectible.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')
    return simple_collectible

def main():
    deploy_create()