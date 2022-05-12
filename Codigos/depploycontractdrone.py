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
        mapping (uint => Drone ) public dronesCadastrados;
        uint  qntDroneCadastrados;
        address payable public contractOwner;     
        
        constructor() payable {
            contractOwner = payable(msg.sender);
            qntDroneCadastrados = 0;
        }

        function cadastrarDrone() public  {
            dronesCadastrados[qntDroneCadastrados] = Drone(payable(msg.sender),"37.5236476", "-122.2551089", 0, qntDroneCadastrados );
            qntDroneCadastrados = qntDroneCadastrados + 1;
        }

        function totalDronesCadastrados() public view returns (uint){
            return qntDroneCadastrados;
        }

        function deposit() public payable {        }
        function recieve() public payable {        }

        function getBalance() public view returns (uint){
            return (contractOwner.balance);
        }

        function withdraw(uint idDrone) public payable returns (uint){
            require(idDrone <= qntDroneCadastrados && idDrone > 0 , "Drone nao cadastrado");
            require(msg.sender == dronesCadastrados[idDrone-1].droneOwner, "You are not drone owner!");
            require(dronesCadastrados[idDrone-1].flying != 0 , "Drone ja esta no destino!.");

            dronesCadastrados[idDrone-1].flying = 0;
            uint amountToSend = 10 ether;

            payable(msg.sender).transfer(amountToSend); 
            
            return (getBalance()); 
        }

        function setDestinoOne(uint idDrone) public payable returns (bool){
            uint amount = msg.value;
            require(amount >= 10 ether, "Amount should be higer then 10 Ether");
            require(idDrone <= qntDroneCadastrados && idDrone > 0 , "Drone nao cadastrado");
            require(dronesCadastrados[idDrone-1].flying == 0 , "Drone nao disponivel.");
          
            uint amountToSend = 10 ether;

            if(amount > amountToSend){
                uint change = msg.value - amountToSend; 
                payable(msg.sender).transfer(change);   
            }
            (contractOwner).transfer(amount);
         
            dronesCadastrados[idDrone-1].latitude_deg = "37.5236476"; 
            dronesCadastrados[idDrone-1].longitude_deg = "-122.2551089";
            dronesCadastrados[idDrone-1].flying = 1;
            
            return true;
        }
        
        function setDestinoTwo(uint idDrone) public payable returns (bool){
            uint amount = msg.value;
            require(amount >= 10 ether, "Amount should be higer then 10 Ether");
            require(idDrone <= qntDroneCadastrados && idDrone > 0 , "Drone nao cadastrado");
            require(dronesCadastrados[idDrone-1].flying == 0 , "Drone nao disponivel.");
          
            uint amountToSend = 10 ether;

            if(amount > amountToSend){
                uint change = msg.value - amountToSend; 
                payable(msg.sender).transfer(change);   
            }
            payable(contractOwner).transfer(amount);

            dronesCadastrados[idDrone-1].latitude_deg = "37.5232366";
            dronesCadastrados[idDrone-1].longitude_deg = "-122.2611083";
            dronesCadastrados[idDrone-1].flying = 1;
            
            return true;
        }
        function setDestinoThree(uint idDrone) public payable returns (bool){
            uint amount = msg.value;
            require(amount >= 10 ether, "Amount should be higer then 10 Ether");
            require(idDrone <= qntDroneCadastrados && idDrone > 0 , "Drone nao cadastrado");
            require(dronesCadastrados[idDrone-1].flying == 0 , "Drone nao disponivel.");
          
            uint amountToSend = 10 ether;

            if(amount > amountToSend){
                uint change = msg.value - amountToSend; 
                payable(msg.sender).transfer(change);   
            }
            (contractOwner).transfer(amount);

            dronesCadastrados[idDrone-1].latitude_deg = "37.53170714024128";
            dronesCadastrados[idDrone-1].longitude_deg = "-122.26597954956488";
            dronesCadastrados[idDrone-1].flying = 1;
            
            return true;
        }

        function getStatusDrone(uint idDrone)public view returns (string memory, string memory,  uint)  {
            return (dronesCadastrados[idDrone -1 ].latitude_deg, dronesCadastrados[idDrone -1].longitude_deg, dronesCadastrados[idDrone -1].flying);
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
