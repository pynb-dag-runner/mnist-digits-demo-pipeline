# `mnist-digits-demo-pipeline`

This repository contains a demo machine learning pipeline that trains a model for predicting the digit 0, ..., 9 from a handwritten 8x8 image of the digit.

The pipeline is implemented using the `pynb-dag-runner` library, see [here](https://github.com/pynb-dag-runner/pynb-dag-runner).

## Running the pipeline

### Run pipeline as part of repo's automated CI pipeline

This repository uses Github Actions automation to run the demo pipeline as part of the repo's CI-pipeline. Each CI-run stores the pipeline outputs (notebooks, models, and logged images and metrics) as build artefacts.

To inspect the pipeline outputs, download a zip build artefact from a recent build from [here](https://github.com/pynb-dag-runner/mnist-digits-demo-pipeline/actions/workflows/ci.yml).

This means:
- The entire pipeline is run for each pull request to this repository.
- From the build artefacts one can inspect the pipeline outputs for each pull request/commit.
- The pipeline runs using (free) compute resources provided by Github.

### Run pipeline as script

To run the pipeline (eg. locally) one needs to install git, make and Docker.

First, clone the demo pipeline repository
```bash
git clone --recurse-submodules git@github.com:pynb-dag-runner/mnist-digits-demo-pipeline.git
```

Now the pipeline can be run as follows:
```bash
make docker-build-all
make clean
make RUN_ENVIRONMENT="dev" test-and-run-pipeline
```

Pipeline outputs (evaluated notebooks, models, logs, and images) are stored in the repo `pipeline-outputs` directory).

This above steps are essentially what is run by the CI-automation (although that is run with `RUN_ENVIRONMENT="ci"` which is slower).

## Pipeline development

This repo is set up for pipeline development using Jupyter notebook via VS Code's remote containers. This is similar to the setup for developing the [pynb-dag-runner](https://github.com/pynb-dag-runner/pynb-dag-runner) library.

The list of development tasks in VS Code, are defined [here](workspace/.vscode/tasks.json). The key task is `mnist-demo-pipeline - watch and run all tasks` which runs the entire pipeline in watch mode, and runs black and mypy static code analysis on the pipeline notebook codes (also in watch mode).

## Contact

A motivation for developing this is to make it easier to set up and work together (on pipelines). If you would like to discuss an idea, please raise an [issue](https://github.com/pynb-dag-runner/mnist-digits-demo-pipeline/issues) or contact me via email.

Please note that this is 🚧🚧🚧🚧🚧. Roadmap, TODO

## License

(c) Matias Dahl 2021, MIT, see [LICENSE.md](./LICENSE.md).
