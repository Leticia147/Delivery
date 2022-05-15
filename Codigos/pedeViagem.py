
from web3 import Web3

# no ganache cli:
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))


# set pre-funded account 2 as sender
w3.eth.default_account = w3.eth.accounts[2]


# get abi
abi = [{'inputs': [], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'inputs': [], 'name': 'cadastrarDrone', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'dronesCadastrados', 'outputs': [{'internalType': 'address payable', 'name': 'droneOwner', 'type': 'address'}, {'internalType': 'string', 'name': 'latitude_deg', 'type': 'string'}, {'internalType': 'string', 'name': 'longitude_deg', 'type': 'string'}, {'internalType': 'uint256', 'name': 'flying', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'getBalance', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'getStatusDrone', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'inTheDestiny', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoOne', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoThree', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoTwo', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [], 'name': 'totalDronesCadastrados', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}]
contract_id = Web3.toChecksumAddress('0x4fb3cc0d5eb73bf4cc03e50ad16ce7fe92c93412')
deposita = w3.eth.contract(address = contract_id,abi = abi)


print( deposita.functions.totalDronesCadastrados(), "totalDronesCadastrados")

print( deposita.functions.getBalance().call()/1000000000000000000)

print(deposita.functions.setDestinoTwo(1).transact({'from': w3.eth.default_account,'value': w3.toWei(10,'ether')}))

print(w3.eth.get_balance(w3.eth.accounts[0])/1000000000000000000, "Saldo da carteira conta 1")
print(w3.eth.get_balance(w3.eth.accounts[1])/1000000000000000000, "Saldo da carteira conta 2")
print(w3.eth.get_balance(w3.eth.accounts[2])/1000000000000000000, "Saldo da carteira conta 3")
print(w3.eth.get_balance(w3.eth.accounts[3])/1000000000000000000, "Saldo da carteira conta 4")
print( deposita.functions.getBalance().call()/1000000000000000000, "Saldo da carteira smart contract")