import json
import os
import time
from datetime import datetime

import numpy as np
import open3d as o3d
from loguru import logger
from matplotlib import pyplot as plt
from open3d.cuda.pybind.visualization import Visualizer
from pybullet_utils.transformations import quaternion_matrix

# x = o3d.t.io.RealSenseSensor.list_devices()
# print(x)


D415_POSE = [
    (0.896359, -0.558836, 0.532884),
    (0.841755, 0.362692, -0.117135, -0.382337),
]

D415_EXTRINSICS = quaternion_matrix(D415_POSE[1])
D415_EXTRINSICS[:3, 3] = D415_POSE[0]
# use inverse so its world coord to camera coord
D415_EXTRINSICS = np.linalg.inv(D415_EXTRINSICS)


D435_POSE = [(0.948026, 0.501282, 0.493286), (0.357508, 0.841146, -0.370672, -0.165119)]

D435_EXTRINSICS = quaternion_matrix(D435_POSE[1])
D435_EXTRINSICS[:3, 3] = D435_POSE[0]
# use inverse so its world coord to camera coord
D435_EXTRINSICS = np.linalg.inv(D435_EXTRINSICS)


def start_realsense(config_fname: str = "") -> o3d.t.io.RealSenseSensor:
    """
    Initialize and start capturing for a RealSense camera, with the
    given configuration. If no configuration specified, open3d will
    automatically select the first camera it can discover.
    """
    rs = o3d.t.io.RealSenseSensor()
    # Dump to ros bag
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{now}.bag"

    if config_fname:
        with open(config_fname, "r") as f:
            config_dict = json.load(f)
        config = o3d.t.io.RealSenseSensorConfig(config_dict)
        rs.init_sensor(config, filename=filename)
    else:
        rs.init_sensor(filename=filename)

    # Start capturing
    rs.start_capture(start_record=False)
    return rs


def warmup_realsense(rs: o3d.t.io.RealSenseSensor, n_warmup: int = 100):
    """
    Warm up the realsense camera by capturing n_warmup frames.
    """
    for _ in range(n_warmup):
        rs.capture_frame(True, True)
    logger.info("Warmed up realsense")


def main():

    device = "cuda:0" if o3d.core.cuda.is_available() else "cpu:0"
    print("Using device:", device)
    o3d_device = o3d.core.Device(device)
    extrinsics = o3d.core.Tensor(D435_EXTRINSICS.tolist(), device=o3d_device)

    rs = start_realsense("realsense_config.json")
    metadata = rs.get_metadata()

    intrinsics = metadata.intrinsics
    depth_scale = metadata.depth_scale
    print("Captured metadata")

    print(metadata)
    warmup_realsense(rs)

    # extrinsics = o3d.core.Tensor.eye(4, dtype=o3d.core.Dtype.Float32, device=o3d_device)
    intrinsic_matrix = o3d.core.Tensor(
        metadata.intrinsics.intrinsic_matrix,
        dtype=o3d.core.Dtype.Float32,
        device=o3d_device,
    )

    # first = False
    # for _ in range(200):
    while True:
        raw_rgbd = rs.capture_frame(True, True)
        pcd = o3d.t.geometry.PointCloud.create_from_rgbd_image(
            raw_rgbd,
            intrinsic_matrix,
            extrinsics,
            metadata.depth_scale,
        )

        o3d.t.io.write_image("color.png", raw_rgbd.color)
        o3d.t.io.write_image("depth.png", raw_rgbd.depth)

        pcd_cpu = pcd.to_legacy()
        # Save PCD to file
        filename = f"d435.pcd"
        o3d.io.write_point_cloud(filename, pcd_cpu)

        # TODO: worker threads to save to disk
        # pcd_cpu.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
        # Visualize pcd
        o3d.visualization.draw_geometries([pcd_cpu])


if __name__ == "__main__":
    main()

# device = "cuda:0" if o3d.core.cuda.is_available() else "cpu:0"
# o3d_device = o3d.core.Device(device)
#
# intrinsic_matrix = o3d.core.Tensor(
#     metadata.intrinsics.intrinsic_matrix,
#     dtype=o3d.core.Dtype.Float32,
#     device=o3d_device,
# )
#
# extrinsics = o3d.core.Tensor.eye(4, dtype=o3d.core.Dtype.Float32, device=o3d_device)
#
# time.sleep(3.0)
# for fid in range(1):
#     im_rgbd = rs.capture_frame(True, True)  # wait for frames and align them
#     # process im_rgbd.depth and im_rgbd.color
#
#     # plt.subplot(1, 2, 1)
#     # plt.title('grayscale image')
#     # plt.imshow(im_rgbd.color)
#     # plt.subplot(1, 2, 2)
#     # plt.title('depth image')
#     # plt.imshow(im_rgbd.depth)
#     # plt.show()
#
#     print(im_rgbd, type(im_rgbd))
#     print(intrinsics, type(intrinsics))
#
#     im_rgbd = im_rgbd.to(o3d_device)
#
#     pcd = o3d.t.geometry.PointCloud.create_from_rgbd_image(
#         im_rgbd,
#         intrinsic_matrix,
#         extrinsics,
#         metadata.depth_scale,
#         3.0,
#         # self.pcd_stride,
#         # self.flag_normals,
#     )
#     # print(pcd)
#     # # pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
#     # o3d.visualization.draw_geometries([pcd.cpu()])
#
# rs.stop_capture()
