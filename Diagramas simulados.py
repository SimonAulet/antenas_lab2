# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import numpy as np

# Leer el archivo, saltando las primeras 2 líneas (encabezado y separador)
# Usamos sep='\s+' en lugar de delim_whitespace (deprecado)
df = pd.read_csv('./simulaciones/Diagrama_2_7GHz_PlanoHorizontal.txt',
                 sep=r'\s+',
                 skiprows=2,
                 header=None)

# Los datos estarán perfectamente estructurados en un DataFrame
print(df.head())
print(df.columns)


# %%
# Verificamos la estructura de los datos
print("Shape:", df.shape)
print("Info:")
print(df.info())

# %%
# Si las columnas no tienen nombres, podemos asignarles nombres manualmente
# basados en el encabezado original del archivo
column_names = [
    'Theta_deg',
    'Phi_deg',
    'Abs_Grlz_dBi',
    'Abs_Horiz_dBi',
    'Phase_Horiz_deg',
    'Abs_Verti_dBi',
    'Phase_Verti_deg',
    'Ax_Ratio_dB'
]

# Renombramos las columnas ya que estamos leyendo sin encabezado
df.columns = column_names
print("Columnas renombradas:")
print(df.columns)

# %%
# También podemos leer directamente con los nombres de columnas
# Esto es más robusto y evita problemas con el encabezado
df_clean = pd.read_csv('./simulaciones/Diagrama_2_7GHz_PlanoHorizontal.txt',
                       sep=r'\s+',
                       skiprows=2,  # Saltamos encabezado y línea de separación
                       names=column_names)

print("Datos leídos con nombres de columnas explícitos:")
print(df_clean.head())
print(df_clean.columns)

# %%
df
