// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {FlashToken} from "./FlashToken.sol";

abstract contract ReentrancyGuard {
    uint256 transient _locked;

    modifier nonReentrant() {
        require(_locked == 0);
        _locked = 1;
        _;
        _remove();
    }

    // sets to 0
    function _remove() internal {
        delete _locked;
    }
}

contract Flashloan is ReentrancyGuard {
    uint256 immutable MAX = 100_000 * 1e18;
    uint256 immutable MIN_AMOUNT = 1e18;
    uint256 immutable BUY_OWNER = 100e18;
    uint256 immutable fee_rate = 10;

    address public owner;
    address public governance;
    address public feeRecipient;
    bool public isOwner;

    FlashToken public token;

    enum Status {
        None,
        Pending,
        Active,
        Completed
    }

    struct Request {
        address requester;
        uint256 userId;
        uint256 amount;
        Status status;
    }

    Request[] public requests;
    mapping(address => uint256) public requestIndex;
    mapping(address => bool) public hasRequest;

    constructor(address _feeRecipient, address _token) payable {
        owner = msg.sender;
        governance = owner;
        feeRecipient = _feeRecipient;
        token = FlashToken(_token);
    }

    modifier onlyOwner() {
        if (msg.sender == owner || owner == address(0)) {
            isOwner = true;
        } else {
            isOwner = false;
        }
        _;
    }

    function Calculatefee(uint256 amount) public pure returns (uint256) {
        require(amount >= 1e18);
        return ((amount * fee_rate) / 100) + 1;
    }


    function getRequest(address user) public view returns (Request memory) {
        require(hasRequest[user], "No request found");
        return requests[requestIndex[user]];
    }

    function totalRequests() public view returns (uint256) {
        return requests.length;
    }

   // create request to take loan
    function request(uint256 _amount) public {
        require(_amount >= MIN_AMOUNT, "deposit atleast 1 ether");
        require(
            !hasRequest[msg.sender] || requests[requestIndex[msg.sender]].status == Status.Completed,
            "Already has active request"
        );

        requests.push(
            Request({
                requester: msg.sender, userId: uint256(uint160(msg.sender)), amount: _amount, status: Status.Pending
            })
        );

        requestIndex[msg.sender] = requests.length - 1;
        hasRequest[msg.sender] = true;
    }

    function cancelRequest() public {
        require(hasRequest[msg.sender], "No request");

        uint256 idx = requestIndex[msg.sender];
        Request storage req = requests[idx];

        require(req.status == Status.Pending, "Can only cancel pending request");
        require(req.userId == uint256(uint160(msg.sender)), "Not yours");

        uint256 lastIdx = requests.length - 1;
        if (idx != lastIdx) {
            Request storage last = requests[lastIdx];
            requests[idx] = last;
            requestIndex[last.requester] = idx;
        }

        requests.pop();
        hasRequest[msg.sender] = false;
    }

    //
    function takeLoan(address _target, bytes calldata data, uint256 amount) public  {
        require(_target != address(token));
        owner = governance;
        require(hasRequest[msg.sender], "No request");
        // check if owner is correct address.
        require(owner == governance);

        uint256 idx = requestIndex[msg.sender];
        Request storage req = requests[idx];

        require(req.status == Status.Pending, "No pending request");
        require(req.userId == uint256(uint160(msg.sender)), "Not yours");
        require(amount == req.amount, "Amount mismatch");
        require(amount <= token.balanceOf(address(this)), "Insufficient pool balance");

        uint256 fee = Calculatefee(amount);
        uint256 balanceBefore = token.balanceOf(address(this));

        req.status = Status.Active;

        bool sent = token.transfer(_target, amount);
        require(sent, "transfer failed");
        // @TODO add nonReentrant modifier.
        (bool success,) = _target.call(data);
        require(success, "failed");

        require(token.balanceOf(address(this)) >= balanceBefore + fee, "loan not repaid");

        bool feeOk = token.transfer(feeRecipient, fee);
        require(feeOk, "fee transfer failed");

        req.status = Status.Completed;
    }

    // Buy OWNER with 100 ETH.
    // Owner can change fee feeRecipient
    function buyowner(address _change, address _feeRecipient) public nonReentrant onlyOwner {
        require(_change != address(0));
        require(address(this).balance > 0);
        if (!isOwner) {
            require(token.balanceOf(msg.sender) >= MAX, "insufficient funds");
            bool success = token.transferFrom(msg.sender, feeRecipient, BUY_OWNER);
            require(success);
        }

        owner = _change;
        // if there eth left transfer to feeRecipient
        // its transfered to previous owner recipient
        if (address(this).balance > 0) feeRecipient.call{value: address(this).balance}("");
        feeRecipient = _feeRecipient;
    }

    function withdraw(uint256 amount) public onlyOwner {
        require(msg.sender == owner, "Only owner withdraw");
        require(amount <= token.balanceOf(address(this)));
        bool success = token.transfer(msg.sender, amount);
        require(success);
    }

    receive() external payable nonReentrant {
        revert("NO ETH required we just updated to tokens and only possible through constructor");
    }

    fallback() external nonReentrant {}
}
