pragma solidity ^0.4.24;
 
contract Mortal {
    address owner;
     
    modifier require_owner() {
        require(owner == msg.sender, "Must be owner");
        _; //Executes function body
    }
    
    constructor() public {
        owner = msg.sender;
    }
    
    function kill() public require_owner {
        selfdestruct(owner);
    }
   
}
contract Greeter is Mortal {
    string greeting;
    
    // Runs when contract is created
    constructor(string _greeting) public {
        greeting = _greeting;
        owner = msg.sender;
    }
    
    // Returns greeting, view means it will does not modify state
    function greet() public view returns (string) {
        return greeting;
    }
    
    function set_greeting(string new_greeting) public require_owner {
        greeting = new_greeting;
    }
}

