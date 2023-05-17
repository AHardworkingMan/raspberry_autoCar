#ifndef ENGINE_POST_DANGE_H_
#define ENGINE_POST_DANGE_H_
#include "common.h"
#include "engine_handle.h"

/**
 * @brief: common post_process
 */
class EnginePostDange{
public:
    static int _s_flag ;
  /**
   * @brief: construction function
   */
  EnginePostDange();

  /**
   * @brief: the destruction function
   */
  ~EnginePostDange() = default;

  /**
   * @brief: common post_process engine initialize
   * @param [in]: engine's parameters which configured in graph.config
   * @param [in]: model description
   * @return: HIAI_StatusT
   */

    int Init();

  /**
   * @brief: engine processor
   *         1. dealing results
   *         2. call OSD to draw box and label if needed
   *         3. call DVPP to change YUV420SP to JPEG
   *         4. call presenter agent to send JPEG to server
   * @param [in]: input size
   * @param [in]: output size
   */
    int HandleResults(float* Pdata,int size, int mode);
    int handle_preview(ImageData& result, int mode);

private:
    int common_shm_init(void);
    int hand_wheel(void);
    int Handle_dange_mode(float *result,int size);
    int Handle_off_mode(float *result,int size);
    int Handle_remote_mode(float *result,int size);
    EngineHandle EngineHan;
    //    i2c i2c_ctrl;
    //    wheel wheel_ctrl;


};

#endif /* COMMON_POST_DANGE_H_ */