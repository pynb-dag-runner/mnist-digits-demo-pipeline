from pathlib import Path

#
import numpy as np

#
from common.io import write_numpy, read_numpy, datalake_root


def test_datalake_root():
    P = {"data_lake_root": "/foo/bar"}

    assert datalake_root(P) == Path("/foo/bar")


def test_numpy_read_write(tmp_path: Path):
    filepath = tmp_path / "foo" / "bar" / "baz.numpy"
    assert not filepath.is_file()

    v1 = np.random.rand(1, 2, 3, 4)
    assert v1.shape == (1, 2, 3, 4)
    write_numpy(filepath, v1)
    assert filepath.is_file()

    v2 = read_numpy(filepath)
    assert v1.shape == v2.shape
    assert (v1 == v2).all()
