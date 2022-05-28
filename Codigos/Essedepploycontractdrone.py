from web3 import Web3
from solcx import compile_source 

# Solidity source code
compiled_sol = compile_source(
     '''
     pragma solidity >0.5.0;

     contract Delivery {
        struct Drone {
            address payable droneOwner;
            string latitude_deg;
            string longitude_deg;
            uint flying;
            uint idDrone;
        }
        mapping (uint => Drone ) public registerDrones;
        uint qntDrones;
    
        constructor()  {
            qntDrones = 0;
        }

        function registerDrone() public returns (uint)  {
            registerDrones[qntDrones] = Drone(payable(msg.sender),"37.5236476", "0", 0, qntDrones );
            qntDrones = qntDrones + 1;
            return qntDrones;
        }

        function getRegisterDrones() public view returns (uint){
            return qntDrones;
        }

        function getBalance() public view returns (uint){
            return (address(this).balance);
        }

        function inTheDestiny (uint idDrone) public {
            require(idDrone <= qntDrones && idDrone > 0 , "Drone nao cadastrado");
            require(msg.sender == registerDrones[idDrone-1].droneOwner, "You are not drone owner!");
            require(registerDrones[idDrone-1].flying != 0 , "Drone ja esta no destino!. Nenhum valor para sacar");

            registerDrones[idDrone-1].flying = 0;
            payable(msg.sender).transfer(10 ether); 
        }

        function setDestinoOne(uint idDrone) public payable returns (bool){
            uint amount = msg.value;
            require(amount >= 10 ether, "Amount should be higer then 10 Ether");
            require(idDrone <= qntDrones && idDrone > 0 , "Drone nao cadastrado");
            require(registerDrones[idDrone-1].flying == 0 , "Drone nao disponivel.");
          
            uint amountToSend = 10 ether;

            if(amount > amountToSend){
                uint change = msg.value - amountToSend; 
                payable(msg.sender).transfer(change);   
            }
         
            registerDrones[idDrone-1].latitude_deg = "37.5236488"; 
            registerDrones[idDrone-1].longitude_deg = "-122.25511039999999";
            registerDrones[idDrone-1].flying = 1;
            
            return true;
        }
        
        function setDestinoTwo(uint idDrone) public payable returns (bool){
            uint amount = msg.value;
            require(amount >= 10 ether, "Amount should be higer then 10 Ether");
            require(idDrone <= qntDrones && idDrone > 0 , "Drone nao cadastrado");
            require(registerDrones[idDrone-1].flying == 0 , "Drone nao disponivel.");
          
            uint amountToSend = 10 ether;

            if(amount > amountToSend){
                uint change = msg.value - amountToSend; 
                payable(msg.sender).transfer(change);   
            }

            registerDrones[idDrone-1].latitude_deg = "37.52520345925217"; 
            registerDrones[idDrone-1].longitude_deg = "-122.2561141299747";
            registerDrones[idDrone-1].flying = 1;
            
            return true;
        }
        function setDestinoThree(uint idDrone) public payable returns (bool){
            uint amount = msg.value;
            require(amount >= 10 ether, "Amount should be higer then 10 Ether");
            require(idDrone <= qntDrones && idDrone > 0 , "Drone nao cadastrado");
            require(registerDrones[idDrone-1].flying == 0 , "Drone nao disponivel.");
          
            uint amountToSend = 10 ether;

            if(amount > amountToSend){
                uint change = msg.value - amountToSend; 
                payable(msg.sender).transfer(change);   
            }

            registerDrones[idDrone-1].latitude_deg = "37.52402990567395";
            registerDrones[idDrone-1].longitude_deg = "-122.25355683927624";
            registerDrones[idDrone-1].flying = 1;
            
            return true;
        }

        function getStatusDrone(uint idDrone)public view returns (string memory, string memory,  uint)  {
            return (registerDrones[idDrone -1 ].latitude_deg, registerDrones[idDrone -1].longitude_deg, registerDrones[idDrone -1].flying);
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
