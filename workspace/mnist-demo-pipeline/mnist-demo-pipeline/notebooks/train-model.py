# %% [markdown]
# # Train model
#
# The purpose of this notebook is:
#
# - Load all training data (images and labels).
# - Limit train data to only `task.nr_train_images` number of images.
# - Train a support vector machine model using sklearn.
# - Persist the trained model using the ONNX format.
#

# %% [markdown]
# ### Determine run parameters

# %%
# ----------------- Parameters for interactive development --------------
import uuid

P = {
    "data_lake_root": "/pipeline-outputs/data-lake",
    "run.run_directory": f"/pipeline-outputs/runlogs/{uuid.uuid4()}",
    "task.nr_train_images": 600,
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
from common.io import runlog_root
from common.genlogger import GenLogger

# %%
logger = GenLogger(runlog_root(P))


# %% [markdown]
# ## Load all limit train data

# %%
def load_and_limit_train_data(P):
    from common.io import datalake_root, read_numpy
    from sklearn.model_selection import train_test_split

    X_train_all = read_numpy(datalake_root(P) / "train-data" / "digits.numpy")
    y_train_all = read_numpy(datalake_root(P) / "train-data" / "labels.numpy")

    assert isinstance(P["task.nr_train_images"], int)
    assert 0 < P["task.nr_train_images"] <= len(y_train_all)

    if P["task.nr_train_images"] == len(y_train_all):
        # train_test_split fails in this case
        X_train, y_train = X_train_all, y_train_all
    else:
        X_train, _, y_train, _ = train_test_split(
            X_train_all,
            y_train_all,
            train_size=P["task.nr_train_images"],
            test_size=None,
            stratify=y_train_all,
            shuffle=True,
            random_state=123,
        )

    assert X_train.shape == (len(y_train), 8 * 8)
    return X_train, y_train


X_train, y_train = load_and_limit_train_data(P)

# %% [markdown]
# ## Train model using sklearn
#
# Below we assume that the hyperparameters are known.
#
# However, these should ideally be found by a hyperparameter search. That could be
# done in parallel on the Ray cluster, but this needs some more work. Ie., to use
# multiple cores in the notebook, those cores should be reserved when starting the
# notebook task (TODO).
#
# - https://docs.ray.io/en/latest/tune/key-concepts.html

# %%
from sklearn.svm import SVC

# %%
model = SVC(C=0.001, kernel="linear", probability=True)

model.fit(X_train, y_train)

# %%
# Note: cv-scores would need to be computed here, since they depend on the train data.
# After this notebook only the onnx-model is available

# %% [markdown]
# ## Persist model

# %%
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

#
from common.io import datalake_root, write_onnx

# %%
# convert sklearn model into onnx and persist to data lake
model_onnx = convert_sklearn(
    model, initial_types=[("float_input_8x8_image", FloatTensorType([None, 8 * 8]))]
)
write_onnx(
    datalake_root(P)
    / "models"
    / f"nr_train_images={P['task.nr_train_images']}"
    / "model.onnx",
    model_onnx,
)

# %%
# ---

# %%
logger.persist()
