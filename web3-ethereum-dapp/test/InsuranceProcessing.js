const { expect } = require("chai");

describe("InsuranceProcessing", function () {
  let owner;
  let provider;
  let policyHolder1;
  let policyHolder2;
  let _token;
  let _nft;
  let InsuranceProcessing;

  const COVERAGE = 1000;
  const PREMIUM = 100;
  const EXPIRATION = Math.floor(Date.now() / 1000) + 60 * 60 * 24 * 30; // 30 days from now
  const POLICY_ID = 1;

  before(async function () {
    [owner, provider, policyHolder1, policyHolder2] = await ethers.getSigners();

    const Token = await ethers.getContractFactory("MockToken");
    _token = await Token.deploy("Mock Token", "MT", 100000000);

    const NFT = await ethers.getContractFactory("MockNFT");
    _nft = await NFT.deploy();

    const InsuranceProcessing = await ethers.getContractFactory("InsuranceProcessing");
    InsuranceProcessing = await InsuranceProcessing.deploy(_token.address, _nft.address);
    await InsuranceProcessing.setInsuranceProvider(provider.address);

    await _token.transfer(policyHolder1.address, 1000);
    await _token.connect(policyHolder1).approve(InsuranceProcessing.address, 1000);
    await _nft.mint(policyHolder1.address, POLICY_ID);
    await _nft.connect(policyHolder1).setApprovalForAll(InsuranceProcessing.address, true);

    await _token.transfer(policyHolder2.address, 1000);
    await _token.connect(policyHolder2).approve(InsuranceProcessing.address, 1000);
  });

  describe("createPolicy", function () {
    it("should create a policy", async function () {
      await InsuranceProcessing.createPolicy(COVERAGE, PREMIUM, EXPIRATION);

      const policy = await InsuranceProcessing.getPolicies(policyHolder1.address);
      expect(policy.id).to.equal(POLICY_ID);
      expect(policy.coverage).to.equal(COVERAGE);
      expect(policy.premium).to.equal(PREMIUM);
      expect(policy.expiration).to.equal(EXPIRATION);
      expect(policy.beneficiary).to.equal(policyHolder1.address);
      expect(policy.claimed).to.equal(false);
    });

    it("should not create a policy if policy already exists", async function () {
      await expect(InsuranceProcessing.createPolicy(COVERAGE, PREMIUM, EXPIRATION)).to.be.revertedWith("InsuranceProcessing: policy already exists");
    });

    it("should not create a policy if expiration date is in the past", async function () {
      await expect(InsuranceProcessing.createPolicy(COVERAGE, PREMIUM, Math.floor(Date.now() / 1000) - 1)).to.be.revertedWith("InsuranceProcessing: expiration date must be in the future");
    });
  });

  describe("processClaim", function () {
    it("should process a claim", async function () {
      const balanceBefore = await _token.balanceOf(policyHolder1.address);

      await InsuranceProcessing.processClaim(POLICY_ID);

      const policy = await InsuranceProcessing.getPolicies(policyHolder1.address);
      expect(policy.claimed).to.equal(true);

      const balanceAfter = await _token.balanceOf(policyHolder1.address);
      expect(balanceAfter).to.equal(balanceBefore.add(COVERAGE));
    });

    it("should not process a claim if policy does not exist", async function () {
      await expect(InsuranceProcessing.processClaim(999)).to.be.revertedWith("InsuranceProcessing: policy does not exist");
    });
  });
});

describe("withdrawPremium", function () {
  it("allows policyholder to withdraw premium", async function () {
    await InsuranceProcessing.connect(policyholder).createPolicy(coverage, premium, expiration);
    await InsuranceProcessing.connect(policyholder).withdrawPremium();
    const balance = await token.balanceOf(policyholder.address);
    expect(balance).to.equal(premium);
  });

  it("does not allow non-policyholder to withdraw premium", async function () {
    await expect(InsuranceProcessing.connect(insuranceProvider).withdrawPremium()).to.be.revertedWith("InsuranceProcessing: policy does not exist");
  });
});



