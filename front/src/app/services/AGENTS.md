# Servicios de la Aplicación RAG

## Introducción

Este directorio contiene los servicios que gestionan la comunicación con el backend de la aplicación RAG. Cada servicio implementa un patrún híbrido que combina **peticiones REST** (para operaciones síncronas) y **WebSockets** (para streaming en tiempo real de respuestas generadas por IA).

**Patrón de diseño:**
- Todos los servicios utilizan WebSockets para consultas que requieren generación de texto por parte del modelo de IA
- El marcador `__END__` indica el final de una transmisión WebSocket
- Las respuestas se procesan y emiten a través de RxJS Observables para integración reactiva con los componentes

## Archivos

### auth.service.ts
**Propósito:** Gestión de autenticación de usuarios
**Funcionalidades:**
- Login y logout
- Validación de credenciales
- Almacenamiento y recuperación de tokens JWT en localStorage
- Verificación de sesión activa

### ddbb.service.ts
**Propósito:** Interacción con bases de datos para RAG (Retrieval Augmented Generation)
**Funcionalidades:**
- Configuración de conexiones a bases de datos (MySQL, PostgreSQL, etc.)
- Ejecución de consultas SQL con contexto semántico
- Streaming de resultados mediante WebSocket
- Gestión de esquemas y tablas

### excel.service.ts
**Propósito:** Procesamiento y análisis de archivos Excel
**Funcionalidades:**
- Upload de archivos .xlsx, .xlsm, .csv
- Parsing y extracción de datos de hojas de cálculo
- Consultas naturales sobre datos de Excel
- Streaming de respuestas generadas por IA

### models.service.ts
**Propósito:** Gestión de modelos de IA disponibles
**Funcionalidades:**
- Listado de modelos configurados en el backend
- Selección del modelo activo para consultas
- Recuperación de metadatos de modelos (nombre, descripción, capacidades)

### collections.service.ts
**Propósito:** Gestión de colecciones de documentos PDF
**Funcionalidades:**
- Listado de colecciones de documentos
- Asociación de documentos PDF por temas/proyectos
- Búsqueda y recuperación por colección
- Metadata de colecciones

### multimedia.service.ts
**Propósito:** Service for video management and multimedia RAG
**Base URL:** http://localhost:8006
**WebSocket URL:** ws://localhost:8006
**Funcionalidades:**
- Listado y gestión de conversaciones multimedia
- Upload de archivos de video (multipart/form-data)
- Obtención y eliminación de videos
- Creación y eliminación de conversaciones
- Streaming de respuestas mediante WebSocket con marcador __END__
**Métodos:**
- `listConversations()`: GET /api/conversations - returns list of conversations
- `uploadVideo(file: File, metadata?: string)`: POST /api/upload - upload video with multipart/form-data
- `getVideo(fileId: string)`: GET /api/media/{file_id} - returns video URL
- `deleteVideo(fileId: string)`: DELETE /api/media/{file_id}
- `getConversation(conversationId: string)`: GET /api/conversations/{id}
- `createConversation(name: string)`: POST /api/conversations - create a new conversation
- `deleteConversation(conversationId: string)`: DELETE /api/conversations/{id}
- `sendMessage(conversationId: string, message: string, onMessage: (data: any) => void)`: WebSocket streaming
**Autenticación:** JWT via getHeaders() - `Authorization: Bearer ${localStorage.getItem('access_token')}`
**Uso:**
```typescript
constructor(private multimediaService: MultimediaService) {}

// List conversations
this.multimediaService.listConversations().subscribe({
  next: (data) => {
    this.conversations = data.conversations || [];
  }
});

// Upload video
this.multimediaService.uploadVideo(file).subscribe({
  next: (response) => {
    this.videoUrl = response.url;
  }
});

// Send message with streaming
this.multimediaService.sendMessage(conversationId, message, (data) => {
  this.handleMultimediaMessage(data);
}).subscribe({
  next: (data) => {},
  complete: () => {
    this.isSending = false;
  }
});
```

## Integración

Estos servicios son consumidos por:
- **Componentes:** `sidebar-ddbb-item`, `sidebar-excel-item`, `sidebar-pdf-item`, `models-list`
- **Pantallas:** `rag_ddbb`, `excels`, `rag_pdf`, `chatbot`
- **Interceptors:** `auth.interceptor.ts` (inyecta tokens en peticiones HTTP)
