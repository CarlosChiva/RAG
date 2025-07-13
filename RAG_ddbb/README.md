## Overview

This document describes the API endpoints available in this FastAPI application. The application provides functionalities for interacting with a chatbot, retrieving information from databases (PostgreSQL and MySQL), and managing document collections. All routes are protected by JWT (JSON Web Tokens). You must include a valid JWT token in the `Authorization` header of your requests.
You can to get JWT when you access sucessfully at app by login page to frontend, or if you are using programs like Postman, you can to get it using the routes `/log-in` or `/sing-up` from ddbb container.

## Authentication

All routes are protected by JWT authentication. You must include a valid JWT token in the `Authorization` header of your requests.

## Routes

### 1. `/question` (POST) - LLM Response

*   **Description:** This endpoint allows users to ask questions to the chatbot and retrieve a response. It queries a configured database (PostgreSQL or MySQL) for rellevant information and uses the retrieved data to generate a response.
*   **Request Body:**
    *   `input` (string): The user's question.
    *   `database_conf` (object): Database configuration details (e.g., connection string).
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `result` (object): The chatbot's response and any error messages.
    *   `table` (object): The table returned from the database query.

### 2. `/get-list-configurations` (GET) - Get Collection List

*   **Description:** Retrieves a list of available document collections.
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `result` (list of strings): A list of configurations of databases connections names.

### 3. `/add_configuration` (POST) - Add Collection

*   **Description:** Adds a new document collection.
*   **Request Body:**
    *   `conf` (object): Collection configuration details (e.g., name).
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `result` (object): Indicates success or failure of the database connection creation.

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

### 5. `/remove-configuration` (DELETE) - Remove Collection

*   **Description:** Removes a specified document collection.
*   **Request Body:**
    *   `conf_rm` (object): Collection configuration details (e.g., name).
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `Response` (object): Indicates if the configuration of database has been success or failure deletion.

