#ifndef SHARED_H_
#define SHARED_H_

char* trim(const char* str);
char* get_cpuinfo(const char* param);
int rpi_version();
void fsleep(float time);

#endif // SHARED_H_

