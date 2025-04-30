# Notifier API

## Overview

This project implements a solution for the task defined in the [TASK.md](docs/TASK.md) file.

It's a simple backend API built with Flask and Python, following Hexagonal Architecture principles (Ports & Adapters). The API receives assistance requests via a webhook and routes them to different notification channels (Slack for Sales, Email/Log for Pricing) based on the request topic.

The main notification endpoint runs at: `http://localhost:8080/v1/notify` (when using Docker/Nginx) or `http://localhost:5000/v1/notify` (when running Flask directly).

A health check endpoint is available at `/v1/health`.

## Architectural Overview

The application uses a Hexagonal Architecture:

- **Domain:** Core business logic (`AssistanceRequest`, `HandleAssistanceRequest`).
- **Ports:** Interfaces defining interactions (`NotificationChannel` interface).
- **Adapters:**
  - _Input:_ Flask API endpoint (`app/api/notify.py`) translates HTTP requests.
  - _Output:_ Notification handlers (`SlackNotificationAdapter`, `EmailNotificationAdapter`) translate domain events into external calls (Slack API, Logging).
- **Application Layer:** Orchestrates the flow using a factory pattern (`app/__init__.py`) to wire components.

## Environment variables

The application requires the following environment variables:

```sh
# Flask Configuration
FLASK_APP=run.py        # Entry point for the flask command
FLASK_CONFIG=development # Config to use (development, testing, production)

# Slack Configuration (Required for Sales notifications)
SLACK_BOT_TOKEN=<your_slack_bot_token>
SLACK_CHANNEL_ID=<target_slack_channel_id>

# --- Variables primarily for Testing ---
TEST_SLACK_BOT_TOKEN=<optional_override_token_for_tests>
TEST_SLACK_CHANNEL_ID=<optional_override_channel_for_tests>
```

- Set `FLASK_CONFIG` to `production` for production deployments.
- `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID` are essential for the Slack integration to work. Get these from your Slack app configuration.
- You can use a `.env` file to manage these variables locally.

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

## Running the app

### 1. Using Poetry

Ensure environment variables are set or available in a `.env` file.

```sh
# Run the development server
poetry run flask run

# The app will be available at http://localhost:5000
```

### 2. Using Docker Compose (Recommended)

This method uses the [docker/docker-compose.yml](docker/docker-compose.yml) file which runs the Flask app along with an Nginx proxy.

Ensure your `.env` file is in the project root, as `docker-compose.yml` is depends on it.

Build and start the containers in detached mode via the helper script:

```sh
sh docker/run.sh -d up
```

The app will be available via Nginx at `http://localhost:8080`

- View logs: `cd docker && docker compose logs -f`
- Stop containers: `sh docker/run.sh down`

## API Endpoint: Assistance Request Notification

- **URL:** `/v1/notify`
- **Method:** `POST`
- **Request Body:** JSON
  ```json
  {
    "topic": "string (e.g., 'sales', 'pricing')",
    "description": "string"
  }
  ```
- **Example Request (`curl`):**
  ```sh
  curl -X POST http://localhost:8080/v1/notify \
       -H "Content-Type: application/json" \
       -d '{
             "topic": "sales",
             "description": "Hello, I am interested in learning more about your enterprise tiers."
           }'
  ```
- **Success Response (202 Accepted):**
  ```json
  {
    "message": "Request received and processing."
  }
  ```
- **Error Responses:**
  - `400 Bad Request`: If `topic` or `description` are missing or invalid.
  - `500 Internal Server Error`: If an unexpected error occurs during processing.

## Running Tests

Ensure development dependencies are installed (`poetry install --with dev`). Set necessary test environment variables (e.g., `FLASK_CONFIG=testing`).

```sh
poetry run pytest
```
