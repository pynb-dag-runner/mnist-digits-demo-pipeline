from common.utils import chunkify


def test_chunkify():
    assert list(chunkify([1, 2, 3], 1)) == [[1], [2], [3]]
    assert list(chunkify([1, 2, 3], 2)) == [[1, 2], [3]]
    assert list(chunkify([1, 2, 3], 3)) == [[1, 2, 3]]
    assert list(chunkify([1, 2, 3], 4)) == [[1, 2, 3]]
