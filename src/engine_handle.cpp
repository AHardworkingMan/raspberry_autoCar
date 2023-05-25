#include "engine_handle.h"
#include <ios>
#include <vector>
#include <sstream>
#include <cmath>
#include <regex>

#include <thread>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <malloc.h>
#include <unistd.h>
#include <sys/prctl.h>

#include <sys/shm.h>

#include "uart_print.h"
#include "tcp_server.h"
#include "wheel.h"
#include "i2c.h"
#include "oled.h"
#include "common_post.h"
#include "utils.h"
using namespace std;

namespace {

    char mode_off[20] = "OFF";
    char mode_dange[20] = "Avoid Dange";
    char mode_follow[20] = "Follow Object";
    char mode_road[20] = "Road Run";
    char mode_remote[20] = "Remote";
    char getting_ip[20] = "getting ip";

    int uart_print_count = 0;  // 0: print 1: not print
    oled oled_ctrl;

    struct shared_common_st* shared_stuff;  // shared memory

    struct PostData post_data;  // post data

    void* shared_memory = (void*)0;
    int shmid;  // shared memory id

    int current_work_mode = ASCBOT_ROAD_MODE; // ASCBOT_ROAD_MODE ASCBOT_OFF ASCBOT_REMOTE_MODE ASCBOT_FOLLOW_MODE ASCBOT_DANGE_MODE ASCBOT_IP_MODE ASCBOT_GET_IP_MODE

    int current_remote_left_speed = 0;
    int current_remote_right_speed = 0;
    int current_remote_direction = 0;

    int current_wheel_left_speed = 0;
    int current_wheel_right_speed = 0;

}

// constants
EngineHandle::EngineHandle() {

}

int EngineHandle::common_shm_init(void)  // 初始化共享内存
{
    INFO_LOG("common_shm_init_handle------------ \n");
    shmid = shmget((key_t)1234, sizeof(struct shared_common_st), 0666 | IPC_CREAT);  // 创造共享内存

    if (shmid == -1) {  // 检查共享内存是否创建成功
        ERROR_LOG("shmget failed\n");  // 打印错误信息
        return -1;
    }
     shared_memory = shmat(shmid, (void *)0, 0);  // 附加共享内存
     if (shared_memory == (void *)-1) {  // 检查共享内存是否附加成功
         ERROR_LOG("shmat failed\n");  // 打印错误信息
        return -1;
    }
    shared_stuff = (struct shared_common_st *)shared_memory;  // 将共享内存转换为结构体
    shared_stuff->written_flag = 0;  // 初始化共享内存
    return 0;
}



int EngineHandle::common_shm_process_handle(void)  // 处理共享内存
{
    INFO_LOG(" shared_stuff->written_flag:%d shared_stuff->wheel_speed_written_flag:%d\n", shared_stuff->written_flag,shared_stuff->wheel_speed_written_flag);  // 打印共享内存写入标志位
    if (shared_stuff->written_flag == 1)  // 检查共享内存写入标志位
    {
        post_data.work_mode = shared_stuff->work_mode;  // 读取共享内存
        post_data.remote_direction = shared_stuff->remote_direction;
        post_data.remote_left_speed = shared_stuff->remote_left_speed;
        post_data.remote_right_speed = shared_stuff->remote_right_speed;
        shared_stuff->written_flag = 0;
    }

    if (shared_stuff->wheel_speed_written_flag == 1)
    {
        post_data.wheel_left_speed =  shared_stuff->wheel_left_speed;
        post_data.wheel_right_speed =  shared_stuff->wheel_right_speed;
        shared_stuff->wheel_speed_written_flag = 0;

        if(shared_stuff->wheel_force_stop == 1)  // 强制停止
        {
            post_data.wheel_left_speed = 0;  // 左轮速度
            post_data.wheel_right_speed = 0;  // 右轮速度
        }
    }

    if(shared_stuff->ip_written_flag == 1)  // 获取ip
    {
        strncpy(post_data.ip_address , shared_stuff->ip_address,20);  // ip地址
        shared_stuff->ip_written_flag = 0;  // 重置标志位
        post_data.ip_get_flag = 1;  // ip获取标志位
        ERROR_LOG("post_data.ip_address------------- %s  \n",post_data.ip_address);  // 打印ip地址
    }
    INFO_LOG("left_speed:%d,right_speed:%d\n",post_data.wheel_left_speed,post_data.wheel_right_speed);  // 打印左右轮速度
    return 0;
}

