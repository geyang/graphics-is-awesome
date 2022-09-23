import json
import os
import time

import open3d as o3d
from matplotlib import pyplot as plt

# x = o3d.t.io.RealSenseSensor.list_devices()
# print(x)

config_filename = "realsense_config.json"
with open(config_filename) as cf:
    rs_cfg = o3d.t.io.RealSenseSensorConfig(json.load(cf))

rs = o3d.t.io.RealSenseSensor()
bag_filename = "realsense.bag"
# os.remove(bag_filename)
rs.init_sensor(rs_cfg, 0, bag_filename)
rs.start_capture(True)
metadata = rs.get_metadata()

intrinsics = metadata.intrinsics
depth_scale = metadata.depth_scale
print("Captured metadata")

# warmup the realsense
# for _ in range(30):
#     rs.capture_frame(True, True)

print("Warmed up")

device = "cuda:0" if o3d.core.cuda.is_available() else "cpu:0"
o3d_device = o3d.core.Device(device)

intrinsic_matrix = o3d.core.Tensor(
    metadata.intrinsics.intrinsic_matrix,
    dtype=o3d.core.Dtype.Float32,
    device=o3d_device,
)

extrinsics = o3d.core.Tensor.eye(4, dtype=o3d.core.Dtype.Float32, device=o3d_device)

time.sleep(3.0)
for fid in range(1):
    im_rgbd = rs.capture_frame(True, True)  # wait for frames and align them
    # process im_rgbd.depth and im_rgbd.color

    # plt.subplot(1, 2, 1)
    # plt.title('grayscale image')
    # plt.imshow(im_rgbd.color)
    # plt.subplot(1, 2, 2)
    # plt.title('depth image')
    # plt.imshow(im_rgbd.depth)
    # plt.show()

    print(im_rgbd, type(im_rgbd))
    print(intrinsics, type(intrinsics))

    im_rgbd = im_rgbd.to(o3d_device)

    pcd = o3d.t.geometry.PointCloud.create_from_rgbd_image(
        im_rgbd,
        intrinsic_matrix,
        extrinsics,
        metadata.depth_scale,
        3.0,
        # self.pcd_stride,
        # self.flag_normals,
    )
    # print(pcd)
    # # pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    # o3d.visualization.draw_geometries([pcd.cpu()])

rs.stop_capture()
