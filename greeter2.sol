pragma solidity ^0.4.24;
 
contract Greeter {
    string greeting;
    
    // Runs when contract is created
    constructor(string _greeting) public {
        greeting = _greeting;
    }
    
    // Returns greeting, view means it does not modify state
    function greet() public view returns (string) {
        return greeting;
    }
}

