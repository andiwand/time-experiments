CC=gcc
CFLAGS=-c -Wall
LDFLAGS=

all: gpio_station

clean:
	rm -f *.o
	rm -f gpio_station

.c.o:
	$(CC) $(CFLAGS) $< -o $@

gpio_station: gpio_station.o gpio.o shared.o
	$(CC) $(LDFLAGS) $^ -o $@
