from brownie import network
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
import pytest
from scripts.AdvancedCollectible.deploy_and_create import deploy_create



def test_can_create_advanced_collectible():
    #deploy a contract
    #create a nft
    #get a random breed back

    #arrange 
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS: 
        pytest.skip()
    #act
    advanced_collectabile, creation_tx =   deploy_create()  
    request_id = creation_tx.events["requestedCollectible"]["requestId"]
    get_contract("vrf_coordinator").callBackWithRandomness(request_id, 777, advanced_collectabile.address, {"from": get_account()})

    #Assert 
    assert advanced_collectabile.tokenCounter() == 1
    assert advanced_collectabile.tokenIdToBreed(0) == 777 % 3