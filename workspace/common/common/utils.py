import itertools as it


def chunkify(arr, chunk_size: int):
    """
    Split a list (or numpy array) into chunks of equal sizes (chunk_size), and a last
    chunk with any remaining entries.

     - The chunks are returned as an iterator.
     - For a numpy array, the chunks are split on the first axis.

    Numpy has a similar function, but it does not guarantee that all chunks (except
    the last one) are of equal length. It attemts to adjust the chunk lengths to have
    similar lengths. See,

       https://numpy.org/doc/stable/reference/generated/numpy.array_split.html

    """
    if not chunk_size > 0:
        raise Exception("chunk_size should be positive integer")

    next_chunk, rest = arr[:chunk_size], arr[chunk_size:]

    if len(rest) > 0:
        return it.chain(iter([next_chunk]), chunkify(rest, chunk_size))
    else:
        return iter([next_chunk])
