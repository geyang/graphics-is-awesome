import numpy as np
import open3d as o3d

if __name__ == '__main__':
    rgb = o3d.io.read_image("color.png")
    d = o3d.io.read_image("depth.png")

    depth_scale = 999.99993896484375
    depth = np.asarray(d) / depth_scale
