import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import time
from tabulate import tabulate

# Importar los generadores implementados
from generadores import GeneradorGCL, GeneradorCuadrados

# Importar las pruebas
from pruebas import (
    prueba_frecuencia, 
    prueba_series, 
    prueba_rachas, 
    prueba_chi_cuadrado,
    prueba_frecuencia_monobit,
    graficar_distribucion,
    graficar_series
)

def cargar_numeros_desde_csv(archivo_csv="random_org_numeros.csv"):
    """Carga los números aleatorios desde un archivo CSV"""
    try:
        df = pd.read_csv(archivo_csv, header=None)
        return df[0].tolist()
    except FileNotFoundError:
        raise Exception(f"El archivo {archivo_csv} no se encuentra.")

def generar_numeros_python(n):
    """Genera n números aleatorios usando el generador de Python"""
    return list(random.random() for _ in range(n))

def generar_numeros_numpy(n):
    """Genera n números aleatorios usando NumPy"""
    return np.random.random(n).tolist()

def medir_tiempo(funcion, *args):
    """Mide el tiempo de ejecución de una función"""
    inicio = time.time()
    resultado = funcion(*args)
    fin = time.time()
    return resultado, fin - inicio

def ejecutar_pruebas(generador, nombre, n, bins=20):
    """
    Ejecuta todas las pruebas sobre un generador y retorna los resultados.
    
    Args:
        generador: Función o método que genera n números aleatorios
        nombre: Nombre del generador
        n: Cantidad de números a generar
        bins: Número de intervalos para las pruebas
    
    Returns:
        dict: Resultados de las pruebas
    """
    # Generar números y medir tiempo
    if callable(generador):
        numeros, tiempo = medir_tiempo(generador, n)
    else:
        inicio = time.time()
        numeros = generador.generar_secuencia(n)
        tiempo = time.time() - inicio
    
    # Realizar pruebas
    resultado_monobit = prueba_frecuencia_monobit(numeros)
    resultado_frecuencia = prueba_frecuencia(numeros, bins=bins)
    resultado_series = prueba_series(numeros, bins=bins)
    resultado_rachas = prueba_rachas(numeros)
    resultado_chi2 = prueba_chi_cuadrado(numeros, bins=bins)
    
    # Generar gráficos
    graficar_distribucion(numeros, nombre, bins=bins)
    graficar_series(numeros, nombre, bins=bins)
    
    return {
        "nombre": nombre,
        "tiempo": tiempo,
        "monobit": resultado_monobit,
        "frecuencia": resultado_frecuencia,
        "series": resultado_series,
        "rachas": resultado_rachas,
        "chi2": resultado_chi2
    }

def comparar_generadores(n=10000, bins=20):
    """
    Compara diferentes generadores pseudoaleatorios.
    
    Args:
        n: Cantidad de números a generar
        bins: Número de intervalos para las pruebas
    
    Returns:
        pd.DataFrame: Tabla con los resultados
    """
    # Crear generadores
    gcl_1 = GeneradorGCL(semilla=12345, a=1664525, c=1013904223, m=2**32)  # Parámetros buenos
    gcl_2 = GeneradorGCL(semilla=12345, a=65539, c=0, m=2**31)  # RANDU (parámetros malos)
    cuadrados = GeneradorCuadrados(semilla=9731, digitos=4) # Semilla que no decae a cero, repite valores

    try:
        numeros_random_org = cargar_numeros_desde_csv()
    except Exception as e:
        print(e)
        return pd.DataFrame()
    
    # Lista de generadores a comparar
    generadores = [
        (lambda n: numeros_random_org, "Random_org"),
        (gcl_1, "GCL (buenos parámetros)"),
        (gcl_2, "GCL (RANDU)"),
        (cuadrados, "Cuadrados Medios"),
        (generar_numeros_python, "Python_random"),
        (generar_numeros_numpy, "NumPy_random")
    ]
    
    # Ejecutar pruebas para cada generador
    resultados = []
    for gen, nombre in generadores:
        print(f"Evaluando: {nombre}...")
        resultados.append(ejecutar_pruebas(gen, nombre, n, bins))
    
    # Crear tabla de resultados
    tabla = []
    for res in resultados:
        fila = [
            res["nombre"],
            f"{res['tiempo']:.6f}",
            f"{res['monobit']['p_valor']:.4f} ({res['monobit']['resultado']})",
            f"{res['frecuencia']['p_valor']:.4f} ({res['frecuencia']['resultado']})",
            f"{res['series']['p_valor']:.4f} ({res['series']['resultado']})",
            f"{res['rachas']['p_valor']:.4f} ({res['rachas']['resultado']})",
            f"{res['chi2']['p_valor']:.4f} ({res['chi2']['resultado']})"
        ]
        tabla.append(fila)
    
    # Crear DataFrame con los resultados
    df = pd.DataFrame(
        tabla,
        columns=[
            "Generador", 
            "Tiempo (s)", 
            "Test Monobit",
            "Test Frecuencia", 
            "Test Series", 
            "Test Rachas", 
            "Test Chi-cuadrado"
        ]
    )
    
    return df

