# %% [markdown]
# # Train model
#
# The purpose of this notebook is:
#
# - Load all training data (images and labels)
# - Limit this to only use ratio `task.train_size` (in range 0..1) of images. This
#   ratio is provided as a run parameter.
# - Train a support vector machine using sklearn
# - Persist the trained model using the ONNX format
#

# %% [markdown]
# ### Determine run parameters

# %%
# ----------------- Parameters for interactive development --------------
import uuid

P = {
    "data_lake_root": "/pipeline-outputs/data-lake",
    "run.run_directory": f"/pipeline-outputs/runlogs/{uuid.uuid4()}",
    "task.train_size": 0.60,
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

    assert isinstance(P["task.train_size"], float)
    assert 0 < P["task.train_size"] <= 1

    X_train, _, y_train, _ = train_test_split(
        X_train_all,
        y_train_all,
        train_size=P["task.train_size"],
        test_size=None,
        stratify=y_train_all,
        shuffle=True,
        random_state=123,
    )

    print(len(y_train_all))
    assert X_train.shape == (len(y_train), 8 * 8)
    return X_train, y_train


X_train, y_train = load_and_limit_train_data(P)

# %%
logger.log("nr_train_samples", len(y_train))

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
    datalake_root(P) / "models" / f"train_samples={len(y_train)}" / "model.onnx",
    model_onnx,
)

# %%
# ---

# %%
logger.persist()
