# Aplicación RAG - Frontend

## Resumen Ejecutivo

Aplicación web frontend para un sistema de **Retrieval Augmented Generation (RAG)** que permite interactuar con diferentes fuentes de datos (PDFs, bases de datos, Excel) mediante lenguaje natural utilizando modelos de IA. La aplicación también incluye un chatbot general con capacidad de integrar herramientas externas (ComfyUI para generación de imágenes, MCP para herramientas personalizadas).

**Tecnologías principales:**
- **Framework:** Angular 19.2.0 (standalone components)
- **Lenguaje:** TypeScript
- **Comunicación:** HTTP REST + WebSockets para streaming en tiempo real
- **Autenticación:** JWT con localStorage
- **Arquitectura:** 6 pantallas, 18 componentes reutilizables, 5 servicios, 6 interfaces

## Inventario de Directorios

### Directorios Principales

- [components](./components/AGENTS.md) - 18 componentes reutilizables de UI (entrada, salida, navegación, configuración)
- [screens](./screens/AGENTS.md) - 6 pantallas principales (login, menu, rag_pdf, rag_ddbb, chatbot, excels)
- [services](./services/AGENTS.md) - 5 servicios de comunicación con backend (auth, ddbb, excel, models, collections)
- [interfaces](./interfaces/AGENTS.md) - 6 interfaces TypeScript que definen el contrato de datos
- [guards](./guards/AGENTS.md) - Guard de autenticación para protección de rutas
- [interceptors](./interceptors/AGENTS.md) - Interceptor HTTP para inyección automática de tokens

### Archivos de Configuración de la Aplicación

#### app.component.ts
**Propósito:** Componente raíz de la aplicación
**Funcionalidad:** Contenedor principal que utiliza `<router-outlet>` para renderizar las pantallas según la ruta actual. Componente minimalista que no contiene lógica de negocio.

#### app.config.ts
**Propósito:** Configuración centralizada de la aplicación Angular
**Funcionalidad:**
- Define providers de la aplicación usando `provideRouter` (rutas)
- Configura `provideHttpClient` con interceptores para HTTP
- Establece `provideAnimations` para animaciones de Angular
- Punto de entrada para configuración de servicios globales

#### app.routes.ts
**Propósito:** Definición de rutas de navegación de la aplicación
**Rutas configuradas:**
- `/login` → LoginComponent (pública)
- `/menu` → MenuComponent (protegida)
- `/rag-pdf` → RagPdfComponent (protegida)
- `/rag-ddbb` → RagDdbbComponent (protegida)
- `/chatbot` → ChatbotComponent (protegida)
- `/excels` → ExcelsComponent (protegida)
- `**` → Redirección a `/login` (ruta por defecto)

**Protección:** Las rutas protegidas utilizan `auth.guard.ts` mediante el guard `CanActivate`

## Arquitectura de la Aplicación

### Flujo de Autenticación
1. Usuario accede a la aplicación → Redirección a `/login`
2. Usuario ingresa credenciales → `auth.service.ts` valida con backend
3. Backend retorna JWT → Se almacena en localStorage
4. `auth.guard.ts` permite acceso → Redirección a `/menu`
5. Todas las peticiones HTTP → `auth.interceptor.ts` añade header Authorization

### Flujo de RAG (ejemplo con PDF)
1. Usuario navega a `/rag-pdf`
2. Carga PDFs mediante `upload_pdf` component → `excel.service.ts` (o servicio PDF)
3. `collections.service.ts` lista documentos disponibles
4. Usuario selecciona documentos en `sidebar-pdf-item`
5. Usuario escribe consulta en `user-input`
6. `chatbot-interaction` envía consulta + contexto de PDFs al backend
7. Backend procesa con RAG → Responde vía WebSocket
8. `chat-output` renderiza respuesta con streaming en tiempo real
9. Conversación se guarda y aparece en `sidebar-conversations-item`

### Flujo de Chatbot con Herramientas
1. Usuario navega a `/chatbot`
2. Usuario configura ComfyUI en `upload_comfy_conf` (opcional)
3. Usuario configura MCP tools en `upload_mcp_conf` (opcional)
4. Usuario escribe consulta en `user-input-chatbot`
5. `chatbot-interaction` detecta necesidad de herramienta
6. Backend ejecuta herramienta (ej: generar imagen en ComfyUI)
7. Resultado se incluye en respuesta → `chat-output-chatbot` renderiza

## Patrones de Diseño Globales

1. **Standalone Components:** Angular 19 sin NgModules para mayor modularidad
2. **WebSocket Streaming:** Todas las respuestas de IA se transmiten en tiempo real con marcador `__END__`
3. **Base Class Pattern:** `chatbot-interaction` usa clase base para compartir estado entre variantes
4. **JWT Authentication:** Token-based con localStorage + guard + interceptor
5. **Service-oriented:** 5 servicios especializados por dominio (auth, ddbb, excel, models, collections)
6. **TypeScript Interfaces:** Contrato estricto de datos entre frontend y backend

## Estructura de Archivos

```
front/src/app/
├── components/          # 18 componentes reutilizables
│   ├── button-container/
│   ├── chat-output-chatbot/
│   ├── chat-output/
│   ├── chatbot-interaction/
│   ├── ddbb_conf/
│   ├── excel-uploader/
│   ├── models-list/
│   ├── sidebar/
│   ├── sidebar-conversations-item/
│   ├── sidebar-ddbb-item/
│   ├── sidebar-excel-item/
│   ├── sidebar-pdf-item/
│   ├── tabla/
│   ├── upload_comfy_conf/
│   ├── upload_mcp_conf/
│   ├── upload_pdf/
│   ├── user-input-chatbot/
│   └── user-input/
├── screens/            # 6 pantallas principales
│   ├── login/
│   ├── menu/
│   ├── rag_pdf/
│   ├── rag_ddbb/
│   ├── chatbot/
│   └── excels/
├── services/           # 5 servicios de backend
│   ├── auth.service.ts
│   ├── ddbb.service.ts
│   ├── excel.service.ts
│   ├── models.service.ts
│   └── collections.service.ts
├── interfaces/         # 6 interfaces de datos
│   ├── chat-message.ts
│   ├── config.interface.ts
│   ├── conversations.interface.ts
│   ├── db-conf.interface.ts
│   ├── messages.interface.ts
│   └── models.interface.ts
├── guards/             # 1 guard de rutas
│   └── auth.guard.ts
├── interceptors/       # 1 interceptor HTTP
│   └── auth.interceptor.ts
├── app.component.ts    # Componente raíz
├── app.config.ts       # Configuración de la aplicación
└── app.routes.ts       # Definición de rutas
```

## Documentación Completa

Cada directorio y componente cuenta con su propio archivo `AGENTS.md` con documentación detallada. Utilice los enlaces en los inventarios de cada directorio para acceder a la documentación específica.
