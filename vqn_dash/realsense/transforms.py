import json
from typing import NamedTuple, Tuple

import numpy as np
from pybullet_utils.transformations import quaternion_matrix


class Extrinsics(NamedTuple):
    """Camera extrinsics in world frame."""

    translation: Tuple[float, float, float]
    quaternion: Tuple[float, float, float, float]  # xyzw

    @property
    def c2w(self) -> np.ndarray:
        """Camera to world transformation matrix."""
        c2w = quaternion_matrix(self.quaternion)
        c2w[:3, 3] = self.translation
        return c2w

    @property
    def w2c(self):
        """World to camera transformation matrix."""
        return np.linalg.inv(self.c2w)


def load_extrinsics(extrinsics_fname: str) -> Extrinsics:
    """Load extrinsics from JSON file and return Intrinsics object."""
    with open(extrinsics_fname, "r") as f:
        extrinsics_dict = json.load(f)

    extrinsics = Extrinsics(
        extrinsics_dict["translation"], extrinsics_dict["quaternion"]
    )
    if "c2w" in extrinsics_dict:
        assert np.allclose(extrinsics.c2w, extrinsics_dict["c2w"])
    return extrinsics


if __name__ == "__main__":
    extrinsics_ = load_extrinsics("scratch/extrinsics.json")
    print(extrinsics_.c2w)
