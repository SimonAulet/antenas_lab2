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
# # Preprocesado de los archivos
# Los archivos extraídos del analizador de espectro tienen una cobertura mayor ya que la tornamesa va de -190 a +190 grados con lo cual una partecita está superpuesta. También fué girada en distinto sentido en cada medición. El generador de RF fué configurado a 20dBm

# %% [markdown] jp-MarkdownHeadingCollapsed=true
# El orden el el siguiente
#
# | Número archivo | Polarización | Frecuencia | Pos. inicial | Pos final |
# |---------------|--------------|------------|--------------|---------------------|
# | 1 | Directa | 3.1GHz | -190 | +190 |
# | 2 | Directa | 2.7GHz | +190 | -190 |
# | 3 | Directa | 2.9GHz | -190 | +190 |
# | 4 | Cruzada | 2.7GHz | -190 | +190 |
# | 5 | Cruzada | 2.9GHz | +190 | -190 |
# | 6 | Cruzada | 3.1GHz | -190 | +190 |

# %% [markdown]
# Vamos a probar el espejado y guardado de archivos

# %%
from scripts.sa_data import SAData, load_sa_data

# %%
data = load_sa_data('./Mediciones/1ra med 31Ghz.DAT')

# %%
data.plot_time(mag='dB')

# %%
# Sin desplazamientos
#fig, ax = data.plot_superposition(mag='dBm')

# Con desplazamientos de 10° en ambos lados
#fig, ax = data.plot_superposition(mag='dBm', left_shift_deg=10, right_shift_deg=10)

# Solo desplazar lado derecho 15°
#fig, ax = data.plot_superposition(mag='dBm', right_shift_deg=15)

# Desplazar hacia adentro (negativo)
fig, ax = data.plot_superposition(mag='dBm', left_shift_deg=10, right_shift_deg=10)


# %%

# %%

# %%

# %%

# %%

# %%

# %%
from scripts.sa_data import SAData, load_sa_data

# %%

# %%
directa_2_7GHz = load_sa_data('./Mediciones/3ra med 27Ghz.DAT')

# %%
directa_2_7GHz.plot_polar()

# %%
piso_ruido         = load_sa_data('./data/File_001_PISO_DE_RUIDO2.DAT')
biantena_vertical1 = load_sa_data('./data/biantenavertical.DAT')#esta
biantena_vertical2 = load_sa_data('./data/File_001_biantena_vert.DAT')
biantena_vertical3 = load_sa_data('./data/2da_medicioon_de_antenavert.DAT')

biantena_horizontal1 = load_sa_data('./data/biantenhorz_001.DAT')#esta
biantena_horizontal2 = load_sa_data('./data/2da-medicion-horizontal_002.DAT')
biantena_horizontal3 = load_sa_data('./data/2da-medicion-horizontal_003.DAT')

# %%
piso_ruido2 = SAData('./data/File_001_PISO_DE_RUIDO2.DAT')

# %%
piso_ruido.plot_time(mag='dBm', y_limits=(-90, -70), legend=True, savefig='ploteos/piso_ruido.png',
                    figsize=(12, 3))

# %%
biantena_vertical1.plot_time(mag='dBm', legend=True, y_limits=(-60, -40), savefig='ploteos/biconica_vertical_1.png')
biantena_vertical1.plot_polar(mag='dB', legend=True, normalize=True, mag_limits=(-6, 3), savefig='ploteos/biconica_vertical_1_polar.png')

# %%
biantena_horizontal1.plot_time(mag='dBm', y_limits=(-70, -40), savefig='ploteos/biconica_horizontal_1.png')
biantena_horizontal1.plot_polar(mag='dB', mag_limits=(-39, 3), legend=True, savefig='ploteos/biconica_horizontal_1_polar.png')

# %%
biantena_vertical2.plot_time(mag='dBm', y_limits=(-60, -40), savefig='ploteos/biconica_vertical_2.png')
biantena_vertical2.plot_polar(mag='dBm', mag_limits=(-60, -40), savefig='ploteos/biconica_vertical_2_polar.png')

# %%
biantena_vertical3.plot_time(mag='dBm', legend=True, y_limits=(-60, -30))
#biantena_vertical3.plot_polar(mag='dBm', mag_limits=(-60, -30), savefigure='Ploteos/cambio_polarizacion.png')

# %% [markdown]
# Vamos a analizar la polarizaación cruzada. Para esto uso de los datos anteriores la medición en polarización cruzada y derecha

# %%
y = biantena_vertical3.get_y1_data()
x = biantena_vertical3.get_x_data()

# %%
import matplotlib.pyplot as plt
import numpy as np

# Ejemplo: si no los tenés definidos
# x = np.linspace(0,100,500)
# y = -50 + 10*np.sin(np.radians(x))

# Parámetros opcionales
plot_params = {'linewidth': 1.5, 'label': 'Medición'}
ax_params = {
    'title': 'Medicion de polarizacion cruzada',
    'xlabel': 'Ángulo [°]',
    'ylabel': 'Potencia [dBm]',
    'xlim': (min(x), max(x)),
    'ylim': (-60, -30)
}

# Crear figura y eje
fig, ax = plt.subplots(figsize=(8,6))

# Plot principal
ax.plot(x, y, **plot_params)

# Puntos de interés
targets = {20: "Polarización cruzada", 60: "Polarización co-polar"}
for xtarget, label in targets.items():
    idx = np.argmin(np.abs(x - xtarget))   # índice más cercano a xtarget
    x_val, y_val = x[idx], y[idx]

    # Línea vertical
    ax.axvline(x_val, color="red", linestyle="--", alpha=0.7)

    # Flecha + etiqueta con valor
    ax.annotate(f"{label}\n{y_val:.2f} dBm",
                xy=(x_val, y_val),            # punto en la curva
                xytext=(x_val+5, y_val+3),    # posición del texto
                arrowprops=dict(facecolor="black", arrowstyle="->"),
                fontsize=11,
                bbox=dict(boxstyle="round,pad=0.3", fc="w", ec="k", alpha=0.6))

# Configuración de ejes
ax.set_title(ax_params.get('title', 'Medición'), fontsize=14)
ax.set_xlabel(ax_params.get('xlabel', 'X'), fontsize=12)
ax.set_ylabel(ax_params.get('ylabel', 'Y'), fontsize=12)

if 'xlim' in ax_params:
    ax.set_xlim(ax_params['xlim'])
if 'ylim' in ax_params:
    ax.set_ylim(ax_params['ylim'])

ax.grid(True, which='both', linestyle='--', alpha=0.7)
ax.legend()

# Guardar imagen
plt.savefig('ploteos/polarizacion_cruzada.png', dpi=300, bbox_inches='tight')
plt.show()


# %%
biantena_horizontal2.plot_time(mag='dBm')
#biantena_horizontal2.plot_polar(mag='dBm')

# %%
biantena_horizontal3.plot_time(mag='dBm')
#biantena_horizontal3.plot_polar(mag='dBm')

# %%
biantena_vertical3.data['y1'].max()

# %% [markdown]
# # Comparativa para ganancia
# Voy a superponer dos gráficos para calcular la ganancia

# %%

# %%

# %%

# %%
