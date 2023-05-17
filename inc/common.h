#ifndef COMMON_PARAMS_H_
#define COMMON_PARAMS_H_
#include "utils.h"
struct CommonInfoT {
    int work_mode = 0;
    int exit_flag = 0;
};

template<class Archive>
void serialize(Archive& ar, CommonInfoT& data) {
  ar(data.work_mode, data.exit_flag);
}

struct ScaleInfoT {
  float scale_width = 1;
  float scale_height = 1;
};

template<class Archive>
void serialize(Archive& ar, ScaleInfoT& data) {
  ar(data.scale_width, data.scale_height);
}

#endif /* COMMON_PARAMS_H_ */