# Guards de Autenticación

## Introducción

Este directorio contiene los guards de Angular que protegen las rutas de la aplicación, asegurando que solo los usuarios autenticados puedan acceder a las pantallas principales del sistema RAG.

**Patrón de diseño:**
- Implementación del patrón CanActivate de Angular
- Verificación de tokens en localStorage antes de permitir navegación
- Redirección automática a login si la autenticación falla

## Archivos

### auth.guard.ts
**Propósito:** Guard de rutas que verifica autenticación de usuario
**Funcionalidades:**
- Intercepta intentos de navegación a rutas protegidas
- Verifica la existencia y validez del token JWT en localStorage
- Redirige a `/login` si el usuario no está autenticado
- Permite el acceso si la autenticación es exitosa

**Lógica de operación:**
1. Se ejecuta antes de cargar cualquier ruta protegida
2. Consulta localStorage para obtener el token de sesión
3. Si el token existe y es válido → permite la navegación
4. Si el token no existe o es inválido → redirige a login

**Rutas protegidas:**
- `/menu` - Pantalla de menú principal
- `/rag-pdf` - RAG con documentos PDF
- `/rag-ddbb` - RAG con bases de datos
- `/chatbot` - Chatbot general
- `/excels` - RAG con Excel

**Rutas públicas:**
- `/login` - Pantalla de login (no requiere autenticación)

## Integración

Este guard es configurado en:
- `app.routes.ts` - Asociado a rutas que requieren autenticación
- Funciona en conjunto con `auth.interceptor.ts` para protección completa de la aplicación
