from cmx import doc
import gym
from pathlib import Path
import matplotlib.pyplot as plt

doc @ """
requires `gym-fetch`. Run:

```
pip install gym-fetch
```
"""

with doc, doc.table().figure_row() as row:
    env = gym.make('fetch:PickPlace-v0')
    env.reset()

    image, depth = env.render('rgbd', width=640, height=480)

    far = 4
    depth[depth > far] = far
    row.figure(depth, f"{Path(__file__).stem}/depth.png", normalize=True)
    row.figure(image, f"{Path(__file__).stem}/rgb.png")

with doc @ """
The camera intrinsics are """:
    doc.print('')
