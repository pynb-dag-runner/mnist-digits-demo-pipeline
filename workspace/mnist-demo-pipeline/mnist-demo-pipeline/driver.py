from pathlib import Path
import uuid, datetime, shutil
from typing import List

#
import ray

#
from pynb_dag_runner.tasks.tasks import make_jupytext_task_ot
from pynb_dag_runner.opentelemetry_helpers import SpanRecorder
from pynb_dag_runner.core.dag_runner import (
    run_in_sequence,
    fan_in,
    start_and_await_tasks,
)

from pynb_dag_runner.notebooks_helpers import JupytextNotebook
from pynb_dag_runner.helpers import write_json

print("---- Initialize Ray cluster ----")

# Setup Ray and enable tracing using default OpenTelemetry support; traces are
# written to files /tmp/spans/<pid>.txt in JSON format.
shutil.rmtree("/tmp/spans", ignore_errors=True)
ray.init(_tracing_startup_hook="ray.util.tracing.setup_local_tmp_tracing:setup_tracing")


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

COMMON_PARAMETERS = {
    # data lake root is pipeline-scoped parameter
    "flow.data_lake_root": args.data_lake_root,
    "flow.runlogs_root": args.runlogs_root,
    "flow.run_environment": args.run_environment,
    "flow.pipeline_run_id": str(uuid.uuid4()),
}


def make_runlogs_root():
    # If we are running in dev (eg automatic run in VS Code, or triggerd from cli)
    # then put each pipeline run in a separate directory under runlogs_root.
    if args.run_environment == "dev":
        start_time: str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        runlog_prefix = start_time
    else:
        runlog_prefix = ""

    result = Path(args.runlogs_root) / runlog_prefix
    result.mkdir(parents=True, exist_ok=True)
    return result


def make_notebook_task(
    nb_name: str, timeout_s=None, max_nr_retries: int = 1, task_parameters={}
):
    nb_path: Path = (Path(__file__).parent) / "notebooks"

    return make_jupytext_task_ot(
        notebook=JupytextNotebook(nb_path / nb_name),
        tmp_dir=nb_path,
        timeout_s=timeout_s,
        max_nr_retries=max_nr_retries,
        parameters={**COMMON_PARAMETERS, **task_parameters},
    )


print("---- Setting up tasks and task dependencies ----")

task_ingest = make_notebook_task(nb_name="ingest.py", timeout_s=10, max_nr_retries=15)

task_eda = make_notebook_task(nb_name="eda.py")
run_in_sequence(task_ingest, task_eda)

# --- tasks defined using old API ---

# task_split_train_test = make_notebook_task(
#     notebook_path=Path("./notebooks/split-train-test.py"),
#     parameters={"parameters.task.train_test_ratio": 0.7},
# )
# run_in_sequence(task_ingest, task_split_train_test)

# nr_train_digits: List[int] = {
#     "ci": list(range(600, 1201, 100)) + [1257],
#     "dev": [400, 500, 600],
# }[args.run_environment]

# task_trainers = [
#     make_notebook_task(
#         notebook_path=Path("./notebooks/train-model.py"),
#         parameters={"parameters.task.nr_train_images": k},
#     )
#     for k in nr_train_digits
# ]

# task_benchmarks = [
#     make_notebook_task(
#         notebook_path=Path("./notebooks/benchmark-model.py"),
#         parameters={"parameters.task.nr_train_images": k},
#     )
#     for k in nr_train_digits
# ]

# task_summary = make_notebook_task(notebook_path=Path("./notebooks/summary.py"))

###

print("---- Running mnist-demo-pipeline ----")

with SpanRecorder() as rec:
    _ = start_and_await_tasks([task_ingest], [task_eda], arg={})

ray.shutdown()

print("---- Exceptions ----")

for s in rec.spans.exception_events():
    print(80 * "=")
    print(s)

print("---- Writing spans ----")

print(" - Total number of spans recorded   :", len(rec.spans))
span_path = make_runlogs_root() / "spans.json"
print(" - Output filename                  :", str(span_path))
write_json(span_path, list(rec.spans))

print("---- Done ----")
