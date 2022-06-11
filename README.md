# Blockchain-Based Delivery Drone System

## Build PX4-Autopilot

### Build (Using the jMAVSim Simulator)

First we'll build a simulated target using a console environment. This allows us to validate the system setup before moving on to real hardware and an IDE.

Navigate into the PX4-Autopilot directory and start jMAVSim using the following command:



    $ cd @PROJECT_FOLDER@/blockchain-based-delivery-drone-system
    $ git submodule update --init --recursive
    $ cd PX4-Autopilot
    $ bash ./Tools/setup/ubuntu.sh
    $ make px4_sitl jmavsim

The drone can be flown by typing:

    $ pxh> commander takeoff

### Build (Using the Gazebo Simulator)

    $ cd ~/blockchain-based-delivery-drone-system/PX4-Autopilot
    $ make px4_sitl gazebo

## Install MAVSDK

First, download the prebuilt C++ [MAVSDK library version 1.0.8](https://github.com/mavlink/MAVSDK/releases/tag/v1.0.8)



## Usage

WIP

Demonstration

![](figures/out.mp4)

--------------------------------------------------------------------------------------------------------------

#### pwd pega o caminho atual

### Ir para a raiz
$ cd ~

### Para instalar a px4 na pasta PX4-Autopilot:
    $ cd ~/TCC/integration/blockchain-based-delivery-drone-system/
    $ git clone https://github.com/PX4/PX4-Autopilot.git

### Ir para a pasta em que a px4 foi clonada:
    $ cd /PX4-Autopilot

### Para compilar ã primeira vez:
    $ make px4_sitl

### Executar o gazebo com o drone typhoon_h480 no ambiente vazio (padrão):
    $ make px4_sitl gazebo_typhoon_h480

### Executar o gazebo com o drone typhoon_h480 e o ambiente aeroporto KSQL:
    $ make px4_sitl gazebo_typhoon_h480__ksql_airport

	
### Setar as variáveis para permitir a execução em software in the loop é preciso desabilitar RC failsafe:

$ pxh>
$	param set NAV_RCL_ACT 0
$	param set NAV_DLL_ACT 0

### É possível realizar alguns testes com a simulação do Gazebo, como:
### Levantar voo:
$ pxh> 
$	commander takeoff	
	
### Pousar:
$ pxh>
$	commander land
	
	
### Para executar o ganache CLI:
$ ganache

### Os arquivos com os códigos estão em:
$ cd ~/TCC/integration/blockchain-based-delivery-drone-system/Codigos/Codigos

Para desploy do Smart Contract na Blockchain Ethereum local fornecida pelo Ganache:

$ 	SmartContractDelivery.py 
	
Para integração VANT-Smart Contract:
	
$ 	CadastrarVeiculo.PY

Para solicitação de entrega: 

$	DestinoOne.py
$	DestinoTwo.py
$	DestinoThree.py

