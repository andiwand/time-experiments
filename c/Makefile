CC=gcc
CFLAGS=-c -std=c11 -Wall -D _GNU_SOURCE
LDFLAGS=

all: adjtimex gpio_station gpio_polling

clean:
	rm -f *.o
	rm -f adjtimex gpio_station gpio_polling

.c.o:
	$(CC) $(CFLAGS) $< -o $@

adjtimex: adjtimex.o
	$(CC) $(LDFLAGS) $^ -o $@

gpio_station: gpio_station.o gpio.o shared.o
	$(CC) $(LDFLAGS) $^ -o $@

 gpio_polling: gpio_polling.o gpio.o shared.o
	$(CC) $(LDFLAGS) $^ -o $@
