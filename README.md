# Blockchain-Based Delivery Drone System

Proposta de um sistema de entrega com veículos aéreos não tripulados baseados em Blockchain e Smart Contract. 2022. 

Trabalho de Conclusão de Curso – Curso de Engenharia de Computação, Universidade Tecnológica Federal do Paraná. Pato Branco, 2022.


Repositorio referente ao trabalho - Proposta de um sistema de entrega com veículos aéreos não tripulados baseados em Blockchain e Smart Contract.

--------------------------------------------------------------------------------------------------------------

Após clonar o projeto.


### Instalar o Gazebo  https://gazebosim.org/

	https://docs.px4.io/v1.12/en/simulation/gazebo.html

### Instalar a px4 na pasta PX4-Autopilot:

    	$ git clone https://github.com/PX4/PX4-Autopilot.git

Ir para a pasta em que a px4 foi clonada:

    	$ cd /PX4-Autopilot

Para compilar a PX4:

    	$ make px4_sitl

Executar o gazebo com o drone typhoon_h480 no ambiente vazio (padrão):

    	$ make px4_sitl gazebo_typhoon_h480

### Executar o gazebo com o drone typhoon_h480 e o ambiente aeroporto KSQL:

    	$ make px4_sitl gazebo_typhoon_h480__ksql_airport

	
Setar as variáveis desabilitando o RC failsafe para permitir a execução em software in the loop:

	$ pxh>
	$	param set NAV_RCL_ACT 0
	$	param set NAV_DLL_ACT 0

É possível realizar alguns testes com o veículo na simulação do Gazebo:
Levantar voo:

	$ pxh> 
	$	commander takeoff	
	
Pousar:

	$ pxh>
	$	commander land
	
### Instalar a ferramenta Ganache CLI https://trufflesuite.com/ganache/ 

	https://www.npmjs.com/package/ganache-cli
	
Para executar Ganache CLI:

	$ 	ganache

Os arquivos com os códigos para os testes estão em:

	$ 	cd ~/Codigos/Codigos
	
### Necessário instalar as bibliotecas para Python 3

	mavsdk: https://github.com/mavlink/MAVSDK-Python
	web3: 	https://web3py.readthedocs.io/en/stable/   	https://pypi.org/project/web3/
	solcx:  https://solcx.readthedocs.io/en/latest/ 	https://pypi.org/project/py-solc-x/	

#### Para desploy do Smart Contract na Blockchain Ethereum local fornecida pelo Ganache:

	$ 	SmartContractDelivery.py 
	
#### Para integração VANT-Smart Contract:
	
	$ 	CadastrarVeiculo.PY

#### Para solicitação de entrega: 

	$	DestinoOne.py
	$	DestinoTwo.py
	$	DestinoThree.py

