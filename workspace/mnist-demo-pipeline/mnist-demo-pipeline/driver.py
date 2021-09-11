from pathlib import Path
import uuid

#
from pynb_dag_runner.wrappers.runlog import Runlog

from pynb_dag_runner.tasks.tasks import JupytextNotebookTask, get_task_dependencies
from pynb_dag_runner.notebooks_helpers import JupytextNotebook
from pynb_dag_runner.core.dag_runner import run_tasks, TaskDependencies
from pynb_dag_runner.helpers import flatten, write_json


def get_args():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "--runlogs_root",
        type=str,
        help="local directory for pipeline runlog outputs",
    )
    parser.add_argument(
        "--data_lake_root",
        type=str,
        help="local directory for data artefacts (normally written to a data lake)",
    )

    args = parser.parse_args()

    print("*** Command line parameters ***")
    print(f"  - runlogs_root     : {args.runlogs_root}")
    print(f"  - data_lake_root   : {args.data_lake_root}")

    return args


args = get_args()

COMMON_PARAMETERS = {
    # data lake root is pipeline-scoped parameter
    "parameters.data_lake_root": args.data_lake_root,
}


def make_run_path(runlog: Runlog):
    """
    Define organization of runlog-files from this pipeline
    """
    # extract filename of Jupytext notebook being run
    task_name = Path(runlog["notebook_path"]).name.replace(".py", "")

    return Path(args.runlogs_root) / task_name / runlog["parameters.run.id"]


def make_notebook_task(
    notebook_path: Path, timeout_s=None, n_max_retries=1, parameters={}
):
    jupytext_notebook = JupytextNotebook(notebook_path)
    return JupytextNotebookTask(
        jupytext_notebook,
        get_run_path=make_run_path,
        n_max_retries=n_max_retries,
        timeout_s=timeout_s,
        task_id=str(uuid.uuid4()),
        parameters={
            **COMMON_PARAMETERS,
            **parameters,
            "task_type": "PythonNotebookTask",
            "notebook_path": str(notebook_path),
        },
    )


print("---- Setting up tasks and task dependencies ----")

task_ingest = make_notebook_task(notebook_path=Path("./notebooks/ingest.py"))

tasks = [task_ingest]
task_dependencies = TaskDependencies()

print("---- Running mnist-demo-pipeline ----")

_ = flatten(run_tasks(tasks, task_dependencies))

write_json(
    Path(args.runlogs_root) / "task_dependencies.json",
    get_task_dependencies(task_dependencies),
)

print("---- Done ----")
