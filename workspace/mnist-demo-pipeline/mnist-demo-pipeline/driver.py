from pathlib import Path
import uuid, datetime

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
    parser.add_argument(
        "--run_environment",
        type=str,
        choices=["ci", "dev"],
        help="run environment for running pipeline",
    )

    args = parser.parse_args()

    print("*** Command line parameters ***")
    print(f"  - runlogs_root     : {args.runlogs_root}")
    print(f"  - data_lake_root   : {args.data_lake_root}")
    print(f"  - run_environment  : {args.run_environment}")

    return args


args = get_args()
start_time: str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

COMMON_PARAMETERS = {
    # data lake root is pipeline-scoped parameter
    "parameters.data_lake_root": args.data_lake_root,
    "parameters.run_environment": args.run_environment,
}


def make_runlogs_root():
    # If we are running in dev (eg automatic run in VS Code, or triggerd from cli)
    # then put each pipeline run in a separate directory under runlogs_root.
    if args.run_environment == "dev":
        runlog_prefix = start_time
    else:
        runlog_prefix = ""

    return Path(args.runlogs_root) / runlog_prefix


def make_task_runlogs_root(runlog: Runlog):
    """
    Define organization of runlog-files from this pipeline
    """
    # extract filename of Jupytext notebook being run
    task_name = Path(runlog["notebook_path"]).name.replace(".py", "")

    return make_runlogs_root() / task_name / runlog["parameters.run.id"]


def make_notebook_task(
    notebook_path: Path, timeout_s=None, n_max_retries=1, parameters={}
):
    jupytext_notebook = JupytextNotebook(notebook_path)
    return JupytextNotebookTask(
        jupytext_notebook,
        get_run_path=make_task_runlogs_root,
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

task_ingest = make_notebook_task(
    notebook_path=Path("./notebooks/ingest.py"), timeout_s=3, n_max_retries=10
)
task_eda = make_notebook_task(notebook_path=Path("./notebooks/eda.py"))

tasks = [task_ingest, task_eda]
task_dependencies = TaskDependencies(task_ingest >> task_eda)

print("---- Running mnist-demo-pipeline ----")

_ = flatten(run_tasks(tasks, task_dependencies))

write_json(
    make_runlogs_root() / "task_dependencies.json",
    get_task_dependencies(task_dependencies),
)

print("---- Done ----")
