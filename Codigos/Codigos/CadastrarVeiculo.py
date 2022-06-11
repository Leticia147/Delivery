import asyncio
from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)
from web3 import Web3
import time

async def run():
    drone = System()
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    w3.eth.default_account = w3.eth.accounts[1]
    abi = [{'inputs': [], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'inputs': [], 'name': 'getBalance', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'getRegisterDrones', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'getStatusDrone', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'inTheDestiny', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'registerDrone', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'registerDrones', 'outputs': [{'internalType': 'address payable', 'name': 'droneOwner', 'type': 'address'}, {'internalType': 'string', 'name': 'latitude_deg', 'type': 'string'}, {'internalType': 'string', 'name': 'longitude_deg', 'type': 'string'}, {'internalType': 'uint256', 'name': 'flying', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoOne', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoThree', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'idDrone', 'type': 'uint256'}], 'name': 'setDestinoTwo', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'payable', 'type': 'function'}]
    contract_id = Web3.toChecksumAddress('0xeaa7d50e23d7c7cab11d8bc2df939db51d7c186f')
    deliveryDrone = w3.eth.contract(address = contract_id,abi = abi)
    w3.eth.wait_for_transaction_receipt( deliveryDrone.functions.registerDrone().transact())
    idDrone = 1
    await drone.connect(system_address="udp://:14540")
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    while True:
        while deliveryDrone.functions.getStatusDrone(idDrone).call()[2] != 1: 
            print("Aguardando solicitação de entrega...")
            time.sleep(5)    

        if deliveryDrone.functions.getStatusDrone(idDrone).call()[2] == 1:
            mission_items = []
            mission_items.append(MissionItem(
                                    float(deliveryDrone.functions.getStatusDrone(idDrone).call()[0]),
                                    float(deliveryDrone.functions.getStatusDrone(idDrone).call()[1]),
                                    50,
                                    100,
                                    True,
                                    float('nan'),
                                    float('nan'),
                                    MissionItem.CameraAction.NONE,
                                    float('nan'),
                                    float('nan'),
                                    float('nan'),
                                    float('nan'),
                                    float('nan')))
                                
            mission_plan = MissionPlan(mission_items)

            print("-- Uploading mission")
            await drone.mission.upload_mission(mission_plan)

            print("Waiting for drone to have a global position estimate...")
            async for health in drone.telemetry.health():
                if health.is_global_position_ok and health.is_home_position_ok:
                    print("-- Global position state is good enough for flying.")
                    break 
         
            print("-- Starting mission")
            await drone.mission.start_mission()
    
            print("-- Arming")
            await drone.action.arm() 

            async for mission_progress in drone.mission.mission_progress():
                print("-- Delivering...")
                if(mission_progress.current == mission_progress.total):
                    print("At a delivery point...")
                    await drone.action.land();
                    print("-- Landing...")
                    async for is_in_air in drone.telemetry.in_air():
                        if not is_in_air:
                            break
                    break

            deliveryDrone.functions.inTheDestiny(idDrone).transact()
            print("Delivery Sucessfull complete!")
            print(w3.eth.get_balance(w3.eth.default_account)/1000000000000000000)
            async for state in drone.core.connection_state():
                if state.is_connected:
                    print(f"-- Connected to drone!")
                    break

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
