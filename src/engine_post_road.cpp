#include "engine_post_road.h"
#include <cstdio>
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
#include "common_post.h"
using namespace std;


namespace {

int wheel_speed_offset = 0;  //(-2----5)

int uart_print_count = 0;

struct shared_common_st *shared_stuff;
void *shared_memory = (void *)0;
int shmid;

struct PostData post_data;
}

int EnginePostRoad::_s_flag = 0;

EnginePostRoad::EnginePostRoad() {

}


int EnginePostRoad::common_shm_init(void)
{
    shmid = shmget((key_t)1234, sizeof(struct shared_common_st), 0666 | IPC_CREAT);
    if (shmid == -1) {
        ERROR_LOG( "shmget failed\n");
        return -1;
    }

    shared_memory = shmat(shmid, (void *)0, 0);

    if (shared_memory == (void *)-1) {
        ERROR_LOG( "shmat failed\n");
        return -1;
    }

    shared_stuff = (struct shared_common_st *)shared_memory;
    shared_stuff->written_flag = 0;
    shared_stuff->wheel_speed_written_flag = 0;

    return 0;
}

int EnginePostRoad::Init() {
    INFO_LOG("EnginePostRoad Begin initialize!\n");

    common_shm_init();

    post_data.angle = 0;
    post_data.direction = 0;
    post_data.work_mode = 0;

    return 0;
}


int EnginePostRoad::hand_wheel(void)
{
    if(post_data.work_mode==ASCBOT_ROAD_MODE)
    {
        if (post_data.angle == 180 && post_data.direction == 1)
        {
            post_data.wheel_left_speed = 0x00;
            post_data.wheel_right_speed = 0x07;
        }
        else  if (post_data.angle == -180 && post_data.direction == 1)
        {
            post_data.wheel_left_speed = 0x07;
            post_data.wheel_right_speed = 0x00;
        }
        else  if (post_data.angle == 0 && post_data.direction == 1)
        {
            post_data.wheel_left_speed = 0x05;
            post_data.wheel_right_speed = 0x05;
        }
        else  if (post_data.angle >= 45 && post_data.direction == 1)
        {
            post_data.wheel_left_speed = -0x03;
            post_data.wheel_right_speed = 0x07;
        }
        else  if (post_data.angle >= 30 && post_data.direction == 1)
        {
            post_data.wheel_left_speed = -0x03;
            post_data.wheel_right_speed = 0x07;
        }
        else  if (post_data.angle >= 15 && post_data.direction == 1)
        {
            post_data.wheel_left_speed = 0x05;
            post_data.wheel_right_speed = 0x05;
        }
        else  if (post_data.angle >= 5 && post_data.direction == 1)
        {
            post_data.wheel_left_speed = 0x05;
            post_data.wheel_right_speed = 0x05;
        }
        else  if (post_data.angle <= -45 && post_data.direction == 1)
        {
            post_data.wheel_left_speed = 0x07;
            post_data.wheel_right_speed = 0x00;
        }
        else  if (post_data.angle <= -30 && post_data.direction == 1)
        {
            post_data.wheel_left_speed = 0x07;
            post_data.wheel_right_speed = 0x00;
        }
        else  if (post_data.angle <= -15 && post_data.direction == 1)
        {
            post_data.wheel_left_speed = 0x05;
            post_data.wheel_right_speed = 0x05;
        }
        else  if (post_data.angle <= -5 && post_data.direction == 1)
        {
            post_data.wheel_left_speed = 0x05;
            post_data.wheel_right_speed = 0x05;
        }
        else  if (post_data.direction == 0)
        {
            post_data.wheel_left_speed = 0;
            post_data.wheel_right_speed = 0;
        }


        if(post_data.work_mode == ASCBOT_ROAD_MODE)
             wheel_speed_offset = 2;
        else
             wheel_speed_offset = 0;

        //set shared memory
        if(shared_stuff->wheel_speed_written_flag == 0)
        {
            shared_stuff->wheel_left_speed = post_data.wheel_left_speed + wheel_speed_offset;
            shared_stuff->wheel_right_speed = post_data.wheel_right_speed + wheel_speed_offset;
            shared_stuff->wheel_speed_written_flag = 1;
        }
    }
    INFO_LOG("road post_data.wheel_left_speed:%d  post_data.wheel_right_speed:%d\n",post_data.wheel_left_speed,post_data.wheel_right_speed);

    return 0;
}
int EnginePostRoad::Handle_off_mode(float *result,int size)
{
    post_data.angle = 0;
    post_data.direction = 0;
    return 0;
}


int EnginePostRoad::Handle_road_mode(float *result,int size)
{
    float pos_x = result[0];
    float pos_y = result[1];

    if(pos_x < 0.3)
    {
        post_data.angle = 45;
        post_data.direction = 1;
    }
    else if(pos_x < 0.4)
    {
        post_data.angle = 30;
        post_data.direction = 1;
    }
    else if(pos_x < 0.45)
    {
        post_data.angle = 15;
        post_data.direction = 1;
    }
    else if(pos_x < 0.49)
    {
        post_data.angle = 5;
        post_data.direction = 1;
    }
     else if(pos_x > 0.7)
    {
         post_data.angle = -45;
         post_data.direction = 1;
    }
    else if(pos_x > 0.6)
    {
        post_data.angle = -30;
        post_data.direction = 1;
    }
    else if(pos_x > 0.55)
    {
        post_data.angle = -15;
        post_data.direction = 1;
    }
    else if(pos_x > 0.51)
    {
         post_data.angle = -5;
         post_data.direction = 1;
    }
    else
    {
         post_data.angle = 0;
         post_data.direction = 1;
    }
    INFO_LOG(" road angle %d, direction %d\n",post_data.angle,post_data.direction);
    return 0;
}


int EnginePostRoad::HandleResults(float * result,int size,int mode) {
    post_data.work_mode = mode;
    INFO_LOG(" enter post road\n");
    if(mode != ASCBOT_ROAD_MODE)
        return 0;
    Handle_road_mode(result,size);
    hand_wheel();
    return 0;
}

int EnginePostRoad::handle_preview(ImageData& result,int mode)
{
    if(mode!=ASCBOT_ROAD_MODE)
        return -1;

    if (shared_stuff->image_data_written_flag == 0)
    {
        memcpy(shared_stuff->image_data, result.data.get(),result.size);
        shared_stuff->image_data_size = result.size;
        shared_stuff->image_data_width = 256;
        shared_stuff->image_data_height = 256;
        shared_stuff->image_data_written_flag = 1;
    }
    return 0;
}
