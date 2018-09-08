contract Greeter {
    string greeting;
    address owner;
    
    // modifiers work similarly to python decorators
    modifier require_owner() {
        require(owner == msg.sender, "Must be owner");
        _; // Executes modified function body
    }
    
    // Runs when contract is created
    constructor(string _greeting) public {
        greeting = _greeting;
        owner = msg.sender;
    }
    
    // Returns greeting, view means it will does not modify state
    function greet() public view returns (string) {
        return greeting;
    }
    
    // modified by require_owner so only the owner who deployed to contract can call it
    // If called by a non-owner gas will still be spent even though the call failed
    function set_greeting(string new_greeting) public require_owner {
        greeting = new_greeting;
    }
}

