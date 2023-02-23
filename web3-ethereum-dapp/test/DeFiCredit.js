const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Credit", function () {
  let credit, accounts;

  before(async function () {
    accounts = await ethers.getSigners();
    const Credit = await ethers.getContractFactory("Credit");
    credit = await Credit.deploy(ethers.utils.parseEther("1000"), 10);
    await credit.deployed();
  });

  it("Should have initial credit limit", async function () {
    expect(await credit.creditLimit()).to.equal(ethers.utils.parseEther("1000"));
  });

  it("Should disburse credit to borrower", async function () {
    await credit.disburse(accounts[1].address, ethers.utils.parseEther("500"));
    expect(await credit.creditLine(accounts[1].address)).to.equal(ethers.utils.parseEther("500"));
  });

  it("Should fail to disburse credit beyond credit limit", async function () {
    await expect(credit.disburse(accounts[2].address, ethers.utils.parseEther("1500"))).to.be.reverted;
    expect(await credit.creditLine(accounts[2].address)).to.equal(0);
  });

  it("Should repay credit to lender", async function () {
    const initialBalance = await ethers.provider.getBalance(accounts[0].address);
    await credit.disburse(accounts[1].address, ethers.utils.parseEther("500"));
    const tx = await credit.repay(accounts[0].address, ethers.utils.parseEther("250"));
    const receipt = await tx.wait();
    const gasUsed = receipt.gasUsed.mul(tx.gasPrice);
    expect(await ethers.provider.getBalance(accounts[0].address)).to.equal(initialBalance.add(ethers.utils.parseEther("250")).sub(gasUsed));
    expect(await credit.creditLine(accounts[1].address)).to.equal(ethers.utils.parseEther("250"));
  });

  it("Should fail to repay more than credit line balance", async function () {
    await credit.disburse(accounts[1].address, ethers.utils.parseEther("500"));
    await expect(credit.repay(accounts[0].address, ethers.utils.parseEther("1000"))).to.be.reverted;
    expect(await credit.creditLine(accounts[1].address)).to.equal(ethers.utils.parseEther("500"));
  });

  it("Should accrue interest over time", async function () {
    const initialBalance = await ethers.provider.getBalance(accounts[0].address);
    await credit.disburse(accounts[1].address, ethers.utils.parseEther("500"));
    const tx = await credit.accrueInterest();
    const receipt = await tx.wait();
    const gasUsed = receipt.gasUsed.mul(tx.gasPrice);
    expect(await credit.interestAccrued()).to.equal(ethers.utils.parseEther("50"));
    expect(await credit.totalDebt()).to.equal(ethers.utils.parseEther("550"));
    expect(await ethers.provider.getBalance(accounts[0].address)).to.equal(initialBalance.add(ethers.utils.parseEther("0")).sub(gasUsed));
  });
});