# API de Gestión de Usuarios y Servicios

Esta carpeta implementa una API REST con FastAPI para autenticación de usuarios y gestión de servicios. Todos los endpoints (excepto `/log-in` y `/sing_up`) requieren autenticación JWT.

## Configuración

### `.env`
**Propósito:** Variables de entorno para conexión a base de datos MySQL y configuración de JWT.

**Variables:**
- `DB_HOST`: Host del servidor MySQL (default: `db`)
- `DB_USER`: Usuario de base de datos
- `DB_PASSWORD`: Contraseña de base de datos
- `DB_DATABASE`: Nombre de la base de datos
- `SECRET_KEY`: Clave secreta para firmar tokens JWT
- `ALGORITHM`: Algoritmo de encriptación (default: `HS256`)

### `requirements.txt`
**Propósito:** Dependencias del proyecto.

**Paquetes principales:**
- `fastapi==0.115.9`: Framework async para la API
- `uvicorn==0.30.6`: Servidor ASGI
- `mysql-connector-python==9.1.0`: Conector MySQL
- `PyJWT==2.10.1`: Generación y validación de tokens JWT
- `bcrypt==4.2.0`: Hashing de contraseñas
- `python-dotenv==1.0.1`: Carga de variables de entorno

### `Dockerfile`
**Propósito:** Imagen de contenedor para despliegue en Docker.

**Configuración:**
- Base: `python:3.10-slim`
- Puerto expuesto: `8001`
- Working directory: `/app`
- Comando: `uvicorn main:app --host 0.0.0.0 --port 8001`

---

## Archivos de Código

### `main.py`
**Propósito:** Punto de entrada de la aplicación FastAPI y configuración del servidor.

**Componentes principales:**
- **Aplicación:**
  - `app`: Instancia de FastAPI con middleware CORS configurado para `http://localhost:4200`

- **Configuración:**
  - Middleware CORS: Permite todas las credenciales, métodos y encabezados
  - Router: Incluye el router de rutas desde `routes.routes`
  - Servidor: Uvicorn ejecutándose en `0.0.0.0:8001`

**Dependencias:** `fastapi`, `uvicorn`, `routes.routes`
**Integración:** Punto de entrada principal, importa y monta todas las rutas

---

### `routes/routes.py`
**Propósito:** Definición de todos los endpoints HTTP de la API.

**Componentes principales:**
- **Modelos Pydantic:**
  - `User`: Modelo para datos de usuario con campos `username` y `password`

- **Endpoints de Autenticación (sin protección):**
  - `GET /log-in`: Autentica usuario con username y password, retorna JWT token
    - Parámetros: `username: str`, `password: str`
    - Retorna: `{"access_token": token}`
    - Error 401: Usuario no encontrado
  
  - `POST /sing_up`: Registra nuevo usuario y retorna JWT token
    - Body: `User` model (username, password)
    - Retorna: `{"access_token": token}`
    - Error 401: Credenciales inválidas

- **Endpoints de Servicios (protegidos con JWT):**
  - `GET /get-services`: Obtiene servicios habilitados del usuario autenticado
    - Auth: `Depends(credentials_controllers.verify_jws)`
    - Retorna: `{"services": [lista de servicios]}`
  
  - `GET /get-services-available`: Obtiene servicios disponibles (no habilitados) para el usuario
    - Auth: `Depends(credentials_controllers.verify_jws)`
    - Retorna: `{"services": [lista de servicios disponibles]}`
  
  - `GET /add-services`: Habilita un servicio para el usuario
    - Auth: `Depends(credentials_controllers.verify_jws)`
    - Parámetro Query: `service: str`
    - Retorna: `{"services": [lista actualizada]}`
    - Error 401: No es posible añadir el servicio
  
  - `GET /remove-services`: Deshabilita un servicio para el usuario
    - Auth: `Depends(credentials_controllers.verify_jws)`
    - Parámetro Query: `service: str`
    - Retorna: `{"services": [lista actualizada]}`

