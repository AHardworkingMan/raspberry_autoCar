#pragma once
#include <cstdint>

#include "acl/acl.h"
#include "acl/ops/acl_dvpp.h"
#include "utils.h"

/**
 * DvppProcess
 */
class DvppProcess {
public:
    DvppProcess();

    ~DvppProcess();

    Result resize(ImageData& src, ImageData& dest, uint32_t width, uint32_t height);
    Result cvtjpeg2yuv420sp(ImageData& src, ImageData& dest);
    Result cvtyuv420sp2jpeg(ImageData& dest, ImageData& src);
    Result init_resource(aclrtStream& stream);

protected:
    int isInitOk_;
    aclrtStream stream_;
    acldvppChannelDesc *dvppChannelDesc_;
    bool isGlobalContext_;

private:
    void DestroyResource();
};
