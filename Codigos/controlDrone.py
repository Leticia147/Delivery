#!/usr/bin/env python3 
# executar o gazebo
# cd /home/leticia/Documentos/TCC/integration/blockchain-based-delivery-drone-system/PX4-Autopilot
# make px4_sitl gazebo_typhoon_h480__ksql_airport
#
#comparar com ataque haquer em carros da tesla que chegava perto e ligava, sistemas ciberfisicos 
# de pagamanento cyberfisico 
#ganache para rodar o ganache CLI
#cartoes de cŕeditos clonados 
#
#o drone chama o contrato
#usar a funçaõ que bloqueia o drone
#o deploy contrato é separado, mas o é só o drone que vai poder editar, ver pelo dono da carteira
#

import asyncio
from mavsdk import System
from web3 import Web3
import time
from solcx import compile_source


def atDestino(atual_latitude_deg,dest_latitude_deg, atual_longitude_deg,  dest_longitude_deg):
    n = 4
    m = n
    atual_latitude_deg_truncated = int(float(atual_latitude_deg) * 10**n)/10**n
    atual_longitude_deg_truncated = int(float(atual_longitude_deg) * 10**m)/10**m
    dest_latitude_deg_truncated = int(float(dest_latitude_deg) * 10**n)/10**n
    dest_longitude_deg_truncated = int(float(dest_longitude_deg) * 10**m)/10**m
    print("atDestino?")
    if(atual_latitude_deg_truncated == dest_latitude_deg_truncated and atual_longitude_deg_truncated == dest_longitude_deg_truncated):
        print("são iguais")
        return True

    return False

async def run():
    drone = System()

    # no ganache cli:
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    # set pre-funded account as sender
    w3.eth.default_account = w3.eth.accounts[1]

    # get abi
    abi = abi = [{'inputs': [], 'stateMutability': 'payable', 'type': 'constructor'}, {'inputs': [], 'name': 'cadastrarDrone', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'contractOwner', 'outputs': [{'internalType': 'address payable', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'deposit', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'dronesCadastrados', 'outputs': [{'internalType': 'address payable', 'name': 'droneOwner', 'type': 'address'}, {'internalType': 'string', 'name': 'latitude_deg', 'type': 'string'}, {'internalType': 'string', 'name': 'longitude_deg', 'type': 'string'}, {'internalType': 'uint256', 'name': 'flying', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'getBalance', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}, {'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'getStatusDrone', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'inTheDestiny', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}, {'internalType': 'address payable', 'name': '', 'type': 'address'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoOne', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoThree', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoTwo', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [], 'name': 'totalDronesCadastrados', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}]
    contract_id = Web3.toChecksumAddress('0xca0ce4b7eafc7a6a773be5015c5c6d0eb52837c7')
    deliveryDrone = w3.eth.contract(address = contract_id,abi = abi)
    w3.eth.wait_for_transaction_receipt( deliveryDrone.functions.cadastrarDrone().transact())

    idDrone = 1
     
    print(deliveryDrone.functions.getStatusDrone(idDrone).call())

    while True:
         
        while deliveryDrone.functions.getStatusDrone(idDrone).call()[2] != 1: 
            print("Aguardando voo")
            print(w3.eth.get_balance(w3.eth.default_account)/1000000000000000000)
            time.sleep(5)    
    
        #ler dados de uma trsação especifica 
        #transaction = w3.eth.get_transaction('0x8d2ed830adf2285fb6f80c542852fdc329083085658fe019c8c49d61c0fb09cd') 
        #print(delivery.decode_function_input(transaction.input))

        if deliveryDrone.functions.getStatusDrone(idDrone).call()[2] == 1:
            await drone.connect(system_address="udp://:14540")

            print("Waiting for drone to connect...")
            async for state in drone.core.connection_state():
                if state.is_connected:
                    print(f"-- Connected to drone!")
                    break

            print("Waiting for drone to have a global position estimate...")
            async for health in drone.telemetry.health():
                if health.is_global_position_ok and health.is_home_position_ok:
                    print("-- Global position state is good enough for flying.")
                    print(drone.telemetry.flight_mode)
                    break

            print("Fetching amsl altitude at home location....")

            print("-- Arming")
            await drone.action.arm() 

            print("-- Taking off")  
            await drone.action.takeoff()

            await asyncio.sleep(1)

            print("-- Going to position: ", deliveryDrone.functions.getStatusDrone(idDrone).call())
            await drone.action.goto_location(float(deliveryDrone.functions.getStatusDrone(idDrone).call()[0]),float(deliveryDrone.functions.getStatusDrone(idDrone).call()[1]), 100 , 0)

            while True:
                print("Staying connected, press Ctrl-C to exit")
                async for position in drone.telemetry.position():
                    print(position," to " , deliveryDrone.functions.getStatusDrone(idDrone).call())
                    await asyncio.sleep(5)
                    print( position.latitude_deg, deliveryDrone.functions.getStatusDrone(idDrone).call()[0],position.longitude_deg, deliveryDrone.functions.getStatusDrone(idDrone).call()[1])
                    if(atDestino( position.latitude_deg, deliveryDrone.functions.getStatusDrone(idDrone).call()[0],position.longitude_deg, deliveryDrone.functions.getStatusDrone(idDrone).call()[1]) == True): 
                        print("-- Chegou ao destino!")
                        await drone.action.land()
                        print("Pousando at" ,position)
                        async for in_air in drone.telemetry.in_air():
                            if in_air:
                                print("in air! Pousando")
                            else:
                                print("on ground! Pousado")
                                deliveryDrone.functions.inTheDestiny(idDrone).transact()
                                break
                        break  
                break
            print("Delivery Sucessfull complete!")
            print(w3.eth.get_balance(w3.eth.default_account)/1000000000000000000)


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
