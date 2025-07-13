## Overview
This is the container for chatbot capacities to interact with your models downloaded via Ollama. All routes are protected by JWT (JSON Web Tokens). You must include a valid JWT token in the `Authorization` header of your requests.
You can to get JWT when you access sucessfully at app by login page to frontend, or if you are using programs like Postman, you can to get it using the routes `/log-in` or `/sing-up` from ddbb container.
## Authentication
All routes are protected by JWT authentication. You must include a valid JWT token in the `Authorization` header of your requests.
## Routes
### 1. `/query` (POST) - Send Query to Chatbot
* **Description:** Sends a query to the chatbot and retrieves the response.
* **Request Body:**
   * `config` (object): Configuration parameters for the chatbot.
* **Authentication:** Required (JWT)
* **Response (JSON):**
   * `content` (string): The chatbot's response.

### 2. `/get_ollama_models` (GET) - Get Ollama Models
* **Description:** Retrieves a list of available Ollama models.
* **Authentication:** Required (JWT)
* **Response (JSON):**
   * `list of dict`: A list of dictionaries, each representing an Ollama model.

### 3. `/new_chat` (POST) - Create a New Chat
* **Description:** Creates a new chat session with a specified name.
* **Request Body:**
   * `chatName` (string): The name of the new chat.
* **Authentication:** Required (JWT)
* **Response (JSON):**
   * `Response` (dict): A dictionary containing information about the new chat session.

### 4. `/get_chats` (GET) - Get All Chats
* **Description:** Retrieves a list of all existing chat sessions.
* **Authentication:** Required (JWT)
* **Response (JSON):**
   * `collections_name` (dict[str, list[dict]]): A dictionary where keys are chat names and values are lists of chat messages.

### 5. `/remove-chat` (POST) - Remove a Chat
* **Description:** Removes a specified chat session.
* **Request Body:**
   * `chatName` (string): The name of the chat to remove.
* **Authentication:** Required (JWT)
* **Response (JSON):**
   * `Response` (dict): A dictionary indicating the result of the removal operation.

### 6. `/get-conversation` (GET) - Get Chat Conversation
* **Description:** Retrieves the conversation history for a specified chat session.
* **Request Body:**
   * `chatName` (string): The name of the chat to retrieve the conversation from.
* **Authentication:** Required (JWT)
* **Response (JSON):**
   * `list[dict[str, str]]`: A list of dictionaries, each representing a message in the conversation with "sender" and "message" keys.

### 7. `/update-chat-name` (POST) - Update Chat Name
* **Description:** Updates the name of an existing chat session.
* **Request Body:**
   * `oldChatName` (string): The current name of the chat.
   * `newChatName` (string): The new name for the chat.
* **Authentication:** Required (JWT)
* **Response (JSON):**
   * `Response` (dict): A dictionary indicating the result of the chat name update operation.
