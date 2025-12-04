## Overview

This document describes the API endpoints available in this FastAPI application. The application provides functionalities for interacting with a chatbot, retrieving information from databases (PostgreSQL and MySQL), and managing database configurations. All routes are protected by JWT (JSON Web Tokens). You must include a valid JWT token in the `Authorization` header of your requests.
You can get JWT when you access successfully at app by login page to frontend, or if you are using programs like Postman, you can get it using the routes `/log-in` or `/sing-up` from ddbb container.

## Authentication

All routes are protected by JWT authentication. You must include a valid JWT token in the `Authorization` header of your requests.

## Routes

### 1. `/question` (POST) - LLM Response

*   **Description:** This endpoint allows users to ask questions to the chatbot and retrieve a response. It queries a configured database (PostgreSQL or MySQL) for relevant information and uses the retrieved data to generate a response.
*   **Request Body:**
    *   `input` (string): The user's question.
    *   `database_conf` (object): Database configuration details (e.g., connection string).
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `result` (object): The chatbot's response and any error messages.
    *   `table` (object): The table returned from the database query.

### 2. `/get-list-configurations` (GET) - Get Configuration List

*   **Description:** Retrieves a list of available database configurations.
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `result` (list of strings): A list of database connection configuration names.

### 3. `/add_configuration` (POST) - Add Configuration

*   **Description:** Adds a new database configuration.
*   **Request Body:**
    *   `conf` (object): Configuration details (e.g., name, connection parameters).
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `result` (object): Indicates success or failure of the database connection configuration creation.

### 4. `/try-connection` (GET) - Test Database Connection

*   **Description:** Attempts to establish a connection to a specified database.
*   **Query Parameters:**
    *   `connection_name` (string): The name of the database connection.
    *   `type_db` (string): The type of database (e.g., "postgres", "mysql").
    *   `user` (string): The database username.
    *   `password` (string): The database password.
    *   `host` (string): The database host.
    *   `port` (string): The database port.
    *   `database_name` (string): The database name.
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `message` (string): "Connection successful" if the connection is successful.

### 5. `/remove-configuration` (DELETE) - Remove Configuration

*   **Description:** Removes a specified database configuration.
*   **Request Body:**
    *   `conf_rm` (object): Configuration details (e.g., name).
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `Response` (object): Indicates if the database configuration has been successfully deleted or not.

## Environment Variables

The application uses the following environment variables, defined in `.env`:

*   `CONFIG_FOLDER`: Path to the folder containing configuration files.
*   `SQL_MODEL`: The name of the SQL model to use (default: `qwen2.5`).
*   `ALGORITHM`: The JWT algorithm used for signing tokens (default: `HS256`).
*   `SECRET_KEY`: The secret key used for signing JWT tokens (default: `secret_key`).

## Docker

This project includes a `Dockerfile` to containerize the application. It uses Python 3.12 as the base image, installs required dependencies from `requirements.txt`, and sets up the application to run with `uvicorn` on port 8002.

### Building the Docker Image

To build the Docker image, run:

```bash
docker build -t rag-ddbb .
```

### Running the Container

To run the container, use:

```bash
docker run -p 8002:8002 rag-ddbb
```

### Using Docker Compose

If you are using Docker Compose, ensure you have a `docker-compose.yml` file in the root directory of the project. Then run:

```bash
docker-compose up
```

This will start the application container, mapping port 8002 to the host.

## Requirements

The application requires the following dependencies, as specified in `requirements.txt`:

*   FastAPI
*   uvicorn
*   SQLAlchemy
*   PyJWT
*   langchain
*   ollama
*   psycopg2-binary
*   PyMySQL
*   and others...
