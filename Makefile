###########################################################################
# PX4 Makefile
# 
# A useful PX4 commands
#
# @Author: Jeferson Lima
###########################################################################

.PHONY: start_gazebo build test_takeoff env_vars

MODEL="typhoon_h480"
WORLD="ksql_airport"

.DEFAULT: help
help:
	@echo "make tests_takeoff"
	@echo "     Simple takeoff test" 

test_takeoff:
	./build/bin/test_takeoff udp://:14540

build:
	@cmake -Bbuild -H.
	@cmake --build build -j$(nproc)

build_tests:
	@cmake -Bbuild -H. -DCOMPILE_TESTS=YES
	@cmake --build build -j$(nproc)

start_gazebo:
	@cd PX4-Autopilot/ && $(MAKE) px4_sitl gazebo_$(MODEL)__$(WORLD)

env_vars:
	@cd PX4-Autopilot/ && $(SOURCE) Tools/setup_gazebo.bash $(PWD)/PX4-Autopilot $(PWD)/PX4-Autopilot/build/px4_sitl_default


clean:
	rm -rf build


