 #Codigo

 import numpy as np
import random
import matplotlib.pyplot as plt
import sys
import getopt
import os
# --- Ingreso de parámetros por consola ---
argv = sys.argv[1:]
try:
opciones, args = getopt.getopt(argv, "c:n:e:", ["corridas=",
"tiradas=", "numero="])
for dato, valor in opciones:
if dato in ['-c', '--corridas']:
nro_corridas = int(valor)
if dato in ['-n', '--tiradas']:
nro_tiradas = int(valor)
if dato in ['-e', '--numero']:
nro_elegido = int(valor)

except:
print("Uso: ruleta.py -c <nro_corridas> -n <nro_tiradas> -e
<nro_elegido>")
sys.exit(1)
# --- Constantes teóricas ---
ar = np.arange(37)
frec_esperada = 1 / 37
prom_esperado = np.mean(ar)
varianza_esperada = np.var(ar)
desvio_esperado = np.std(ar)
# --- Inicialización de acumuladores ---
frec_relativa_acum, promedio_acum, desvio_acum, varianza_acum = [], [], [],
[]
corridas_tot = []
count_total_cero = count_total_pd = count_total_sd = count_total_td = 0
count_total_rojo = count_total_negro = count_total_verde = 0
# --- Colores ---
colors = ["#a855f7", "#c084fc", "#f97316", "#fdba74"] * ((nro_corridas //
4) + 1)
# --- Crear carpeta para guardar imágenes ---
os.makedirs("graficos", exist_ok=True)

# --- Definir números por color ---
rojos = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
negros = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}
# --- Bucle principal ---
for p in range(nro_corridas):
corrida = [np.random.randint(0, 37) for _ in range(nro_tiradas)]
corridas_tot.extend(corrida)
frec_abs = 0
count_cero = count_pd = count_sd = count_td = 0
count_rojo = count_negro = count_verde = 0
frec_relativa, promedio, desvio, varianza = [], [], [], []
for i in range(nro_tiradas):
valor = corrida[i]
if valor == nro_elegido:
frec_abs += 1
if valor == 0:
count_cero += 1
count_verde += 1
elif 1 <= valor <= 12:
count_pd += 1
elif 13 <= valor <= 24:
count_sd += 1
elif 25 <= valor <= 36:
count_td += 1
if valor in rojos:
count_rojo += 1
elif valor in negros:
count_negro += 1
frec_relativa.append(frec_abs / (i + 1))
promedio.append(np.mean(corrida[:i + 1]))
desvio.append(np.std(corrida[:i + 1]))
varianza.append(np.var(corrida[:i + 1]))
frec_relativa_acum.extend(frec_relativa)
promedio_acum.extend(promedio)
desvio_acum.extend(desvio)
varianza_acum.extend(varianza)
count_total_cero += count_cero
count_total_pd += count_pd

count_total_sd += count_sd
count_total_td += count_td
count_total_rojo += count_rojo
count_total_negro += count_negro
count_total_verde += count_verde
x_range = range(1, nro_tiradas + 1)
plt.figure(figsize=(8, 6))
plt.hist(corrida, bins=37, edgecolor="black", color="#a855f7")
plt.xlabel("Valores")
plt.ylabel("Frecuencia")
plt.title(f"Histograma - Corrida {p + 1}")
plt.savefig(f"graficos/Histograma_corrida_{p + 1}.png")
plt.clf()
plt.figure(figsize=(8, 6))
plt.pie([count_cero, count_pd, count_sd, count_td], labels=['CERO',
'PRIMERA', 'SEGUNDA', 'TERCERA'], autopct='%1.1f%%', colors=["#a855f7",
"#f97316", "#c084fc", "#fdba74"], textprops={'fontsize': 18})
plt.title(f'Distribución por Docena - Corrida {p + 1}')
plt.savefig(f"graficos/GraficoTorta_corrida_{p + 1}.png")
plt.clf()
plt.figure(figsize=(8, 6))
plt.pie([count_rojo, count_negro, count_verde], labels=['ROJO',
'NEGRO', 'VERDE'], autopct=lambda p: f'{p:.1f}%', colors=['red', 'black',
'green'], textprops={'fontsize': 18,'color': 'white'})
plt.title(f'Distribución por Color - Corrida {p + 1}')
plt.savefig(f"graficos/GraficoColor_corrida_{p + 1}.png")
plt.clf()
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.plot(x_range, frec_relativa, color='#f97316')
plt.axhline(y=frec_esperada, color='#a855f7', linestyle='--')
plt.title("Frecuencia Relativa")
plt.ylim(0, 0.1)
plt.subplot(2, 2, 2)
plt.plot(x_range, promedio, color='#f97316')
plt.axhline(y=prom_esperado, color='#a855f7', linestyle='--')
plt.title("Promedio")
plt.subplot(2, 2, 3)
plt.plot(x_range, varianza, color='#f97316')

