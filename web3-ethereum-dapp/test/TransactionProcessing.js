// Import the required libraries
const { expect } = require('chai');
const { ethers } = require('hardhat');

describe('TransactionProcessing', function () {
  let token, transaction;
  const initialSupply = ethers.utils.parseEther('100000');

  before(async function () {
    // Deploy an ERC20 token for testing
    const Token = await ethers.getContractFactory('TestToken');
    token = await Token.deploy(initialSupply);
    await token.deployed();

    // Deploy the TransactionProcessing contract
    const Transaction = await ethers.getContractFactory('TransactionProcessing');
    transaction = await Transaction.deploy(token.address);
    await transaction.deployed();
  });

  describe('deposit', function () {
    it('should increase the user balance by the deposited amount', async function () {
      const amount = ethers.utils.parseEther('1000');
      const initialBalance = await transaction.balances(accounts[0]);

      await token.approve(transaction.address, amount);
      await transaction.deposit(amount);

      const finalBalance = await transaction.balances(accounts[0]);
      expect(finalBalance).to.equal(initialBalance.add(amount));
    });

    it('should emit a Deposit event', async function () {
      const amount = ethers.utils.parseEther('1000');

      await token.approve(transaction.address, amount);

      await expect(transaction.deposit(amount))
        .to.emit(transaction, 'Deposit')
        .withArgs(accounts[0], amount);
    });

    it('should revert when the user does not have sufficient allowance', async function () {
      const amount = ethers.utils.parseEther('1000');
      const initialBalance = await transaction.balances(accounts[0]);

      await expect(transaction.deposit(amount))
        .to.be.revertedWith('ERC20: transfer amount exceeds allowance');

      const finalBalance = await transaction.balances(accounts[0]);
      expect(finalBalance).to.equal(initialBalance);
    });
  });

  describe('withdraw', function () {
    beforeEach(async function () {
      const amount = ethers.utils.parseEther('1000');

      await token.approve(transaction.address, amount);
      await transaction.deposit(amount);
    });

    it('should decrease the user balance by the withdrawn amount', async function () {
      const amount = ethers.utils.parseEther('500');
      const initialBalance = await transaction.balances(accounts[0]);

      await transaction.withdraw(amount);

      const finalBalance = await transaction.balances(accounts[0]);
      expect(finalBalance).to.equal(initialBalance.sub(amount));
    });

    it('should emit a Withdrawal event', async function () {
      const amount = ethers.utils.parseEther('500');

      await expect(transaction.withdraw(amount))
        .to.emit(transaction, 'Withdrawal')
        .withArgs(accounts[0], amount);
    });

    it('should revert when the user does not have sufficient balance', async function () {
      const amount = ethers.utils.parseEther('2000');
      const initialBalance = await transaction.balances(accounts[0]);

      await expect(transaction.withdraw(amount))
        .to.be.revertedWith('TransactionProcessing: insufficient balance');

      const finalBalance = await transaction.balances(accounts[0]);
      expect(finalBalance).to.equal(initialBalance);
    });
  });
});
