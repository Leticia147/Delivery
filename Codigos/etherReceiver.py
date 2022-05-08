from web3 import Web3
from solcx import compile_source

# no ganache cli:
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# set pre-funded account 2 as sender
w3.eth.default_account = w3.eth.accounts[1]

compiled_sol = compile_source(
     '''
    pragma solidity >0.5.0; 
    
    contract Payable {
        address payable public owner;

        constructor() payable {
            owner =  payable(msg.sender);
        }

        function deposit() external payable {}

        function notPayable() public {}

        function Transfer(uint amount,address reciever) public payable returns (bool) {
            require(amount >= 10 ,"Amount should higer then 10 Ether");
            uint amountToSend = 10 ;
            if(amount > amountToSend){
                uint change = amount - amountToSend; 
                payable(msg.sender).transfer(change);
            }
            payable(reciever).transfer(amountToSend);
            return true;
        }     
    }

    ''',
    output_values=['abi', 'bin']
)

# retrieve the contract interface
contract_id, contract_interface = compiled_sol.popitem()

# get bytecode / bin
bytecode = contract_interface['bin']

# get abi
abi = contract_interface['abi']

print(abi)

# web3.py instance   ganache interface
#w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# no ganache cli:
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))


# set pre-funded account as sender
w3.eth.default_account = w3.eth.accounts[0]

Delivery = w3.eth.contract(abi=abi, bytecode=bytecode)

# Submit the transaction that deploys the contract
tx_hash = Delivery.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

delivery = w3.eth.contract(
     address=tx_receipt.contractAddress,
     abi=abi
 )
