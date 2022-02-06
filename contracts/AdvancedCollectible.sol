// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase{

    uint256 public tokenCounter ;
    bytes32 public keyHash ;
    uint256 public fee;
    enum Breed{PUG,INU,BERNARD}
    mapping (uint256 => Breed) public tokenIdToBreed;
    mapping (bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned (uint256 indexed tokenId, Breed breed );

    constructor (address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public ERC721("Doggie", "DOG") VRFConsumerBase(_vrfCoordinator, _linkToken){
        tokenCounter = 0;
        keyHash = _keyhash;
        fee = _fee;
    }

    function createCollectible () public returns (bytes32){
        bytes32 requestID = requestRandomness (keyHash, fee);
        requestIdToSender [requestID] = msg.sender;
        emit requestedCollectible(requestID, msg.sender);
        return requestID;

    }

    function fulfillRandomness (bytes32 requestId, uint256 randomNumber) internal override {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed [newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        _safeMint(requestIdToSender[requestId],  newTokenId);
        // _setTokenURI (newTokenId, );
        
        tokenCounter +=1;
    }
    function setTokenURI (uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not owner");
        _setTokenURI(tokenId, _tokenURI);
    }
}