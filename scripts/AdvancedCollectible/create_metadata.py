import json
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests

def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_collectibles} collectibles")
    for tokenId in range (number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(tokenId))
        metadata_filename = (f"./metadata/{network.show_active()}/{tokenId}-{breed}.json")
        collectible_metadata = metadata_template
        if (Path(metadata_filename).exists()):
            print(f"{metadata_filename} already exists")
        else:
            print(f"Creating Metadata file {metadata_filename}")
            collectible_metadata["name"]=  breed
            collectible_metadata["description"] = f"An addorable {breed} pup !"
            image_path = "./img/"+breed.lower().replace("_","-")+".png"
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri
            with open(metadata_filename,"w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_filename)

    
def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        #uploading stuff
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url+endpoint, files = {"file": image_binary})
        print(response.json())
        ipfs_hash = response.json()["Hash"]
        # "./img/PUG.png" -> PUG.png
        filename = filepath.split("/")[-1:][0]
        # https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri


