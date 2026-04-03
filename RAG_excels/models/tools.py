from langchain.tools import tool
import pandas as pd
from langchain_core.documents import Document
import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import shutil
import re
from datetime import datetime
from services.excel_loader import load_and_process_excel, load_existing_vectorstore, save_vectorstore

# Configuración global
BACKUP_DIR = "backups_excel"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Global variables
retriever = None
current_file_path = None
vectorstore = None

def set_retriever(global_retriever):
    """Set the global retriever for tools"""
    global retriever
    retriever = global_retriever

def set_vectorstore(global_vectorstore):
    """Set the global vectorstore"""
    global vectorstore
    vectorstore = global_vectorstore

def create_backup(file_path: str) -> str:
    """Crea backup automático antes de cualquier edición"""
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(BACKUP_DIR) / f"{Path(file_path).stem}_{timestamp}.xlsx"
    shutil.copy2(file_path, backup_path)
    return str(backup_path)

def initialize(file_path: str, use_existing: bool = False) -> Tuple[bool, str]:
    """
    Initialize the agent with vector store and retriever
    Returns: (success: bool, message: str)
    """
    global current_file_path, retriever, vectorstore
    
    try:
        if use_existing and current_file_path == file_path:
            # Ya está inicializado con el mismo archivo
            return True, "✅ Usando vectorstore existente"
        
        if use_existing:
            # Cargar vectorstore existente
            vs, ret, embeddings = load_existing_vectorstore()
            vectorstore = vs
            retriever = ret
        else:
            # Crear nuevo vectorstore
            vs, ret, embeddings = load_and_process_excel(file_path)
            vectorstore = vs
            retriever = ret
            # Guardar para reutilizar
            save_vectorstore(vs)
        
        current_file_path = file_path
        return True, "✅ Vectorstore inicializado correctamente"
        
    except Exception as e:
        return False, f"❌ Error inicializando: {str(e)}"

def parse_cell_reference(cell_ref: str) -> Tuple[Optional[int], Optional[int], str]:
    """
    Parsea referencia de celda Excel (ej: 'A1', 'AB123', 'Z999')
    Returns: (row_idx, col_idx, error_msg)
    """
    try:
        # Extraer letra(s) de columna y número de fila
        match = re.match(r'^([A-Z]+)(\d+)$', cell_ref.upper())
        if not match:
            return None, None, f"Formato inválido: '{cell_ref}'. Use formato como 'A1', 'B10', 'AA100'"
        
        col_letters, row_num = match.groups()
        
        # Convertir columna de letras a índice (A=0, B=1, ..., Z=25, AA=26, etc.)
        col_idx = 0
        for i, letter in enumerate(reversed(col_letters)):
            col_idx += (ord(letter) - ord('A') + 1) * (26 ** i)
        col_idx -= 1  # Ajustar a índice 0-based
        
        row_idx = int(row_num) - 1  # Excel es 1-based, pandas es 0-based
        
        if row_idx < 0:
            return None, None, f"Número de fila debe ser mayor a 0"
        
        return row_idx, col_idx, ""
        
    except Exception as e:
        return None, None, f"Error parseando celda: {str(e)}"

def column_index_to_letter(col_idx: int) -> str:
    """Convierte índice de columna a letra Excel (0->A, 25->Z, 26->AA)"""
    result = ""
    col_idx += 1  # Convertir a 1-based
    while col_idx > 0:
        col_idx -= 1
        result = chr(col_idx % 26 + ord('A')) + result
        col_idx //= 26
    return result

