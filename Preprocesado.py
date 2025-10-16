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
# | 2 | Directa | 2.9GHz | +190 | -190 |
# | 3 | Directa | 2.7GHz | -190 | +190 |
# | 4 | Cruzada | 2.7GHz | -190 | +190 |
# | 5 | Cruzada | 2.9GHz | +190 | -190 |
# | 6 | Cruzada | 3.1GHz | -190 | +190 |

# %% [markdown]
# Preprocesado de archivos para recortar el angulo extra de 10° por lado y espejar las mediciones con la tornamesa en posición inicial positiva y final negativa.<br>
# Como el disparo de los instrumentos se hizo a mano me doy un margen de 50° para recortar las mediciónes por desvios de error humano

# %%
from scripts.sa_data import SAData, load_sa_data

# %%
medicion_1 = load_sa_data('./Mediciones/Originales/1ra med 31Ghz.DAT')
medicion_2 = load_sa_data('./Mediciones/Originales/2da med 29Ghz.DAT')
medicion_3 = load_sa_data('./Mediciones/Originales/3ra med 27Ghz.DAT')
medicion_4 = load_sa_data('./Mediciones/Originales/4ta med 27Ghz.DAT')
medicion_5 = load_sa_data('./Mediciones/Originales/5ta med 29Ghz cruz.DAT')
medicion_6 = load_sa_data('./Mediciones/Originales/6ta med 31Ghz cruz.DAT')
medicion_7 = load_sa_data('./Mediciones/Originales/7ma med piso ruido.DAT')

# %% [markdown]
# ## Medicion 1: Polarizacion directa, secuencia directa, 3.1GHz

# %%
crop_data_1 = medicion_1.plot_superposition(left_shift_deg=15, right_shift_deg=20)

# %%
medicion_1.crop_data(**crop_data_1)

# %%
medicion_1.set_output_filename('directa_3.1GHz')

# %%
medicion_1.save_processed_data(output_dir='Mediciones/')

# %% [markdown]
# ## Medicion 2: Polarizacion directa, secuencia espejada, 2.9GHz

# %%
crop_data_2 = medicion_2.plot_superposition(left_shift_deg=0, right_shift_deg=45)

# %%
medicion_2.crop_data(**crop_data_2)

# %%
medicion_2.mirror_data()

# %%
medicion_2.set_output_filename('directa_2.9GHz')

# %%
medicion_2.save_processed_data(output_dir='Mediciones/')

# %% [markdown]
# ## Medicion 3: Polarizacion directa, secuencia directa, 2.7GHz

# %%
crop_data_3 = medicion_3.plot_superposition(left_shift_deg=30, right_shift_deg=10)

# %%
medicion_3.crop_data(**crop_data_3)

# %%
medicion_3.set_output_filename('directa_2.7GHz')

# %%
medicion_3.save_processed_data(output_dir='Mediciones/')

# %% [markdown]
# ## Medicion 4: Polarizacion cruzada, secuencia directa, 2.7GHz

# %%
crop_data_4 = medicion_4.plot_superposition(left_shift_deg=0, right_shift_deg=40)

# %%
medicion_4.crop_data(**crop_data_4)

# %%
medicion_4.set_output_filename('cruzada_2.7GHz')

# %%
medicion_4.save_processed_data(output_dir='Mediciones/')

# %% [markdown]
# ## Medicion 5: Polarizacion cruzada, secuencia espejada, 2.9GHz

# %%
crop_data_5 = medicion_5.plot_superposition(left_shift_deg=15, right_shift_deg=5)

# %%
medicion_5.crop_data(**crop_data_5)

# %%
medicion_5.mirror_data()

# %%
medicion_5.set_output_filename('cruzada_2.9GHz')

# %%
medicion_5.save_processed_data(output_dir='Mediciones/')

# %% [markdown]
# ## Medicion 6: Polarizacion cruzada, secuencia directa, 3.1GHz

# %%
crop_data_6 = medicion_6.plot_superposition(left_shift_deg=10, right_shift_deg=10)

# %%
medicion_6.crop_data(**crop_data_6)

# %%
medicion_6.set_output_filename('cruzada_3.1GHz')

# %%
medicion_6.save_processed_data(output_dir='Mediciones/')

# %% [markdown]
# ## Medicion 7 Piso de ruido

# %% [markdown]
# Copio directamente archivo renombrandolo a `piso_ruido.DAT`
