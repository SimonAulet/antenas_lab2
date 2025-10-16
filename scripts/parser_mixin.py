# ParserMixin - Mixin para funcionalidad de parsing de archivos .DAT de analizadores de espectro
# Autor: [Simón Aulet]
# Fecha: 2025-09-10

import re
from typing import Dict, List, Tuple, Optional
import numpy as np

class ParserMixin:
    """
    Mixin para funcionalidad de parsing de archivos .DAT de analizadores de espectro
    """
    
    def _parse_file(self) -> None:
        """Parsear el archivo completo y extraer header y datos"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Encontrar la línea que separa header de datos
            data_start_index = self._find_data_start(lines)
            
            # Parsear header
            self._parse_header(lines[:data_start_index])
            
            # Parsear datos
            self._parse_data(lines[data_start_index:])
            
        except Exception as e:
            raise ValueError(f"Error al parsear el archivo {self.file_path}: {str(e)}")
    
    def _find_data_start(self, lines: List[str]) -> int:
        """
        Encuentra el índice donde comienzan los datos numéricos
        
        Parameters:
        -----------
        lines : List[str]
            Lista de líneas del archivo
            
        Returns:
        --------
        int
            Índice de la primera línea de datos
        """
        for i, line in enumerate(lines):
            # Buscar líneas que contengan valores numéricos (datos)
            if self._is_data_line(line):
                return i
        raise ValueError("No se encontraron datos en el archivo")
    
    def _is_data_line(self, line: str) -> bool:
        """
        Determina si una línea contiene datos numéricos
        
        Parameters:
        -----------
        line : str
            Línea a evaluar
            
        Returns:
        --------
        bool
            True si la línea contiene datos numéricos
        """
        # Verificar si la línea tiene el formato de datos (números separados por ;)
        parts = line.strip().split(';')
        if len(parts) >= 2:
            try:
                # Intentar convertir las primeras dos partes a float
                float(parts[0])
                float(parts[1])
                return True
            except ValueError:
                pass
        return False
    
    def _parse_header(self, header_lines: List[str]) -> None:
        """
        Extrae y almacena los metadatos del header
        
        Parameters:
        -----------
        header_lines : List[str]
            Líneas del header a parsear
        """
        for line in header_lines:
            line = line.strip()
            if line and ';' in line:
                parts = line.split(';')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    
                    # Almacenar información completa después del primer punto y coma
                    # Esto preserva las unidades y cualquier información adicional
                    complete_value = ';'.join(parts[1:]).strip()
                    
                    # Almacenar solo si no es una línea vacía o de valores
                    if key and value and key != "Values":
                        self.header_data[key] = complete_value
                    
                    # Extraer número de puntos si está disponible
                    if key == "Values":
                        try:
                            self.n_points = int(value)
                        except ValueError:
                            pass
    
    def _parse_data(self, data_lines: List[str]) -> None:
        """
        Extrae y almacena los datos de medición
        
        Parameters:
        -----------
        data_lines : List[str]
            Líneas de datos a parsear
        """
        x_values = []
        y1_values = []
        
        for line in data_lines:
            line = line.strip()
            if line and ';' in line:
                parts = line.split(';')
                
                # Extraer las primeras dos columnas (solo x e y1)
                try:
                    x_val = float(parts[0])
                    y1_val = float(parts[1])
                    x_values.append(x_val)
                    y1_values.append(y1_val)
                        
                except (ValueError, IndexError):
                    # Saltar líneas que no se pueden convertir a números
                    continue
        
        # Convertir a arrays de NumPy - solo almacenamos x e y1
        self.data = {
            'x': np.array(x_values),
            'y1': np.array(y1_values)
        }