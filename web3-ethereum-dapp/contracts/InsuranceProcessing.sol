// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/IERC721Metadata.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract InsuranceProcessing is IERC721Receiver {
    using SafeMath for uint256;

    IERC20 private _token;
    IERC721 private _nft;

    struct Policy {
        uint256 id;
        uint256 coverage;
        uint256 premium;
        uint256 expiration;
        address beneficiary;
        bool claimed;
    }

    mapping(address => Policy) private _policies;
    mapping(uint256 => address) private _policyHolders;
    mapping(address => bool) private _isPolicyholder;

    uint256 private _policyCount;
    uint256 private _claimCount;
    uint256 private _balance;
    uint256 private _totalPremiums;

    address private _insuranceProvider;

    event PolicyCreated(
        address indexed beneficiary,
        uint256 coverage,
        uint256 premium,
        uint256 expiration,
        uint256 policyId
    );
    event ClaimProcessed(
        address indexed beneficiary,
        uint256 amount,
        uint256 policyId
    );
    event PremiumWithdrawn(address indexed beneficiary, uint256 amount);
    event BalanceWithdrawn(address indexed beneficiary, uint256 amount);

    constructor(IERC20 token, IERC721 nft) {
        _token = token;
        _nft = nft;
    }

    function createPolicy(
        uint256 coverage,
        uint256 premium,
        uint256 expiration
    ) public {
        require(
            _policies[msg.sender].id == 0,
            "InsuranceProcessing: policy already exists"
        );
        require(
            expiration > block.timestamp,
            "InsuranceProcessing: expiration date must be in the future"
        );

        uint256 policyId = ++_policyCount;

        _token.transferFrom(msg.sender, address(this), premium);
        _nft.safeTransferFrom(msg.sender, address(this), policyId);

        _policies[msg.sender] = Policy(
            policyId,
            coverage,
            premium,
            expiration,
            msg.sender,
            false
        );
        _policyHolders[policyId] = msg.sender;

        emit PolicyCreated(msg.sender, coverage, premium, expiration, policyId);
    }

    function processClaim(uint256 policyId) public {
        require(
            _policyHolders[policyId] == msg.sender,
            "InsuranceProcessing: policy does not exist or does not belong to sender"
        );
        require(
            !_policies[msg.sender].claimed,
            "InsuranceProcessing: policy has already been claimed"
        );
        require(
            block.timestamp < _policies[msg.sender].expiration,
            "InsuranceProcessing: policy has expired"
        );

        uint256 amount = _policies[msg.sender].coverage;
        _token.transfer(msg.sender, amount);
        _policies[msg.sender].claimed = true;
        _claimCount++;

        emit ClaimProcessed(msg.sender, amount, policyId);
    }

    function withdrawPremium() public {
        uint256 premium = _policies[msg.sender].premium;
        require(premium > 0, "InsuranceProcessing: policy does not exist");

        _token.transfer(msg.sender, premium);

        emit PremiumWithdrawn(msg.sender, premium);
    }

    function withdrawBalance() public {
        require(
            msg.sender == _nft.ownerOf(1),
            "InsuranceProcessing: only the insurance provider can withdraw balance"
        );

        uint256 balance = _token.balanceOf(address(this));
        _token.transfer(msg.sender, balance);

        emit BalanceWithdrawn(msg.sender, balance);
    }

    function setInsuranceProvider(address newProvider) public {
        require(
            msg.sender == _insuranceProvider,
            "InsuranceProcessing: only the insurance provider can set a new provider"
        );
        _insuranceProvider = newProvider;
    }

    function getInsuranceProvider() public view returns (address) {
        return _insuranceProvider;
    }

    function onERC721Received(
        address,
        address,
        uint256,
        bytes memory
    ) public virtual override returns (bytes4) {
        return this.onERC721Received.selector;
    }
}
