# SAData - Clase para manejar datos de archivos .DAT de analizadores de espectro
# Autor: [Simón Aulet]
# Fecha: 2025-09-10

from typing import Dict, List, Tuple, Optional
import numpy as np

from .conversion_mixin import ConversionMixin
from .parser_mixin import ParserMixin
from .plot_mixin import PlotMixin
from .processing_mixin import ProcessingMixin

class SAData(ParserMixin, ConversionMixin, PlotMixin, ProcessingMixin):
    """
    Clase para manejar datos de archivos .DAT generados por analizadores de espectro.

    Esta clase carga, parsea y almacena tanto los metadatos del header como los datos de medición
    en un objeto Python para su posterior análisis y procesamiento.
    """

    def __init__(self, file_path: str):
        """
        Inicializa el objeto de datos con la ruta al archivo .DAT

        Parameters:
        -----------
        file_path : str
            Ruta completa al archivo .DAT
        """
        self.file_path = file_path
        self.header_data: Dict[str, str] = {}
        self.data: Optional[Dict[str, np.ndarray]] = None
        self.n_points: Optional[int] = None
        
        # Inicializar mixin de procesamiento
        ProcessingMixin.__init__(self)

        # Parsear el archivo al inicializar
        self._parse_file()

    def get_header(self) -> Dict[str, str]:
        """
        Retorna los metadatos del header

        Returns:
        --------
        Dict[str, str]
            Diccionario con los parámetros del header
        """
        return self.header_data.copy()

    def get_data(self) -> Dict[str, np.ndarray]:
        """
        Retorna los datos de medición como arrays de NumPy

        Returns:
        --------
        Dict[str, np.ndarray]
            Diccionario con arrays NumPy para cada columna
        """
        if self.data is None:
            raise ValueError("No hay datos disponibles")
        return self.data.copy()

    def get_x_data(self) -> np.ndarray:
        """
        Retorna los datos del eje x

        Returns:
        --------
        np.ndarray
            Array con los valores del eje x
        """
        return self.data['x'].copy() if self.data else None

    def get_y1_data(self) -> np.ndarray:
        """
        Retorna los datos del primer canal y

        Returns:
        --------
        np.ndarray
            Array con los valores del primer canal y
        """
        return self.data['y1'].copy() if self.data else None

    def get_n_points(self) -> Optional[int]:
        """
        Retorna el número de puntos de datos

        Returns:
        --------
        Optional[int]
            Número de puntos o None si no está disponible
        """
        return self.n_points

    def get_data_shape(self) -> Tuple[int, int]:
        """
        Retorna la forma de los datos (puntos, canales)

        Returns:
        --------
        Tuple[int, int]
            (número_de_puntos, número_de_canales)
        """
        if self.data is None:
            return (0, 0)
        n_points = len(self.data['x'])
        # Solo tenemos 1 canal (y1)
        n_channels = 1
        return (n_points, n_channels)

    def __repr__(self) -> str:
        """Representación string del objeto"""
        if self.data is None:
            n_points = 0
            n_channels = 0
        else:
            n_points = len(self.data['x'])
            n_channels = 1  # Solo y1

        return (f"SAData(file_path='{self.file_path}', "
                f"header_params={len(self.header_data)}, "
                f"data_points={n_points}, "
                f"channels={n_channels})")

    def __str__(self) -> str:
        """Representación legible del objeto"""
        if self.data is None:
            n_points = 0
            n_channels = 0
            data_types = "N/A"
        else:
            n_points = len(self.data['x'])
            n_channels = 1  # Solo y1
            data_types = {key: str(arr.dtype) for key, arr in self.data.items()}

        return (f"SAData - Archivo: {self.file_path}\n"
                f"Parámetros del header: {len(self.header_data)}\n"
                f"Puntos de datos: {n_points}\n"
                f"Canales: {n_channels}\n"
                f"Tipos de datos: {data_types}")

# Función de conveniencia para crear instancias fácilmente
def load_sa_data(file_path: str) -> SAData:
    """
    Función de conveniencia para cargar datos de archivos de analizador de espectro

    Parameters:
    -----------
    file_path : str
        Ruta al archivo .DAT

    Returns:
    --------
    SAData
        Instancia con los datos cargados
    """
    return SAData(file_path)
