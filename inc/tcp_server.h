
#ifndef TCP_SERVER_H_
#define TCP_SERVER_H_
#include <iostream>
#include <string>
#include <vector>
#include <stdint.h>
#include <stdio.h>

#include "common.h"
#include "gpio.h"
class tcp_server {
public:
    tcp_server(void) ;
    ~tcp_server(void) ;
    int tcp_server_create(void);
private:
    int server_shm_init(void);
    gpio io_ctrl;
};

//int tcp_server_create(void);

#endif // TCP_SERVER_H_
