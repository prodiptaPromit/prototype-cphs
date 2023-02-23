const { expect } = require('chai');
const { ethers } = require('hardhat');

const tokens = (n) => {
    return ethers.utils.parseUnits(n.toString(), 'ether')
}

describe('AssetExchange', () => {
    let buyer, seller, inspector, lender
    let realEstate, AssetExchange

    beforeEach(async () => {
        // Setup accounts
        [buyer, seller, inspector, lender] = await ethers.getSigners()

        // Deploy Real Estate
        const RealEstate = await ethers.getContractFactory('RealEstate')
        realEstate = await RealEstate.deploy()

        // Mint 
        let transaction = await realEstate.connect(seller).mint("https://ipfs.io/ipfs/QmTudSYeM7mz3PkYEWXWqPjomRPHogcMFSq7XAvsvsgAPS")
        await transaction.wait()

        // Deploy AssetExchange
        const AssetExchange = await ethers.getContractFactory('AssetExchange')
        AssetExchange = await AssetExchange.deploy(
            realEstate.address,
            seller.address,
            inspector.address,
            lender.address
        )

        // Approve Property
        transaction = await realEstate.connect(seller).approve(AssetExchange.address, 1)
        await transaction.wait()

        // List Property
        transaction = await AssetExchange.connect(seller).list(1, buyer.address, tokens(10), tokens(5))
        await transaction.wait()
    })

    describe('Deployment', () => {
        it('Returns NFT address', async () => {
            const result = await AssetExchange.nftAddress()
            expect(result).to.be.equal(realEstate.address)
        })

        it('Returns seller', async () => {
            const result = await AssetExchange.seller()
            expect(result).to.be.equal(seller.address)
        })

        it('Returns inspector', async () => {
            const result = await AssetExchange.inspector()
            expect(result).to.be.equal(inspector.address)
        })

        it('Returns lender', async () => {
            const result = await AssetExchange.lender()
            expect(result).to.be.equal(lender.address)
        })
    })

    describe('Listing', () => {
        it('Updates as listed', async () => {
            const result = await AssetExchange.isListed(1)
            expect(result).to.be.equal(true)
        })

        it('Returns buyer', async () => {
            const result = await AssetExchange.buyer(1)
            expect(result).to.be.equal(buyer.address)
        })

        it('Returns purchase price', async () => {
            const result = await AssetExchange.purchasePrice(1)
            expect(result).to.be.equal(tokens(10))
        })

        it('Returns AssetExchange amount', async () => {
            const result = await AssetExchange.AssetExchangeAmount(1)
            expect(result).to.be.equal(tokens(5))
        })

        it('Updates ownership', async () => {
            expect(await realEstate.ownerOf(1)).to.be.equal(AssetExchange.address)
        })
    })

    describe('Deposits', () => {
        beforeEach(async () => {
            const transaction = await AssetExchange.connect(buyer).depositEarnest(1, { value: tokens(5) })
            await transaction.wait()
        })

        it('Updates contract balance', async () => {
            const result = await AssetExchange.getBalance()
            expect(result).to.be.equal(tokens(5))
        })
    })

    describe('Inspection', () => {
        beforeEach(async () => {
            const transaction = await AssetExchange.connect(inspector).updateInspectionStatus(1, true)
            await transaction.wait()
        })

        it('Updates inspection status', async () => {
            const result = await AssetExchange.inspectionPassed(1)
            expect(result).to.be.equal(true)
        })
    })

    describe('Approval', () => {
        beforeEach(async () => {
            let transaction = await AssetExchange.connect(buyer).approveSale(1)
            await transaction.wait()

            transaction = await AssetExchange.connect(seller).approveSale(1)
            await transaction.wait()

            transaction = await AssetExchange.connect(lender).approveSale(1)
            await transaction.wait()
        })

        it('Updates approval status', async () => {
            expect(await AssetExchange.approval(1, buyer.address)).to.be.equal(true)
            expect(await AssetExchange.approval(1, seller.address)).to.be.equal(true)
            expect(await AssetExchange.approval(1, lender.address)).to.be.equal(true)
        })
    })

    describe('Sale', () => {
        beforeEach(async () => {
            let transaction = await AssetExchange.connect(buyer).depositEarnest(1, { value: tokens(5) })
            await transaction.wait()

            transaction = await AssetExchange.connect(inspector).updateInspectionStatus(1, true)
            await transaction.wait()

            transaction = await AssetExchange.connect(buyer).approveSale(1)
            await transaction.wait()

            transaction = await AssetExchange.connect(seller).approveSale(1)
            await transaction.wait()

            transaction = await AssetExchange.connect(lender).approveSale(1)
            await transaction.wait()

            await lender.sendTransaction({ to: AssetExchange.address, value: tokens(5) })

            transaction = await AssetExchange.connect(seller).finalizeSale(1)
            await transaction.wait()
        })

        it('Updates ownership', async () => {
            expect(await realEstate.ownerOf(1)).to.be.equal(buyer.address)
        })

        it('Updates balance', async () => {
            expect(await AssetExchange.getBalance()).to.be.equal(0)
        })
    })
})