// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount)
        external
        returns (bool);

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool);

    function approve(address spender, uint256 amount) external returns (bool);
}

contract DeFiCredit {
    struct Member {
        uint256 balance;
        uint256 creditLimit;
        uint256 loanAmount;
        uint256 loanDueDate;
        uint256 loanInterest;
    }

    uint256 private constant INTEREST_RATE = 100; // 1% per term

    mapping(address => Member) public members;
    IERC20 public token;

    event Deposit(address member, uint256 amount);
    event Disbursement(
        address borrower,
        uint256 amount,
        uint256 dueDate,
        uint256 interest
    );
    event Repayment(address borrower, uint256 amount, uint256 interest);

    constructor(address _token) {
        token = IERC20(_token);
    }

    function deposit(uint256 amount) external {
        require(
            token.transferFrom(msg.sender, address(this), amount),
            "Token transfer failed"
        );
        members[msg.sender].balance += amount;
        emit Deposit(msg.sender, amount);
    }

    function disburse(
        address borrower,
        uint256 amount,
        uint256 term
    ) external {
        require(
            amount <= members[borrower].creditLimit,
            "Exceeds credit limit"
        );
        require(
            token.balanceOf(address(this)) >= amount,
            "Insufficient liquidity"
        );
        Member storage borrowerMember = members[borrower];
        borrowerMember.loanAmount += amount;
        borrowerMember.loanDueDate = block.timestamp + term;
        borrowerMember.loanInterest =
            (amount * term * INTEREST_RATE) /
            (100 * 365);
        require(token.transfer(borrower, amount), "Token transfer failed");
        emit Disbursement(
            borrower,
            amount,
            borrowerMember.loanDueDate,
            borrowerMember.loanInterest
        );
    }

    function repay(uint256 amount) external {
        Member storage payerMember = members[msg.sender];
        require(payerMember.loanAmount > 0, "No outstanding loan");
        require(block.timestamp <= payerMember.loanDueDate, "Loan is overdue");

        uint256 interest = payerMember.loanInterest;
        uint256 remainingLoan = payerMember.loanAmount - amount;

        if (remainingLoan <= 0) {
            amount = payerMember.loanAmount;
            remainingLoan = 0;
            payerMember.loanInterest = 0;
            payerMember.loanDueDate = 0;
        } else {
            payerMember.loanAmount = remainingLoan;
            payerMember.loanInterest =
                (remainingLoan *
                    (payerMember.loanDueDate - block.timestamp) *
                    INTEREST_RATE) /
                (100 * 365);
        }

        require(
            token.transferFrom(msg.sender, address(this), amount),
            "Token transfer failed"
        );
        payerMember.balance += amount - interest;
        emit Repayment(msg.sender, amount, interest);
    }
}