**Dependencias:** `fastapi`, `controllers`, `credentials_controllers`, `pydantic`
**Integración:** Monta rutas en `main.py`, delega lógica de negocio a `controllers`

---

### `controllers/controllers.py`
**Propósito:** Capa de lógica de negocio que coordina operaciones entre la API y la base de datos.

**Componentes principales:**
- **Funciones de Autenticación:**
  - `check_user(user_name: str, password: str)`: Verifica credenciales contra base de datos
  - `registrer(user_name: str, password: str)`: Registra nuevo usuario, retorna `id_user`
  - `add_token(user_name: str, token: str)`: Guarda token JWT en base de datos

- **Funciones de Servicios:**
  - `get_services(credential: str)`: Obtiene servicios habilitados del usuario
    - Extrae `id_user` del credential, consulta servicios activos
  - `get_services_available(credential: str)`: Obtiene servicios disponibles (no habilitados)
    - Extrae `id_user` del credential, consulta servicios inactivos
  - `add_services(credential: str, service: str)`: Habilita un servicio
    - Actualiza campo del servicio a `TRUE` en base de datos
  - `remove_services(credential: str, service: str)`: Deshabilita un servicio
    - Actualiza campo del servicio a `FALSE` en base de datos

**Dependencias:** `mysql_manager`
**Integración:** Usado por `routes.py`, delega operaciones SQL a `mysql_manager.py`

---

### `controllers/mysql_manager.py`
**Propósito:** Capa de acceso a datos MySQL con operaciones CRUD asíncronas.

**Componentes principales:**
- **Conexión:**
  - `db_connect()`: Establece conexión MySQL usando variables de entorno
    - Host, user, password, port (3306), database desde `.env`

- **Operaciones de Usuarios:**
  - `checker_users(user_name: str, password: str)`: Verifica usuario en tabla `users`
    - Query: `SELECT username, password_hash FROM users WHERE username = ? AND password_hash = ?`
    - Retorna: `True` si existe, `False` si no
  
  - `registrer_users(user_name: str, password: str)`: Inserta nuevo usuario
    - Inserta en `users` y crea registro vacío en `services`
    - Retorna: `id_user` del nuevo registro
  
  - `registrer_token(user_name: str, token: str)`: Actualiza token JWT del usuario
    - Query: `UPDATE users SET jwt_token = ? WHERE username = ?`
  
  - `check_user_by_credential(credential: str)`: Obtiene `id_user` por token JWT
    - Query: `SELECT id_user FROM users WHERE jwt_token = ?`

- **Operaciones de Servicios:**
  - `get_user_services(id_user: str)`: Obtiene servicios habilitados (`TRUE`)
    - Query: `SELECT chatbot, pdf, multimedia, excel, ddbb FROM services WHERE user_id = ?`
    - Retorna: Lista de nombres de servicios activos
  - `get_user_services_available(id_user: str)`: Obtiene servicios deshabilitados (`FALSE`)
    - Misma consulta, retorna servicios inactivos
  - `add_user_services(service: str, id_user: str)`: Habilita servicio
    - Query: `UPDATE services SET {service} = TRUE WHERE user_id = {id_user}`
    - **Nota:** Usa interpolación directa (posible SQL injection)
  - `remove_user_services(service: str, id_user: str)`: Deshabilita servicio
    - Query: `UPDATE services SET {service} = FALSE WHERE user_id = {id_user}`

**Dependencias:** `mysql.connector`, `dotenv`
**Integración:** Usado exclusivamente por `controllers.py`

---

### `controllers/credentials_controllers.py`
**Propósito:** Gestión de tokens JWT y hashing de contraseñas.

**Componentes principales:**
- **Configuración:**
  - `SECRET_KEY`: Clave secreta desde `.env` para firmar tokens
  - `ALGORITHM`: Algoritmo de encriptación (HS256)
  - `security`: Instancia de `HTTPBearer` para extraer tokens de headers

- **Funciones de Hashing:**
  - `generar_hash(password: str)`: Genera hash SHA-256 de contraseña
    - **Nota:** Usa SHA-256 simple, no bcrypt (aunque está en requirements)

