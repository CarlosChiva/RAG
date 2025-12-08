from langchain.tools import tool
import pandas as pd
from langchain_core.documents import Document
import os
from pathlib import Path
from typing import Optional, Any
import shutil
from services.excel_loader import load_and_process_excel, load_existing_vectorstore, save_vectorstore

# Configuración global
BACKUP_DIR = "backups_excel"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Global retriever variable (will be set by the agent)
retriever = None

# Global file path (will be set when EcelTooler is initialized)



def set_retriever( global_retriever):
    """Set the global retriever for tools"""
    global retriever
    retriever = global_retriever

def create_backup(file_path):
    """Crea backup automático antes de cualquier edición"""
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(BACKUP_DIR) / f"{Path(file_path).stem}_{timestamp}.xlsx"
    shutil.copy2(file_path, backup_path)
    return str(backup_path)

def initialize(file_path, use_existing:bool=False):
    """Initialize the agent with vector store and retriever"""
    if use_existing:
        # Cargar vectorstore existente
        vectorstore,retriever, embeddings = load_existing_vectorstore()
    else:
        # Crear nuevo vectorstore
        vectorstore, retriever, embeddings = load_and_process_excel(file_path)
        # Guardar para reutilizar
        save_vectorstore(vectorstore)
    
    # Set the retriever for tools
    set_retriever(retriever)

@tool(response_format="content_and_artifact")
def buscar_en_excel(file_path:str, query: str) -> tuple[str, list[Document]]:
    """Busca información relevante en el archivo Excel para responder preguntas."""
    initialize(file_path=file_path)
    
    if retriever is None:
        return "❌ ERROR: No se ha configurado el retriever para buscar en Excel", []
    
    docs = retriever.invoke(query)
    
    # Serializar para LLM (con metadata)
    context = "\n\n".join([
        f"Hoja: {doc.metadata.get('sheet_name', 'N/A')}\n"
        f"Celda: {doc.metadata.get('cell', 'N/A')}\n"
        f"Contenido: {doc.page_content[:300]}..."
        for doc in docs
    ])
    
    return context, docs  # LLM ve 'context', app ve 'docs'

@tool
def editar_excel(file_path:str,hoja: str, celda: str, nuevo_valor: str, confirmacion: Optional[str] = None) -> str:
    """
    Edita una celda específica en el archivo Excel.
    
    Args:
        hoja: Nombre exacto de la hoja (case-sensitive)
        celda: Referencia de celda como 'A1', 'B10', 'Z100'
        nuevo_valor: Nuevo valor para la celda (texto, número, fecha)
        confirmacion: Confirma con 'SI' para ejecutar (seguridad)
    
    AVISO: Solo ejecuta con confirmacion='SI'. Crea backup automático.
    """
    
    # Validación de seguridad CRÍTICA
    if confirmacion != "SI":
        return "❌ ERROR DE SEGURIDAD: Debes confirmar con 'confirmacion=SI' para editar."
    
    try:
        # Crear backup
        backup = create_backup()
        
        # Cargar Excel
        xls = pd.ExcelFile(file_path)
        
        if hoja not in xls.sheet_names:
            return f"❌ Hoja '{hoja}' no existe. Hojas disponibles: {xls.sheet_names}"
        
        # Cargar hoja específica
        df = pd.read_excel(file_path, sheet_name=hoja)
        
        # Parsear celda (A1 -> fila 0, columna 0)
        col_letter = celda[0].upper()
        row_num = int(celda[1:]) - 1  # Excel es 1-based
        
        # Validar celda
        col_idx = ord(col_letter) - ord('A')
        if col_idx < 0 or col_idx >= 26 or row_num < 0 or row_num >= len(df):
            return f"❌ Celda '{celda}' inválida para esta hoja (filas: {len(df)}, cols: A-{chr(ord('A')+len(df.columns)-1)})"
        
        # Valor anterior
        valor_anterior = df.iloc[row_num, col_idx]
        
        # Actualizar
        df.iloc[row_num, col_idx] = nuevo_valor
        
        # Guardar
        df.to_excel(file_path, sheet_name=hoja, index=False, header=False)
        
        return f"✅ EDITADO EXITOSO\n" \
            f"📁 Backup: {backup}\n" \
            f"📊 Hoja: {hoja}\n" \
            f"📍 Celda: {celda}\n" \
            f"📈 Antes: '{valor_anterior}'\n" \
            f"✏️ Después: '{nuevo_valor}'\n" \
            f"💾 Archivo actualizado: {file_path}"
            
    except Exception as e:
        return f"❌ Error editando: {str(e)}"

# Tool adicional para LISTAR hojas y estructura
@tool
def explorar_excel(file_path:str, hoja: Optional[str] = None) -> str:
    """Explora estructura del Excel: hojas, dimensiones, muestra datos."""
    try:
        xls = pd.ExcelFile(file_path)
        
        if not hoja:
            # Listar todas las hojas
            info = f"📋 Hojas disponibles ({len(xls.sheet_names)}):\n"
            for i, sheet in enumerate(xls.sheet_names, 1):
                df = pd.read_excel(file_path, sheet_name=sheet)
                info += f"{i}. '{sheet}' ({df.shape[0]} filas x {df.shape[1]} cols)\n"
            return info
        
        # Info específica de hoja
        if hoja not in xls.sheet_names:
            return f"❌ Hoja '{hoja}' no encontrada"
        
        df = pd.read_excel(file_path, sheet_name=hoja)
        sample = df.head(3).to_string(max_colwidth=20)
        
        return f"📊 Hoja '{hoja}': {df.shape[0]} filas x {df.shape[1]} columnas\n\n" \
            f"🔍 Vista previa (primeras 3 filas):\n{sample}"
            
    except Exception as e:
        return f"❌ Error explorando: {str(e)}"

def get_tools():
    """Returns all tools for the agent"""
    return [
        buscar_en_excel,
        editar_excel,
        explorar_excel
    ]
