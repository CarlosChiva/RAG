# Interceptors de HTTP

## Introducción

Este directorio contiene los interceptores de HTTP de Angular que interceptan y modifican peticiones HTTP salientes y respuestas entrantes. Actualmente implementa la inyección automática de tokens de autenticación.

**Patrón de diseño:**
- Implementación del patrón HttpInterceptor de Angular
- Middleware de peticiones HTTP usando RxJS Observables
- Inyección de cabeceras de autenticación transparente para el resto de la aplicación

## Archivos

### auth.interceptor.ts
**Propósito:** Interceptor que añade tokens JWT a todas las peticiones HTTP
**Funcionalidades:**
- Intercepta todas las peticiones HTTP realizadas por la aplicación
- Recupera el token JWT almacenado en localStorage
- Añade el header `Authorization: Bearer <token>` a cada petición
- Permite el flujo de la petición modificada al backend

**Lógica de operación:**
1. Se registra en `app.config.ts` como provider de HTTP interceptores
2. Cada petición HTTP pasa por este interceptor antes de ser enviada
3. El interceptor lee el token de localStorage
4. Si existe token → añade header Authorization
5. Si no existe token → envía petición sin header (para endpoints públicos como login)
6. La petición continúa hacia el backend

**Endpoints que requieren autenticación:**
- `/api/ddbb/*` - Operaciones con bases de datos
- `/api/excel/*` - Operaciones con Excel
- `/api/pdf/*` - Operaciones con PDF
- `/api/collections/*` - Gestión de colecciones
- `/api/models/*` - Listado de modelos

**Endpoints públicos:**
- `/api/auth/login` - Login (no requiere token previo)

## Integración

Este interceptor está configurado en:
- `app.config.ts` - Registrado como provider usando `provideHttpClient` con interceptores
- Funciona en conjunto con `auth.guard.ts` para protección completa (rutas + peticiones)
- Es utilizado automáticamente por todos los servicios que usan `HttpClient`