- **Funciones de Token JWT:**
  - `generate_token(password_hashed: str)`: Crea token JWT
    - Payload: `{"sub": password_hashed, "exp": +1hora, "iat": now}`
    - Firma: HS256 con `SECRET_KEY`
    - Retorna: Token codificado
  
  - `verify_jws(credentials: HTTPAuthorizationCredentials)`: Valida token JWT
    - Extrae token del header `Authorization: Bearer <token>`
    - Decodifica y verifica expiración
    - Retorna: Token (usado como credential)
    - Error 401: Token expirado o inválido
  
  - `get_current_user(credentials: HTTPAuthorizationCredentials)`: Obtiene usuario actual
    - Similar a `verify_jws` pero retorna `payload["sub"]` (password_hashed)

**Dependencias:** `jwt`, `fastapi.security.HTTPBearer`, `hashlib`, `datetime`
**Integración:** Usado por `routes.py` en `Depends()` para proteger endpoints

---

## Esquema de Base de Datos

### Tabla `users`
| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_user` | INT (PK) | Identificador único autoincremental |
| `username` | VARCHAR | Nombre de usuario único |
| `password_hash` | VARCHAR | Hash SHA-256 de la contraseña |
| `jwt_token` | VARCHAR | Token JWT actual del usuario |

### Tabla `services`
| Columna | Tipo | Descripción |
|---------|------|-------------|
| `user_id` | INT (FK) | Referencia a `users.id_user` |
| `chatbot` | BOOLEAN | Servicio chatbot habilitado |
| `pdf` | BOOLEAN | Servicio PDF habilitado |
| `multimedia` | BOOLEAN | Servicio multimedia habilitado |
| `excel` | BOOLEAN | Servicio Excel habilitado |
| `ddbb` | BOOLEAN | Servicio ddbb habilitado |

---

## Flujo de Autenticación

1. **Registro/Login:**
   ```
   Frontend → POST /sing_up o GET /log-in
   → Hash password con SHA-256
   → Verificar/Crear usuario en MySQL
   → Generar JWT token (expiración: 1 hora)
   → Guardar token en users.jwt_token
   → Retornar token al cliente
   ```

2. **Request Protegido:**
   ```
   Frontend → GET /get-services con header "Authorization: Bearer <token>"
   → verify_jws() valida token
   → Extrae credential (token)
   → check_user_by_credential() obtiene id_user
   → get_user_services() consulta MySQL
   → Retorna lista de servicios
   ```

---

## Consideraciones de Seguridad

⚠️ **Vulnerabilidades detectadas:**

1. **SQL Injection** en `mysql_manager.py`:
   - `add_user_services()` y `remove_user_services()` usan interpolación directa de strings en queries
   - **Recomendación:** Usar placeholders `?` y validar que `service` esté en lista blanca: `['chatbot', 'pdf', 'multimedia', 'excel', 'ddbb']`

2. **Hashing de Contraseñas:**
   - Usa SHA-256 simple en lugar de bcrypt
   - **Recomendación:** Implementar bcrypt con salt (ya está en requirements)

3. **JWT con password_hashed como subject:**
   - El token usa `password_hashed` como `sub` en lugar de `id_user` o `username`
   - **Recomendación:** Usar identificador de usuario no secreto

4. **SECRET_KEY en .env:**
   - La clave secreta está en el repositorio
   - **Recomendación:** Usar variable de entorno en producción, nunca commitar `.env`

---

## Endpoints Resumen

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| GET | `/log-in` | No | Autenticar usuario |
| POST | `/sing_up` | No | Registrar nuevo usuario |
| GET | `/get-services` | JWT | Obtener servicios habilitados |
| GET | `/get-services-available` | JWT | Obtener servicios disponibles |
| GET | `/add-services?service=X` | JWT | Habilitar servicio |
| GET | `/remove-services?service=X` | JWT | Deshabilitar servicio |

**Nota:** Los endpoints `add-services` y `remove-services` usan método `GET` en lugar de `POST`, lo cual es anti-pattern para operaciones que modifican estado.
