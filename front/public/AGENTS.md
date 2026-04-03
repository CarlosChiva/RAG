# Assets Estáticos

## Resumen Ejecutivo

Directorio `public/` contiene los archivos estáticos que se copian directamente al output de compilación sin procesamiento. Estos assets son accesibles desde la raíz del servidor y se utilizan principalmente para iconos y favicon de la aplicación.

---

## Inventario de Directorios

### Directorios

- **`icons/`**: Iconos utilizados en la interfaz de usuario (PDF, Excel, base de datos, chat, etc.).

---

## Archivos en este Nivel

*No hay archivos en este nivel. Todos los assets están organizados en subdirectorios.*

---

## Estructura

```
public/
└── icons/     # Iconos para la UI
```

---

## Configuración en Angular

En `angular.json`, este directorio se configura como asset:

```json
"assets": [
  {
    "glob": "**/*",
    "input": "public"
  }
]
```

Esto significa que:
- Todos los archivos en `public/` se copian recursivamente a `dist/login-app/`
- Son accesibles desde la raíz del servidor (ej: `/icons/nombre.png`)
- No pasan por el bundler (se copian tal cual)

---

## Uso en la Aplicación

Los iconos se referencian en los componentes con rutas relativas:

```html
<!-- Ejemplo en un componente -->
<img src="/icons/pdf-icon.png" alt="PDF">
<!-- o -->
<img src="./icons/pdf-icon.png" alt="PDF">
```

**Nota:** En producción, ambos formatos funcionan porque los assets están en la raíz del despliegue.

---

## Referencias

- **Configuración de assets:** `../angular.json` (sección `architect.build.options.assets`)
- **Documentación del proyecto:** `../AGENTS.md`
