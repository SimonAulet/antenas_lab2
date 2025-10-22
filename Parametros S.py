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
import skrf as rf

# %%
simulados = rf.Network('./simulaciones/Parametros_S_Simulados.s2p')
medidos = rf.Network('./mediciones/Parametros_S_Medidos.s2p')

# %%
rf.stylely()

# %%
simulados

# %%
medidos

# %% [markdown]
# Recorto las frecuencias a 2.4 - 3.3 para que quede todo igualito
# %%
simulados = simulados['2.4-3.4ghz']
medidos = medidos['2.4-3.4ghz']
# %% [markdown]
# # Parametros medidos

# %% [markdown]
# ## Parametros S

# %%
import matplotlib.pyplot as plt

# %%
medidos.frequency.unit = 'ghz'
medidos.plot_s_db(n=0, m=0, label='S11', title='Parametros S medidos')
medidos.plot_s_db(n=1, m=0, label='S21')
plt.savefig('./ploteos/S_medidos.png')

# %%
frequencies = ['2.7ghz', '2.9ghz', '3.1ghz']
for freq in frequencies:
    s11 = medidos[freq].s_db[0, 0, 0]
    s21 = medidos[freq].s_db[0, 1, 0]
    print(f'S11 {freq.upper()}: {s11:.2f} dB')
    print(f'S21 {freq.upper()}: {s21:.2f} dB')
    print()

# %% [markdown]
# ## VSWR

# %%
medidos.plot_s_vswr(n=0, m=0, label='VSWR', title='VSWR medido')
plt.savefig('./ploteos/VSWR_medido')
# %%
frequencies = ['2.7ghz', '2.9ghz', '3.1ghz']
for freq in frequencies:
    s11 = medidos[freq].s_vswr[0, 0, 0]
    print(f'S11 {freq.upper()}: {s11:.2f} dB')

# %% [markdown]
# # Parametros Simulados

# %% [markdown]
# ## Parametros S

# %%
simulados.frequency.unit = 'ghz'
simulados.plot_s_db(n=0, m=0, label='S11', title='Parametros S simulados')
simulados.plot_s_db(n=1, m=0, label='S21')
plt.savefig('./ploteos/S_simulados.png')

# %%
frequencies = ['2.7ghz', '2.9ghz', '3.1ghz']
for freq in frequencies:
    s11 = simulados[freq].s_db[0, 0, 0]
    s21 = simulados[freq].s_db[0, 1, 0]
    print(f'S11 {freq.upper()}: {s11:.2f} dB')
    print(f'S21 {freq.upper()}: {s21:.2f} dB')
    print()

# %% [markdown]
# ## VSWR

# %%
simulados.plot_s_vswr(n=0, m=0, label='VSWR', title='VSWR simulado')
plt.savefig('./ploteos/VSWR_simulado')

# %%
frequencies = ['2.7ghz', '2.9ghz', '3.1ghz']
for freq in frequencies:
    s11 = simulados[freq].s_vswr[0, 0, 0]
    print(f'S11 {freq.upper()}: {s11:.2f} dB')
