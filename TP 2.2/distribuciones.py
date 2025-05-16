"""
Distribuciones a desarrollar y testear:
- Uniforme
- Exponencial
- Gamma
- Normal
- Pascal (Binomial Negativa)
- Binomial
- Hipergeométrica
- Poisson
- Empírica Discreta
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from math import log, exp
from functools import partial
from typing import Callable

#Generadores Manuales
def uniforme(a, b):
    r = random.random()
    return a + (b - a) * r

def exponencial(alfa):
    r = random.random()
    return -alfa * log(r)

def gamma(k, alfa):
    tr = 1.0
    for _ in range(k):
        tr *= random.random()
    return -log(tr) / alfa

def normal(ex, stdx):
    sum_r = sum(random.random() for _ in range(12))
    return stdx * (sum_r - 6.0) + ex

def pascal(k, q):
    tr = 1.0
    for _ in range(k):
        tr *= random.random()
    return log(tr) / log(q)

def binomial(n, p):
    return sum(1 for _ in range(n) if random.random() < p)

def hipergeometrica(tn, ns, p):
    x = 0
    for _ in range(ns):
        r = random.random()
        s = 1 if r < p else 0
        x += s
        p = (tn * p - s) / (tn - 1)
        tn -= 1
    return x

def poisson(lam):
    x = 0
    b = exp(-lam)
    tr = 1.0
    while tr > b:
        tr *= random.random()
        x += 1
    return x - 1

def empirica_discreta(valores, probas):
    r = random.random()
    acumulada = 0.0
    for v, p in zip(valores, probas):
        acumulada += p
        if r < acumulada:
            return v
    return valores[-1]

def graficar(f: Callable, *args, nombre="Distribucion", bins=50):
    datos = [f(*args) for _ in range(5000)]
    plt.hist(datos, bins=bins, density=True, alpha=0.6, color="#DB6DDB", edgecolor='black')
    plt.title(nombre)
    plt.xlabel('Valor')
    plt.ylabel('Densidad')
    plt.grid(True)

    ruta = f"Distribucion_{nombre}.png"
    plt.savefig(ruta)
    print(f"Gráfico guardado en: {ruta}")
    plt.clf()

if __name__ == "__main__":

    # Numpy
    graficar(np.random.uniform, 0, 1, nombre="Uniforme_Numpy")
    graficar(np.random.exponential, 1, nombre="Exponencial_Numpy")
    graficar(np.random.gamma, 1, 1, nombre="Gamma_Numpy")
    graficar(np.random.normal, 0, 1, nombre="Normal_Numpy")
    graficar(np.random.negative_binomial, 1, 0.5, nombre="Pascal_Numpy")
    graficar(np.random.binomial, 10, 0.5, nombre="Binomial_Numpy")
    graficar(np.random.hypergeometric, 10, 5, 5, nombre="Hipergeometrica_Numpy")
    graficar(np.random.poisson, 1, nombre="Poisson_Numpy")
    graficar(partial(np.random.choice, [0, 1, 2, 3, 4], p=[0.1, 0.2, 0.3, 0.2, 0.2]), nombre="Empirica_Discreta_Numpy")

    # Manuales
    graficar(uniforme, 0, 1, nombre="Uniforme")
    graficar(exponencial, 1, nombre="Exponencial")
    graficar(gamma, 2, 1, nombre="Gamma")
    graficar(normal, 0, 1, nombre="Normal")
    graficar(pascal, 2, 0.5, nombre="Pascal")
    graficar(binomial, 10, 0.5, nombre="Binomial")
    graficar(hipergeometrica, 20, 5, 0.5, nombre="Hipergeometrica")
    graficar(poisson, 1, nombre="Poisson")
    graficar(empirica_discreta, [0, 1, 2, 3, 4], [0.1, 0.2, 0.3, 0.2, 0.2], nombre="Empirica_Discreta")
