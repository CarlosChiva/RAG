# Interfaces de la Aplicación RAG

## Introducción

Este directorio contiene las definiciones de TypeScript que establecen el contrato de datos entre el frontend y el backend. Todas las interfaces representan estructuras de datos utilizadas en la comunicación con los servicios y en el estado local de la aplicación.

**Patrón de diseño:**
- Las interfaces siguen la convención de nomenclatura del backend (snake_case para campos)
- Se utilizan tipos primitivos de TypeScript (string, number, boolean, arrays, objects)
- Las propiedades son mayoritariamente requeridas para garantizar integridad de datos

## Archivos

### chat-message.ts
**Propósito:** Definición de mensajes en conversaciones de chat
**Campos principales:**
- `id`: Identificador único del mensaje
- `role`: Rol del emisor ('user' | 'assistant')
- `content`: Contenido textual del mensaje
- `timestamp`: Fecha/hora de creación
- `metadata`: Datos adicionales opcionales

### config.interface.ts
**Propósito:** Configuraciones de conexión y parámetros para diferentes tipos de RAG
**Campos principales:**
- Configuraciones de bases de datos (host, puerto, credenciales)
- Configuraciones de ComfyUI para generación de imágenes
- Configuraciones de MCP (Model Context Protocol) para herramientas externas

### conversations.interface.ts
**Propósito:** Estructura de conversaciones completas y su persistencia
**Campos principales:**
- `id`: Identificador único de la conversación
- `title`: Título descriptivo de la conversación
- `messages`: Array de mensajes (tipo ChatMessage)
- `createdAt`: Fecha de creación
- `updatedAt`: Fecha de última modificación
- `type`: Tipo de conversación ('pdf', 'ddbb', 'excel', 'chatbot')

### db-conf.interface.ts
**Propósito:** Configuración específica de conexiones a bases de datos
**Campos principales:**
- `name`: Nombre de la configuración guardada
- `type`: Tipo de base de datos (mysql, postgresql, sqlite, etc.)
- `host`: Host del servidor de base de datos
- `port`: Puerto de conexión
- `database`: Nombre de la base de datos
- `user`/`password`: Credenciales de acceso

### messages.interface.ts
**Propósito:** Estructura de mensajes para diferentes contextos de comunicación
**Campos principales:**
- Variantes de mensajes para diferentes tipos de RAG
- Mensajes con resultados de consultas SQL
- Mensajes con datos de Excel
- Mensajes con información de documentos PDF

### models.interface.ts
**Propósito:** Definición de modelos de IA disponibles en el sistema
**Campos principales:**
- `id`: Identificador único del modelo
- `name`: Nombre del modelo
- `description`: Descripción de capacidades
- `type`: Tipo de modelo (llm, image-generation, etc.)
- `isActive`: Estado de activación

## Integración

Estas interfaces son utilizadas por:
- **Servicios:** Todos los servicios importan las interfaces relevantes para tipar respuestas y peticiones
- **Componentes:** Componentes de UI utilizan interfaces para tipar datos mostrados
- **Pantallas:** Las pantallas importan múltiples interfaces para gestionar estado complejo
