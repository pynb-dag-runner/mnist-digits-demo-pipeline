SHELL := /bin/bash

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
	make COMMAND="(cd common; make clean)" docker-run-in-cicd

test-all:
	# Single command to run all tests
	make COMMAND="( \
	    cd common; \
	    make install; \
	    make test-pytest test-mypy test-black; \
	    make clean; \
	    ) && ( \
	    cd mnist-demo-pipeline; \
	    make test-mypy test-black; \
	    make run; \
	)" docker-run-in-cicd
