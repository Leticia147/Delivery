from web3 import Web3
from solcx import compile_source 
#usar 3-4 posições prontas 
#colocar as posições dentro do contrato e não fora
# Solidity source code
compiled_sol = compile_source(
     '''
     pragma solidity >0.5.0;

     contract Delivery {

        struct Destiny {
            string latitude_deg;
            string longitude_deg;
            string flying;
        }
        Destiny destiny;
         
        constructor() public {
            destiny = Destiny("0", "0", "0");
        }
   
        function inTheDestiny() public {

            destiny.flying = "0";
        }

        function setDestinoOne() public {

            destiny = Destiny("37.5236476", "-122.2551089", "1");
        }
        function setDestinoTwo() public {

            destiny = Destiny("37.5232366", "-122.2611083", "1");
        }
        function setDestinoThree() public {

            destiny = Destiny("37.5247619", "-122..2576713", "1");
        }

        function getDestino()public view returns (string memory, string memory,  string memory)  {
            return (destiny.latitude_deg, destiny.longitude_deg, destiny.flying);
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

#print(delivery.functions.getDestino().call())

#tx_hash = delivery.functions.setDestino('0','0','0').transact()
#tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
#print(delivery.functions.getDestino().call())
