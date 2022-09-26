import json
import os

import numpy as np
import open3d as o3d

if __name__ == "__main__":
    voxel_size = 50
    pcd_1 = o3d.io.read_point_cloud("d415.pcd")
    pcd_2 = o3d.io.read_point_cloud("d435.pcd")
    import os

    # os.makedirs('./logs')
    with open('./logs/view_1.json', 'w+') as f:
        json.dump({'points': np.asarray(pcd_1.points).tolist(), 'colors': np.asarray(pcd_1.colors).tolist()}, f)
    with open('./logs/view_2.json', 'w+') as f:
        json.dump({'points': np.asarray(pcd_2.points).tolist(), 'colors': np.asarray(pcd_2.colors).tolist()}, f)
    print('done')
    # pcd_d415.voxel_down_sample(voxel_size=voxel_size)
    # pcd_d435 = o3d.io.read_point_cloud("d435.pcd")
    # pcd_d435.voxel_down_sample(voxel_size=voxel_size)
    #
    # o3d.visualization.draw_geometries([pcd_d415, pcd_d435])
