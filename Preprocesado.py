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
# # Preprocesado de los archivos medidos
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

# %% [markdown]
# # Preprocesado de los archivos simulados
#
# Los archivos simulados tienen más información como la fase y el radio axial. Son archivos .txt con una fila por cada grado de medición. Se tienen las componentes $\theta$ que es el angulo que varía y $\phi$ que es el angulo fijo. $\theta$ varía de 0 a 180 y luego de 180 a 0 mientras que $\phi$ está fijo en 90 para la primer mitad y luego está fijo en 270. Esta variación complica la extracción ya que tengo datos repetidos en el eje $x$. Se llegaría al mismo resultado físico dejando $\phi$ fijo en 90 y variando $\theta$ de 0 a 360.<br>
# Entonces desestimo los valores de $\theta$ y de $\phi$ y genero un nuevo indice $t$ para el eje $x$, tomo los valores de $y$ como vienen y luego convierto $t$ a grados para los gráficos, que ya lo tengo implementado. El resultado es el mismo

# %% [markdown]
# Los valores a tomar para tener equivalencias con los archivos medidos son Abs(Horiz)[dBi] como polarización directa y Abs(Verti)[dBi] como polarización cruzada. Relación axial y fase los desestimo.
#
# La magnitud de los datos es $dBi$. En el resto de los ploteos uso $dB$ lo cual es poco claro ya que en verdad $dB$ se obtiene normalizando $dBm$. En cualquier caso, para  mantener consistencia, uso $dB$ normalizados los cuales consigo simplemente desplazando $dBi$ con la función ya implementada para $dBm$. No se pierde información. Que práctico es laburar de decibeles por favorrr
#
# El campo simulado es el campo magnético $H$ pero como se está en campo lejano y $H$ es proporcional a $E$, al estar los datos normalizados las representaciónes son iguales con lo cual tambien desestimo esto sin problema.

# %%
from scripts.sa_data import SAData, load_sa_data

# %% [markdown]
# ## Simulaciónes a 2.7GHz

# %%
from scripts.txt2dat import load_text_file

output_path = load_text_file(
    file_path='./simulaciones/originales/Diagrama_2_7GHz_PlanoHorizontal.txt',
    output_path='./simulaciones/',
    y_col=3, #Abs(horiz)[dBi   ]=pol directa
    start_row=3,
    end_row=363,
    y_unit='dBi',
    circular_shift=180
)


# %%
# !mv ./simulaciones/Diagrama_2_7GHz_PlanoHorizontal.DAT ./simulaciones/directa_2.7GHz.DAT

# %%
from scripts.txt2dat import load_text_file

output_path = load_text_file(
    file_path='./simulaciones/originales/Diagrama_2_7GHz_PlanoHorizontal.txt',
    output_path='./simulaciones/',
    y_col=5, #Abs(Verti)[dBi   ]=pol cruzada
    start_row=3,
    end_row=363,
    y_unit='dBi',
    circular_shift=180
)


# %%
# !mv ./simulaciones/Diagrama_2_7GHz_PlanoHorizontal.DAT ./simulaciones/cruzada_2.7GHz.DAT

# %% [markdown]
# ## Simulaciónes a 2.9GHz

# %%
from scripts.txt2dat import load_text_file

output_path = load_text_file(
    file_path='./simulaciones/originales/Diagrama_2_9GHz_PlanoHorizontal.txt',
    output_path='./simulaciones/',
    y_col=3, #Abs(horiz)[dBi   ]=pol directa
    start_row=3,
    end_row=363,
    y_unit='dBi',
    circular_shift=180
)


# %%
# !mv ./simulaciones/Diagrama_2_9GHz_PlanoHorizontal.DAT ./simulaciones/directa_2.9GHz.DAT

# %%
from scripts.txt2dat import load_text_file

output_path = load_text_file(
    file_path='./simulaciones/originales/Diagrama_2_9GHz_PlanoHorizontal.txt',
    output_path='./simulaciones/',
    y_col=5, #Abs(Verti)[dBi   ]=pol cruzada
    start_row=3,
    end_row=363,
    y_unit='dBi',
    circular_shift=180
)


# %%
# !mv ./simulaciones/Diagrama_2_9GHz_PlanoHorizontal.DAT ./simulaciones/cruzada_2.9GHz.DAT

# %% [markdown]
# ## Simulaciónes a 3.1GHz

# %%
from scripts.txt2dat import load_text_file

output_path = load_text_file(
    file_path='./simulaciones/originales/Diagrama_3_1GHz_PlanoHorizontal.txt',
    output_path='./simulaciones/',
    y_col=3, #Abs(horiz)[dBi   ]=pol directa
    start_row=3,
    end_row=363,
    y_unit='dBi',
    circular_shift=180
)


# %%
# !mv ./simulaciones/Diagrama_3_1GHz_PlanoHorizontal.DAT ./simulaciones/directa_3.1GHz.DAT

# %%
from scripts.txt2dat import load_text_file

output_path = load_text_file(
    file_path='./simulaciones/originales/Diagrama_3_1GHz_PlanoHorizontal.txt',
    output_path='./simulaciones/',
    y_col=5, #Abs(Verti)[dBi   ]=pol cruzada
    start_row=3,
    end_row=363,
    y_unit='dBi',
    circular_shift=180
)


# %%
# !mv ./simulaciones/Diagrama_3_1GHz_PlanoHorizontal.DAT ./simulaciones/cruzada_3.1GHz.DAT
