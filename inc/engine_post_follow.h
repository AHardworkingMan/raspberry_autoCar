#ifndef ENGINE_POST_FOLLOW_H_
#define ENGINE_POST_FOLLOW_H_
#include "common.h"
#include "engine_handle.h"

/**
 * @brief: common post_process
 */
class EnginePostFollow {
public:
    static int _s_flag;
    EnginePostFollow();
    ~EnginePostFollow() = default;
    int Init();
    int handle_preview(ImageData& result, int mode);
    int HandleResults(float* result, int size, int mode);
private:
    int common_shm_init(void);
    int hand_wheel(void);
    int Handle_off_mode(float* result, int size);
    int Handle_follow_mode(float* result, int size);
    int Handle_object_mode(float* result, int size);
    EngineHandle EngineHan_2;

};

#endif /* COMMON_POST_DANGE_H_ */