@tool()#(response_format="content_and_artifact")
def buscar_en_excel(file_path: str, query: str,  
                    filter_sheet: Optional[str] = None) -> Tuple[str, List[Document]]:
    """
    Busca información relevante en el archivo Excel usando búsqueda semántica.
    
    Args:
        file_path: Ruta al archivo Excel
        query: Pregunta o término de búsqueda
        filter_sheet: Opcional - filtrar solo por una hoja específica
    
    Returns:
        Contexto formateado y lista de documentos encontrados
    """
    # Inicializar si es necesario
    success, msg = initialize(file_path=file_path, use_existing=True)
    if not success:
        return f"❌ {msg}", []
    
    if retriever is None:
        return "❌ ERROR: No se ha configurado el retriever para buscar en Excel", []
    
    try:
        # Buscar documentos relevantes
        docs = retriever.invoke(query)
        
        # Filtrar por hoja si se especifica
        if filter_sheet:
            docs = [doc for doc in docs if doc.metadata.get('sheet_name') == filter_sheet]
        
         
        if not docs:
            return f"ℹ️ No se encontraron resultados para: '{query}'", []
        
        # Agrupar por hoja para mejor presentación
        docs_by_sheet = {}
        for doc in docs:
            sheet = doc.metadata.get('sheet_name', 'Desconocido')
            if sheet not in docs_by_sheet:
                docs_by_sheet[sheet] = []
            docs_by_sheet[sheet].append(doc)
        
        # Formatear contexto
        context_parts = [f"📊 RESULTADOS DE BÚSQUEDA: '{query}'\n" + "="*50]
        
        for sheet_name, sheet_docs in docs_by_sheet.items():
            context_parts.append(f"\n📋 Hoja: {sheet_name}")
            context_parts.append("-" * 40)
            
            for i, doc in enumerate(sheet_docs, 1):
                cell = doc.metadata.get('cell', 'N/A')
                content = doc.page_content[:500]  # Aumentado a 500 caracteres
                
                # Información adicional si está disponible
                row = doc.metadata.get('row', 'N/A')
                col = doc.metadata.get('column', 'N/A')
                
                context_parts.append(
                    f"\n{i}. 📍 Celda: {cell} | Fila: {row} | Columna: {col}\n"
                    f"   💬 Contenido: {content}..."
                )
        
        context_parts.append(f"\n{'='*50}\n✅ Total: {len(docs)} resultados encontrados")
        context = "\n".join(context_parts)
        
        return context, docs
        
    except Exception as e:
        return f"❌ Error en búsqueda: {str(e)}", []

