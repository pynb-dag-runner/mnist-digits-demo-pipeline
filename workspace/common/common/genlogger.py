from typing import Any
from pathlib import Path
import datetime


class GenLogger:
    """
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
        self.log_directory = log_directory
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

    def persist(self):
        pass
