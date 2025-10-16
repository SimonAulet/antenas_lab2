# ProcessingMixin - Mixin para procesamiento de datos de archivos .DAT de analizadores de espectro
# Autor: [Simón Aulet]
# Fecha: 2025-10-15

from typing import Dict, List, Tuple, Optional
import numpy as np
import os

class ProcessingMixin:
    """
    Mixin para funcionalidad de procesamiento de datos de archivos .DAT de analizadores de espectro

    Proporciona métodos para:
    - Espejar datos (corregir sentido de tornamesa)
    - Realizar recortes en los datos
    - Preparar archivos para guardado
    """

    def __init__(self):
        """Inicializa variables de procesamiento"""
        self.processed_data: Optional[Dict[str, np.ndarray]] = None
        self.output_filename: Optional[str] = None

    def set_output_filename(self, filename: str) -> None:
        """
        Establece el nombre del archivo de salida

        Parameters:
        -----------
        filename : str
            Nombre del archivo de salida (sin extensión o con extensión .DAT)
        """
        if not filename.endswith('.DAT'):
            filename += '.DAT'
        self.output_filename = filename

    def get_output_filename(self) -> Optional[str]:
        """
        Retorna el nombre del archivo de salida configurado

        Returns:
        --------
        Optional[str]
            Nombre del archivo de salida o None si no está configurado
        """
        return self.output_filename

    def mirror_data(self, in_place: bool = False) -> Dict[str, np.ndarray]:
        """
        Espeja los datos invirtiendo solo los valores de y1 (potencia)

        Útil para corregir el sentido de la tornamesa cuando se giró en direcciones opuestas.
        Mantiene el eje x (tiempo) intacto para preservar la cronología.

        Parameters:
        -----------
        in_place : bool, optional
            Si es True, modifica los datos originales. Si es False, retorna una copia

        Returns:
        --------
        Dict[str, np.ndarray]
            Diccionario con los datos espejados
        """
        if self.data is None:
            raise ValueError("No hay datos disponibles para espejar")

        mirrored_data = {
            'x': self.data['x'].copy(),  # Mantener tiempo en orden cronológico
            'y1': self.data['y1'][::-1].copy()  # Solo invertir valores de potencia
        }

        if in_place:
            self.data = mirrored_data
            return self.data
        else:
            self.processed_data = mirrored_data
            return mirrored_data

    def crop_data(self, start_index: Optional[int] = None, end_index: Optional[int] = None,
                  start_value: Optional[float] = None, end_value: Optional[float] = None,
                  in_place: bool = False) -> Dict[str, np.ndarray]:
        """
        Realiza un recorte de los datos basado en índices o valores

        Parameters:
        -----------
        start_index : Optional[int]
            Índice de inicio para el recorte (0-based)
        end_index : Optional[int]
            Índice de fin para el recorte (exclusivo)
        start_value : Optional[float]
            Valor de x para iniciar el recorte (se usará el índice más cercano)
        end_value : Optional[float]
            Valor de x para finalizar el recorte (se usará el índice más cercano)
        in_place : bool, optional
            Si es True, modifica los datos originales. Si es False, retorna una copia

        Returns:
        --------
        Dict[str, np.ndarray]
            Diccionario con los datos recortados

        Raises:
        -------
        ValueError
            Si no se proporcionan parámetros válidos para el recorte
        """
        if self.data is None:
            raise ValueError("No hay datos disponibles para recortar")

        x_data = self.data['x']
        y_data = self.data['y1']

        # Determinar índices de recorte
        if start_index is not None and end_index is not None:
            # Usar índices directamente
            start_idx = start_index
            end_idx = end_index
        elif start_value is not None and end_value is not None:
            # Usar valores para encontrar índices más cercanos
            start_idx = np.argmin(np.abs(x_data - start_value))
            end_idx = np.argmin(np.abs(x_data - end_value))
        else:
            raise ValueError("Debe proporcionar start_index y end_index, o start_value y end_value")

        # Asegurar que los índices estén en orden correcto
        if start_idx > end_idx:
            start_idx, end_idx = end_idx, start_idx

        # Aplicar recorte
        cropped_data = {
            'x': x_data[start_idx:end_idx].copy(),
            'y1': y_data[start_idx:end_idx].copy()
        }

        if in_place:
            self.data = cropped_data
            self.n_points = len(cropped_data['x'])
            return self.data
        else:
            self.processed_data = cropped_data
            return cropped_data

    def get_processed_data(self) -> Optional[Dict[str, np.ndarray]]:
        """
        Retorna los datos procesados si están disponibles

        Returns:
        --------
        Optional[Dict[str, np.ndarray]]
            Datos procesados o None si no hay datos procesados
        """
        return self.processed_data

    def reset_processing(self) -> None:
        """
        Resetea los datos procesados, volviendo a los datos originales
        """
        self.processed_data = None

    def save_processed_data(self, output_dir: str = '.', use_original_name: bool = False) -> str:
        """
        Guarda los datos procesados en un archivo .DAT compatible

        Parameters:
        -----------
        output_dir : str
            Directorio donde guardar el archivo
        use_original_name : bool
            Si es True, usa el nombre del archivo original con sufijo '_processed'

        Returns:
        --------
        str
            Ruta completa del archivo guardado

        Raises:
        -------
        ValueError
            Si no hay datos procesados o no se configuró nombre de salida
        """
        if self.processed_data is None:
            raise ValueError("No hay datos procesados para guardar")

        # Determinar nombre del archivo
        if use_original_name:
            base_name = os.path.splitext(os.path.basename(self.file_path))[0]
            filename = f"{base_name}_processed.DAT"
        elif self.output_filename:
            filename = self.output_filename
        else:
            raise ValueError("No se configuró nombre de salida. Use set_output_filename() o use_original_name=True")

        output_path = os.path.join(output_dir, filename)

        # Guardar archivo .DAT compatible
        self._save_dat_file(output_path, self.processed_data)

        return output_path

    def _save_dat_file(self, output_path: str, data_dict: Dict[str, np.ndarray]) -> None:
        """
        Guarda datos en formato .DAT compatible con Rhode & Schwarz

        Parameters:
        -----------
        output_path : str
            Ruta donde guardar el archivo
        data_dict : Dict[str, np.ndarray]
            Diccionario con datos a guardar
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            # Escribir header original
            for key, value in self.header_data.items():
                f.write(f"{key};{value}\n")

            # Escribir línea de valores con el nuevo número de puntos
            n_points = len(data_dict['x'])
            f.write(f"Values;{n_points};\n")

            # Escribir datos
            for i in range(n_points):
                x = data_dict['x'][i]
                y1 = data_dict['y1'][i]
                y2 = data_dict['y1'][i]  # Para compatibilidad, usar y1 también como y2
                f.write(f"{x};{y1};{y2}\n")
