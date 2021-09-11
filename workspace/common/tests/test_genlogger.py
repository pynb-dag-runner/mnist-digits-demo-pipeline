from pathlib import Path

#
from common.genlogger import GenLogger


def test_info(tmp_path: Path):
    logger = GenLogger(log_directory=tmp_path)

    logger.info("hello")
    logger.info(123)
    logger.info([1, 2, {"a": 3}])

    logger.persist()
