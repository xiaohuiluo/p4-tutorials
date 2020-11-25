OUT_DIR=./build
P4C_BM_EXE=p4c-bm2-ss
BMV2_PP_FLAGS=-DTARGET_BMV2

all: build

build: ipv4_fwd.p4
	$(info ************ COMPILING P4 PROGRAM ************)
	mkdir -p $(OUT_DIR)
	$(P4C_BM_EXE) --arch v1model -o $(OUT_DIR)/bmv2.json \
		$(BMV2_PP_FLAGS) $(OTHER_PP_FLAGS) \
		ipv4_fwd.p4

topo: build/bmv2.json
	$(info *********** Run mininet with topo ************)
	sudo python3 topo.py --behavioral-exe simple_switch --json build/bmv2.json

table: tables.txt
	$(info *********** Add table entries to bmv2 switch ************)
	sudo simple_switch_CLI --thrift-port=9090 < tables.txt

clean:
	rm -rf ./build
