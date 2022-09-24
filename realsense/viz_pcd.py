import open3d as o3d

if __name__ == "__main__":
    voxel_size = 50
    pcd_d415 = o3d.io.read_point_cloud("d415.pcd")
    pcd_d415.voxel_down_sample(voxel_size=voxel_size)
    pcd_d435 = o3d.io.read_point_cloud("d435.pcd")
    pcd_d435.voxel_down_sample(voxel_size=voxel_size)

    o3d.visualization.draw_geometries([pcd_d415, pcd_d435])
