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

    parser.add_argument(
        "--github_step_summary_path",
        type=Path,
        help="filepath to write pipeline summary, see "
        "https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#adding-a-job-summary",
    )

    return parser.parse_args()


print(f"--- Command line parameters")
print(f"  - pipeline_outputs_path    : {args().pipeline_outputs_path}")
print(f"  - github_step_summary_path : {args().github_step_summary_path}")


def make_markdown_report(pipeline_outputs_path: Path) -> str:
    report_lines = []

    for file in pipeline_outputs_path.glob("*"):
        print(file)

    report_lines.append("# Pipeline run")
    report_lines.append("- foo 1")
    report_lines.append("- foo 2")
    report_lines.append("- `foo 3`")

    return "\n".join(report_lines)


args().github_step_summary_path.write_text(
    make_markdown_report(args().pipeline_outputs_path)
)


print("--- Done ---")
