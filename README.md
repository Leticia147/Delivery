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

    $ cd ~//blockchain-based-delivery-drone-system/PX4-Autopilot
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

### É necessário baixar e intalar a px4 na pasta PX4-Autopilot que está vazia, para isso:
    $ cd /home/leticia/Documentos/TCC/integration/blockchain-based-delivery-drone-system/
    $ git clone https://github.com/PX4/PX4-Autopilot.git

### Ir para a pasta em que a px4 foi clonada:
    $ cd /home/leticia/Documentos/TCC/integration/blockchain-based-delivery-drone-system/PX4-Autopilot

### Para compilar primeira vez:
    $ make px4_sitl

### Executar o gazebo com o drone typhoon_h480 no mundo vazio (padrão):
    $ make px4_sitl gazebo_typhoon_h480

### Executar o gazebo com o drone typhoon_h480 no mundo aeroporto KSQL:
    $ make px4_sitl gazebo_typhoon_h480__ksql_airport

### You can bring it into the air by typing:
pxh> 
	$	commander takeoff	
	
### Caso o drone não voar, setar essas variáveis:

pxh>
	$	param set NAV_RCL_ACT 0
	$	param set NAV_DLL_ACT 0

### You can bring it down from air by typing:
pxh>
	$	commander land
	
### Para executar o ganache, digitar no terminal
$ ganache

### Os arquivo de blockchain e smartcontracts e drone estão aqui
$ cd /home/leticia/Documentos/TCC/integration/blockchain-based-delivery-drone-system/tests/MAVSDK-Python/tests


# Tcc
