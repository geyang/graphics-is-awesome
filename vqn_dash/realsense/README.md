# Realsense File Schemas

For each session created for the Realsense (i.e. sensor initialized 
and created), we dump the following files:

1. Metadata JSON file which contains intrinsics and depth scale. The schema for this is 
    whatever Open3D has defined in the camera metadata. The more important fields are:
   - `intrinsics` - intrinsics of the camera. This is a dict with:
     ```json
     {
       "height": int,
       "width": int,
       "intrinsic_matrix": [
         [float, float, float],
         [float, float, float],
         [float, float, float]
       ]   
     }
     ```
   - `depth_scale` - depth scale of the camera
2. Extrinsics JSON which contains the extrinsics of the camera (i.e. camera to world)
   - Quaternion is specified in xyzw convention
   - Euler angle is specified in xyz convention (i.e., roll pitch yaw)
   - `c2w` is the 4x4 transformation matrix from camera to world
   - **Note:** this is all specified in conventional robotics coordinate frames.
    ```json
    {
      "device_name": str,
      "serial_number": str,
      "translation": [float, float, float],
      "quaternion": [float, float, float, float],
      "c2w": [
        [float, float, float, float],
        [float, float, float, float],
        [float, float, float, float],
        [float, float, float, float]
      ]
    }
    ```

Then, for each frame captured by the Realsense camera, we dump the following:

1. Color image, as a PNG with 3 channels and 8 bits per channel
2. Depth image, as a PNG with 1 channel and 16 bits per channel

Note that the color and depth image are aligned. The filenames of the 
color and depth images are such that they follow chronological order.