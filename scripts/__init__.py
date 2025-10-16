# __init__.py - Package initialization for scripts module
# Autor: [Simón Aulet]
# Fecha: 2025-09-10

"""
Módulo scripts - Utilidades para procesamiento de datos de analizadores de espectro

Este módulo proporciona clases y funciones para trabajar con archivos .DAT
generados por analizadores de espectro Rohde & Schwarz.
"""

from .sa_data import SAData, load_sa_data
from .conversion_mixin import ConversionMixin
from .parser_mixin import ParserMixin

# Exportar las principales clases y funciones
__all__ = [
    'SAData',
    'load_sa_data',
    'ConversionMixin',
    'ParserMixin'
]

# Información del paquete
__version__ = '0.1.0'
__author__ = 'Simón Aulet'
__description__ = 'Herramientas para procesamiento de datos de analizadores de espectro'