@tool()
def editar_excel(file_path: str, hoja: str, celda: str, nuevo_valor: Any, 
                 confirmacion: Optional[str] = None) -> str:
    """
    Edita una celda específica en el archivo Excel con validaciones robustas.
    
    Args:
        file_path: Ruta al archivo Excel
        hoja: Nombre exacto de la hoja (case-sensitive)
        celda: Referencia de celda como 'A1', 'B10', 'AA100', 'Z999'
        nuevo_valor: Nuevo valor para la celda (texto, número, fecha, fórmula)
        confirmacion: OBLIGATORIO - Debe ser 'SI' para ejecutar la edición
    
    IMPORTANTE: 
    - Siempre crea un backup automático antes de editar
    - Mantiene el formato original de la celda cuando es posible
    - Soporta columnas más allá de Z (AA, AB, etc.)
    """
    
    # Validación de seguridad CRÍTICA
    if confirmacion != "SI":
        return (
            "⚠️ CONFIRMACIÓN REQUERIDA\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Para ejecutar esta edición debes confirmar con: confirmacion='SI'\n\n"
            "Vista previa de cambio:\n"
            f"  📊 Hoja: {hoja}\n"
            f"  📍 Celda: {celda}\n"
            f"  ✏️  Nuevo valor: '{nuevo_valor}'\n\n"
            "❌ Edición CANCELADA por falta de confirmación"
        )
    
    try:
        # Validar que el archivo existe
        if not os.path.exists(file_path):
            return f"❌ Archivo no encontrado: {file_path}"
        
        # Crear backup
        backup_path = create_backup(file_path)
        
        # Cargar Excel con todas las hojas
        xls = pd.ExcelFile(file_path)
        
        # Validar que la hoja existe
        if hoja not in xls.sheet_names:
            available = "', '".join(xls.sheet_names)
            return (
                f"❌ Hoja '{hoja}' no existe\n\n"
                f"📋 Hojas disponibles:\n  '{available}'"
            )
        
        # Parsear referencia de celda
        row_idx, col_idx, error = parse_cell_reference(celda)
        if error:
            return f"❌ {error}"
        
        # Cargar la hoja específica sin tratar primera fila como header
        df = pd.read_excel(file_path, sheet_name=hoja, header=None)
        
        # Validar que la celda existe en el DataFrame
        if row_idx >= len(df):
            return (
                f"❌ Fila {row_idx + 1} fuera de rango\n"
                f"   La hoja '{hoja}' tiene {len(df)} filas"
            )
        
        if col_idx >= len(df.columns):
            max_col = column_index_to_letter(len(df.columns) - 1)
            return (
                f"❌ Columna {column_index_to_letter(col_idx)} fuera de rango\n"
                f"   La hoja '{hoja}' tiene columnas hasta {max_col}"
            )
        
        # Obtener valor anterior
        valor_anterior = df.iloc[row_idx, col_idx]
        
        # Convertir nuevo valor al tipo apropiado
        if isinstance(nuevo_valor, str):
            # Detectar si es número, fecha o texto
            try:
                if nuevo_valor.replace('.', '').replace('-', '').isdigit():
                    nuevo_valor = float(nuevo_valor) if '.' in nuevo_valor else int(nuevo_valor)
                elif '/' in nuevo_valor or '-' in nuevo_valor:
                    # Intentar parsear como fecha
                    nuevo_valor = pd.to_datetime(nuevo_valor)
            except:
                pass  # Mantener como string
        
        # Actualizar celda
        df.iloc[row_idx, col_idx] = nuevo_valor
        
        # Guardar de vuelta al Excel manteniendo otras hojas
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=hoja, index=False, header=False)
        
        # Actualizar vectorstore si está inicializado
        if current_file_path == file_path and vectorstore is not None:
            try:
                # Re-procesar el Excel para actualizar el vectorstore
                success, msg = initialize(file_path, use_existing=False)
            except:
                pass  # No crítico si falla la actualización del vectorstore
        
        return (
            "✅ EDICIÓN COMPLETADA EXITOSAMENTE\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💾 Backup creado: {backup_path}\n"
            f"📊 Hoja: '{hoja}'\n"
            f"📍 Celda: {celda} (Fila {row_idx + 1}, Col {column_index_to_letter(col_idx)})\n"
            f"📉 Valor anterior: '{valor_anterior}'\n"
            f"📈 Valor nuevo: '{nuevo_valor}'\n"
            f"🔄 Archivo actualizado: {file_path}"
        )
            
    except Exception as e:
        return f"❌ Error al editar: {str(e)}\n\n💡 Tip: Verifica el formato de la celda y que el archivo no esté abierto"

