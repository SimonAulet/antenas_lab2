# txt2dat.py - Text to DAT converter
# Author: [Simón Aulet]
# Date: 2025-09-10

import re
from typing import List, Tuple
import os

def load_text_file(file_path: str, y_col: int, 
                  start_row: int, end_row: int, y_unit: str, circular_shift: int = 0, 
                  output_path: str = None) -> str:
    """
    Carga un archivo de texto y genera un archivo .DAT con las columnas y rangos especificados

    Parameters:
    -----------
    file_path : str
        Ruta del archivo de texto a cargar
    y_col : int
        Número de columna para eje Y (0-based)
    start_row : int
        Número de fila inicial (incluida)
    end_row : int
        Número de fila final (no incluida)
    y_unit : str
        Y-axis unit ('dBm', 'dBi', 'dB')
    circular_shift : int
        Circular shift amount for Y data (0 = no shift)

    Returns:
    --------
    str
        Path of the generated .DAT file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Encontrar la línea donde comienzan los datos (después del header)
        data_start = _find_text_data_start(lines)

        # Procesar datos según los parámetros especificados
        y_values = []
        
        for i in range(max(data_start, start_row), min(end_row, len(lines))):
            line = lines[i].strip()
            if not line:
                continue
                
            # Parsear línea separando por espacios múltiples
            parts = re.split(r'\s+', line)
            parts = [p for p in parts if p]  # Remover strings vacíos
            
            if len(parts) > y_col:
                try:
                    y_val = float(parts[y_col])
                    y_values.append(y_val)
                except (ValueError, IndexError):
                    continue
        
        # Aplicar desplazamiento circular si se especificó
        if circular_shift != 0 and len(y_values) > 0:
            shift_amount = circular_shift % len(y_values)
            y_values = y_values[-shift_amount:] + y_values[:-shift_amount]
        
        # Generar eje X automático (0, 1, 2, 3...)
        x_values = list(range(len(y_values)))

        # Generar archivo .DAT
        if output_path is None:
            base_name = os.path.splitext(file_path)[0]
            output_path = f"{base_name}_processed.DAT"
        else:
            # Si se especificó output_path, usar el mismo nombre del archivo original
            base_name = os.path.basename(file_path)
            output_file_name = os.path.splitext(base_name)[0] + '.DAT'
            output_path = os.path.join(output_path, output_file_name)
        
        _generate_dat_file(output_path, x_values, y_values, y_unit, len(x_values))

        return output_path

    except Exception as e:
        raise ValueError(f"Error loading text file {file_path}: {str(e)}")

def _find_text_data_start(lines: List[str]) -> int:
    """
    Find the index where numeric data starts in text files

    Parameters:
    -----------
    lines : List[str]
        Lista de líneas del archivo

    Returns:
    --------
    int
        Index of the first data line
    """
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Look for lines containing numeric values (data)
        parts = re.split(r'\s+', line)
        parts = [p for p in parts if p]  # Remover strings vacíos

        if len(parts) >= 2:
            try:
                # Try to convert first two parts to float
                float(parts[0])
                float(parts[1])
                return i
            except ValueError:
                pass
    return 0  # If not found, assume it starts from first line

def _generate_dat_file(output_path: str, x_values: List[float], 
                      y_values: List[float], y_unit: str, n_points: int) -> None:
    """
    Generate a .DAT file with the expected structure

    Parameters:
    -----------
    output_path : str
        Ruta donde guardar el archivo .DAT
    x_values : List[float]
        Valores del eje X
    y_values : List[float]
        Valores del eje Y
    y_unit : str
        Unidad del eje Y
    n_points : int
        Número de puntos
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        # Write minimal header consistent with R&S format
        file.write("Type;TXT2DAT;\n")
        file.write("Version;1.0;\n")
        file.write("Mode;PROCESSED;\n")
        file.write("x-Axis;LIN;\n")
        file.write("y-Axis;LOG;\n")

        # X-axis is always time in seconds
        file.write("x-Unit;s;\n")

        # Handle y-unit conversion
        if y_unit.lower() in ['dbm', 'dbi', 'db']:
            file.write(f"y-Unit;{y_unit};\n")
        else:
            file.write(f"y-Unit;{y_unit};\n")

        file.write(f"Values;{n_points};\n")
        file.write("Data Start\n")

        # Escribir datos
        for x, y in zip(x_values, y_values):
            file.write(f"{x};{y}\n")