def graficar_comparacion_3d(n=1000):
    """
    Genera una visualización 3D para comparar los generadores.
    Se toman ternas consecutivas (r_i, r_{i+1}, r_{i+2}).
    
    Args:
        n: Cantidad de números a generar por generador
    """
    # Crear generadores
    gcl_bueno = GeneradorGCL(semilla=12345, a=1664525, c=1013904223, m=2**32)
    gcl_malo = GeneradorGCL(semilla=12345, a=65539, c=0, m=2**31)  # RANDU
    
    # Generar secuencias
    seq_gcl_bueno = gcl_bueno.generar_secuencia(n+2)
    seq_gcl_malo = gcl_malo.generar_secuencia(n+2)
    seq_python = [random.random() for _ in range(n+2)]
    
    # Crear ternas
    ternas_bueno = [(seq_gcl_bueno[i], seq_gcl_bueno[i+1], seq_gcl_bueno[i+2]) for i in range(n)]
    ternas_malo = [(seq_gcl_malo[i], seq_gcl_malo[i+1], seq_gcl_malo[i+2]) for i in range(n)]
    ternas_python = [(seq_python[i], seq_python[i+1], seq_python[i+2]) for i in range(n)]
    
    # Convertir a arrays de NumPy
    ternas_bueno = np.array(ternas_bueno)
    ternas_malo = np.array(ternas_malo)
    ternas_python = np.array(ternas_python)
    
    # Crear gráfico 3D
    fig = plt.figure(figsize=(16, 6))
    
    # GCL bueno
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.scatter(ternas_bueno[:, 0], ternas_bueno[:, 1], ternas_bueno[:, 2], s=1, alpha=0.6)
    ax1.set_title('GCL (buenos parámetros)')
    ax1.set_xlabel('r_i')
    ax1.set_ylabel('r_{i+1}')
    ax1.set_zlabel('r_{i+2}')
    
    # GCL malo (RANDU)
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.scatter(ternas_malo[:, 0], ternas_malo[:, 1], ternas_malo[:, 2], s=1, alpha=0.6)
    ax2.set_title('GCL (RANDU - malos parámetros)')
    ax2.set_xlabel('r_i')
    ax2.set_ylabel('r_{i+1}')
    ax2.set_zlabel('r_{i+2}')
    
    # Python random
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.scatter(ternas_python[:, 0], ternas_python[:, 1], ternas_python[:, 2], s=1, alpha=0.6)
    ax3.set_title('Python random')
    ax3.set_xlabel('r_i')
    ax3.set_ylabel('r_{i+1}')
    ax3.set_zlabel('r_{i+2}')
    
    plt.tight_layout()
    plt.savefig('comparacion_3d.png', dpi=150)
    plt.close()

if __name__ == "__main__":
    print("Comparando generadores pseudoaleatorios...")
    
    # Comparar generadores
    df_resultados = comparar_generadores(n=50000, bins=20)
    
    print("\nResultados de las pruebas:")
    print(tabulate(df_resultados, headers=df_resultados.columns, tablefmt="grid"))
    
    df_resultados.to_csv("resultados_generadores.csv", index=False)
    
    print("\nGenerando visualización 3D...")
    graficar_comparacion_3d(n=10000)
    
    print("\nGeneración completa. Los resultados han sido guardados en archivos.")