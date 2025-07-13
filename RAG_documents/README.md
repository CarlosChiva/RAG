## Overview
This document describes the API endpoints avaiable in this FastAPI application. The application provides functionalities for interacting with a chatbot, retrieving information from databases (PostgreSQL and MySQL), and managing document collections. All routes are protected by JWT (JSON Web Tokens). You must include a valid JWT token in the `Authorization` header of your requests.
You can to get JWT when you access sucessfully at app by login page to frontend, or if you are using programs like Postman, you can to get it using the routes `/log-in` or `/sing-up` from ddbb container.
## Authentication
All routes are protected by JWT authentication. You must include a valid JWT token in the `Authorization` header of your requests.
## Routes
### 1. `/lmm-response` (GET) - LLM Response
*  **Description:** This endpoint allows users to ask questions to the chatbot and retrieve a response. It queries a configured database (PostgreSQL or MySQL) for rellevant information and uses the retrieved data to generate a response.
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