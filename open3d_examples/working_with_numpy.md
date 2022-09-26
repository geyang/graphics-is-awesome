```python
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
```
```python
# Pass xyz to Open3D.o3d.geometry.PointCloud and visualize
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyz)
pcd.colors = o3d.utility.Vector3dVector(xyz / 3 + 1)
# o3d.visualization.draw_geometries([pcd])
# path = ".logs/example_capture.png"
# o3d.visualization.capture_screen_image(path)
# img = o3d.geometry.Image((z_norm * 255).astype(np.uint8))
# o3d.io.write_image(".logs/sync.png", pcd)
savefig(pcd, ".logs/sync.png")
# o3d.visualization.draw_geometries([img])
```
