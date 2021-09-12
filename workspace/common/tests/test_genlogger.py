from pathlib import Path

#
import matplotlib.pyplot as plt

#
from pynb_dag_runner.helpers import read_json
from common.genlogger import GenLogger


def test_genlogger_info_messages_and_empty_output_file(tmp_path: Path):
    logger = GenLogger(log_directory=tmp_path)

    logger.info("hello")
    logger.info(123)
    logger.info([1, 2, {"a": 3}])

    logger.persist()

    # no data was logged, so persisted genlogger.json should be empty
    assert read_json(tmp_path / "genlogger.json") == {"images": [], "key-values": {}}


def test_genlogger_log_key_values(tmp_path: Path):
    logger = GenLogger(log_directory=tmp_path)

    values_to_log = {
        "int": 1,
        "string": "baz",
        "bool": True,
        "none": None,
        "float": 123.2,
        "mixed": [1, 2, {"x.1": 123}],
    }

    for k, v in values_to_log.items():
        logger.log(k, v)

    logger.persist()
    assert read_json(tmp_path / "genlogger.json") == {
        "images": [],
        "key-values": values_to_log,
    }


def test_genlogger_can_persist_images(tmp_path: Path):
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
