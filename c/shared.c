#include "shared.h"
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#include "gpio.h"

char* trim(const char* str) {
    while (isspace((unsigned char) *str)) str++;

    if (*str == '\0') {
        char* out = (char*) malloc(1);
        out[0] = '\0';
        return out;
    }

    const char* end = str + strlen(str) - 1;
    while((end > str) && isspace((unsigned char)* end)) end--;
    end++;

    size_t out_size = end - str;
    char* out = (char*) malloc(out_size + 1);
    memcpy(out, str, out_size);
    out[out_size] = '\0';
    return out;
}

char* get_cpuinfo(const char* param) {
    FILE* cpuinfo = fopen("/proc/cpuinfo", "rb");
    char* tmp = 0;
    size_t tmp_size = 0;
    ssize_t r;
    bool matched = false;
    char* result = NULL;
    
    while (1) {
        r = getdelim(&tmp, &tmp_size, ':', cpuinfo);
        if (r < 0) break;
        matched = strstr(tmp, param) != NULL;
        
        r = getdelim(&tmp, &tmp_size, '\n', cpuinfo);
        if (r < 0) break;
        if (matched) break;
    }
    
    if (matched) result = trim(tmp);
    free(tmp);
    fclose(cpuinfo);
    return result;
}

int rpi_version() {
    char* hardware = get_cpuinfo("Hardware");
    if (hardware == NULL) return -1;
    if (strcmp(hardware, "BCM2708")) return RPI_V1;
    if (strcmp(hardware, "BCM2709")) return RPI_V2;
    return -1;
}

void fsleep(float time) {
    sleep((unsigned int) time);
    time -= (unsigned int) time;
    time *= 1000000;
    usleep((unsigned int) time);
}

