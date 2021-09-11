import sys

# See "write-vs-code-tasks-json" task in repo root
sys.path.append("/home/host_user/pynb-dag-runner/workspace/.vscode/")
from make_tasks_json import write_tasks_file_dict, make_component_tasks

print(" - Writing VS Code tasks.json for mnist-demo-pipeline components ...")

write_tasks_file_dict(
    output_file="tasks.json",
    tasks=make_component_tasks(
        component_name="mnist-demo-pipeline common",
        component_relative_path="common",
        task_commands={
            "run unit tests": "make test-pytest",
            "run static code analysis": "make test-mypy",
            "check code is linted": "make test-black",
        },
    )
    + make_component_tasks(
        component_name="mnist-demo-pipeline",
        component_relative_path="mnist-demo-pipeline",
        task_commands={
            "run pipeline": "make run",
            "run static code analysis": "make test-mypy",
            "check code is linted": "make test-black",
        },
    ),
)

print(" - Done")
