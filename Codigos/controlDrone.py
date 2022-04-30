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


import asyncio
from mavsdk import System
from web3 import Web3
import time
from solcx import compile_source


def atDestino(atual_latitude_deg,dest_latitude_deg, atual_longitude_deg,  dest_longitude_deg, altura):
    n = 5
    m = n+1
    atual_latitude_deg_truncated = int(float(atual_latitude_deg) * 10**n)/10**n
    atual_longitude_deg_truncated = int(float(atual_longitude_deg) * 10**m)/10**m
    dest_latitude_deg_truncated = int(float(dest_latitude_deg) * 10**n)/10**n
    dest_longitude_deg_truncated = int(float(dest_longitude_deg) * 10**m)/10**m

    print(atual_latitude_deg, atual_longitude_deg ,dest_latitude_deg, dest_longitude_deg)
    print(atual_latitude_deg_truncated, atual_longitude_deg_truncated ,dest_latitude_deg_truncated, dest_longitude_deg_truncated)

    if(atual_latitude_deg_truncated == dest_latitude_deg_truncated and atual_longitude_deg_truncated == dest_longitude_deg_truncated):
        print("são iguais")
        if(altura > 2.5):
            print("esperando pousar")
            return False
        return True

    return False

async def run():
    drone = System()

    # conectado no ganache cli:
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    # set pre-funded account 2 as sender
    w3.eth.default_account = w3.eth.accounts[1]

    abi = [{'inputs': [], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'inputs': [], 'name': 'getDestino', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'inTheDestiny', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'setDestinoOne', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'setDestinoThree', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'setDestinoTwo', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}]
    contract_id = Web3.toChecksumAddress('0xaed7328b0970a94009f26a00ced1088d4bb3c5b5')
    delivery = w3.eth.contract(address = contract_id,abi = abi)

    while True:
        
        print(delivery.functions.getDestino().call())

        dataContract = delivery.functions.getDestino().call()     # dataContract [ latitude_deg , longitude_deg , flying]
        
        while dataContract[2] != '1': 
            time.sleep(5)    
            dataContract = delivery.functions.getDestino().call()
            print(dataContract)   

        #ler dados de uma trsação especifica 
        #transaction = w3.eth.get_transaction('0x8d2ed830adf2285fb6f80c542852fdc329083085658fe019c8c49d61c0fb09cd') 
        #print(delivery.decode_function_input(transaction.input))

        if dataContract[2] == '1':
            print("entroooooooooooou")
            await drone.connect(system_address="udp://:14540")

        #  status_text_task = asyncio.ensure_future(print_status_text(drone))

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

            print("going to position: ", dataContract)
            await drone.action.goto_location(float(dataContract[0]),float(dataContract[1]), 40 , 0)

            while True:
                print("Staying connected, press Ctrl-C to exit")
                async for position in drone.telemetry.position():
                    print(position)
                    print(dataContract)
                    await asyncio.sleep(5)
                    if(atDestino( position.latitude_deg, dataContract[0],position.longitude_deg, dataContract[1], position.absolute_altitude_m) == True): 
                        print("chegou")
                        delivery.functions.inTheDestiny().transact()
                        break
                    break
                if(atDestino( position.latitude_deg, dataContract[0],position.longitude_deg, dataContract[1],position.absolute_altitude_m) == True): 
                    print("chegou")
                    break

            print("finalizado")

async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
