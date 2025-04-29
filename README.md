# Notifier API

## Overview

This project implements a solution for the task defined in the [TASK.md](docs/TASK.md) file.

It's a simple backend API that runs at: `http://localhost:5000/v1/<endpoint>`.

## Environment variables

The following environment variables are required to run the app:

```sh
FLASK_APP=run.py
FLASK_CONFIG=testing
TEST_DATABASE_URL
```

## Dependencies

Install dependencies (`poetry` >=1.5.0 needs to be [installed](https://python-poetry.org/docs/#installing-with-the-official-installer) on the system)

Depending on your IDE, you may need to configure the python interpreter to use the poetry environment (i.e. [PyCharm](https://www.jetbrains.com/help/pycharm/poetry.html))

If the previous step has not done it automatically, now you have to install dependencies:

```sh
poetry install
```

Activate `poetry environment`:

```sh
poetry shell
```

Now, if necessary, use the following command to deploy whatever is needed in the database:

```sh
flask deploy
```

## Running the app

```sh
poetry run flask run
```
