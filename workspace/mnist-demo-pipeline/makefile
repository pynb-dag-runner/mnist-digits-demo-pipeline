SHELL := /bin/bash

run:
	(cd mnist-demo-pipeline; \
	    python3 -u driver.py \
	        --data_lake_root /pipeline-outputs/data-lake \
	        --runlogs_root /pipeline-outputs/runlogs/$$(date +"%Y-%m-%d_%H-%M-%S") \
	)

test-mypy:
	mypy --ignore-missing-imports .

test-black:
	black --check --diff .

clean-pipeline-outputs:
	# use with care
	rm -rf /pipeline-outputs/data-lake/*
	touch /pipeline-outputs/data-lake/.gitkeep

	touch /pipeline-outputs/runlogs/.gitkeep;
	rm -rf /pipeline-outputs/runlogs/*;
