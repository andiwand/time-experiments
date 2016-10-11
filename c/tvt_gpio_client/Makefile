MODULE=tvt_gpio_client

CCPREFIX=/opt/raspberry_pi-kernel/tools/arm-bcm2708/arm-bcm2708-linux-gnueabi/bin/arm-bcm2708-linux-gnueabi-
KERNEL_SRC=/lib/modules/$(shell uname -r)/build

obj-m += ${MODULE}.o

all: clean compile

compile:
	#make ARCH=arm CROSS_COMPILE=${CCPREFIX} -C ${KERNEL_SRC} M=$(PWD) modules
	make -C ${KERNEL_SRC} M=$(PWD) modules

clean:
	make -C ${KERNEL_SRC} M=$(PWD) clean

info:
	modinfo ${MODULE}.ko

