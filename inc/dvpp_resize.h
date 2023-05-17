#pragma once
#include <cstdint>

#include "acl/acl.h"
#include "acl/ops/acl_dvpp.h"
#include "utils.h"

class DvppResize {
public:
    /**
    * @brief Constructor
    * @param [in] stream: stream
    */
    DvppResize(aclrtStream &stream, acldvppChannelDesc *dvppChannelDesc,
               uint32_t width, uint32_t height);

    /**
    * @brief Destructor
    */
    ~DvppResize();

    /**
    * @brief dvpp global init
    * @return result
    */
    Result InitResource();

    /**
    * @brief init dvpp output para
    * @param [in] modelInputWidth: model input width
    * @param [in] modelInputHeight: model input height
    * @return result
    */
    Result InitOutputPara(int modelInputWidth, int modelInputHeight);

    /**
    * @brief gett dvpp output
    * @param [in] outputBuffer: pointer which points to dvpp output buffer
    * @param [out] outputSize: output size
    */
    void GetOutput(void **outputBuffer, int &outputSize);

    /**
    * @brief dvpp process
    * @return result
    */
    Result Process(ImageData& resizedImage, ImageData& srcImage);

private:
    Result InitResizeResource(ImageData& inputImage);
    Result InitResizeInputDesc(ImageData& inputImage);
    Result InitResizeOutputDesc();

    void DestroyResizeResource();
    void DestroyResource();
    void DestroyOutputPara();

    aclrtStream stream_;
    acldvppChannelDesc *dvppChannelDesc_;

    acldvppResizeConfig *resizeConfig_;

    acldvppPicDesc *vpcInputDesc_; // vpc input desc
    acldvppPicDesc *vpcOutputDesc_; // vpc output desc

    uint8_t *inDevBuffer_;  // input pic dev buffer
    void *vpcOutBufferDev_; // vpc output buffer
    uint32_t vpcOutBufferSize_;  // vpc output size
    Resolution size_;
    acldvppPixelFormat format_;
};
