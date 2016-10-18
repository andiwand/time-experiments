#ifndef SHARED_H_
#define SHARED_H_

#include "gpio.h"

char* trim(const char* str);
char* get_cpuinfo(const char* param);
int rpi_version();
void fsleep(float time);
void defaults(gpio_t* gpio);

#endif // SHARED_H_

