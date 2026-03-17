// SPDX-License-Identifier: Apache-2.0
pragma solidity 0.8.28;

import {Flashloan} from "./Challenge.sol";
import {FlashToken} from "./FlashToken.sol";

contract Set {
    Flashloan public flashloan;
    FlashToken public token;
    address public player;
    address public fee_recipient;

    uint256 constant SUPPLY = 100_000 * 1e18;

    constructor(address _player, address _fee_recipient) payable{
        fee_recipient = _fee_recipient;
        player = _player;

        token = new FlashToken("MEOW", "CAT");

        flashloan = new Flashloan{value: 1 ether}(fee_recipient, address(token));

        token.mint(address(flashloan), SUPPLY + 100e18);
    }

    function isSolved() public view returns (bool) {
        return token.balanceOf(player) >= SUPPLY;
    }
}