int EngineHandle::Init( ) {
    INFO_LOG("Begin EngineHandle initialize!");
    tcp_server tcp_server_ctrl;  // tcp服务器
    tcp_server_ctrl.tcp_server_create();  // 创建tcp服务器
    wheel_ctrl.wheel_init();  // 初始化电机车轮控制

    common_shm_init();

    oled_ctrl.OLED_Init();
    oled_ctrl.OLED_CLS_RAM();

    oled_ctrl.OLED_ShowStr(0, 0, getting_ip, 1);  // 显示ip获取
    oled_ctrl.OLED_ShowStr(1, 0, mode_off, 1);  // 显示模式
    oled_ctrl.OLED_Screen_display();  // 屏幕显示

    post_data.angle = 0;  // 角度
    post_data.direction = 0;  // 方向
    post_data.work_mode = 0;  // 工作模式
    post_data.ip_get_flag = 0;  // ip获取标志位

    INFO_LOG("End EngineHandle initialize!");
    return 0;
}

int EngineHandle::hand_all(void)
{
    common_shm_process_handle();
    if(post_data.ip_get_flag == 1)  // 对比ip标志位
    {
        oled_ctrl.OLED_RowClear(0,1);  // 清除第一行
        oled_ctrl.OLED_ShowStr(0, 0, post_data.ip_address, 1);  // 显示ip地址
        oled_ctrl.OLED_Screen_display();  // 屏幕显示
        post_data.ip_get_flag = 0; // 重置ip标志位
    }

    if(current_work_mode !=post_data.work_mode)  // 对比工作模式
    {
        current_work_mode = post_data.work_mode;  // 更新工作模式

        oled_ctrl.OLED_RowClear(1,1);  // 清除第二行
        if(current_work_mode==ASCBOT_OFF)  // 当前工作模式为关闭模式
            oled_ctrl.OLED_ShowStr(1, 0, mode_off, 1);  // 显示关闭模式
        else if(current_work_mode == ASCBOT_VOID_DANGER_MODE)  // 当前工作模式为避障模式
            oled_ctrl.OLED_ShowStr(1, 0, mode_dange, 1);  // 显示避障模式
        else if(current_work_mode == ASCBOT_OBJECT_MODE)  // 当前工作模式为物体模式
            oled_ctrl.OLED_ShowStr(1, 0, mode_follow, 1);  // 显示物体模式
        else if(current_work_mode == ASCBOT_ROAD_MODE)  // 当前工作模式为道路模式
            oled_ctrl.OLED_ShowStr(1, 0, mode_road, 1);  // 显示道路模式
        else if(current_work_mode == ASCBOT_REMOTE_MODE)  // 当前工作模式为遥控模式
			oled_ctrl.OLED_ShowStr(1, 0, mode_remote, 1);  // 显示遥控模式

        oled_ctrl.OLED_Screen_display();

        current_wheel_left_speed = 0;
        current_wheel_right_speed = 0;
        wheel_ctrl.wheel_left_move(1,0x00);
        wheel_ctrl.wheel_right_move(1,0x00);

        shared_stuff->wheel_force_stop = 0;
    }

    INFO_LOG("current:%d,%d\n",current_wheel_left_speed,current_wheel_right_speed);  // 打印当前左右轮速度
    if((current_wheel_left_speed!=post_data.wheel_left_speed)||(current_wheel_right_speed!=post_data.wheel_right_speed))
    {
        current_wheel_left_speed = post_data.wheel_left_speed;
        current_wheel_right_speed = post_data.wheel_right_speed;
        INFO_LOG(" current_wheel_left_speed:%d,current_wheel_right_speed:%d\n",current_wheel_left_speed,current_wheel_right_speed);

        if(current_wheel_left_speed<0)
            wheel_ctrl.wheel_left_move(-1,abs(current_wheel_left_speed));
        else
            wheel_ctrl.wheel_left_move(1,abs(current_wheel_left_speed));

        if(current_wheel_right_speed<0)
            wheel_ctrl.wheel_right_move(-1,abs(current_wheel_right_speed));
        else
            wheel_ctrl.wheel_right_move(1,abs(current_wheel_right_speed));
    }

    if((current_remote_left_speed != post_data.remote_left_speed) ||
    (current_remote_right_speed != post_data.remote_right_speed) ||
    (current_remote_direction != post_data.remote_direction))
    {
        current_remote_left_speed = post_data.remote_left_speed;
        current_remote_right_speed = post_data.remote_right_speed;
        current_remote_direction = post_data.remote_direction;
        wheel_ctrl.wheel_left_move(current_remote_direction,current_remote_left_speed);
        wheel_ctrl.wheel_right_move(current_remote_direction,current_remote_right_speed);
    }
    return 0;
}

int EngineHandle::HandleResults( ) {
    INFO_LOG("start Engine Handle Results!\n");
    hand_all();
    return 0;
}

int EngineHandle::HandleGetWorkMode() {
    return current_work_mode;
}