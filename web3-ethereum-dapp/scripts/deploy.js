// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.
const hre = require("hardhat");

const tokens = (n) => {
  return ethers.utils.parseUnits(n.toString(), 'ether')
}

async function main() {
  // Setup accounts
  const [buyer, seller, inspector, lender] = await ethers.getSigners()

  // Deploy Asset
  const Asset = await ethers.getContractFactory('Asset')
  const asset = await Asset.deploy()
  await asset.deployed()

  console.log(`Deployed Real Estate Contract at: ${asset.address}`)
  console.log(`Minting 3 properties...\n`)

  for (let i = 0; i < 3; i++) {
    const transaction = await asset.connect(seller).mint(`https://ipfs.io/ipfs/QmQVcpsjrA6cr1iJjZAodYwmPekYgbnXGo4DFubJiLc2EB/${i + 1}.json`)
    await transaction.wait()
  }

  // Deploy AssetExchange
  const AssetExchange = await ethers.getContractFactory('AssetExchange')
  const assetExchange = await AssetExchange.deploy("0xTOKEN_ADDRESS_HERE")
  await assetExchange.deployed()
  console.log(`Deployed AssetExchange Contract at: ${assetExchange.address}`)

  console.log(`Listing 3 properties...\n`)

  for (let i = 0; i < 3; i++) {
    // Approve properties...
    let transaction = await asset.connect(seller).approve(assetExchange.address, i + 1)
    await transaction.wait()
  }

  // Listing properties...
  transaction = await assetExchange.connect(seller).list(1, buyer.address, tokens(20), tokens(10))
  await transaction.wait()

  transaction = await assetExchange.connect(seller).list(2, buyer.address, tokens(15), tokens(5))
  await transaction.wait()

  transaction = await assetExchange.connect(seller).list(3, buyer.address, tokens(10), tokens(5))
  await transaction.wait()

  // Deploy TransactionProcessing
  const TransactionProcessing = await ethers.getContractFactory("TransactionProcessing");
  const transactionProcessing = await TransactionProcessing.deploy("0xTOKEN_ADDRESS_HERE");
  await transactionProcessing.deployed()
  console.log("TransactionProcessing contract deployed to:", transactionProcessing.address);

  // Deploy InsuranceProcessing
  const InsuranceProcessing = await ethers.getContractFactory("InsuranceProcessing");
  const insuranceProcessing = await InsuranceProcessing.deploy("0xTOKEN_ADDRESS_HERE");
  await insuranceProcessing.deployed()
  console.log("InsuranceProcessing contract deployed to:", insuranceProcessing.address);

  // Deploy ShipmentDelivery
  const ShipmentDelivery = await ethers.getContractFactory("ShipmentDelivery");
  const shipmentDelivery = await ShipmentDelivery.deploy("0xTOKEN_ADDRESS_HERE");
  await shipmentDelivery.deployed()
  console.log("ShipmentDelivery contract deployed to:", shipmentDelivery.address);

  // Deploy DeFiCredit
  const DeFiCredit = await ethers.getContractFactory("DeFiCredit");
  const defiCredit = await DeFiCredit.deploy("0xTOKEN_ADDRESS_HERE");
  await defiCredit.deployed()
  console.log("DeFiCredit contract deployed to:", defiCredit.address);

  console.log(`Finished.`)
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

