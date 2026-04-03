# Componentes de la Aplicación RAG

## Resumen Ejecutivo

Este directorio contiene 18 componentes reutilizables que constituyen los blocs de construcción de la interfaz de usuario de la aplicación RAG. Los componentes siguen el patrón **Standalone** de Angular 19, eliminando la necesidad de NgModules y facilitando la modularidad.

**Arquitectura general:**
- **Componentes de entrada:** Capturan interacciones del usuario (textos, archivos, configuraciones)
- **Componentes de salida:** Presentan resultados generados por la IA (texto, tablas, imágenes)
- **Componentes de navegación:** Sidebar especializados por tipo de recurso (PDF, Excel, Base de Datos)
- **Componentes de configuración:** Formularios para configurar conexiones y herramientas

## Inventario de Subdirectorios

### Componentes de Interacción de Chat
- [chatbot-interaction](./chatbot-interaction/AGENTS.md) - Contenedor principal que gestiona el estado completo de la interacción de chat
- [user-input](./user-input/AGENTS.md) - Área de texto multilínea para entrada del usuario
- [chat-output](./chat-output/AGENTS.md) - Renderizado de respuestas con streaming en tiempo real
- [chat-output-chatbot](./chat-output-chatbot/AGENTS.md) - Variante optimizada para chatbot general con soporte de herramientas

### Componentes de Navegación (Sidebar)
- [sidebar](./sidebar/AGENTS.md) - Barra lateral principal con navegación entre secciones
- [sidebar-pdf-item](./sidebar-pdf-item/AGENTS.md) - Lista de documentos PDF cargados
- [sidebar-ddbb-item](./sidebar-ddbb-item/AGENTS.md) - Lista de tablas disponibles en la base de datos seleccionada
- [sidebar-excel-item](./sidebar-excel-item/AGENTS.md) - Lista de hojas disponibles en el archivo Excel cargado
- [sidebar-conversations-item](./sidebar-conversations-item/AGENTS.md) - Lista de conversaciones guardadas para recuperar sesiones anteriores

### Componentes de Carga de Archivos
- [upload_pdf](./upload_pdf/AGENTS.md) - Upload de documentos PDF individuales o múltiples
- [excel-uploader](./excel-uploader/AGENTS.md) - Upload de archivos Excel con validación de formato
- [upload_comfy_conf](./upload_comfy_conf/AGENTS.md) - Configuración de conexión a ComfyUI para generación de imágenes
- [upload_mcp_conf](./upload_mcp_conf/AGENTS.md) - Configuración de herramientas MCP (Model Context Protocol)

### Componentes de Configuración
- [ddbb_conf](./ddbb_conf/AGENTS.md) - Formulario de configuración de conexión a base de datos
- [models-list](./models-list/AGENTS.md) - Selector de modelos de IA disponibles

### Componentes de Presentación
- [tabla](./tabla/AGENTS.md) - Renderizado de datos tabulares con encabezados dinámicos
- [button-container](./button-container/AGENTS.md) - Contenedor de botones de acción (enviar, limpiar, guardar)

## Archivos a Nivel de Directorio

No hay archivos TypeScript adicionales a este nivel. Todos los componentes están encapsulados en sus respectivos subdirectorios siguiendo la estructura:
```
component-name/
├── component-name.component.ts
├── component-name.component.html
├── component-name.component.css
└── AGENTS.md
```

## Patrones de Diseño Identificados

1. **Base Class Pattern:** `chatbot-interaction` utiliza `chatbot-interaction-base.ts` para compartir lógica de estado entre variantes
2. **WebSocket Streaming:** Componentes de output manejan streaming en tiempo real con el marcador `__END__`
3. **EventEmitter para comunicación:** Padres-hijos se comunican mediante eventos de Angular
4. **Inputs tipados:** Todos los componentes reciben datos mediante `@Input()` con tipado estricto

## Integración

Estos componentes son utilizados por:
- **Pantallas:** Las 6 pantallas de la aplicación combinan múltiples componentes
- **Servicios:** Los componentes consumen servicios para operaciones de negocio
- **Interfaces:** Los componentes importan interfaces para tipado de datos
