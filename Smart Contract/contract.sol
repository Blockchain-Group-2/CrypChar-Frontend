pragma solidity >=0.4.22 <0.7.0;

contract CryptoCharity {
    event txns(bytes TimestampEST, address From, address To, uint Continent, uint Value, bytes Memo, bytes TxnHash);
    uint[7] public bals;
    
    function give(string memory time, address to, uint cont, uint value, string memory memo, string memory hash) public{
        // changes balance
        bals[cont] += value;
        
        // emits event
        emit txns(bytes(time), msg.sender, to, cont, value, bytes(memo), bytes(hash));
    }
    
    function take(string memory time, address to, uint cont, uint value, string memory memo, string memory hash) public{
        // checks balance
        require(
            bals[cont] >= value,
            "Continent must be able to afford withdrawal"
        );
        
        // changes balance
        bals[cont] -= value;
        
        // emits event
        emit txns(bytes(time), msg.sender, to, cont, value, bytes(memo), bytes(hash));
    }
    
    fallback() external payable { }
}
