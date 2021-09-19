# %% [markdown]
# # Split digits and labels into separate training and testing data sets

# %% [markdown]
# ### Determine run parameters

# %%
# ----------------- Parameters for interactive development --------------
import uuid

P = {
    "data_lake_root": "/pipeline-outputs/data-lake",
    "run.run_directory": f"/pipeline-outputs/runlogs/{uuid.uuid4()}",
    "task.train_test_ratio": 0.7,
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
from common.io import datalake_root, runlog_root, read_numpy, write_numpy
from common.genlogger import GenLogger

# %%
logger = GenLogger(runlog_root(P))

# %% [markdown]
# ## Load and split digits data

# %%
X = read_numpy(datalake_root(P) / "raw" / "digits.numpy")
y = read_numpy(datalake_root(P) / "raw" / "labels.numpy")

# %%
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    train_size=P["task.train_test_ratio"],
    test_size=None,
    stratify=y,
    shuffle=True,
    random_state=1,
)

# assert nr of pixels per image is the same for all image vectors
assert X.shape[1] == X_train.shape[1] == X_test.shape[1]

# assert that the (X, y)-pairs have compatible sizes (for both train and test)
assert X_train.shape[0] == len(y_train)
assert X_test.shape[0] == len(y_test)

# assert that all data is used
assert len(y) == len(y_train) + len(y_test)

# %%
logger.log("nr_digits_train", len(y_train))
logger.log("nr_digits_test", len(y_test))

# %% [markdown]
# ### Persist training and test data sets to separate files

# %%
write_numpy(datalake_root(P) / "train-data" / "digits.numpy", X_train)
write_numpy(datalake_root(P) / "train-data" / "labels.numpy", y_train)

#
write_numpy(datalake_root(P) / "test-data" / "digits.numpy", X_test)
write_numpy(datalake_root(P) / "test-data" / "labels.numpy", y_test)

# %%
logger.persist()

# %%
