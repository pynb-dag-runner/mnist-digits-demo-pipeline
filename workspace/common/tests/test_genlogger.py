from pathlib import Path

#
import matplotlib.pyplot as plt

#
from common.genlogger import GenLogger

from pynb_dag_runner.helpers import read_json


def test_info(tmp_path: Path):
    logger = GenLogger(log_directory=tmp_path)

    logger.info("hello")
    logger.info(123)
    logger.info([1, 2, {"a": 3}])

    logger.persist()
    assert read_json(tmp_path / "genlogger.json") == {"images": [], "key-values": {}}


def test_can_persist_images(tmp_path: Path):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3, 3))
    ax.plot([1, 2, 3], [4, 2, 4])

    logger = GenLogger(log_directory=tmp_path)
    logger.log_image("a/b/c.png", fig)
    logger.persist()

    assert (tmp_path / "images" / "a/b/c.png").is_file()

    assert read_json(tmp_path / "genlogger.json") == {
        "images": ["a/b/c.png"],
        "key-values": {},
    }
