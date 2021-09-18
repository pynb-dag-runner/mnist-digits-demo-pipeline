SHELL := /bin/bash

run:
	echo "environment variable RUN_ENVIRONMENT: ${RUN_ENVIRONMENT}"
	(cd mnist-demo-pipeline; \
	    python3 -u driver.py \
	        --data_lake_root /pipeline-outputs/data-lake \
	        --runlogs_root /pipeline-outputs/runlogs \
	        --run_environment ${RUN_ENVIRONMENT} \
	)

test-mypy:
	mypy --ignore-missing-imports .

test-black:
	black --check --diff --exclude /.ipynb_checkpoints/ .

clean-pipeline-outputs:
	# use with care
	rm -rf /pipeline-outputs/data-lake/*
	touch /pipeline-outputs/data-lake/.gitkeep

	touch /pipeline-outputs/runlogs/.gitkeep;
	rm -rf /pipeline-outputs/runlogs/*;
