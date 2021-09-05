#!/bin/bash

# Copy files that will be almost identical from submodule library repo.
# This is here done with a script so it can (if needed) be done again
# later. This also makes it possible to track the origin of these files.

cp pynb-dag-runner/LICENSE.md .
cp pynb-dag-runner/.gitignore .

cp -r pynb-dag-runner/docker .
cp pynb-dag-runner/makefile .

cp pynb-dag-runner/.devcontainer* .

mkdir -p .vscode
cp pynb-dag-runner/.vscode/extensions.json .vscode/

mkdir -p workspace/.vscode
cp pynb-dag-runner/workspace/.vscode/settings.json ./workspace/.vscode/
cp pynb-dag-runner/workspace/.vscode/extensions.json ./workspace/.vscode/
