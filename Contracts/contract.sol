pragma solidity >=0.4.22 <0.7.0;

contract MetaCoin {
    
    int[7] public bals;
    
    function getBals() public returns (int[7] memory){
        return bals;
    }
    
    struct log{
        string time;
        address from;
        address to;
        uint cont;
        int value;
        string memo;
        string hash;
    }
    log[] public logs;
    uint public length=0;
    
    function store(
        string memory time,
        address to,
        uint cont,
        int value,
        string memory memo,
        string memory hash
    ) public returns (bool){
        
        //changes balance
        if (value+bals[cont]<0) return false;
        bals[cont]+=value;
        
        //stores faux event as struct
        log memory t;
        
        t.time=time;
        t.from=msg.sender;
        t.to=to;
        t.cont=cont;
        t.value=value;
        t.memo=memo;
        t.hash=hash;
        
        logs.push(t);
        length++;
        
        return true;
    }
    
    fallback() external payable { }
}
