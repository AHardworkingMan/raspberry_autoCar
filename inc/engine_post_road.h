#ifndef ENGINE_POST_ROAD_H_
#define ENGINE_POST_ROAD_H_
#include "common.h"
#include "engine_handle.h"
class EnginePostRoad {
public:
    static int _s_flag;
    EnginePostRoad();
    ~EnginePostRoad() = default;
    int Init();
    int HandleResults(float * result,int size, int mode);
    int handle_preview(ImageData& result, int mode);
    private:
    int common_shm_init(void);
    int hand_wheel(void);
    int Handle_off_mode(float *result,int size);
    int Handle_road_mode(float *result,int size);
    EngineHandle EngineHan_3;
};

#endif