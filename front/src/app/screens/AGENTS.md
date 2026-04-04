# Pantallas de la Aplicación RAG

## Resumen Ejecutivo

Este directorio contiene las 6 pantallas principales de la aplicación RAG. Cada pantalla representa una vista completa de la aplicación que combina múltiples componentes para ofrecer funcionalidades específicas. Las pantallas siguen el patrón **Standalone** de Angular 19.

**Flujo de la aplicación:**
1. **Login** (pública) → Autenticación del usuario
2. **Menu** (protegida) → Selección de funcionalidad
3. **RAG PDF / RAG DDBB / Chatbot / Excels** (protegidas) → Ejecución de la funcionalidad seleccionada

## Inventario de Subdirectorios

### Pantallas de Autenticación y Navegación
- [login](./login/AGENTS.md) - Pantalla de login con formulario de credenciales y validación
- [menu](./menu/AGENTS.md) - Pantalla de menú principal con tarjetas de navegación a las 4 funcionalidades

### Pantallas de RAG por Tipo de Fuente
- [rag_pdf](./rag_pdf/AGENTS.md) - RAG con documentos PDF (upload, selección de documentos, chat)
- [rag_ddbb](./rag_ddbb/AGENTS.md) - RAG con bases de datos (configuración de conexión, exploración de tablas, chat)
- [excels](./excels/AGENTS.md) - RAG con archivos Excel (upload, selección de hojas, chat)

### Pantalla de Chatbot General
- [chatbot](./chatbot/AGENTS.md) - Chatbot general con soporte de herramientas (ComfyUI, MCP) y generación de imágenes

### Pantalla de Multimedia
- [multimedia](./multimedia/AGENTS.md) - Video management and RAG interaction screen (upload, playback, conversation management, chat)

## Archivos a Nivel de Directorio

No hay archivos TypeScript adicionales a este nivel. Todas las pantallas están encapsuladas en sus respectivos subdirectorios siguiendo la estructura:
```
screen-name/
├── screen-name.component.ts
├── screen-name.component.html
�├── screen-name.component.css
└── AGENTS.md
```

## Patrones de Diseño Identificados

1. **Composición de componentes:** Cada pantalla combina 3-8 componentes reutilizables
2. **Gestión de estado local:** Las pantallas mantienen el estado de la interacción (conversaciones, configuraciones, selecciones)
3. **Integración con servicios:** Cada pantalla consume 1-3 servicios según su funcionalidad
4. **Protección de rutas:** 5 de 6 pantallas requieren autenticación (excepto login)

## Características Comunes

Todas las pantallas de RAG (rag_pdf, rag_ddbb, excels, chatbot) comparten:
- **Layout similar:** Sidebar izquierda + área principal de chat
- **Componente chatbot-interaction:** Motor central de interacción con la IA
- **Gestión de conversaciones:** Capacidad de guardar, cargar y listar conversaciones anteriores
- **Streaming en tiempo real:** Recepción de respuestas mediante WebSocket

## Integración

Estas pantallas están configuradas en:
- `app.routes.ts` - Definición de rutas y asociación con componentes
- Protegidas por `auth.guard.ts` (excepto login)
- Consumen componentes del directorio `components/`
- Utilizan servicios del directorio `services/`
