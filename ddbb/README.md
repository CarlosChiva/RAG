## Overview
This container provides functionalities for managing user data within its main database. All routes are protected by JWT (JSON Web Tokens). You must include a valid JWT token in the `Authorization` header of your requests.
You can to get JWT when you access sucessfully at app by login page to frontend, or if you are using programs like Postman, you can to get it using the routes `/log-in` or `/sing-up` from ddbb container.
## Authentication
All routes are protected by JWT authentication. You must include a valid JWT token in the `Authorization` header of your requests.
## Routes
### 1. `/log-in` (POST) - User Login
* **Description:** Allows users to log in to the system.  It authenticates users based on their username and password.
* **Request Body:**
    * `usernaume` (string): The user's username.
    * `password` (string): The user's password.
* **Authentication:** None required (unprotected endpoint).
* **Response (JSON):**
    * `access_token` (string): A JWT access token upon successful login.

### 2. `/sing_up` (POST) - User Registration
* **Description:** Allows new users to register in the system.
* **Request Body:**
    * `usernaume` (string): The desired username.
    * `password` (string): The desired password.
* **Authentication:** None required (unprotected endpoint).
* **Response (JSON):**
    * `access_token` (string): A JWT access token upon successful registration.

### 3. `/get-services` (GET) - Get Services for Authenticated User
* **Description:** Retrieves a list of services available to the authenticated user.
* **Authentication:** Required (JWT)
* **Response (JSON):**
    * `services` (list of strings): A list of services available to the user.

### 4. `/get-services-available` (GET) - Get All Available Services
* **Description:** Retrieves a list of all services available in the system.
* **Authentication:** Required (JWT)
* **Response (JSON):**
    * `services` (list of strings): A list of all available services.

### 5. `/add-services` (POST) - Add a Service for Authenticated User
* **Description:** Allows the authenticated user to add a new service.
* **Request Body:**
    * `service` (string): The name of the service to add.
* **Authentication:** Required (JWT)
* **Response (JSON):**
    * `services` (list of strings): The updated list of services, including the newly added service.

### 6. `/remove-services` (POST) - Remove a Service for Authenticated User
* **Description:** Allows the authenticated user to remove a service.
* **Request Body:**
    * `service` (string): The name of the service to remove.
* **Authentication:** Required (JWT)
* **Response (JSON):**
    * `services` (list of strings): The updated list of services, excluding the removed service.
