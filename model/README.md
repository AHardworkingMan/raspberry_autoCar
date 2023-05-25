English|[中文](./README_CN.md)

# Model specification

### Track following driving model

Depend on ResNet-18

The road has a white background, black lines, and black dashed lines in the middle. If there are any differences, data collection and training should be conducted again.

Corresponding model file: road_following_model.om

### Obstacle avoidance model

Depend on VGG16-SSD

Corresponding model file: collision_avoidance_model.om

### Object following model

Depend on ResNet-18

Following palm movement.

Corresponding model file: road_object_detection_deploy.om