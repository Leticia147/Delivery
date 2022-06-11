
from web3 import Web3
from solcx import compile_source

 
# no ganache cli:
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# set pre-funded account 2 as sender
w3.eth.default_account = w3.eth.accounts[1]

abi = [{'inputs': [], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'inputs': [], 'name': 'getDestino', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'inTheDestiny', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'setDestinoOne', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'setDestinoThree', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'setDestinoTwo', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}]
contract_id = Web3.toChecksumAddress('0x791755c72bf65b11b761b19be00cfa29843b37b8')
delivery = w3.eth.contract(address = contract_id,abi = abi)

print(delivery.functions.getDestino().call())

try:  
    tx_hash =  delivery.functions.setDestinoOne().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
except:
    if(delivery.functions.getDestino().call()[2] == 1):
        print("Drone indisponível!")
    else:
        print("Erro desconhecido!")    

print(delivery.functions.getDestino().call())


#ler dados de uma trsação especifica 
#transaction = w3.eth.get_transaction('0x8d2ed830adf2285fb6f80c542852fdc329083085658fe019c8c49d61c0fb09cd')
#print(delivery.decode_function_input(transaction.input))