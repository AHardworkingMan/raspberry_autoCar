#include <iostream>
#include "acl/acl.h"
#include "dvpp_resize.h"
#include "dvpp_process.h"

using namespace std;

DvppProcess::DvppProcess()
    : isInitOk_(false), dvppChannelDesc_(nullptr) {
    isGlobalContext_ = false;
}

DvppProcess::~DvppProcess()
{
    DestroyResource();
}

void DvppProcess::DestroyResource()
{
    aclError aclRet;
    if (dvppChannelDesc_ != nullptr) {
        aclRet = acldvppDestroyChannel(dvppChannelDesc_);
        if (aclRet != ACL_SUCCESS) {
            ERROR_LOG("acldvppDestroyChannel failed, aclRet = %d", aclRet);
        }

        (void)acldvppDestroyChannelDesc(dvppChannelDesc_);
        dvppChannelDesc_ = nullptr;
    }

    INFO_LOG("end to destroy context");
}

Result DvppProcess::init_resource(aclrtStream& stream)
{
    aclError aclRet;

    dvppChannelDesc_ = acldvppCreateChannelDesc();
    if (dvppChannelDesc_ == nullptr) {
        ERROR_LOG("acldvppCreateChannelDesc failed");
        return FAILED;
    }

    aclRet = acldvppCreateChannel(dvppChannelDesc_);
    if (aclRet != ACL_SUCCESS) {
        ERROR_LOG("acldvppCreateChannel failed, aclRet = %d", aclRet);
        return FAILED;
    }
    stream_ = stream;
    isInitOk_ = true;
    INFO_LOG("dvpp init resource ok");
    return SUCCESS;
}

Result DvppProcess::resize(ImageData& dest, ImageData& src,
                        uint32_t width, uint32_t height) {
    DvppResize resizeOp(stream_, dvppChannelDesc_, width, height);
    return resizeOp.Process(dest, src);
}