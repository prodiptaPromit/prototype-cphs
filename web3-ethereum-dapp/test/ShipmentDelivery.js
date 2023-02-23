const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Shipment", function () {
    let shipmentInstance;

    beforeEach(async function () {
        const Shipment = await ethers.getContractFactory("Shipment");
        shipmentInstance = await Shipment.deploy();
        await shipmentInstance.deployed();

        const accounts = await ethers.getSigners();
        await shipmentInstance.addCourier(accounts[1].address, 5);
        await shipmentInstance.addCourier(accounts[2].address, 4);
        await shipmentInstance.addCourier(accounts[3].address, 3);
    });

    it("should add a courier", async function () {
        const courierCountBefore = await shipmentInstance.getCourierCount();
        await shipmentInstance.addCourier("0x1234567890123456789012345678901234567890", 5);
        const courierCountAfter = await shipmentInstance.getCourierCount();
        expect(courierCountAfter).to.equal(courierCountBefore + 1);
    });

    it("should not add a courier with duplicate address", async function () {
        await expect(shipmentInstance.addCourier(accounts[1].address, 3)).to.be.revertedWith("Address already exists");
    });

    it("should remove a courier", async function () {
        const courierCountBefore = await shipmentInstance.getCourierCount();
        await shipmentInstance.removeCourier(accounts[1].address);
        const courierCountAfter = await shipmentInstance.getCourierCount();
        expect(courierCountAfter).to.equal(courierCountBefore - 1);
    });

    it("should add a shipment", async function () {
        const shipmentCountBefore = await shipmentInstance.getShipmentCount();
        await shipmentInstance.addShipment("Item1", "0x1234567890123456789012345678901234567890");
        const shipmentCountAfter = await shipmentInstance.getShipmentCount();
        expect(shipmentCountAfter).to.equal(shipmentCountBefore + 1);
    });

    it("should get a shipment", async function () {
        const shipmentId = await shipmentInstance.getShipmentCount();
        await shipmentInstance.addShipment("Item1", "0x1234567890123456789012345678901234567890");
        const shipment = await shipmentInstance.getShipment(shipmentId);
        expect(shipment[0]).to.equal("Item1");
        expect(shipment[1]).to.equal("0x1234567890123456789012345678901234567890");
        expect(shipment[2]).to.equal(false);
    });

    it("should not get a shipment with invalid id", async function () {
        await expect(shipmentInstance.getShipment(0)).to.be.revertedWith("Invalid shipment ID");
    });

    it("should update a shipment", async function () {
        const shipmentId = await shipmentInstance.getShipmentCount();
        await shipmentInstance.addShipment("Item1", "0x1234567890123456789012345678901234567890");
        await shipmentInstance.updateShipment(shipmentId, "Item2", "0x0987654321098765432109876543210987654321", true);
        const shipment = await shipmentInstance.getShipment(shipmentId);
        expect(shipment[0]).to.equal("Item2");
        expect(shipment[1]).to.equal("0x0987654321098765432109876543210987654321");
        expect(shipment[2]).to.equal(true);
    });
})
