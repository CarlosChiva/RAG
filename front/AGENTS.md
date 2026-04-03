# Frontend RAG - Aplicación Angular

## Resumen Ejecutivo

Frontend de la aplicación **Retrieval Augmented Generation (RAG)** construido con Angular 19.2.0. Permite a los usuarios interactuar con diferentes fuentes de datos (PDFs, bases de datos, Excel) mediante lenguaje natural, además de un chatbot general con integración de herramientas externas (ComfyUI, MCP).

**Arquitectura:** Aplicación standalone sin NgModules, con 6 pantallas, 18 componentes reutilizables, 5 servicios, autenticación JWT y comunicación híbrida HTTP/WebSocket.

---

## Inventario de Directorios

### Directorios Principales

- **`src/`**: Código fuente de la aplicación Angular.  
  → [Ver documentación detallada](./src/AGENTS.md)

- **`public/`**: Assets estáticos (iconos, favicon).  
  → [Ver documentación detallada](./public/AGENTS.md)

- **`.vscode/`**: Configuración del entorno de desarrollo Visual Studio Code.

---

## Archivos de Configuración en Raíz

### package.json
**Propósito:** Definición de dependencias y scripts del proyecto Node.js/Angular.

**Dependencias principales:**
- `@angular/core`, `@angular/common`, `@angular/router`: Framework Angular 19.2.0
- `@angular/forms`: Módulo de formularios reactivos y templates
- `marked`: Parser Markdown para renderizar respuestas del chatbot
- `prismjs`: Sintax highlighter para código en respuestas
- `rxjs`: Librería de Observables para programación reactiva

**Scripts configurados:**
- `ng serve`: Inicia servidor de desarrollo en `0.0.0.0:4200`
- `ng build`: Compila la aplicación para producción
- `ng test`: Ejecuta suite de tests con Karma/Jasmine

### angular.json
**Propósito:** Configuración centralizada del CLI de Angular.

**Configuraciones clave:**
- **Project name:** `login-app`
- **Style language:** SCSS
- **Output path:** `dist/login-app`
- **Entry point:** `src/main.ts`
- **Build optimizer:** Habilitado en producción, deshabilitado en desarrollo
- **Source maps:** Habilitados en configuración de desarrollo
- **Budgets:** Máximo 500KB inicial (warning), 1MB (error)

### Dockerfile
**Propósito:** Definición de contenedor Docker para despliegue del frontend.

**Configuración:**
- **Imagen base:** `node:18-alpine`
- **Working directory:** `/app`
- **Puerto expuesto:** `4200`
- **Comando de inicio:** `npm start -- --host 0.0.0.0 --disable-host-check`

**Uso:**
```bash
# Construir imagen
docker build -t rag-frontend .

# Ejecutar contenedor
docker run -p 4200:4200 rag-frontend
```

### tsconfig.json
**Propósito:** Configuración global del compilador TypeScript.

**Ajustes principales:**
- **target:** ES2022
- **module:** ES2022
- **strict:** true (todos los checks estrictos habilitados)
- **esModuleInterop:** true (compatibilidad con módulos CommonJS)
- **skipLibCheck:** true (salta verificación de librerías)

### tsconfig.app.json
**Propósito:** Configuración TypeScript específica para compilación de la aplicación.

**Extiende:** `tsconfig.json`
**Archivos incluidos:** `src/main.ts` y todos los `.ts` en `src/`

### tsconfig.spec.json
**Propósito:** Configuración TypeScript para tests unitarios.

**Extiende:** `tsconfig.json`
**Librerías añadidas:** Jasmine para testing

### .gitignore
**Propósito:** Excluir archivos del control de versiones Git.

**Exclusiones principales:**
- `node_modules/`: Dependencias instaladas
- `dist/`: Archivos compilados
- `.angular/`: Cache de Angular
- `*.log`: Archivos de logs

### .editorconfig
**Propósito:** Estándares de formato de código consistentes entre editores.

**Configuración:**
- **Indentación:** Espacios, 2 por nivel
- **Final de línea:** LF (Unix)
- **Encoding:** UTF-8

---

## Estructura del Proyecto

```
front/
├── src/                    # Código fuente de la aplicación
│   ├── app/               # Componentes, servicios, rutas, pantallas
│   ├── index.html         # Plantilla HTML principal
│   ├── main.ts            # Punto de entrada de la aplicación
│   └── styles.scss        # Estilos globales
├── public/                # Assets estáticos
│   └── icons/             # Iconos utilizados en la UI
├── .vscode/               # Configuración VS Code
├── angular.json           # Configuración Angular CLI
├── package.json           # Dependencias y scripts
├── tsconfig.json          # Configuración TypeScript base
├── tsconfig.app.json      # Config TS para app
├── tsconfig.spec.json     # Config TS para tests
├── Dockerfile             # Definición de contenedor
├── .gitignore            # Exclusiones Git
└── .editorconfig         # Estándares de formato
```

