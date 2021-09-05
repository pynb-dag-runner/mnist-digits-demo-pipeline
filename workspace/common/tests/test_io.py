from common.io import read_numpy


def test_io():
    assert read_numpy(1) == 123
