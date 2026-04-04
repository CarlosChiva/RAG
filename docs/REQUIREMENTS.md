# Requirements - Multimedia RAG Feature

## Descripción General
Implementar una nueva API de gestión multimedia (videos) y su correspondiente pantalla en el frontend Angular para el proyecto RAG existente.

---

## Backend - API Multimedia (Nuevo Microservicio)

### Tecnologías
- FastAPI (Python)
- Puerto: **8006**
- MySQL (para verificar servicios habilitados)
- JWT (autenticación con la misma SECRET_KEY que las otras APIs)

### Funcionalidades
1. Almacenamiento y recuperación de archivos **video**
2. Chats/conversaciones guardadas en **JSON** (por usuario)
3. Autenticación con **JWT**
4. **Arquitectura intercambiable**: Implementar una clase abstracta/interface para el almacenamiento de archivos, permitiendo cambiar fácilmente entre:
   - Almacenamiento local (carpeta + volumen Docker) ← **implementación inicial**
   - Almacenamiento en la nube (AWS S3, Google Cloud Storage, etc.) ← **futuro**
5. Carpeta de almacenamiento por usuario/JWT

### Rutas API
- `GET /conversations` - Listar conversaciones del usuario (filtrado por JWT)
- `POST /upload` - Subir archivo video
- `GET /media/{file_id}` - Obtener archivo video
- `DELETE /media/{file_id}` - Eliminar archivo
- `GET /conversations/{id}` - Obtener conversación específica

### Estructura esperada
```
RAG_multimedia/
├── app.py (o main.py) - FastAPI application
├── core/
│   ├── config.py - Configuración (puerto, paths, etc.)
│   ├── security.py - JWT validation
│   └── storage.py - Abstract storage interface + local implementation
├── api/
│   ├── deps.py - Dependencies (get_current_user, etc.)
│   └── routes.py - API endpoints
├── models/
│   └── schemas.py - Pydantic schemas
├── storage/
│   └── videos/ - Carpeta para videos (con docker volume)
└── conversations/ - Carpeta para JSONs de conversaciones
```

---

## Frontend - Angular

### Tecnologías
- Angular **19.2.0** (mantener framework existente)
- TypeScript 5.7.2
- RxJS

### Requerimientos
1. Nueva **screen Multimedia** accesible desde el menú principal
2. Servicio Angular para comunicación con API multimedia (puerto 8006)
3. Interfaz para:
   - Listar conversaciones
   - Subir videos
   - Visualizar videos
4. Integración con el sistema de autenticación JWT existente
5. Mantener consistencia con el diseño y arquitectura actual (standalone components, interceptores, etc.)

### Estructura esperada en front/src/app
```
├── screens/
│   └── multimedia/
│       ├── multimedia.screen.ts
│       ├── multimedia.screen.html
│       └── multimedia.screen.scss
├── services/
│   └── multimedia.service.ts
└── components/ (si se necesitan componentes reutilizables)
    └── video-player/ (opcional)
```

---

## Base de Datos MySQL

### Cambios en esquema
1. Añadir columna **`multimedia`** (booleano) a la tabla `services`
2. Habilitar/deshabilitar por usuario desde la API `ddbb` (puerto 8001)

### SQL necesario
```sql
ALTER TABLE services ADD COLUMN multimedia BOOLEAN DEFAULT FALSE;
```

---

## Docker

### Requerimientos
1. Nuevo contenedor para la API multimedia (puerto 8006)
2. Volumen Docker para carpeta de almacenamiento de videos
3. Integración con la arquitectura Docker existente (docker-compose.yml)

---

## Pasos de Implementación

### Fase 1: Backend - API Multimedia
1. Crear estructura de carpetas del nuevo microservicio `RAG_multimedia`
2. Implementar la clase abstracta de storage con implementación local
3. Crear endpoints de FastAPI
4. Implementar autenticación JWT
5. Crear Dockerfile
6. Actualizar docker-compose.yml

### Fase 2: Base de Datos
1. Crear script SQL para añadir columna `multimedia` a tabla `services`
2. Actualizar API `ddbb` para manejar el nuevo servicio

### Fase 3: Frontend - Angular
1. Crear servicio multimedia.service.ts
2. Crear screen multimedia con componentes
3. Actualizar menú para incluir la nueva pantalla
4. Implementar interfaz de usuario

### Fase 4: Documentación
1. Crear AGENTS.md para el nuevo módulo RAG_multimedia
2. Actualizar AGENTS.md principal del proyecto

---

## Verificación Final

Al finalizar, el sistema debe:
1. ✅ Tener el nuevo microservicio corriendo en puerto 8006
2. ✅ Poder autenticarse con JWT existente
3. ✅ Subir videos y guardarlos en carpeta local
4. ✅ Listar conversaciones por usuario
5. ✅ Recuperar y visualizar videos
6. ✅ Tener la pantalla en el frontend accesible desde el menú
7. ✅ Estar documentado en AGENTS.md
