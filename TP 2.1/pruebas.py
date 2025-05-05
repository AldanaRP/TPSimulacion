import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math

def prueba_frecuencia(numeros, bins=10, nivel=0.05):
    """
    Prueba de frecuencia para verificar si los números están distribuidos uniformemente.
    
    Args:
        numeros: Lista de números pseudoaleatorios en [0,1)
        bins: Número de intervalos para dividir [0,1)
        nivel: Nivel de significancia para la prueba
    
    Returns:
        dict: Resultado de la prueba conteniendo estadístico, p-valor y resultado
    """
    n = len(numeros)
    intervalos = np.linspace(0, 1, bins + 1)
    observado, _ = np.histogram(numeros, bins=intervalos)
    
    # Frecuencia esperada para una distribución uniforme
    esperado = np.full(bins, n/bins)
    
    # Calculamos chi-cuadrado
    chi2, p_valor = stats.chisquare(observado, esperado)
    
    # El resultado es OK si p_valor > nivel
    resultado = "OK" if p_valor > nivel else "ERROR"
    
    return {
        "estadistico": chi2,
        "p_valor": p_valor,
        "resultado": resultado
    }

def prueba_series(numeros, bins=10, nivel=0.05):
    """
    Prueba de series para verificar la independencia de pares consecutivos.
    
    Args:
        numeros: Lista de números pseudoaleatorios en [0,1)
        bins: Número de intervalos para dividir [0,1) en cada dimensión
        nivel: Nivel de significancia para la prueba
    
    Returns:
        dict: Resultado de la prueba conteniendo estadístico, p-valor y resultado
    """
    n = len(numeros) - 1  # Un par menos que la cantidad de números
    
    # Crear pares de números consecutivos
    pares = np.array([(numeros[i], numeros[i+1]) for i in range(n)])
    
    # Dividir el espacio [0,1) x [0,1) en bins x bins celdas
    intervalos = np.linspace(0, 1, bins + 1)
    H, _, _ = np.histogram2d(pares[:, 0], pares[:, 1], bins=[intervalos, intervalos])
    
    # Frecuencia esperada para cada celda
    esperado = n / (bins * bins)
    
    # Aplanar la matriz para realizar la prueba chi-cuadrado
    observado = H.flatten()
    esperado_array = np.full(bins * bins, esperado)
    
    # Calculamos chi-cuadrado (ignorando las celdas con frecuencia esperada muy baja)
    valid_indices = esperado_array >= 5
    
    if np.sum(valid_indices) > 0:
        chi2, p_valor = stats.chisquare(observado[valid_indices], esperado_array[valid_indices])
    else:
        # Si todas las celdas tienen frecuencia esperada muy baja, aproximamos
        chi2 = np.sum((observado - esperado_array) ** 2 / esperado_array)
        # Grados de libertad: (bins*bins - 1)
        p_valor = 1 - stats.chi2.cdf(chi2, (bins*bins - 1))
    
    # El resultado es OK si p_valor > nivel
    resultado = "OK" if p_valor > nivel else "ERROR"
    
    return {
        "estadistico": chi2,
        "p_valor": p_valor,
        "resultado": resultado
    }

def prueba_rachas(numeros, nivel=0.05):
    """
    Prueba de rachas para verificar la aleatoriedad de la secuencia.
    
    Args:
        numeros: Lista de números pseudoaleatorios en [0,1)
        nivel: Nivel de significancia para la prueba
    
    Returns:
        dict: Resultado de la prueba conteniendo estadístico, p-valor y resultado
    """
    n = len(numeros)
    
    # Convertir los números a una secuencia binaria (sobre/bajo la mediana)
    mediana = 0.5  # Para una distribución uniforme en [0,1)
    secuencia = ['1' if x >= mediana else '0' for x in numeros]
    secuencia_str = ''.join(secuencia)
    
    # Contar rachas
    rachas = 1
    for i in range(1, n):
        if secuencia[i] != secuencia[i-1]:
            rachas += 1
    
    # Contar n1 (ceros) y n2 (unos)
    n1 = secuencia.count('0')
    n2 = secuencia.count('1')
    
    # Valor esperado y varianza para la cantidad de rachas
    esperado = 1 + (2 * n1 * n2) / n
    varianza = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n * n * (n - 1))
    
    # Estadístico Z
    if varianza > 0:
        z = (rachas - esperado) / np.sqrt(varianza)
        p_valor = 2 * (1 - stats.norm.cdf(abs(z)))  # Prueba de dos colas
    else:
        z = 0
        p_valor = 1
    
    # El resultado es OK si p_valor > nivel
    resultado = "OK" if p_valor > nivel else "ERROR"
    
    return {
        "estadistico": z,
        "p_valor": p_valor,
        "resultado": resultado
    }

