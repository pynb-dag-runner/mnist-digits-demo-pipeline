from pathlib import Path
from functools import lru_cache


@lru_cache
def args():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "--pipeline_outputs_path",
        type=Path,
        help="output path where OpenTelemetry spans have been expanded (tmp)",
    )

    return parser.parse_args()


print(f"--- Command line parameters")
print(f"  - pipeline_outputs_path         : {args().pipeline_outputs_path}")


def make_markdown_report(pipeline_outputs_path: Path) -> str:
    report_lines = []

    for file in pipeline_outputs_path.glob("*"):
        print(file)

    report_lines.append("## DAG diagram of task dependencies in this pipeline")
    report_lines.append("```mermaid")
    report_lines.append((pipeline_outputs_path / "dag.mmd").read_text())
    report_lines.append("```")

    report_lines.append("## Gantt diagram of task runs in pipeline")
    report_lines.append("```mermaid")
    report_lines.append((pipeline_outputs_path / "gantt.mmd").read_text())
    report_lines.append("```")

    return "\n".join(report_lines)


(args().pipeline_outputs_path / "pipeline_run_summary.md").write_text(
    make_markdown_report(args().pipeline_outputs_path)
)


print("--- Done ---")
