# %% [markdown]
# # Summarize model performances
#
# This notebooks plots the performances (using averaged ROC AUC scores) for models
# trained with different training sets.
#
# Note: The below approach load runlog and genlogger json files from local files. This
# might not be ideal. These files neither currently capture the hierarchy between tasks
# (which would be useful when querying).
#
# - Could the stored metrics (eg ROC scores) and traces (task timings) be queried
#   (and correlated) via an API?
# - Could the OpenTelemetry standard be suitable for that?

# %% [markdown]
# ### Determine run parameters

# %%
# ----------------- Parameters for interactive development --------------
import uuid

P = {
    "runlogs_root": "/pipeline-outputs/runlogs",
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
import glob
from pathlib import Path

#
import pandas as pd
import matplotlib.pyplot as plt

#
from pynb_dag_runner.helpers import read_json

#
from common.io import runlog_root
from common.genlogger import GenLogger

# %%
logger = GenLogger(runlog_root(P))


# %%
def get_model_benchmarks_data(benchmark_runlogs_filepath: Path):
    """
    Return Python dict with summary of model performance for one choice of
    training set size.
    """
    benchmark_genlog = read_json(benchmark_runlogs_filepath)
    benchmark_runlog = read_json(benchmark_runlogs_filepath.parent / "runlog.json")
    assert benchmark_runlog["out.status"] == "SUCCESS"

    return {
        "pipeline_run_id": benchmark_runlog["parameters.pipeline_run_id"],
        "nr_train_images": benchmark_runlog["parameters.task.nr_train_images"],
        "runtime_ms": benchmark_runlog["out.timing.duration_ms"],
        "roc_auc": benchmark_genlog["key-values"]["roc_auc_class_mean"],
    }


def get_all_model_performance_benchmark_data(runlogs_root: str):
    genlogger_files = [
        f
        for f in glob.glob(f"{runlogs_root}/**/*", recursive=True)
        if f.endswith("genlogger.json") and "benchmark-model" in f
    ]

    df_data = pd.DataFrame(
        get_model_benchmarks_data(Path(f)) for f in genlogger_files
    ).sort_values(by="nr_train_images")

    return df_data


df_data = get_all_model_performance_benchmark_data(P["runlogs_root"])
df_data

# %%
if len(set(df_data["pipeline_run_id"])) > 1:
    print("WARNING: runlogs_root contains multiple pipeline runs!")


# %%
def plot_classifier_performance_summary(df_data):
    fig, (ax0, ax1) = plt.subplots(nrows=2, ncols=1, figsize=(16, 8), sharex=True)

    #
    ax0.plot(df_data["nr_train_images"], df_data["roc_auc"], marker="o", linestyle="--")
    ax0.set_title(
        f"ROC AUC digit classifier performance on evaluation digits", fontsize=17
    )
    ax0.set_ylabel("ROC AUC", fontsize=14)

    #
    ax1.plot(
        df_data["nr_train_images"], df_data["runtime_ms"], marker="o", linestyle="--"
    )
    ax1.set_title(f"Total training time [ms]", fontsize=17)
    ax1.set_xlabel("Number of images in training set", fontsize=14)
    ax1.set_ylabel("ms", fontsize=14)

    #
    fig.tight_layout()
    fig.show()

    return fig


fig = plot_classifier_performance_summary(df_data)

# %%
logger.log_image("auc-roc-model-performances.png", fig)

# %%
###

# %%
logger.persist()