def prueba_chi_cuadrado(numeros, bins=10, nivel=0.05):
    """
    Prueba chi-cuadrado para verificar la bondad de ajuste a una distribución uniforme.
    
    Args:
        numeros: Lista de números pseudoaleatorios en [0,1)
        bins: Número de intervalos para dividir [0,1)
        nivel: Nivel de significancia para la prueba
    
    Returns:
        dict: Resultado de la prueba conteniendo estadístico, p-valor y resultado
    """
    # Esta prueba es similar a la prueba de frecuencia pero más general
    n = len(numeros)
    intervalos = np.linspace(0, 1, bins + 1)
    observado, _ = np.histogram(numeros, bins=intervalos)
    
    # Frecuencia esperada para una distribución uniforme
    esperado = np.full(bins, n/bins)
    
    # Calculamos chi-cuadrado
    chi2, p_valor = stats.chisquare(observado, esperado)
    
    # Grados de libertad
    grados_libertad = bins - 1
    
    # Valor crítico
    valor_critico = stats.chi2.ppf(1 - nivel, grados_libertad)
    
    # El resultado es OK si chi2 <= valor_critico
    resultado = "OK" if chi2 <= valor_critico else "ERROR"
    
    return {
        "estadistico": chi2,
        "p_valor": p_valor,
        "valor_critico": valor_critico,
        "resultado": resultado
    }

def graficar_distribucion(numeros, generador_nombre, bins=20):
    """
    Crea un histograma para visualizar la distribución de los números.
    
    Args:
        numeros: Lista de números pseudoaleatorios en [0,1)
        generador_nombre: Nombre del generador
        bins: Número de intervalos para el histograma
    """
    plt.figure(figsize=(10, 6))
    plt.hist(numeros, bins=bins, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title(f'Distribución de números pseudoaleatorios - {generador_nombre}')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.grid(True, alpha=0.3)
    plt.savefig(f'distribucion_{generador_nombre}.png')
    plt.close()

def graficar_series(numeros, generador_nombre, bins=20):
    """
    Crea un gráfico de dispersión para visualizar pares consecutivos.
    
    Args:
        numeros: Lista de números pseudoaleatorios en [0,1)
        generador_nombre: Nombre del generador
        bins: Número de intervalos para la densidad
    """
    x = numeros[:-1]  # Todos menos el último
    y = numeros[1:]   # Todos menos el primero
    
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, alpha=0.5, s=5)
    plt.title(f'Prueba de series - {generador_nombre}')
    plt.xlabel('ri')
    plt.ylabel('ri+1')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.savefig(f'series_{generador_nombre}.png')
    plt.close()

if __name__ == "__main__":
    # Este código se ejecutará si el script se corre directamente
    # Ejemplo con números aleatorios de Python
    from random import random
    
    # Generar secuencia de prueba
    n = 10000
    numeros = [random() for _ in range(n)]
    
    # Realizar las pruebas
    print("Prueba de frecuencia:", prueba_frecuencia(numeros))
    print("Prueba de series:", prueba_series(numeros))
    print("Prueba de rachas:", prueba_rachas(numeros))
    print("Prueba chi-cuadrado:", prueba_chi_cuadrado(numeros))
    
    # Generar gráficos
    graficar_distribucion(numeros, "Python Random")
    graficar_series(numeros, "Python Random")