---

## Flujo de Ejecución

### 1. Inicio de la Aplicación
```
index.html → main.ts → bootstrapApplication(AppComponent, appConfig)
```

### 2. Configuración de la Aplicación
`app.config.ts` define:
- Router con las rutas de `app.routes.ts`
- HTTP Client con interceptores
- Animaciones de Angular

### 3. Navegación Inicial
- Router carga ruta por defecto (`**`) → Redirección a `/login`
- `auth.guard.ts` verifica token en localStorage
- Si no hay token → muestra `LoginComponent`
- Si hay token válido → redirige a `/menu`

### 4. Comunicación con Backend
- **HTTP:** Para autenticación, carga de documentos, listas de modelos
- **WebSocket:** Para streaming de respuestas en tiempo real (marcador `__END__`)
- **Interceptors:** `auth.interceptor.ts` añade token JWT automáticamente

---

## Patrones de Arquitectura

### Standalone Components
Angular 19 sin NgModules. Cada componente es autónomo y declara sus propias dependencias en el decorador `@Component({ imports: [] })`.

### Service-Oriented Architecture
5 servicios especializados:
- `auth.service.ts`: Autenticación y gestión de sesión
- `collections.service.ts`: Listado de documentos/collections disponibles
- `ddbb.service.ts`: Operaciones con bases de datos
- `excel.service.ts`: Operaciones con archivos Excel
- `models.service.ts`: Listado y selección de modelos AI

### WebSocket Streaming
Las respuestas del backend llegan en chunks mediante WebSocket:
```typescript
ws.onmessage = (event) => {
  const data = event.data;
  if (data.includes('__END__')) {
    // Respuesta completa, cerrar conexión
  } else {
    // Acumular chunk en tiempo real
  }
}
```

### Base Class Pattern
`chatbot-interaction` usa `chatbot-interaction-base.ts` para compartir lógica entre la variante RAG y la variante Chatbot general.

### JWT Authentication Flow
1. Login → Backend retorna JWT
2. JWT guardado en `localStorage.setItem('token', ...)`
3. `auth.interceptor.ts` lee token y añade header `Authorization: Bearer <token>`
4. `auth.guard.ts` verifica presencia de token para rutas protegidas

---

## Estilos Globales

### styles.scss
**Background:** Gradiente lineal 135° (`#504f4f` → `#333`)
**Tipografía:** Segoe UI, Tahoma, Geneva, Verdana, sans-serif
**Color texto:** `#e0e0e0` (gris claro)
**Overflow:** Hidden (evita barras de desplazamiento innecesarias)
**Altura:** 100% en html y body para layout full-height

---

## Cómo Ejecutar el Proyecto

### Desarrollo Local
```bash
cd /home/dread/VsCode/RAG/front
npm install              # Primera vez o después de cambios en package.json
ng serve                 # Inicia en http://localhost:4200
```

### Producción
```bash
ng build --configuration production
# Output en: dist/login-app/
# Desplegar en servidor web (Nginx, Apache, etc.)
```

### Docker
```bash
# Construir imagen
docker build -t rag-frontend .

# Ejecutar
docker run -p 4200:4200 rag-frontend

# Con docker-compose (si existe backend)
docker-compose up -d
```

---

## Documentación Detallada

Para documentación específica de cada módulo del frontend:

- **Aplicación Angular completa:** [./src/app/AGENTS.md](./src/app/AGENTS.md)
- **Componentes UI:** [./src/app/components/AGENTS.md](./src/app/components/AGENTS.md)
- **Pantallas:** [./src/app/screens/AGENTS.md](./src/app/screens/AGENTS.md)
- **Servicios:** [./src/app/services/AGENTS.md](./src/app/services/AGENTS.md)
- **Interfaces:** [./src/app/interfaces/AGENTS.md](./src/app/interfaces/AGENTS.md)
- **Guards:** [./src/app/guards/AGENTS.md](./src/app/guards/AGENTS.md)
- **Interceptors:** [./src/app/interceptors/AGENTS.md](./src/app/interceptors/AGENTS.md)

---

## Consideraciones Técnicas

### Versiones
- **Node.js:** 18.x (LTS)
- **Angular:** 19.2.0
- **TypeScript:** 5.7.2
- **npm:** Compatible con package-lock.json v2

### Presupuesto de Bundle
- **Inicial:** Máximo 500KB (warning), 1MB (error)
- **Componente individual:** Máximo 4kB (warning), 8kB (error)

### Seguridad
- JWT almacenado en localStorage (vulnerable a XSS, considerar httpOnly cookies en producción)
- CORS configurado en backend (el frontend solo consume APIs)
- Rutas protegidas con guard de autenticación

### Performance
- Standalone components reducen bundle size
- Lazy loading implícito por router de Angular
- WebSocket streaming mejora percepción de velocidad
- Production build con AOT (Ahead-of-Time compilation)
