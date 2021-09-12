# %% [markdown]
# # EDA for digits data

# %% [markdown]
# ### Determine run parameters

# %%
# ----------------- Parameters for interactive development --------------
import uuid

P = {
    "data_lake_root": "/pipeline-outputs/data-lake",
    "run.run_directory": f"/pipeline-outputs/runlogs/{uuid.uuid4()}",
}
# %% tags=["parameters"]
# - During automated runs parameters will be injected in the below cell -
# %%
# -----------------------------------------------------------------------
# %% [markdown]
# ---

# %% [markdown]
# ### Notebook code


# %%
from typing import Dict, Tuple

#
import collections
import matplotlib.pyplot as plt

#
from common.io import datalake_root, runlog_root, read_numpy
from common.genlogger import GenLogger

# %%
logger = GenLogger(runlog_root(P))

# %%
X = read_numpy(datalake_root(P) / "raw" / "digits.numpy")
y = read_numpy(datalake_root(P) / "raw" / "labels.numpy")

# %% [markdown]
# ## Check shapes of digit image and label vectors

# %%
X.shape, y.shape

# %%
# labels in y has shape of vector
assert y.shape == (len(y),)

# X and y have compatible shape (ie., both have equal number of rows)
assert X.shape[0] == len(y) == y.shape[0]

# each image is 8x8 pixels
assert X.shape[1] == 8 * 8

# %%
logger.log("nr_digits", len(y))
logger.log("pixels_per_digit", X.shape[1])


# %% [markdown]
# ## Check distribution of labels

# %%
def plot_dict_to_barplot(
    values_dict: Dict[int, int],
    title: str,
    x_label: str,
    y_label: str,
    figsize: Tuple[int, int] = (16, 5),
    font_size: int = 18,
    title_font_size: int = 22,
):
    """
    Draw bar plots from count data in a dict
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)

    keys, counts = zip(*values_dict.items())  # type: ignore
    ax.bar(keys, counts)
    ax.set_xticks(keys)

    ax.set_title(title + "\n", fontsize=title_font_size)

    ax.set_xlabel(x_label, fontsize=font_size)
    ax.set_ylabel(y_label + "\n", fontsize=font_size)

    ax.tick_params(axis="both", which="major", labelsize=font_size)

    fig.tight_layout()

    return fig


# %%
# all labels in y are in set 0, 1, ..., 8, 9 (possible digits)
assert set(y) == set(range(10))

# %%
digit_counts: Dict[int, int] = dict(collections.Counter(y))

logger.log_dict({f"nr_digits.{k}": v for k, v in digit_counts.items()})

# %%
fig = plot_dict_to_barplot(
    digit_counts,
    title=f"Number of samples per digit (n={len(y)})",
    x_label="Digit",
    y_label="Nr of samples",
)

# %%
logger.log_image("samples_per_digit.png", fig)

# %% [markdown]
# - All digits 0, 1, ..., 8, 9 are (approximatively) equally represented in the data set

# %% [markdown]
# ## Check distribution of pixel values

# %%
assert X.reshape(-1).shape == (X.shape[0] * X.shape[1],)

# %%
# all labels in y are in set 0, 1, ..., 8, 9 (possible digits)
assert set(X.reshape(-1)) == set(float(x) for x in range(17))

# %%
pixel_value_counts: Dict[int, int] = dict(collections.Counter(X.reshape(-1)))

# %%
fig = plot_dict_to_barplot(
    pixel_value_counts,
    title=f"Distribution of pixel values over all digit images (n={len(X.reshape(-1))})",
    x_label="Pixel value",
    y_label="Counts",
)

# %%
logger.log_image("pixel_value_counts.png", fig)

# %% [markdown]
# - The pixel values in the images are encoded with numbers 0, .., 16.
# - Pixel value 0 occur most frequently (background color).
# - The second most frequent pixel value is 16.0 (digit draw color).

# %%
logger.persist()

# %%
