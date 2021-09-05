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
	    --workdir /home/host_user/workspace/ \
	    mnist-demo-pipeline-cicd \
	    "$(COMMAND)"


### Outline for testing and running demo pipeline; Implementation TODO

clean:
	make COMMAND="(cd .; echo todo-clean)" docker-run-in-cicd

build:
	make COMMAND="(cd .; echo todo-build)" docker-run-in-cicd

test:
	# Run all tests for library
	make COMMAND="( \
	    cd .; \
	    echo \
	        todo \
			test-pytest \
	        test-mypy \
	        test-black \
	)" docker-run-in-cicd
