pragma solidity >=0.4.22 <0.7.0;

contract MetaCoin {
    
    uint[7] public bals;
    
    event trans(
        bytes TimestampEST,
        address From,
        address To,
        uint Continent,
        uint Value,
        bytes Memo,
        bytes TxnHash
    );
    
    function give(
        string memory time,
        address to,
        uint cont,
        uint value,
        string memory memo,
        string memory hash
    ) public returns (bool){
        
        // changes balance
        bals[cont]+=value;
        
        // emits event
        emit trans(
            bytes(time),
            msg.sender,
            to,
            cont,
            value,
            bytes(memo),
            bytes(hash)
        );
        
        return true;
    }
    
    function take(
        string memory time,
        address to,
        uint cont,
        uint value,
        string memory memo,
        string memory hash
    ) public returns (bool){
        
        // changes balance
        if (bals[cont]<value) return false;
        bals[cont]-=value;
        
        // emits event
        emit trans(
            bytes(time),
            msg.sender,
            to,
            cont,
            value,
            bytes(memo),
            bytes(hash)
        );
        
        return true;
    }
    
    fallback() external payable { }
}
