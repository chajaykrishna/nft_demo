from brownie import network
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
import pytest
from scripts.AdvancedCollectible.deploy_and_create import deploy_create
import time


def test_can_create_advanced_collectible_integration():
    #deploy a contract
    #create a nft
    #get a random breed back

    #arrange 
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS: 
        pytest.skip()
    #act
    advanced_collectabile, creation_tx =   deploy_create()  
    time.sleep(60)
    #Assert 
    assert advanced_collectabile.tokenCounter() == 1
    