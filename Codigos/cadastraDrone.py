
from web3 import Web3

# no ganache cli:
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# set pre-funded account 2 as sender
w3.eth.default_account = w3.eth.accounts[1]


# get abi
abi = [{'inputs': [], 'stateMutability': 'payable', 'type': 'constructor'}, {'inputs': [], 'name': 'cadastrarDrone', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'contractOwner', 'outputs': [{'internalType': 'address payable', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'deposit', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'dronesCadastrados', 'outputs': [{'internalType': 'address payable', 'name': 'droneOwner', 'type': 'address'}, {'internalType': 'string', 'name': 'latitude_deg', 'type': 'string'}, {'internalType': 'string', 'name': 'longitude_deg', 'type': 'string'}, {'internalType': 'uint256', 'name': 'flying', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'getBalance', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'getStatusDrone', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'recieve', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoOne', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoThree', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoTwo', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [], 'name': 'totalDronesCadastrados', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'withdraw', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'payable', 'type': 'function'}]
contract_id = Web3.toChecksumAddress('0x747ff7bd12b47fead567f775f3a9de0e48ff3fe4')
deposita = w3.eth.contract(address = contract_id,abi = abi)

#receipt =  w3.eth.wait_for_transaction_receipt( deposita.functions.cadastrarDrone().transact())
print( deposita.functions.totalDronesCadastrados().call())

idDrone = 1
#transaction = w3.eth.get_transaction(w3.toHex(w3.eth.send_transaction(tx)))  #transferindo valor
#print(transaction)



#transaction = w3.eth.get_transaction('0xe8ca4a6bce23e1a1ddf23e75509601ecb35367966a5692056cee66d49aaaf6b9') 
#print(transaction)

#print( deposita.functions.getBalance().call())

#print(deposita.functions.setDestinoOne(idDrone).transact({'from': w3.eth.default_account,'value': w3.toWei(10,'ether')}))


print( deposita.functions.withdraw(1).transact())


print(w3.eth.get_balance(w3.eth.accounts[0])/1000000000000000000)
print(w3.eth.get_balance(w3.eth.accounts[1])/1000000000000000000)
print(w3.eth.get_balance(w3.eth.accounts[2])/1000000000000000000)
print(w3.eth.get_balance(w3.eth.accounts[3])/1000000000000000000)
