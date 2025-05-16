""" 
  Distribuciones a desarrollar
  - Uniforme
  - Exponencial
  - Gamma
  - Normal
  - Pascal
  - Binomial
  - Hipergeometrica
  - Poisson
  - Empirica Discreta 
"""

import random
from math import log, exp
from functools import partial
import numpy as np
from typing import Callable
import matplotlib.pyplot as plt

def uniforme(a, b):
  r = random.random()
  x = a + (b - a) * r
  return x

def exponencial(alfa):  #en el libro alfa es EX (que seria?)
  r = random.random()
  x = -alfa * log(r)
  return x

def gamma(k, alfa):
  tr = 0.1  #en el libro dice 1.0
  for i in range(k):
    r = random.random()
    tr = tr * r
  x = -log(tr) / alfa
  return x

def normal ( ex, stdx ):
  sum = 0.0
  for i in range (12): # el libro pide 12 pero por que ese valor
    r = random.random()
    sum = sum + r
  x = stdx *(sum - 6.0) + ex
  return x

def pascal(k ,q):
  tr = 1.0
  qr = log(q)
  for i in range(k):
    r = random.random()
    tr = tr * r
  nx = log(tr) / qr
  return nx

def binomial(n, p):
  x = 0.0
  for i in range(n):
    r = random.random()
    if r < p:
      x = x + 1.0
  return x

def hipergeometrica(tn, ns, p):
  x = 0.0
  for i in range(ns):
    r = random.random()
    if r < p:
      s = 1.0
      x = x + 1.0
    else:
      s = 0.0
    p = (tn * p - s) / (tn - 1.0)
    tn = tn - 1.0
  return x

def poisson(p):
  x = 0.0
  b = exp(-p)
  tr = 1.0
  r = random.random()
  tr = tr * r
  while (tr > b):
    x= x + 1.0
    r = random.random()
    tr = tr * r
  return x

def empirica_discreta(m, n, i, p): #en donde p es una matriz 10x10, x es una lista de 10 elementos
  x = []
  for k in range(m):
    x.append(0.0)
  for k in range(n):
    r = random.random()
    for j in range(m):
      if (p[i][j] > r):
        break
    i = j
    x[i] = x[i] + 1.0
  return x

def graficar(f : Callable, *args):
  y = []
  for i in range(5000):
    y.append(f(*args))
  y.sort()

  plt.hist(y, bins=50, color='#6DAEDB', edgecolor='black')
  plt.title(f"Distribucion_{nombre_funcion}")
  plt.xlabel('Valor')
  plt.ylabel('Frecuencia')
  plt.savefig(f"./TP 2.2/Distribucion_{nombre_funcion}.png")
  plt.clf()

if __name__ == "__main__":

  # Distribuciones con los generadores de numpy

  nombre_funcion = "Uniforme_Numpy"
  graficar(partial(np.random.uniform, 0, 1))
  

  nombre_funcion = "Exponencial_Numpy"
  graficar(partial(np.random.exponential, 1))

  nombre_funcion = "Gamma_Numpy"
  graficar(partial(np.random.gamma, 1, 1)) # mismo comportamiento que la exponencial

  nombre_funcion = "Normal_Numpy"
  graficar(partial(np.random.normal, 0, 1))

  nombre_funcion = "Pascal_Numpy"
  graficar(partial(np.random.negative_binomial, 1, 0.5)) # no se si es correcto

  nombre_funcion = "Binomial_Numpy"
  graficar(partial(np.random.binomial, 10, 0.5))

  nombre_funcion = "Hipergeometrica_Numpy"
  graficar(partial(np.random.hypergeometric, 10, 5, 5)) # parecido a la binomial

  nombre_funcion = "Poisson_Numpy"
  graficar(partial(np.random.poisson, 1))

  nombre_funcion = "Empirica Discreta_Numpy"
  graficar(partial(np.random.choice, [0, 1, 2, 3, 4], p=[0.1, 0.2, 0.3, 0.2, 0.2])) # esto ni idea

  # Distribuciones con los generadores programados

  nombre_funcion = "Uniforme"
  graficar(partial(uniforme, 0, 1))

  nombre_funcion = "Exponencial"
  graficar(partial(exponencial, 1))

  nombre_funcion = "Gamma"
  graficar(partial(gamma, 1, 1))

  nombre_funcion = "Normal"
  graficar(partial(normal, 0, 1))

  nombre_funcion = "Pascal"
  graficar(partial(pascal, 1, 0.5)) # se ve distinta a la de numpy

  nombre_funcion = "Binomial"
  graficar(partial(binomial, 10, 0.5))

  nombre_funcion = "Hipergeometrica"
  graficar(partial(hipergeometrica, 10, 5, 5)) # se ve distinta a la de numpy

  nombre_funcion = "Poisson"
  graficar(partial(poisson, 1))

  nombre_funcion = "Empirica Discreta"
  graficar(partial(empirica_discreta, [0, 1, 2, 3, 4], p=[0.1, 0.2, 0.3, 0.2, 0.2])) # esta falla, se tienen que arreglar los argumentos