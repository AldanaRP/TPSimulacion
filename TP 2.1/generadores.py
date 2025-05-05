import numpy as np
import matplotlib.pyplot as plt
import random
import math

class GeneradorGCL:
    """
    Generador Congruencial Lineal (GCL)
    X_{n+1} = (a * X_n + c) mod m
    
    Donde:
    - X_n es el número actual de la secuencia
    - a es el multiplicador
    - c es el incremento
    - m es el módulo
    """
    def __init__(self, semilla, a, c, m):
        """
        Inicializa el generador GCL
        
        Args:
            semilla: Valor inicial X_0
            a: Multiplicador
            c: Incremento
            m: Módulo
        """
        self.actual = semilla
        self.a = a
        self.c = c
        self.m = m
        self.semilla_original = semilla
    
    def siguiente(self):
        """
        Genera el siguiente número en la secuencia
        
        Returns:
            Siguiente número pseudoaleatorio en el rango [0,1)
        """
        self.actual = (self.a * self.actual + self.c) % self.m
        return self.actual / self.m
    
    def generar_secuencia(self, n):
        """
        Genera una secuencia de n números pseudoaleatorios
        
        Args:
            n: Cantidad de números a generar
            
        Returns:
            Lista con n números pseudoaleatorios
        """
        return [self.siguiente() for _ in range(n)]
    
    def reiniciar(self):
        """Reinicia el generador a la semilla original"""
        self.actual = self.semilla_original


class GeneradorCuadrados:
    """
    Método de los cuadrados medios (Middle-Square Method)
    Un método clásico propuesto por John von Neumann
    """
    def __init__(self, semilla, digitos=4):
        """
        Inicializa el generador de cuadrados medios
        
        Args:
            semilla: Valor inicial (debe tener la longitud apropiada)
            digitos: Cantidad de dígitos para extraer del medio
        """
        # Aseguramos que la semilla tenga al menos 'digitos' caracteres
        self.semilla = semilla
        self.digitos = digitos
        self.actual = semilla
        self.semilla_original = semilla
    
    def siguiente(self):
        """
        Genera el siguiente número en la secuencia
        
        Returns:
            Siguiente número pseudoaleatorio en el rango [0,1)
        """
        # Elevamos al cuadrado
        cuadrado = self.actual ** 2
        
        # Convertimos a string para manipular los dígitos
        str_cuadrado = str(cuadrado).zfill(self.digitos * 2)
        
        # Extraemos los dígitos del medio
        inicio = (len(str_cuadrado) - self.digitos) // 2
        medio = str_cuadrado[inicio:inicio + self.digitos]
        
        # Actualizamos el valor actual
        self.actual = int(medio)
        
        # Devolvemos el valor normalizado entre 0 y 1
        return self.actual / (10 ** self.digitos)
    
    def generar_secuencia(self, n):
        """
        Genera una secuencia de n números pseudoaleatorios
        
        Args:
            n: Cantidad de números a generar
            
        Returns:
            Lista con n números pseudoaleatorios
        """
        return [self.siguiente() for _ in range(n)]
    
    def reiniciar(self):
        """Reinicia el generador a la semilla original"""
        self.actual = self.semilla_original


# Ejemplo de uso
if __name__ == "__main__":
    # Parámetros para el GCL (valores de RANDU, un GCL famoso pero con problemas)
    semilla_gcl = 12345
    a = 65539
    c = 0
    m = 2**31
    
    # Crear instancia del generador GCL
    gcl = GeneradorGCL(semilla_gcl, a, c, m)
    
    # Generar 10 números pseudoaleatorios
    numeros_gcl = gcl.generar_secuencia(10)
    print("Números generados por GCL:")
    print(numeros_gcl)
    
    # Parámetros para el generador de cuadrados medios
    semilla_cuadrados = 1234
    
    # Crear instancia del generador de cuadrados medios
    cuadrados = GeneradorCuadrados(semilla_cuadrados)
    
    # Generar 10 números pseudoaleatorios
    numeros_cuadrados = cuadrados.generar_secuencia(10)
    print("\nNúmeros generados por el método de cuadrados medios:")
    print(numeros_cuadrados)