@tool()
def explorar_excel(file_path: str, hoja: Optional[str] = None, 
                    mostrar_columnas: bool = True) -> str:
    """
    Explora la estructura del archivo Excel: hojas, dimensiones, columnas y datos de muestra.
    
    Args:
        file_path: Ruta al archivo Excel
        hoja: Opcional - Nombre de hoja específica para explorar en detalle
        mostrar_columnas: Si se deben mostrar los nombres de columnas (default: True)
    
    Returns:
        Información detallada sobre la estructura del Excel
    """
    try:
        # Validar que el archivo existe
        if not os.path.exists(file_path):
            return f"❌ Archivo no encontrado: {file_path}"
        
        xls = pd.ExcelFile(file_path)
        
        if not hoja:
            # Vista general de todas las hojas
            info_parts = [
                "📊 ESTRUCTURA DEL ARCHIVO EXCEL",
                "=" * 50,
                f"📁 Archivo: {Path(file_path).name}",
                f"📋 Total de hojas: {len(xls.sheet_names)}\n"
            ]
            
            for i, sheet_name in enumerate(xls.sheet_names, 1):
                df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
                total_cells = df.shape[0] * df.shape[1]
                max_col = column_index_to_letter(df.shape[1] - 1)
                
                info_parts.append(
                    f"{i}. 📄 '{sheet_name}'\n"
                    f"   └─ Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas (A-{max_col})\n"
                    f"   └─ Total celdas: {total_cells:,}"
                )
            
            info_parts.append(
                f"\n{'=' * 50}\n"
                f"💡 Usa hoja='nombre_hoja' para ver detalles de una hoja específica"
            )
            
            return "\n".join(info_parts)
        
        # Exploración detallada de una hoja específica
        if hoja not in xls.sheet_names:
            available = "', '".join(xls.sheet_names)
            return (
                f"❌ Hoja '{hoja}' no encontrada\n\n"
                f"📋 Hojas disponibles:\n  '{available}'"
            )
        
        # Cargar hoja con y sin headers para análisis completo
        df_no_header = pd.read_excel(file_path, sheet_name=hoja, header=None)
        df_with_header = pd.read_excel(file_path, sheet_name=hoja)
        
        max_col = column_index_to_letter(df_no_header.shape[1] - 1)
        
        info_parts = [
            f"📊 ANÁLISIS DETALLADO: '{hoja}'",
            "=" * 50,
            f"📐 Dimensiones: {df_no_header.shape[0]} filas × {df_no_header.shape[1]} columnas",
            f"🔤 Rango de columnas: A hasta {max_col}",
            f"📍 Última celda: {max_col}{df_no_header.shape[0]}\n"
        ]
        
        # Información de columnas
        if mostrar_columnas and df_with_header.shape[1] > 0:
            info_parts.append("📋 COLUMNAS DETECTADAS:")
            info_parts.append("-" * 40)
            
            for i, col_name in enumerate(df_with_header.columns):
                col_letter = column_index_to_letter(i)
                dtype = df_with_header[col_name].dtype
                non_null = df_with_header[col_name].notna().sum()
                
                info_parts.append(
                    f"{col_letter}. '{col_name}' ({dtype}) - {non_null} valores"
                )
        

        
        # Formatear preview con ancho limitado para mejor legibilidad
        preview = df_with_header.to_string(
            max_colwidth=30,
            index=True
        )
        info_parts.append(preview)
        
        # Estadísticas adicionales
        info_parts.append(f"\n📊 ESTADÍSTICAS:")
        info_parts.append("-" * 40)
        info_parts.append(f"Celdas totales: {df_no_header.shape[0] * df_no_header.shape[1]:,}")
        info_parts.append(f"Celdas vacías: {df_with_header.isna().sum().sum():,}")
        info_parts.append(f"Tipos de datos: {', '.join(df_with_header.dtypes.astype(str).unique())}")
        
        return "\n".join(info_parts)
            
    except Exception as e:
        return f"❌ Error explorando archivo: {str(e)}"

@tool()
def buscar_columna(file_path: str, nombre_columna: str, hoja: Optional[str] = None) -> str:
    """
    Busca una columna por su nombre en el Excel y muestra información sobre ella.
    
    Args:
        file_path: Ruta al archivo Excel
        nombre_columna: Nombre de la columna a buscar (búsqueda parcial)
        hoja: Opcional - Buscar solo en esta hoja específica
    
    Returns:
        Información sobre las columnas encontradas
    """
    try:
        if not os.path.exists(file_path):
            return f"❌ Archivo no encontrado: {file_path}"
        
        xls = pd.ExcelFile(file_path)
        sheets_to_search = [hoja] if hoja else xls.sheet_names
        
        results = []
        
        for sheet_name in sheets_to_search:
            if sheet_name not in xls.sheet_names:
                continue
                
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Buscar columnas que coincidan (case-insensitive, parcial)
            matching_cols = [
                col for col in df.columns 
                if nombre_columna.lower() in str(col).lower()
            ]
            
            if matching_cols:
                for col in matching_cols:
                    col_idx = df.columns.get_loc(col)
                    col_letter = column_index_to_letter(col_idx)
                    
                    # Estadísticas de la columna
                    non_null = df[col].notna().sum()
                    null_count = df[col].isna().sum()
                    dtype = df[col].dtype
                    
                    # Muestra de valores únicos (primeros 5)
                    unique_vals = df[col].dropna().unique()[:5]
                    unique_preview = ", ".join([f"'{v}'" for v in unique_vals])
                    
                    results.append(
                        f"📊 Hoja: '{sheet_name}'\n"
                        f"   📍 Columna: {col_letter} - '{col}'\n"
                        f"   📊 Tipo: {dtype}\n"
                        f"   ✅ Valores: {non_null} | ❌ Vacíos: {null_count}\n"
                        f"   🔍 Muestra: {unique_preview}{'...' if len(unique_vals) >= 5 else ''}"
                    )
        
        if not results:
            return (
                f"ℹ️ No se encontraron columnas que coincidan con '{nombre_columna}'\n\n"
                f"💡 Tip: Usa explorar_excel() para ver todas las columnas disponibles"
            )
        
        header = f"🔍 RESULTADOS PARA: '{nombre_columna}'\n{'=' * 50}\n\n"
        return header + "\n\n".join(results)
        
    except Exception as e:
        return f"❌ Error buscando columna: {str(e)}"

