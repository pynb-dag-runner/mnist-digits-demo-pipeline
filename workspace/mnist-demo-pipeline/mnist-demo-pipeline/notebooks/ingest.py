# %% [markdown]
# # Ingest toy version of MNIST digit data from sklearn

# %% [markdown]
# ### Determine run parameters

# %%
# ----------------- Parameters for interactive development --------------
P = {
    "run_environment": "dev",
    "data_lake_root": "/pipeline-outputs/data-lake",
    "run.retry_nr": 1,
}
# %% tags=["parameters"]
# - During automated runs parameters will be injected in the below cell -
# %%
# -----------------------------------------------------------------------
# %% [markdown]
# ---

# %% [markdown]
# ### Simulate different types of failures (for testing timeout and retry logic)

# %%
import time, random

if P["run.retry_nr"] < {"dev": 2, "ci": 10}[P["run_environment"]]:  # type: ignore
    # fail ingestion on first tries
    if random.random() < 0.5:
        print("Hanging notebook to check that notebook is canceled by timeout ...")
        time.sleep(1e6)
    else:
        # notebook should be retried on failure
        raise Exception("Simulated exception failure from ingestion step notebook!")

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
