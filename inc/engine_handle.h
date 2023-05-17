#ifndef ENGINE_HANDLE_H_
#define ENGINE_HANDLE_H_

#include "common.h"
#include "i2c.h"
#include "wheel.h"

/**
 * @brief: common post_process
 */
class EngineHandle{
public:
    EngineHandle();
    ~EngineHandle() = default;
    int Init( );
    int HandleResults();
    int HandleGetWorkMode();

private:

    int common_shm_init(void);
    int common_shm_process_handle(void);
    int hand_all(void);
    wheel wheel_ctrl;

};

#endif /* COMMON_HANDLE_H_ */