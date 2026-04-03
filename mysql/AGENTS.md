# Módulo de Base de Datos MySQL

Esta carpeta contiene la configuración inicial y el esquema de base de datos para el servicio MySQL del proyecto RAG.

## Archivos

### `.env`
**Propósito:** Variables de entorno para la configuración del contenedor MySQL.

**Variables configuradas:**
- `MYSQL_ROOT_PASSWORD=rootpassword`: Contraseña del usuario root de MySQL.
- `MYSQL_DATABASE=app_db`: Nombre de la base de datos que se crea automáticamente.
- `MYSQL_USER=app_user`: Usuario de aplicación con permisos limitados.
- `MYSQL_PASSWORD=app_password`: Contraseña del usuario de aplicación.

**Uso:** Este archivo es referenciado por el contenedor MySQL durante el inicio para configurar credenciales y base de datos inicial.

---

### `init.sql`
**Propósito:** Script de inicialización que define el esquema de base de datos y las tablas principales.

**Estructura creada:**

**Tabla `users`:**
- `id_user` (INT, AUTO_INCREMENT, PRIMARY KEY): Identificador único de usuario.
- `username` (VARCHAR(255), UNIQUE, NOT NULL): Nombre de usuario único.
- `password_hash` (VARCHAR(255), NOT NULL): Hash de contraseña del usuario.
- `jwt_token` (VARCHAR(255), DEFAULT NULL): Token JWT activo del usuario (para sesiones).

**Tabla `services`:**
- `id_service` (INT, AUTO_INCREMENT, PRIMARY KEY): Identificador único de servicio.
- `user_id` (INT, NOT NULL): Clave foránea que referencia `users.id_user`.
- `chatbot` (BOOLEAN, DEFAULT TRUE): Flag de servicio de chatbot habilitado por defecto.
- `pdf` (BOOLEAN, DEFAULT FALSE): Flag de servicio de procesamiento PDF.
- `multimedia` (BOOLEAN, DEFAULT FALSE): Flag de servicio multimedia.
- `excel` (BOOLEAN, DEFAULT FALSE): Flag de servicio de procesamiento Excel.
- `ddbb` (BOOLEAN, DEFAULT FALSE): Flag de servicio de bases de datos.

**Relaciones:**
- `services.user_id` → `users.id_user` con `ON DELETE CASCADE` (elimina servicios al borrar usuario).

**Dependencias:** Requiere MySQL 5.7+ para soporte de BOOLEAN y AUTO_INCREMENT.

**Integración:** Este script se ejecuta automáticamente al iniciar el contenedor MySQL mediante el volumen `docker-entrypoint-initdb.d`.

## Resumen

Este módulo proporciona la infraestructura de persistencia para:
1. Gestión de usuarios y autenticación (tabla `users`).
2. Control de servicios habilitados por usuario (tabla `services`).
