CC=gcc
CFLAGS=-c -Wall
LDFLAGS=
SOURCES=tvt_gpio_server.c gpio.c shared.c
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=tvt_gpio_server

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.c.o:
	$(CC) $(CFLAGS) $< -o $@

