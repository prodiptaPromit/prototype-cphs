// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/IERC721Metadata.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Shipment is IERC721Receiver {
    enum ShipmentStatus {
        Requested,
        Accepted,
        InTransit,
        Delivered,
        Disputed,
        Resolved
    }

    IERC20 private _token;
    IERC721 private _nft;

    struct Courier {
        address payable courierAddress;
        bool available;
        uint256 reputation;
    }

    struct ShipmentRequest {
        address payable customerAddress;
        string origin;
        string destination;
        uint256 fee;
        ShipmentStatus status;
        uint256 courierIndex;
        uint256 customsFee;
    }

    struct Dispute {
        uint256 shipmentId;
        address disputedBy;
        uint256 disputedAmount;
        bool resolved;
    }

    address payable public owner;
    Courier[] public couriers;
    ShipmentRequest[] public shipmentRequests;
    Dispute[] public disputes;
    mapping(address => uint256) public customerReputation;
    mapping(address => uint256) public courierReputation;
    mapping(address => uint256) public balances;

    event ShipmentRequested(uint256 shipmentId);
    event ShipmentAccepted(uint256 shipmentId);
    event ShipmentInTransit(uint256 shipmentId);
    event ShipmentDelivered(uint256 shipmentId);
    event ShipmentDisputed(uint256 shipmentId);
    event DisputeResolved(uint256 disputeId);

    constructor() {
        owner = payable(msg.sender);
    }

    function addCourier(address payable _courierAddress, uint256 _reputation)
        external
    {
        require(msg.sender == owner, "Only owner can add couriers");
        couriers.push(
            Courier({
                courierAddress: _courierAddress,
                available: true,
                reputation: _reputation
            })
        );
    }

    function requestShipment(
        string memory _origin,
        string memory _destination,
        uint256 _fee,
        uint256 _customsFee
    ) external payable {
        require(
            msg.value == _fee + _customsFee,
            "Fee and customs fee must be paid upfront"
        );
        shipmentRequests.push(
            ShipmentRequest({
                customerAddress: payable(msg.sender),
                origin: _origin,
                destination: _destination,
                fee: _fee,
                status: ShipmentStatus.Requested,
                courierIndex: 0,
                customsFee: _customsFee
            })
        );
        emit ShipmentRequested(shipmentRequests.length - 1);
    }

    function getCourierCount() external view returns (uint256) {
        return couriers.length;
    }

    function getShipmentCount() external view returns (uint256) {
        return shipmentRequests.length;
    }

    function acceptShipment(uint256 _shipmentId) external {
        require(_shipmentId < shipmentRequests.length, "Invalid shipment ID");
        require(couriers.length > 0, "No couriers available");
        require(
            couriers[shipmentRequests[_shipmentId].courierIndex].available,
            "Courier not available"
        );
        require(
            msg.sender ==
                couriers[shipmentRequests[_shipmentId].courierIndex]
                    .courierAddress,
            "Only assigned courier can accept shipment"
        );

        shipmentRequests[_shipmentId].status = ShipmentStatus.Accepted;
        shipmentRequests[_shipmentId].courierIndex = getNextAvailableCourier();
        couriers[shipmentRequests[_shipmentId].courierIndex].available = false;
        emit ShipmentAccepted(_shipmentId);
    }

    function deliverShipment(uint256 _shipmentId) external {
        require(_shipmentId < shipmentRequests.length, "Invalid shipment ID");
        require(
            msg.sender == shipmentRequests[_shipmentId].customerAddress,
            "Only customer can confirm delivery"
        );

        shipmentRequests[_shipmentId].status = ShipmentStatus.Delivered;
        couriers[shipmentRequests[_shipmentId].courierIndex].available = true;
        balances[owner] += shipmentRequests[_shipmentId].fee;
        balances[
            shipmentRequests[_shipmentId].customerAddress
        ] -= shipmentRequests[_shipmentId].fee;
        emit ShipmentDelivered(_shipmentId);
    }

    function getNextAvailableCourier() private view returns (uint256) {
        for (uint256 i = 0; i < couriers.length; i++) {
            if (couriers[i].available) {
                return i;
            }
        }
        revert("No available couriers");
    }
}
