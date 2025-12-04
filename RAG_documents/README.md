
## Overview
This document describes the API endpoints available in this FastAPI application. The application provides functionalities for interacting with a chatbot, retrieving information from databases (PostgreSQL and MySQL), and managing document collections. All routes are protected by JWT (JSON Web Tokens). You must include a valid JWT token in the `Authorization` header of your requests.
You can get JWT when you access successfully at app by login page to frontend, or if you are using programs like Postman, you can get it using the routes `/log-in` or `/sing-up` from ddbb container.
## Authentication
All routes are protected by JWT authentication. You must include a valid JWT token in the `Authorization` header of your requests.
## Routes
### 1. `/lmm-response` (GET) - LLM Response
*  **Description:** This endpoint allows users to ask questions to the chatbot and retrieve a response. It queries a configured database (PostgreSQL or MySQL) for relevant information and uses the retrieved data to generate a response.
*  **Query Parameters:**
   *  `input` (string): The user's question.
   *  `collection_name` (string): The name of the collection to query.
*  **Authentication:** Required (JWT)
*  **Response (JSON):**
   *  `result` (string): The chatbot's response.
   *  `error` (string, optional): An error message if the question is invalid.
### 2. `/add_document` (POST) - Add Document
*  **Description:** Adds a new document to an existing collection.
*  **Request Body:**
   *  `file` (file): The PDF file to add.
   *  `name_collection` (string): The name of the collection to add the document to.
*  **Authentication:** Required (JWT)
*  **Response (JSON):**
   *  `data` (dict): The identifier of the added document.
   *  `error` (string, optional): An error message if the document cannot be added.
### 3. `/collections` (GET) - Get Collections List
*  **Description:** Retrieves a list of existing collection names.
*  **Authentication:** Required (JWT)
*  **Response (JSON):**
   *  `collections_name` (list of strings): A list of collection names.
### 4. `/self-collection-name` (GET) - Get Current Collection Name
*  **Description:** Retrieves the name of the current collection.
*  **Authentication:** Required (JWT)
*  **Response (JSON):**
   *  `collection_name` (string): The name of the current collection.
### 5. `/new-collection-name` (POST) - Set New Collection Name
*  **Description:** Sets a new name for the collection.
*  **Request Body:**
   *  `name_collection` (string): The new name for the collection.
*  **Authentication:** Required (JWT)
*  **Response (JSON):**
   *  `message` (string): A message indicating success or failure.
## Environment Variables
The application uses the following environment variables:
*   `PERSIST_DIRECTORY`: The directory where the data is persisted (default: "PersistDirectory").
*   `MODEL`: The model to use for the chatbot (default: "llama3.2").
*   `EMBEDD_MODEL`: The embedding model to use (default: "bge-m3:latest").
*   `ALGORITHM`: The algorithm used for JWT (default: "HS256").
*   `SECRET_KEY`: The secret key for JWT (default: "secret_key").
*   `PATH_CONVERSATIONS`: The path to the conversations file (default: "/app/conversations/conversations.json").
## Docker
This project uses Docker for containerization. To build and run the application, use the following commands:
```bash
docker build -t rag-app .
docker run -p 8000:8000 rag-app
```
## Running with Docker Compose
You can also run the application using Docker Compose:
```bash
docker-compose up
```
## Requirements
The application requires the following dependencies:
*   Python 3.10
*   FastAPI
*   Uvicorn
*   ChromaDB
*   LangChain
*   Ollama
*   Other dependencies listed in `requirements.txt`
## Usage
To use the application, follow these steps:
1.  Start the application using Docker.
2.  Obtain a JWT token by logging in or signing up.
3.  Use the API endpoints with the JWT token in the `Authorization` header.
4.  Add documents to collections using the `/add_document` endpoint.
5.  Query the chatbot using the `/lmm-response` endpoint.
6.  Manage collections using the `/collections`, `/self-collection-name`, and `/new-collection-name` endpoints.
## API Endpoints
### 1. `/lmm-response` (GET) - LLM Response
*   **Description:** This endpoint allows users to ask questions to the chatbot and retrieve a response. It queries a configured database (PostgreSQL or MySQL) for relevant information and uses the retrieved data to generate a response.
*   **Query Parameters:**
    *   `input` (string): The user's question.
    *   `collection_name` (string): The name of the collection to query.
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `result` (string): The chatbot's response.
    *   `error` (string, optional): An error message if the question is invalid.
### 2. `/add_document` (POST) - Add Document
*   **Description:** Adds a new document to an existing collection.
*   **Request Body:**
    *   `file` (file): The PDF file to add.
    *   `name_collection` (string): The name of the collection to add the document to.
*   **Authentication:** Required (JWT)
*  **Response (JSON):**
    *   `data` (dict): The identifier of the added document.
    *   `error` (string, optional): An error message if the document cannot be added.
### 3. `/collections` (GET) - Get Collections List
*   **Description:** Retrieves a list of existing collection names.
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `collections_name` (list of strings): A list of collection names.
### 4. `/self-collection-name` (GET) - Get Current Collection Name
*   **Description:** Retrieves the name of the current collection.
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `collection_name` (string): The name of the current collection.
### 5. `/new-collection-name` (POST) - Set New Collection Name
*   **Description:** Sets a new name for the collection.
*   **Request Body:**
    *   `name_collection` (string): The new name for the collection.
*   **Authentication:** Required (JWT)
*   **Response (JSON):**
    *   `message` (string): A message indicating success or failure.
