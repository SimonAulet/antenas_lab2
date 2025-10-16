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

# %% [markdown]
# # Ploteos
# Ploteo los datos pre-procesados de las mediciones

# %%
from scripts.sa_data import SAData, load_sa_data

# %%
directa_27 = load_sa_data('./Mediciones/directa_2.7GHz.DAT')
directa_29 = load_sa_data('./Mediciones/directa_2.9GHz.DAT')
directa_31 = load_sa_data('./Mediciones/directa_3.1GHz.DAT')
cruzada_27 = load_sa_data('./Mediciones/cruzada_2.7GHz.DAT')
cruzada_29 = load_sa_data('./Mediciones/cruzada_2.9GHz.DAT')
cruzada_31 = load_sa_data('./Mediciones/cruzada_3.1GHz.DAT')

# %%
directa_27.plot_deg(mag='dBm', y_limits=(-80, -30), min_deg=-180, max_deg=180, savefig='Ploteos/directa_2.7GHz_dBm.png', title='Polarizacion directa 2.7GHz')
directa_27.plot_deg(mag='dB', min_deg=-180, max_deg=180, savefig='Ploteos/directa_2.7GHz_dB.png', title='Polarizacion directa 2.7GHz')
directa_27.plot_polar(savefig='Ploteos/directa_2.7GHz_polar.png', title='Polarizacion directa 2.7GHz')

# %%
directa_29.plot_deg(mag='dBm', y_limits=(-80, -30), min_deg=-180, max_deg=180, savefig='Ploteos/directa_2.9GHz_dBm.png', title='Polarización Directa 2.9 GHz - dBm')
directa_29.plot_deg(mag='dB', min_deg=-180, max_deg=180, savefig='Ploteos/directa_2.9GHz_dB.png', title='Polarización Directa 2.9 GHz - dB')
directa_29.plot_polar(savefig='Ploteos/directa_2.9GHz_polar.png', title='Polarización Directa 2.9 GHz - Polar')

# %%
directa_31.plot_deg(mag='dBm', y_limits=(-80, -30), min_deg=-180, max_deg=180, savefig='Ploteos/directa_3.1GHz_dBm.png', title='Polarización Directa 3.1 GHz - dBm')
directa_31.plot_deg(mag='dB', min_deg=-180, max_deg=180, savefig='Ploteos/directa_3.1GHz_dB.png', title='Polarización Directa 3.1 GHz - dB')
directa_31.plot_polar(savefig='Ploteos/directa_3.1GHz_polar.png', title='Polarización Directa 3.1 GHz - Polar')

# %%
cruzada_27.plot_deg(mag='dBm', y_limits=(-80, -30), min_deg=-180, max_deg=180, savefig='Ploteos/cruzada_2.7GHz_dBm.png', title='Polarización Cruzada 2.7 GHz - dBm')
cruzada_27.plot_deg(mag='dB', min_deg=-180, max_deg=180, savefig='Ploteos/cruzada_2.7GHz_dB.png', title='Polarización Cruzada 2.7 GHz - dB')
cruzada_27.plot_polar(savefig='Ploteos/cruzada_2.7GHz_polar.png', title='Polarización Cruzada 2.7 GHz - Polar')

# %%
cruzada_29.plot_deg(mag='dBm', y_limits=(-80, -30), min_deg=-180, max_deg=180, savefig='Ploteos/cruzada_2.9GHz_dBm.png', title='Polarización Cruzada 2.9 GHz - dBm')
cruzada_29.plot_deg(mag='dB', min_deg=-180, max_deg=180, savefig='Ploteos/cruzada_2.9GHz_dB.png', title='Polarización Cruzada 2.9 GHz - dB')
cruzada_29.plot_polar(savefig='Ploteos/cruzada_2.9GHz_polar.png', title='Polarización Cruzada 2.9 GHz - Polar')


# %%
cruzada_31.plot_deg(mag='dBm', y_limits=(-80, -30), min_deg=-180, max_deg=180, savefig='Ploteos/cruzada_3.1GHz_dBm.png', title='Polarización Cruzada 3.1 GHz - dBm')
cruzada_31.plot_deg(mag='dB', min_deg=-180, max_deg=180, savefig='Ploteos/cruzada_3.1GHz_dB.png', title='Polarización Cruzada 3.1 GHz - dB')
cruzada_31.plot_polar(savefig='Ploteos/cruzada_3.1GHz_polar.png', title='Polarización Cruzada 3.1 GHz - Polar')

# %% [markdown]
# # Ploteos superpuestos

# %% [markdown]
# Ploteo superpuesto similar al del informe

# %%
directas_db = {'deg': directa_27.convert_to_degree(min_deg=-180, max_deg=180), '2.7GHz': directa_27.convert_to_dBm(), '2.9GHz': directa_29.convert_to_dBm(), '3.1GHz': directa_31.convert_to_dBm()}

# %%
cruzadas_db = {'deg': cruzada_27.convert_to_degree(min_deg=-180, max_deg=180), '2.7GHz': cruzada_27.convert_to_dBm(), '2.9GHz': cruzada_29.convert_to_dBm(), '3.1GHz': cruzada_31.convert_to_dBm()}

