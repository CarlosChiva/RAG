import pandas as pd
from langchain.tools import tool
from langchain_core.documents import Document
import os
from pathlib import Path
from typing import Optional
import shutil

# Configuración global
EXCEL_PATH = "tu_archivo.xlsx"
BACKUP_DIR = "backups_excel"
os.makedirs(BACKUP_DIR, exist_ok=True)

def create_backup():
    """Crea backup automático antes de cualquier edición"""
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(BACKUP_DIR) / f"{Path(EXCEL_PATH).stem}_{timestamp}.xlsx"
    shutil.copy2(EXCEL_PATH, backup_path)
    return str(backup_path)

@tool(response_format="content_and_artifact")
def buscar_en_excel(query: str) -> tuple[str, list[Document]]:
    """Busca información relevante en el archivo Excel para responder preguntas."""
    # Esta función necesita acceder al retriever, que se inyectará desde el agente
    # Por ahora, se deja como plantilla, se inyectará el retriever en la clase agente
    pass

@tool
def editar_excel(
    hoja: str,
    celda: str,  # Formato A1, B10, etc.
    nuevo_valor: str,
    confirmacion: Optional[str] = None
) -> str:
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
        xls = pd.ExcelFile(EXCEL_PATH)
        
        if hoja not in xls.sheet_names:
            return f"❌ Hoja '{hoja}' no existe. Hojas disponibles: {xls.sheet_names}"
        
        # Cargar hoja específica
        df = pd.read_excel(EXCEL_PATH, sheet_name=hoja)
        
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
        df.to_excel(EXCEL_PATH, sheet_name=hoja, index=False, header=False)
        
        return f"✅ EDITADO EXITOSO\n" \
               f"📁 Backup: {backup}\n" \
               f"📊 Hoja: {hoja}\n" \
               f"📍 Celda: {celda}\n" \
               f"📈 Antes: '{valor_anterior}'\n" \
               f"✏️ Después: '{nuevo_valor}'\n" \
               f"💾 Archivo actualizado: {EXCEL_PATH}"
               
    except Exception as e:
        return f"❌ Error editando: {str(e)}"

# Tool adicional para LISTAR hojas y estructura
@tool
def explorar_excel(hoja: Optional[str] = None) -> str:
    """Explora estructura del Excel: hojas, dimensiones, muestra datos."""
    try:
        xls = pd.ExcelFile(EXCEL_PATH)
        
        if not hoja:
            # Listar todas las hojas
            info = f"📋 Hojas disponibles ({len(xls.sheet_names)}):\n"
            for i, sheet in enumerate(xls.sheet_names, 1):
                df = pd.read_excel(EXCEL_PATH, sheet_name=sheet)
                info += f"{i}. '{sheet}' ({df.shape[0]} filas x {df.shape[1]} cols)\n"
            return info
        
        # Info específica de hoja
        if hoja not in xls.sheet_names:
            return f"❌ Hoja '{hoja}' no encontrada"
        
        df = pd.read_excel(EXCEL_PATH, sheet_name=hoja)
        sample = df.head(3).to_string(max_colwidth=20)
        
        return f"📊 Hoja '{hoja}': {df.shape[0]} filas x {df.shape[1]} columnas\n\n" \
               f"🔍 Vista previa (primeras 3 filas):\n{sample}"
               
    except Exception as e:
        return f"❌ Error explorando: {str(e)}"
