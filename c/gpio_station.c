#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <time.h>
#include "gpio.h"
#include "shared.h"

void send(void);
void sig_handler(int signo);

volatile unsigned* gpio;
int pin;

int main(int argc, char** argv) {
    float interval = 1;
    
    switch (argc) {
    case 3:
        interval = strtof(argv[2], NULL);
    case 2:
        pin = strtol(argv[1], NULL, 10);
        break;
    default:
        printf("invalid arguments\n");
    }
    
    int version = rpi_version();
    gpio = gpio_setup(version);
    
    INP_GPIO(pin);
    OUT_GPIO(pin);
    
    if (interval == 0) {
        signal(SIGUSR1, sig_handler);
        while (1) sleep(1);
    } else {
        while (1) {
            fsleep(interval);
            send();
        }
    }
    
    return 0;
}

void send(void) {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    
    GPIO_SET = 1 << pin;
    usleep(10);
    GPIO_CLR = 1 << pin;
    
    printf("%ld.%ld\n", ts.tv_sec, ts.tv_nsec);
}

void sig_handler(int signo) {
    send();
}

