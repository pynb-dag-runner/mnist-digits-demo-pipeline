import itertools as it


#
import numpy as np


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


def make_panel_image(X, pad_width: int, background_fill: int, images_per_row: int):
    """
    From an array of images X (with axes: image index, x-dim, y-dim) return a 2d
    numpy array suitable for displaying all images.

    See unit test for examples.
    """
    assert len(X.shape) == 3
    image_dims = tuple(X.shape)[1:]

    # compute size of one padded individual image in the output panel image
    padded_image_dim = np.array(
        (image_dims[0] + pad_width * 2, image_dims[1] + pad_width * 2)
    )

    # store images arrays for each rows (with each image containing cols_per_row
    # smaller images)
    row_images = []

    for X_chunk in chunkify(X, chunk_size=images_per_row):
        current_row_images = []

        for img in X_chunk:
            assert img.shape == image_dims
            img_padded = np.pad(
                img,
                pad_width=pad_width,
                constant_values=(background_fill, background_fill),
                mode="constant",
            )

            assert tuple(img_padded.shape) == tuple(padded_image_dim)
            current_row_images.append(img_padded)

        while len(current_row_images) < images_per_row:
            current_row_images.append(np.zeros(padded_image_dim) + background_fill)

        current_row_image = np.concatenate(current_row_images, axis=1)
        assert tuple(current_row_image.shape) == (
            padded_image_dim[0],
            images_per_row * padded_image_dim[1],
        )
        row_images.append(current_row_image)

    panel_image = np.concatenate(row_images)
    assert tuple(panel_image.shape) == (
        len(row_images) * padded_image_dim[0],
        images_per_row * padded_image_dim[1],
    )

    return panel_image
