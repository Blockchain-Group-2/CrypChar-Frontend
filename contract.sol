pragma solidity >=0.4.22 <0.7.0;

contract CrypChar {

    mapping(uint256 => uint256) public hash; //initializes a Hashtable
    uint256 public i=0; //when first deployed, the index of the hastable is 0

    function store(uint256 num) public returns (bool success){ //stores the data from a hash and increments that value
        hash[i]+=num;
        i++;
        return true;
    }
    
    function get(uint256 i) public view returns (uint256){ //gets data from the hash at index 'i'
        return hash[i];
    }

    mapping (uint256 => uint256) public balances; 
    event t(address sender, address receiver, uint continent, uint amount, bytes memo);
    
    constructor() public{}

    function transfer(address receiver, uint to, uint value, string memory memo) public payable returns (bool success) {  //transfers Ether between the donator and the charity
        balances[to] += value; //changes the value of the balance for the charity
        emit t(msg.sender, receiver, to, value, bytes(memo)); //emits an event logging a transaction
        return true;
    }

    function withdraw(address receiver, uint to, uint value, string memory memo) public payable returns (bool success) {  //allows the charity to allocate money
        if (value > balances[to]) return false; //returns false if the charity does not have enough funds to withdraw
        
        balances[to] -= value;  
        emit t(msg.sender, receiver, to, value, bytes(memo));
        return true;
    }
    
    function getBalance(uint i) public payable returns (uint){  //gets the balance at the index 'i'
        return balances[i];
    }
}
