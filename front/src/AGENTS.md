# Fuente de la Aplicación Angular

## Resumen Ejecutivo

Directorio `src/` contiene todo el código fuente compilable de la aplicación Angular. Incluye el punto de entrada (`main.ts`), la plantilla HTML principal (`index.html`), estilos globales (`styles.scss`) y el directorio `app/` con toda la lógica de negocio, componentes y servicios.

---

## Inventario de Directorios

### Directorios

- **`app/`**: Directorio principal de la aplicación con componentes, servicios, pantallas, rutas, interfaces, guards e interceptores.  
  → [Ver documentación detallada](./app/AGENTS.md)

---

## Archivos en este Nivel

### main.ts
**Propósito:** Punto de entrada de la aplicación Angular.

**Funcionalidad:**
- Importa `bootstrapApplication` de `@angular/platform-browser`
- Importa `appConfig` desde `app/app.config` (configuración del router, HTTP, animaciones)
- Importa `AppComponent` (componente raíz)
- Ejecuta `bootstrapApplication(AppComponent, appConfig)` para iniciar la aplicación
- Manejo de errores básico con `console.error`

**Código:**
```typescript
bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
```

**Dependencias:**
- `@angular/platform-browser`
- `./app/app.config`
- `./app/app.component`

### index.html
**Propósito:** Plantilla HTML principal que sirve como contenedor de la aplicación.

**Estructura:**
- `<!doctype html>`: HTML5
- `<html lang="en">`: Idioma inglés
- `<head>`:
  - Charset UTF-8
  - Title: "RAGApp"
  - Base href: `/`
  - Meta viewport para responsive design
  - Link a favicon.ico
- `<body>`:
  - `<app-root></app-root>`: Selector del AppComponent

**Notas:**
- Angular reemplaza `<app-root>` con el template compilado de AppComponent
- El archivo es minimalista; toda la UI se genera dinámicamente

### styles.scss
**Propósito:** Estilos globales de la aplicación (SCSS).

**Estilos definidos:**
```scss
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  background: linear-gradient(135deg, #504f4f, #333);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #e0e0e0;
  overflow: hidden;
}

.mat-app-background {
  background: transparent;
}
```

**Características:**
- **Background:** Gradiente oscuro (gris medio a gris oscuro)
- **Tipografía:** Stack de fuentes sans-serif
- **Color:** Texto gris claro para contraste
- **Overflow:** Hidden para evitar scrollbars en elementos que llenan la pantalla
- **Altura:** 100% para layout full-height
- **Compatibilidad:** `.mat-app-background` para Angular Material (aunque no se usa en este proyecto)

**Uso:** Importado en `angular.json` como estilo global para toda la aplicación.

---

## Estructura

```
src/
├── app/               # Aplicación Angular completa
│   ├── components/    # 18 componentes reutilizables
│   ├── screens/       # 6 pantallas principales
│   ├── services/      # 5 servicios de backend
│   ├── interfaces/    # 6 interfaces TypeScript
│   ├── guards/        # 1 guard de autenticación
│   ├── interceptors/  # 1 interceptor HTTP
│   ├── app.component.ts
│   ├── app.config.ts
│   └── app.routes.ts
├── index.html         # Plantilla HTML principal
├── main.ts            # Punto de entrada
└── styles.scss        # Estilos globales
```

---

## Flujo de Compilación

1. **TypeScript Compiler:** Lee `tsconfig.app.json` → Compila todos los `.ts` en `src/`
2. **Angular Compiler:** Transforma componentes a código JavaScript optimizado (AOT en producción)
3. **SCSS Compiler:** Compila `styles.scss` a CSS
4. **Webpack/Vite:** Bundla todos los assets en `dist/login-app/`
5. **Output:** HTML, JS, CSS listos para servir en producción

---

## Referencias

- **Documentación completa de la app:** [./app/AGENTS.md](./app/AGENTS.md)
- **Configuración de compilación:** `../angular.json`, `../tsconfig.app.json`
- **Punto de entrada:** `main.ts` (este directorio)
