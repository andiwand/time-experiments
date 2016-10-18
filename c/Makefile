CC=gcc
CFLAGS=-c -Wall -D _GNU_SOURCE
LDFLAGS=

all: gpio_station gpio_polling

clean:
	rm -f *.o
	rm -f gpio_station

.c.o:
	$(CC) $(CFLAGS) $< -o $@

gpio_station: gpio_station.o gpio.o shared.o
	$(CC) $(LDFLAGS) $^ -o $@

gpio_polling: gpio_polling.o gpio.o shared.o
	$(CC) $(LDFLAGS) $^ -o $@