@tool()
def buscar_por_filtro(file_path: str, columna: str, valor_busqueda: Any, 
                      hoja: Optional[str] = None, operador: str = "igual",
                      max_resultados: int = 10) -> str:
    """
    Busca filas en el Excel filtrando por valor en una columna específica.
    Útil para consultas como: "busca todos los registros donde Ciudad es Madrid"
    
    Args:
        file_path: Ruta al archivo Excel
        columna: Nombre de la columna por la que filtrar
        valor_busqueda: Valor a buscar en la columna
        hoja: Opcional - Buscar solo en esta hoja (si no, busca en todas)
        operador: Tipo de comparación ('igual', 'contiene', 'mayor', 'menor', 'mayor_igual', 'menor_igual')
        max_resultados: Máximo número de resultados a mostrar (default: 10)
    
    Returns:
        Filas encontradas que cumplen el criterio
    """
    try:
        if not os.path.exists(file_path):
            return f"❌ Archivo no encontrado: {file_path}"
        
        xls = pd.ExcelFile(file_path)
        sheets_to_search = [hoja] if hoja else xls.sheet_names
        
        all_results = []
        total_found = 0
        
        for sheet_name in sheets_to_search:
            if sheet_name not in xls.sheet_names:
                continue
            
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Verificar si la columna existe
            if columna not in df.columns:
                continue
            
            # Aplicar filtro según operador
            try:
                if operador == "igual":
                    mask = df[columna] == valor_busqueda
                elif operador == "contiene":
                    mask = df[columna].astype(str).str.contains(str(valor_busqueda), case=False, na=False)
                elif operador == "mayor":
                    mask = df[columna] > valor_busqueda
                elif operador == "menor":
                    mask = df[columna] < valor_busqueda
                elif operador == "mayor_igual":
                    mask = df[columna] >= valor_busqueda
                elif operador == "menor_igual":
                    mask = df[columna] <= valor_busqueda
                else:
                    return f"❌ Operador '{operador}' no válido. Usa: igual, contiene, mayor, menor, mayor_igual, menor_igual"
                
                filtered_df = df[mask]
                
                if len(filtered_df) > 0:
                    total_found += len(filtered_df)
                    
                    # Limitar resultados por hoja
                    display_df = filtered_df.head(max_resultados)
                    
                    # Formatear resultados
                    result_text = f"\n📋 Hoja: '{sheet_name}' - {len(filtered_df)} coincidencias\n"
                    result_text += "-" * 50 + "\n"
                    
                    for idx, row in display_df.iterrows():
                        # Número de fila en Excel (idx + 2 porque Excel es 1-based y hay header)
                        excel_row = idx + 2
                        result_text += f"\n📍 Fila {excel_row}:\n"
                        
                        # Mostrar todas las columnas de esa fila
                        for col_name in df.columns:
                            col_idx = df.columns.get_loc(col_name)
                            col_letter = column_index_to_letter(col_idx)
                            value = row[col_name]
                            
                            # Destacar la columna filtrada
                            if col_name == columna:
                                result_text += f"   ⭐ {col_letter}. {col_name}: '{value}'\n"
                            else:
                                result_text += f"   {col_letter}. {col_name}: '{value}'\n"
                    
                    if len(filtered_df) > max_resultados:
                        result_text += f"\n   ... y {len(filtered_df) - max_resultados} filas más\n"
                    
                    all_results.append(result_text)
                    
            except Exception as e:
                continue
        
        if not all_results:
            return (
                f"ℹ️ No se encontraron resultados para:\n"
                f"   Columna: '{columna}'\n"
                f"   Operador: '{operador}'\n"
                f"   Valor: '{valor_busqueda}'\n\n"
                f"💡 Tip: Verifica que la columna existe con buscar_columna() o explorar_excel()"
            )
        
        header = (
            f"🔍 BÚSQUEDA POR FILTRO\n"
            f"{'=' * 50}\n"
            f"📊 Columna: '{columna}'\n"
            f"🔎 Operador: '{operador}'\n"
            f"🎯 Valor: '{valor_busqueda}'\n"
            f"✅ Total encontrado: {total_found} filas\n"
        )
        
        return header + "".join(all_results)
        
    except Exception as e:
        return f"❌ Error en búsqueda por filtro: {str(e)}"

