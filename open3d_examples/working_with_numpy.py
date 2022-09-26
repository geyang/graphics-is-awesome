# examples/Python/Basic/working_with_numpy.py
from cmx import doc
import numpy as np
import open3d as o3d


def savefig(pcd, path, width=640, height=480):
    vis = o3d.visualization.Visualizer()
    vis.create_window(width=width, height=height, visible=False)
    vis.add_geometry(pcd)
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    vis.capture_screen_image(path)
    vis.destroy_window()

def save_depth(pcd, path, width=640, height=480):
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False)
    vis.add_geometry(mesh)
    vis.update_geometry(mesh)
    vis.poll_events()
    vis.update_renderer()
    depth = vis.capture_depth_float_buffer(do_render=False)
    vis.destroy_window()

if __name__ == "__main__":
    with doc:
        # generate some neat n times 3 matrix using a variant of sync function
        x = np.linspace(-3, 3, 401)
        mesh_x, mesh_y = np.meshgrid(x, x)
        z = np.sinc((np.power(mesh_x, 2) + np.power(mesh_y, 2)))
        z_norm = (z - z.min()) / (z.max() - z.min())
        xyz = np.zeros((np.size(mesh_x), 3))
        xyz[:, 0] = np.reshape(mesh_x, -1)
        xyz[:, 1] = np.reshape(mesh_y, -1)
        xyz[:, 2] = np.reshape(z_norm, -1)
        print('xyz', xyz)

    with doc:
        # Pass xyz to Open3D.o3d.geometry.PointCloud and visualize
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)
        pcd.colors = o3d.utility.Vector3dVector(xyz / 3 + 1)
        o3d.visualization.draw_geometries([pcd])
        savefig(pcd, ".logs/sync.png")

    # os.makedirs(".logs")
    # o3d.io.write_point_cloud(".logs/sync.ply", pcd)

    # Load saved point cloud and visualize it
    # pcd_load = o3d.io.read_point_cloud(".logs/TestData/sync.ply")
    # o3d.visualization.draw_geometries([pcd_load])

    # # convert Open3D.o3d.geometry.PointCloud to numpy array
    # xyz_load = np.asarray(pcd_load.points)
    # print('xyz_load')
    # print(xyz_load)
    #
    # # save z_norm as an image (change [0,1] range to [0,255] range with uint8 type)
    # img = o3d.geometry.Image((z_norm * 255).astype(np.uint8))
    # o3d.io.write_image(".logs/sync.png", img)
    # o3d.visualization.draw_geometries([img])