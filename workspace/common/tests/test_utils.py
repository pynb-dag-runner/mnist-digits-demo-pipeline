from common.utils import chunkify

#
import numpy as np


def test_chunkify_list():
    assert list(chunkify([1, 2, 3], 1)) == [[1], [2], [3]]
    assert list(chunkify([1, 2, 3], 2)) == [[1, 2], [3]]
    assert list(chunkify([1, 2, 3], 3)) == [[1, 2, 3]]
    assert list(chunkify([1, 2, 3], 4)) == [[1, 2, 3]]


def test_chunkify_numpy():
    def get_3x4(start_int: int):
        return (np.arange(12) + start_int).reshape(3, 4)

    N = 100
    xs = np.array([get_3x4(k) for k in range(N)])
    assert xs.shape == (N, 3, 4)

    def assert_list_of_arrs_eq(list_of_np_arr1, list_of_np_arr2):
        assert len(list_of_np_arr1) == len(list_of_np_arr2)

        for arr1, arr2 in zip(list_of_np_arr1, list_of_np_arr2):
            assert arr1.shape == arr2.shape
            assert np.allclose(arr1, arr2)

    for xs_chunks in [
        [xs[k].reshape(1, 3, 4) for k in range(N)],
        [np.array([get_3x4(k)]) for k in range(N)],
    ]:
        assert_list_of_arrs_eq(list(chunkify(xs, chunk_size=1)), xs_chunks)

    for xs_chunks in [
        [xs[: (N - 1)], xs[(N - 1) :]],
        [np.array([get_3x4(k) for k in range(N - 1)]), np.array([get_3x4(N - 1)])],
    ]:
        assert_list_of_arrs_eq(list(chunkify(xs, chunk_size=N - 1)), xs_chunks)

    assert_list_of_arrs_eq(list(chunkify(xs, chunk_size=N + 1)), [xs])
