// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract TransactionProcessing {
    using SafeMath for uint256;

    IERC20 private _token;

    struct Transaction {
        uint256 id;
        address sender;
        address recipient;
        uint256 amount;
        bool processed;
    }

    mapping(uint256 => Transaction) private _transactions;

    uint256 private _transactionCount;
    uint256 private _balance;

    event TransactionCreated(
        address indexed sender,
        address indexed recipient,
        uint256 amount,
        uint256 transactionId
    );
    event TransactionProcessed(
        address indexed sender,
        address indexed recipient,
        uint256 amount,
        uint256 transactionId
    );
    event BalanceWithdrawn(address indexed beneficiary, uint256 amount);

    constructor(IERC20 token) {
        _token = token;
    }

    function createTransaction(address recipient, uint256 amount) public {
        require(
            amount > 0,
            "TransactionProcessing: amount must be greater than zero"
        );

        uint256 transactionId = ++_transactionCount;

        _token.transferFrom(msg.sender, address(this), amount);

        _transactions[transactionId] = Transaction(
            transactionId,
            msg.sender,
            recipient,
            amount,
            false
        );

        emit TransactionCreated(msg.sender, recipient, amount, transactionId);
    }

    function processTransaction(uint256 transactionId) public {
        require(
            _transactions[transactionId].recipient == msg.sender,
            "TransactionProcessing: transaction does not exist or does not belong to sender"
        );
        require(
            !_transactions[transactionId].processed,
            "TransactionProcessing: transaction has already been processed"
        );

        uint256 amount = _transactions[transactionId].amount;
        _token.transfer(msg.sender, amount);
        _transactions[transactionId].processed = true;

        emit TransactionProcessed(
            _transactions[transactionId].sender,
            msg.sender,
            amount,
            transactionId
        );
    }

    function withdrawBalance() public {
        uint256 balance = _token.balanceOf(address(this));
        require(balance > 0, "TransactionProcessing: no balance to withdraw");

        _token.transfer(msg.sender, balance);
        _balance = _balance.sub(balance);

        emit BalanceWithdrawn(msg.sender, balance);
    }
}
