import asyncio
from mavsdk import System
from web3 import Web3
import time

def atDestino(atual_latitude_deg,dest_latitude_deg, atual_longitude_deg,  dest_longitude_deg):
    n = 5
    m = n
    atual_latitude_deg_truncated = int(float(atual_latitude_deg) * 10**n)/10**n
    atual_longitude_deg_truncated = int(float(atual_longitude_deg) * 10**m)/10**m
    dest_latitude_deg_truncated = int(float(dest_latitude_deg) * 10**n)/10**n
    dest_longitude_deg_truncated = int(float(dest_longitude_deg) * 10**m)/10**m
    print("atDestino?") 
    print( atual_latitude_deg_truncated ," " , dest_latitude_deg_truncated ," ", atual_longitude_deg_truncated ," ", dest_longitude_deg_truncated)

    if(atual_latitude_deg_truncated == dest_latitude_deg_truncated and atual_longitude_deg_truncated == dest_longitude_deg_truncated):
        print("são iguais")
        return True

    return False

async def run():
    drone = System()
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    w3.eth.default_account = w3.eth.accounts[1]
    abi = [{'inputs': [], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'inputs': [], 'name': 'getBalance', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'getRegisterDrones', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'getStatusDrone', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'inTheDestiny', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'registerDrone', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'registerDrones', 'outputs': [{'internalType': 'address payable', 'name': 'droneOwner', 'type': 'address'}, {'internalType': 'string', 'name': 'latitude_deg', 'type': 'string'}, {'internalType': 'string', 'name': 'longitude_deg', 'type': 'string'}, {'internalType': 'uint256', 'name': 'flying', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoOne', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoThree', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoTwo', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}]
    contract_id = Web3.toChecksumAddress('0x63842de811f63b41b2c68447be7599350f41b1df')
    deliveryDrone = w3.eth.contract(address = contract_id,abi = abi)
    w3.eth.wait_for_transaction_receipt( deliveryDrone.functions.registerDrone().transact())
    idDrone = 1
    while True:
        while deliveryDrone.functions.getStatusDrone(idDrone).call()[2] != 1: 
            print("Aguardando solicitação de entrega...")
            time.sleep(5)    

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
            await drone.action.set_takeoff_altitude(80)
            await drone.action.takeoff()

            print("-- Going to position: ", deliveryDrone.functions.getStatusDrone(idDrone).call())
            
            await drone.action.goto_location(float(deliveryDrone.functions.getStatusDrone(idDrone).call()[0]),float(deliveryDrone.functions.getStatusDrone(idDrone).call()[1]), 80 , 0)
            
            while True:
                print("Staying connected, press Ctrl-C to exit")
                async for position in drone.telemetry.position():
                    print(position," to " , deliveryDrone.functions.getStatusDrone(idDrone).call())
                    async for position_ned in  drone.telemetry.position_velocity_ned():
                        print(position_ned.velocity)
                        break

                    await asyncio.sleep(5)
                    print( position.latitude_deg, deliveryDrone.functions.getStatusDrone(idDrone).call()[0],position.longitude_deg, deliveryDrone.functions.getStatusDrone(idDrone).call()[1])
                    if(atDestino( position.latitude_deg, deliveryDrone.functions.getStatusDrone(idDrone).call()[0],position.longitude_deg, deliveryDrone.functions.getStatusDrone(idDrone).call()[1])): 
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


