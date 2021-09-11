import os
from pathlib import Path

#
import numpy as np


def datalake_root(P):
    return Path(P["data_lake_root"])


def write_numpy(path: Path, numpy_obj):
    """
    Serialize and write a numpy array to a local file
    """
    assert path.suffix == ".numpy"

    # Create local directory for file if it does not exist
    os.makedirs(path.parent, exist_ok=True)

    with open(path, "wb") as f:
        np.save(f, numpy_obj, allow_pickle=False)


def read_numpy(path: Path):
    """
    Read numpy array from a local file saved with write_numpy, see above
    """
    assert path.suffix == ".numpy"
    assert path.is_file()

    with open(path, "rb") as f:
        return np.load(f)