# %% [markdown]
# Por el recorte los ejes quedaron de distinta longitud. Normalizo promediando datos en el medio cuando no hay

# %%
# Normalización de ejes X para igualar dimensiones
import numpy as np
from scipy.interpolate import interp1d

def normalizar_ejes(datos_dict):
    """
    Normaliza todos los arrays al mismo tamaño usando interpolación lineal

    Parameters:
    -----------
    datos_dict : dict
        Diccionario con datos a normalizar

    Returns:
    --------
    dict
        Diccionario con arrays normalizados al mismo tamaño
    """
    # Encontrar el tamaño máximo entre todos los arrays
    tamanos = [len(datos_dict[key]) for key in datos_dict.keys() if key != 'deg']
    max_tamano = max(tamanos)

    # Crear nuevo diccionario normalizado
    datos_norm = {}

    # Para cada frecuencia, interpolar al tamaño máximo
    for key in datos_dict.keys():
        if key == 'deg':
            # Para el eje de grados, crear nuevo rango del tamaño máximo
            datos_norm[key] = np.linspace(np.min(datos_dict[key]), np.max(datos_dict[key]), max_tamano)
        else:
            # Para los datos de potencia, interpolar linealmente
            x_original = np.linspace(0, 1, len(datos_dict[key]))
            x_nuevo = np.linspace(0, 1, max_tamano)

            interpolador = interp1d(x_original, datos_dict[key], kind='linear', fill_value='extrapolate')
            datos_norm[key] = interpolador(x_nuevo)

    return datos_norm

# Aplicar normalización a ambos diccionarios
directas_db_norm = normalizar_ejes(directas_db)
cruzadas_db_norm = normalizar_ejes(cruzadas_db)

print(f"Tamaños originales directas: {[len(directas_db[key]) for key in directas_db.keys() if key != 'deg']}")
print(f"Tamaños originales cruzadas: {[len(cruzadas_db[key]) for key in cruzadas_db.keys() if key != 'deg']}")
print(f"Tamaño normalizado: {len(directas_db_norm['2.7GHz'])}")

# %%
import matplotlib.pyplot as plt
import numpy as np

# Ploteo 1: Polarizaciones directas con las tres frecuencias superpuestas
plt.figure(figsize=(12, 12))
plt.plot(directas_db_norm['deg'], directas_db_norm['2.7GHz'], 'r-', linewidth=2, label='2.7 GHz')
plt.plot(directas_db_norm['deg'], directas_db_norm['2.9GHz'], 'b-', linewidth=2, label='2.9 GHz')
plt.plot(directas_db_norm['deg'], directas_db_norm['3.1GHz'], 'k-', linewidth=2, label='3.1 GHz')

plt.title('Diagramas de Radiación - Polarización Directa', fontsize=14)
plt.xlabel('Ángulo [deg]', fontsize=12)
plt.ylabel('Potencia [dB]', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('./Ploteos/directa.png',dpi=300)
plt.show()

# %%
# Ploteo 2: Polarizaciones cruzadas con las tres frecuencias superpuestas
plt.figure(figsize=(12, 12))
plt.plot(cruzadas_db_norm['deg'], cruzadas_db_norm['2.7GHz'], 'r-', linewidth=2, label='2.7 GHz')
plt.plot(cruzadas_db_norm['deg'], cruzadas_db_norm['2.9GHz'], 'b-', linewidth=2, label='2.9 GHz')
plt.plot(cruzadas_db_norm['deg'], cruzadas_db_norm['3.1GHz'], 'k-', linewidth=2, label='3.1 GHz')

plt.title('Diagramas de Radiación - Polarización Cruzada', fontsize=14)
plt.ylim(-80, -30)
plt.xlabel('Ángulo [deg]', fontsize=12)
plt.ylabel('Potencia [dBi]', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('./Ploteos/cruzada.png',dpi=300)
plt.show()

# %%

# Ploteo 3: Comparación directas vs cruzadas para las tres frecuencias
plt.figure(figsize=(12, 12))

# 2.7 GHz
plt.plot(directas_db_norm['deg'], directas_db_norm['2.7GHz'], 'r-', linewidth=2, label='Directa 2.7 GHz')
plt.plot(cruzadas_db_norm['deg'], cruzadas_db_norm['2.7GHz'], 'r--', linewidth=2, label='Cruzada 2.7 GHz')

# 2.9 GHz
plt.plot(directas_db_norm['deg'], directas_db_norm['2.9GHz'], 'b-', linewidth=2, label='Directa 2.9 GHz')
plt.plot(cruzadas_db_norm['deg'], cruzadas_db_norm['2.9GHz'], 'b--', linewidth=2, label='Cruzada 2.9 GHz')

# 3.1 GHz
plt.plot(directas_db_norm['deg'], directas_db_norm['3.1GHz'], 'k-', linewidth=2, label='Directa 3.1 GHz')
plt.plot(cruzadas_db_norm['deg'], cruzadas_db_norm['3.1GHz'], 'k--', linewidth=2, label='Cruzada 3.1 GHz')

plt.title('Comparación Polarización Directa vs Cruzada', fontsize=14)
plt.xlabel('Ángulo [deg]', fontsize=12)
plt.ylabel('Potencia [dBi]', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('./Ploteos/completo.png',dpi=300)
plt.show()


