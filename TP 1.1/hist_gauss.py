import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os

nro_corridas = 500
nro_tiradas = 1000
medias = []
resultados = []

os.makedirs("./TP 1.1/graficos", exist_ok=True)

for _ in range(nro_corridas):
    corrida = np.random.randint(0, 37, nro_tiradas)
    resultados.extend(corrida)
    medias.append(np.mean(corrida))

plt.figure(figsize=(8, 6))
count, bins, _ = plt.hist(medias, bins=20, density=True, color='#a855f7', edgecolor='black', label='Dist. de medias')
mu_means, std_means = np.mean(medias), np.std(medias)
x = np.linspace(min(medias), max(medias), 1000)
p = stats.norm.pdf(x, mu_means, std_means)
plt.plot(x, p, 'k', linewidth=2, label='Dist. de Gauss')
plt.title('Histograma de medias con dist. de Gauss')
plt.xlabel('Media del resultado')
plt.ylabel('Densidad')
plt.legend()
plt.tight_layout()
plt.savefig("./TP 1.1/graficos/Histograma_medias_gauss.png")
plt.clf()