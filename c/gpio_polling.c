#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <time.h>
#include "gpio.h"
#include "shared.h"

int main(int argc, char** argv) {
    int flags = EDGE_RISING | EDGE_FALLING;
    int pin;
    
    switch (argc) {
    case 3:
        flags = strtol(argv[2], NULL, 10);
    case 2:
        pin = strtol(argv[1], NULL, 10);
        break;
    default:
        printf("invalid arguments\n");
    }
    
    gpio_t gpio;
    defaults(&gpio);
    
    INP_GPIO(gpio, pin);
    
    int last = GET_GPIO(gpio, pin);
    int now;
    struct timespec ts;
    while (1) {
        clock_gettime(CLOCK_REALTIME, &ts);
        now = GET_GPIO(gpio, pin);
        if (last != now) {
            if ((flags & EDGE_RISING) | (flags & EDGE_FALLING)) {
                printf("%ld.%ld %d\n", ts.tv_sec, ts.tv_nsec, now != 0);
            }
        }
        last = now;
    }
    
    return 0;
}