@tool()#(response_format="content_and_artifact")
def consulta_libre_excel(file_path: str, consulta: str, incluir_contexto: bool = True) -> Tuple[str, Dict[str, Any]]:
    """
    Realiza una consulta libre sobre el Excel usando búsqueda semántica Y análisis estructural.
    Esta es la herramienta más potente para responder cualquier pregunta sobre el Excel.
    
    Casos de uso:
    - "¿Cuántos clientes hay en Madrid?"
    - "¿Cuál es el promedio de ventas por región?"
    - "Muéstrame los productos con precio mayor a 100"
    - "¿Qué información hay sobre el empleado Juan Pérez?"
    - "Lista todas las hojas y sus contenidos principales"
    
    Args:
        file_path: Ruta al archivo Excel
        consulta: Pregunta o consulta en lenguaje natural
        incluir_contexto: Si incluir contexto adicional del archivo (default: True)
    
    Returns:
        Respuesta estructurada con datos relevantes y contexto
    """
    try:
        if not os.path.exists(file_path):
            return f"❌ Archivo no encontrado: {file_path}", {}
        
        # Inicializar vectorstore si es necesario
        success, msg = initialize(file_path=file_path, use_existing=True)
        
        response_parts = [
            f"📊 ANÁLISIS DE CONSULTA: '{consulta}'",
            "=" * 50
        ]
        
        result_data = {
            "consulta": consulta,
            "archivo": Path(file_path).name,
            "hojas_analizadas": [],
            "datos_encontrados": []
        }
        
        # 1. BÚSQUEDA SEMÁNTICA (si el vectorstore está disponible)
        if retriever is not None:
            response_parts.append("\n🔍 BÚSQUEDA SEMÁNTICA:")
            response_parts.append("-" * 40)
            
            docs = retriever.invoke(consulta)#[:5]
            
            if docs:
                for i, doc in enumerate(docs, 1):
                    sheet = doc.metadata.get('sheet_name', 'N/A')
                    cell = doc.metadata.get('cell', 'N/A')
                    content = doc.page_content[:200]
                    
                    response_parts.append(
                        f"\n{i}. 📋 {sheet} | 📍 {cell}\n"
                        f"   💬 {content}..."
                    )
                    
                    result_data["datos_encontrados"].append({
                        "sheet": sheet,
                        "cell": cell,
                        "content": content,
                        "tipo": "semantico"
                    })
            else:
                response_parts.append("   ℹ️ No se encontraron coincidencias semánticas")
        
        # 2. ANÁLISIS ESTRUCTURAL (buscar patrones en la consulta)
        xls = pd.ExcelFile(file_path)
        response_parts.append(f"\n\n📋 ANÁLISIS ESTRUCTURAL ({len(xls.sheet_names)} hojas):")
        response_parts.append("-" * 40)
        
        # Detectar palabras clave en la consulta
        consulta_lower = consulta.lower()
        keywords_numericos = ["cuántos", "cuántas", "total", "suma", "promedio", "media", "count"]
        keywords_filtro = ["donde", "con", "que tengan", "igual a", "mayor que", "menor que"]
        
        es_consulta_numerica = any(kw in consulta_lower for kw in keywords_numericos)
        es_consulta_filtro = any(kw in consulta_lower for kw in keywords_filtro)
        
        # Analizar cada hoja buscando datos relevantes
        for sheet_name in xls.sheet_names:
            result_data["hojas_analizadas"].append(sheet_name)
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            response_parts.append(f"\n📄 Hoja: '{sheet_name}'")
            response_parts.append(f"   Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
            
            # Buscar columnas relevantes para la consulta
            columnas_relevantes = []
            for col in df.columns:
                col_str = str(col).lower()
                # Buscar coincidencias entre columnas y términos de la consulta
                palabras_consulta = consulta_lower.split()
                if any(palabra in col_str for palabra in palabras_consulta if len(palabra) > 3):
                    columnas_relevantes.append(col)
            
            if columnas_relevantes:
                response_parts.append(f"   ✨ Columnas relevantes: {', '.join(columnas_relevantes)}")
                
                # Si es consulta numérica, calcular estadísticas
                if es_consulta_numerica:
                    for col in columnas_relevantes:
                        if pd.api.types.is_numeric_dtype(df[col]):
                            stats = {
                                "total": df[col].count(),
                                "suma": df[col].sum(),
                                "promedio": df[col].mean(),
                                "min": df[col].min(),
                                "max": df[col].max()
                            }
                            response_parts.append(f"\n   📊 Estadísticas '{col}':")
                            response_parts.append(f"      Total valores: {stats['total']}")
                            response_parts.append(f"      Suma: {stats['suma']:.2f}")
                            response_parts.append(f"      Promedio: {stats['promedio']:.2f}")
                            response_parts.append(f"      Rango: {stats['min']} - {stats['max']}")
                            
                            result_data["datos_encontrados"].append({
                                "sheet": sheet_name,
                                "columna": col,
                                "estadisticas": stats,
                                "tipo": "numerico"
                            })
                
                # Mostrar muestra de datos de columnas relevantes
                if len(columnas_relevantes) <= 3:
                    muestra = df[columnas_relevantes].head(3)
                    response_parts.append(f"\n   🔍 Muestra de datos:")
                    response_parts.append(f"{muestra.to_string(index=False, max_colwidth=30)}")
        
        # 3. CONTEXTO ADICIONAL (si se solicita)
        if incluir_contexto:
            response_parts.append(f"\n\n💡 CONTEXTO ADICIONAL:")
            response_parts.append("-" * 40)
            response_parts.append(f"Total de hojas: {len(xls.sheet_names)}")
            
            total_filas = sum(pd.read_excel(file_path, sheet_name=s).shape[0] for s in xls.sheet_names)
            response_parts.append(f"Total de filas (todas las hojas): {total_filas:,}")
            
            response_parts.append(f"\n📋 Estructura general:")
            for sheet in xls.sheet_names:
                df_info = pd.read_excel(file_path, sheet_name=sheet)
                response_parts.append(f"   • {sheet}: {list(df_info.columns)[:5]}{'...' if len(df_info.columns) > 5 else ''}")
        
        # 4. SUGERENCIAS
        response_parts.append(f"\n\n🎯 SUGERENCIAS PARA PROFUNDIZAR:")
        response_parts.append("-" * 40)
        response_parts.append("• Usa buscar_por_filtro() para filtrar datos específicos")
        response_parts.append("• Usa explorar_excel() para ver toda la estructura")
        response_parts.append("• Usa buscar_columna() para encontrar columnas por nombre")
        
        final_response = "\n".join(response_parts)
        
        return final_response, result_data
        
    except Exception as e:
        error_msg = f"❌ Error en consulta libre: {str(e)}"
        return error_msg, {"error": str(e)}

def get_tools():
    """Retorna todas las herramientas disponibles para el agente"""
    return [
        buscar_en_excel,
        editar_excel,
        explorar_excel,
        buscar_columna,
        buscar_por_filtro,
        consulta_libre_excel
    ]