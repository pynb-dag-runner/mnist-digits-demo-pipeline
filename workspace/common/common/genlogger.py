from typing import Any, Dict, List
from pathlib import Path
import datetime

from pynb_dag_runner.helpers import write_json


class GenLogger:
    """
    --- to be deprecated ---

    Generic logger for:

     - info-messages        (not persisted, but displayed with timing)
     - key-value pairs      (persisted to runlog directory)
     - matplotlib images    (persisted to runlog directory)

    The log-directory for persisting logged objects will typically be the runlog
    directory (determined by pynb-dag-runner). Then the runlog will be associated to
    one run of a task. That provides the context for logged items.

    By implementing our own logging wrapper we can persist logged objects after a
    pipeline has run without need for external services. This also leaves open the
    option to later replay persisted log messages into eg ML Flow (possibly
    running offline).
    """

    def __init__(self, log_directory: Path):
        self.last_ts: datetime.datetime = datetime.datetime.now()
        self.info("GenLogger initialized")

    def info(self, obj: Any):
        """
        Log info message with timing (current time, and seconds since last log-event)

        Example:
        import time
        logger.info("hello")
        time.sleep(0.5)
        logger.info("world")

        Output:
        11:23:44 |   0.0 | hello
        11:23:45 |   0.5 | world

        """
        seconds_since_last: float = (
            datetime.datetime.now() - self.last_ts
        ).total_seconds()
        self.last_ts = datetime.datetime.now()

        print(
            " | ".join(
                [
                    self.last_ts.strftime("%H:%M:%S"),
                    str(round(seconds_since_last, 2)).rjust(5),
                    str(obj),
                ]
            )
        )

    def log_image(self, imagename: str, fig):
        """
        Save a matplotlib figure to the log-directory
        """
        pass
        # if not imagename.endswith(".png"):
        #     raise ValueError("Filename should end with .png")

        # if imagename.startswith("/") or ".." in imagename:
        #     raise ValueError("Invalid filename")

        # outpath = self.log_directory / "images" / imagename
        # outpath.parent.mkdir(exist_ok=True, parents=True)

        # # plots are transparent by default
        # fig.savefig(outpath, facecolor="white", transparent=False)

        # self.images.append(imagename)
        # self.info(f"Logged matplotlib fig {imagename}.")

    def _log(self, key: str, value: Any):
        pass

    def log_dict(self, kv_dict: Dict[str, Any]):
        pass

    def log(self, key: str, value: Any):
        pass

    def persist(self):
        pass