plt.axhline(y=varianza_esperada, color='#a855f7', linestyle='--')
plt.title("Varianza")
plt.subplot(2, 2, 4)
plt.plot(x_range, desvio, color='#f97316')
plt.axhline(y=desvio_esperado, color='#a855f7', linestyle='--')
plt.title("Desvío Estándar")
plt.tight_layout()
plt.savefig(f"graficos/ParametrosCorrida_{p + 1}.png")
plt.clf()
plt.figure(figsize=(8, 6))
plt.pie([count_total_cero, count_total_pd, count_total_sd, count_total_td],
labels=['CERO', 'PRIMERA', 'SEGUNDA', 'TERCERA'], autopct='%1.1f%%',
colors=["#a855f7", "#f97316", "#c084fc", "#fdba74"], textprops={'fontsize':
18})
plt.title('Distribución por Docena - Total Corridas')
plt.savefig("graficos/GraficoTortaTotalCorridas.png")
plt.clf()
plt.figure(figsize=(8, 6))
plt.pie([count_total_rojo, count_total_negro, count_total_verde],
labels=['ROJO', 'NEGRO', 'VERDE'], autopct=lambda p: f'{p:.1f}%',
colors=['red', 'black', 'green'], textprops={'fontsize': 18,'color':
'white'})
plt.title('Distribución por Color - Total Corridas')
plt.savefig("graficos/GraficoColorTotalCorridas.png")
plt.clf()
x_range = range(1, nro_tiradas + 1)
plt.figure(figsize=(12, 8))
for i, datos in enumerate(zip(*[iter(frec_relativa_acum)] * nro_tiradas)):
plt.subplot(2, 2, 1)
plt.plot(x_range, datos, color=colors[i], alpha=0.7)
for i, datos in enumerate(zip(*[iter(promedio_acum)] * nro_tiradas)):
plt.subplot(2, 2, 2)
plt.plot(x_range, datos, color=colors[i], alpha=0.7)
for i, datos in enumerate(zip(*[iter(varianza_acum)] * nro_tiradas)):
plt.subplot(2, 2, 3)
plt.plot(x_range, datos, color=colors[i], alpha=0.7)
for i, datos in enumerate(zip(*[iter(desvio_acum)] * nro_tiradas)):

plt.subplot(2, 2, 4)
plt.plot(x_range, datos, color=colors[i], alpha=0.7)
plt.subplot(2, 2, 1)
plt.axhline(y=frec_esperada, color='#a855f7', linestyle='--')
plt.title("Frecuencia Relativa")
plt.ylim(0, 0.1)
plt.subplot(2, 2, 2)
plt.axhline(y=prom_esperado, color='#a855f7', linestyle='--')
plt.title("Promedio")
plt.subplot(2, 2, 3)
plt.axhline(y=varianza_esperada, color='#a855f7', linestyle='--')
plt.title("Varianza")
plt.subplot(2, 2, 4)
plt.axhline(y=desvio_esperado, color='#a855f7', linestyle='--')
plt.title("Desvío Estándar")
plt.tight_layout()
plt.savefig("graficos/ParametrosTiradasTotales.png")
plt.clf()
plt.figure(figsize=(8, 6))
plt.hist(corridas_tot, bins=np.arange(38), edgecolor='black',
color='#a855f7')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')
plt.title('Histograma Total de Tiradas')
plt.savefig("graficos/HistogramaTiradasTotales.png")
plt.clf()
# --- Resumen de las corridas ---
print("\nResumen general:")
print(f"Total de tiradas realizadas: {len(corridas_tot)}")
print(f"Frecuencia del número {nro_elegido}:
{corridas_tot.count(nro_elegido)} veces ({(corridas_tot.count(nro_elegido)
/ len(corridas_tot)) * 100:.2f}%)")
print("Gráficos guardados en la carpeta 'graficos/'.")
# --- Cálculos finales del número elegido ---
frec_total = corridas_tot.count(nro_elegido)
frec_relativa_total = frec_total / len(corridas_tot)
promedio_total = np.mean(corridas_tot)
varianza_total = np.var(corridas_tot)

desvio_total = np.std(corridas_tot)
print("\nEstadísticas generales del experimento:")
print(f"Frecuencia relativa del número {nro_elegido}:
{frec_relativa_total:.4f} ({frec_relativa_total*100:.2f}%)")
print(f"Promedio de todas las tiradas: {promedio_total:.2f}")
print(f"Varianza de todas las tiradas: {varianza_total:.2f}")
print(f"Desvío estándar de todas las tiradas: {desvio_total:.2f}")

"""
Consola
Resumen general:
Total de tiradas realizadas: 4000
Frecuencia del número 28: 118 veces (2.95%)
Gráficos guardados en la carpeta 'graficos/'.
Estadísticas generales del experimento:
Frecuencia relativa del número 28: 0.0295 (2.95%)
Promedio de todas las tiradas: 17.86
Varianza de todas las tiradas: 113.95
Desvío estándar de todas las tiradas: 10.67
"""
