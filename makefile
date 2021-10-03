SHELL := /bin/bash

# override when invoking make, eg "make RUN_ENVIRONMENT=ci ..."
RUN_ENVIRONMENT ?= "dev"

docker-build-all:
	# For now manually build wheel file for pynb-dag-runner library dependency
	(cd pynb-dag-runner; \
	    make docker-build-all build)

	# Build docker images for mnist-demo-pipeline
	(cd docker; make \
	    build-base-env-docker-image \
	    build-cicd-env-docker-image \
	    build-dev-env-docker-image)

### Manually start/stop the dev-docker container (can be used without VS Code)

dev-up:
	docker-compose \
	    -f .devcontainer-docker-compose.yml \
	    up \
	    --remove-orphans \
	    --abort-on-container-exit \
	    dev-environment

dev-down:
	docker-compose \
	    -f .devcontainer-docker-compose.yml \
	    down \
	    --remove-orphans

### Define tasks run inside Docker

docker-run-in-cicd:
	docker run --rm \
	    --network none \
	    --env RUN_ENVIRONMENT=$(RUN_ENVIRONMENT) \
	    --volume $$(pwd)/workspace:/home/host_user/workspace \
	    --volume $$(pwd)/pipeline-outputs:/pipeline-outputs \
	    --workdir /home/host_user/workspace/ \
	    mnist-demo-pipeline-cicd \
	    "$(COMMAND)"

write-vs-code-tasks-json:
	# Task to update tasks.json file with task definitions for VS Code. This
	# may not be the most elegant solution; we only need to import <100 lines
	# of Python from pynb-dag-runner. However, one should not need to update
	# the tasks very often.
	docker run --rm \
	    --network none \
	    --volume $$(pwd)/workspace:/home/host_user/workspace \
	    --volume $$(pwd)/pynb-dag-runner:/home/host_user/pynb-dag-runner \
	    --workdir /home/host_user/workspace/.vscode/ \
	    mnist-demo-pipeline-cicd \
	    "( \
	        mypy --ignore-missing-imports write_tasks_json.py; \
	        black write_tasks_json.py; \
	        python3 write_tasks_json.py \
	    )"

clean:
	# The below commands do not depend on RUN_ENVIRONMENT. But, the command
	# is most useful in dev-setup.
	make docker-run-in-cicd \
	    COMMAND=" \
	        (cd common; make clean; ) && \
	        (cd mnist-demo-pipeline; make clean-pipeline-outputs)"

draw-runlog-visuals:
	# Rendering images should only be run when RUN_ENVIRONMENT="ci"
	# (rending will not work in RUN_ENVIRONMENT="ci" due to different
	# directory layout)
	#
	# Only rendering png for now, generated task-dependencies.svg is broken
	if [ "$(RUN_ENVIRONMENT)" = "ci" ]; then ( \
	    export RUNLOGS_ROOT="$$(pwd)/pipeline-outputs/runlogs"; \
	    export IMG_OUTPUT_DIRECTORY="$$(pwd)/pipeline-outputs"; \
	    cd pynb-dag-runner/tools/draw-runlog-visuals; \
	    make draw-runlog-visuals IMG_OUTPUT_FORMAT="png"; \
	); fi

test-and-run-pipeline:
	# Single command to run all tests and the demo pipeline
	make clean

	make docker-run-in-cicd \
	    RUN_ENVIRONMENT=$(RUN_ENVIRONMENT) \
	    COMMAND="( \
	        cd common; \
	        make install; \
	        make clean; \
	    ) && ( \
	        cd mnist-demo-pipeline; \
	        make test-mypy test-black; \
	        make run; \
	    )"

	make draw-runlog-visuals RUN_ENVIRONMENT=$(RUN_ENVIRONMENT)
