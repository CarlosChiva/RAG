# API de gestión de colecciones y documentos
==========================

## Resumen

La presente API está diseñada para gestionar colecciones y documentos en una base de datos. Ofrece rutas para agregar nuevos documentos a una colección, consultar la lista de colecciones existentes y obtener el nombre de la colección actual.

### Rutas principales

#### **GET /llm-response**
------------------------

*   Obtiene un resultado desde un modelo de lenguaje de aprendizaje (LLM) con la pregunta especificada.
*   Requiere que se especifique una pregunta en la URL.
*   Si la pregunta tiene errores, devuelve un código de estado 400.

#### **POST /add_document**
-------------------------

*   Agrega un nuevo documento a una colección existente.
*   Requiere que se especifique el nombre de la colección y un archivo PDF.
*   Si no hay errores, devuelve el identificador del documento agregado.
*   Si hay errores al agregar el documento, devuelve un código de estado 500.

#### **GET /collections**
----------------------

*   Obtiene una lista de nombres de colecciones existentes.
*   Devuelve la lista de nombres de colecciones.

### Rutas de colección

#### **GET /self-collection-name**
----------------------------------

*   Obtiene el nombre de la colección actual.

#### **POST /new-collection-name**
-------------------------------

*   Establece un nuevo nombre para la colección.
*   Requiere que se especifique un nuevo nombre para la colección.
*   Si hay errores al establecer el nuevo nombre, devuelve un código de estado 500.