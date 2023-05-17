#ifndef _CAMERA_H
#define _CAMERA_H

#include "utils.h"
#define CAMERA_NUM     (2)

class Camera {
public:
    Camera(uint32_t id = 0, uint32_t fps = 5, uint32_t width = 1280, uint32_t height = 720);
    ~Camera();
    Result open(int channelID);
    Result close(int channelID);
    Result Read(int channelID,ImageData& frame);
    bool IsOpened(int channelID);
    private:
    uint32_t id_;
    uint32_t fps_;
    uint32_t width_;
    uint32_t height_;
    uint32_t size_;

    Result SetProperty(int channelID);
    bool isAlign_;
    bool isOpened_[2];

    void* outBuf_ = nullptr ;
};

#endif
