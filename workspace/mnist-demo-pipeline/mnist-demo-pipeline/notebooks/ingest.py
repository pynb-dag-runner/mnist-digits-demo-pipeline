# %% [markdown]
# # Ingest toy version of MNIST digit data from sklearn

# %% [markdown]
# ### Determine run parameters

# %%
# ----------------- Parameters for interactive development --------------
P = {
    "data_lake_root": "/pipeline-outputs/data-lake",
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
from sklearn import datasets

#
from common.io import datalake_root, write_numpy

# %%
digits = datasets.load_digits()

X = digits["data"]
y = digits["target"]


# %%
X.shape, y.shape

# %%
write_numpy(datalake_root(P) / "raw" / "digits.numpy", X)
write_numpy(datalake_root(P) / "raw" / "labels.numpy", y)

# %%
