# Tabla Component

## Introduction

Table rendering component that converts database query results into HTML tables. Transforms JSON data structure into rows and columns for display in chat responses.

## Files Documentation

### tabla.component.ts

**Purpose:** Renders tabular data from database queries.

**Main Components:**
- `TablaComponent`: Standalone component

**Inputs:**
- `data`: JSON object with column-based structure

**Getters:**
- `columnas`: Extracts column names from data keys
- `filas`: Transforms column-based data into row-based array

**Data Transformation:**
- Input format: `{ column1: { row1: value, row2: value }, column2: { ... } }`
- Output: Array of row objects `{ column1: value, column2: value }`

**Dependencies:**
- `@angular/core`: Component, Input
- `@angular/common`: CommonModule

**Integration:**
- Used in: `chat-output` component
- Displays database query results in RAG responses

### tabla.component.html

**Purpose:** Template for table HTML structure.

**Structure:**
- Table element with headers and rows
- Dynamic column/row rendering

### tabla.component.scss

**Purpose:** Styling for table display.

**Key Styles:**
- Table borders and spacing
- Header styling
- Row alternating colors

### tabla.component.spec.ts

**Purpose:** Unit test suite for table rendering.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)
