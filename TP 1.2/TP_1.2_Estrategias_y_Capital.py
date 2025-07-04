import argparse
import random
import matplotlib.pyplot as plt
import numpy as np

class Ruleta:
    def __init__(self, tipo="europea"):
        """Inicializa la ruleta según el tipo (europea o americana)"""
        if tipo.lower() == "europea":
            # Ruleta europea: números del 0 al 36
            self.numeros = list(range(37))
        else:
            # Ruleta americana: números del 0 al 36 más el 00
            self.numeros = list(range(37)) + [00]

        # Definir colores
        self.colores = {0: "verde", 00: "verde"}
        rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        for num in self.numeros:
            if num in rojos:
                self.colores[num] = "rojo"
            elif num != 0 and num != 00:
                self.colores[num] = "negro"

    def girar(self):
        """Simula el giro de la ruleta y devuelve el número resultante"""
        return random.choice(self.numeros)

class EstrategiaApuesta:
    def __init__(self, capital_inicial=100, apuesta_base=1, seleccion_apuesta=None, capital_infinito=False):
        self.capital_inicial = capital_inicial
        self.capital = capital_inicial
        self.apuesta_base = apuesta_base
        self.apuesta_actual = apuesta_base
        self.historial_capital = [capital_inicial]
        self.resultados = []
        self.tiradas = 0
        self.victorias = 0
        self.derrotas = 0
        self.seleccion_apuesta = seleccion_apuesta
        self.capital_infinito = capital_infinito

    def reiniciar(self):
        """Reinicia la estrategia a sus valores iniciales"""
        self.capital = self.capital_inicial
        self.apuesta_actual = self.apuesta_base
        self.historial_capital = [self.capital_inicial]
        self.resultados = []
        self.tiradas = 0
        self.victorias = 0
        self.derrotas = 0

    def calcular_siguiente_apuesta(self, resultado):
        """Método a implementar en las clases hijas"""
        pass

    def determinar_ganancia(self, resultado_ruleta):
        """Determina si la apuesta actual fue ganadora y cuánto se ganó.
        Este método base maneja un solo tipo de apuesta: Color rojo
        Otras apuestas pueden ser implementadas según sea necesario
        """
        if self.seleccion_apuesta == "rojo" and ruleta.colores.get(resultado_ruleta) == "rojo":
            return True, 1  # Pago de 1:1
            
        return False, 0  # Perdimos la apuesta

    def realizar_apuesta(self, ruleta):
        """Realiza una apuesta y actualiza el capital"""
        self.tiradas += 1
        resultado_ruleta = ruleta.girar()
        ganador, ganancia = self.determinar_ganancia(resultado_ruleta)

        if ganador:
            self.capital += self.apuesta_actual * ganancia
            resultado = True
            self.victorias += 1
        else:
            self.capital -= self.apuesta_actual
            resultado = False
            self.derrotas += 1

        self.resultados.append(resultado)
        self.historial_capital.append(self.capital)

        # Calcular siguiente apuesta según la estrategia
        self.calcular_siguiente_apuesta(resultado)

        return resultado

class Martingala(EstrategiaApuesta):
    def __init__(self, capital_inicial=100, apuesta_base=1, seleccion_apuesta=None, capital_infinito=False):
        super().__init__(capital_inicial, apuesta_base, seleccion_apuesta, capital_infinito)

    def calcular_siguiente_apuesta(self, resultado):
        """En Martingala, duplicamos la apuesta tras cada pérdida"""
        if resultado:  # Si ganamos
            self.apuesta_actual = self.apuesta_base
        else:  # Si perdemos
            self.apuesta_actual *= 2

        # Si tenemos capital finito, limitamos la apuesta al capital disponible
        if not self.capital_infinito and self.capital < self.apuesta_actual:
            self.apuesta_actual = min(self.apuesta_actual, self.capital)

class DAlembert(EstrategiaApuesta):
    def __init__(self, capital_inicial=100, apuesta_base=1, seleccion_apuesta=None, capital_infinito=False):
        super().__init__(capital_inicial, apuesta_base, seleccion_apuesta, capital_infinito)

    def calcular_siguiente_apuesta(self, resultado):
        """En D'Alembert, aumentamos en 1 unidad tras perder y disminuimos en 1 tras ganar"""
        if resultado:  # Si ganamos
            self.apuesta_actual = max(self.apuesta_base, self.apuesta_actual - 1)
        else:  # Si perdemos
            self.apuesta_actual += 1

        # Si tenemos capital finito, limitamos la apuesta al capital disponible
        if not self.capital_infinito and self.capital < self.apuesta_actual:
            self.apuesta_actual = min(self.apuesta_actual, self.capital)

class Fibonacci(EstrategiaApuesta):
    def __init__(self, capital_inicial=100, apuesta_base=1, seleccion_apuesta=None, capital_infinito=False):
        super().__init__(capital_inicial, apuesta_base, seleccion_apuesta, capital_infinito)
        self.secuencia = [1, 1]  # Primeros términos de Fibonacci
        self.indice = 0

    def reiniciar(self):
        super().reiniciar()
        self.secuencia = [1, 1]
        self.indice = 0

    def calcular_siguiente_apuesta(self, resultado):
        """En Fibonacci, avanzamos en la secuencia tras perder y retrocedemos 2 posiciones tras ganar"""
        if resultado:  # Si ganamos
            self.indice = max(0, self.indice - 2)
            self.apuesta_actual = self.apuesta_base * self.secuencia[self.indice] if self.secuencia else self.apuesta_base
        else:  # Si perdemos
            self.indice += 1

            # Extendemos la secuencia si es necesario
            if self.indice >= len(self.secuencia):
                self.secuencia.append(self.secuencia[-1] + self.secuencia[-2])

            self.apuesta_actual = self.apuesta_base * self.secuencia[self.indice] if self.secuencia else self.apuesta_base

        # Si tenemos capital finito, limitamos la apuesta al capital disponible
        if not self.capital_infinito and self.capital < self.apuesta_actual:
            self.apuesta_actual = min(self.apuesta_actual, self.capital)

class Paroli(EstrategiaApuesta):
    """Estrategia de la Paroli: duplicar apuesta tras ganar hasta 3 victorias consecutivas"""
    def __init__(self, capital_inicial=100, apuesta_base=1, seleccion_apuesta=None, capital_infinito=False):
        super().__init__(capital_inicial, apuesta_base, seleccion_apuesta, capital_infinito)
        self.victorias_consecutivas = 0

    def reiniciar(self):
        super().reiniciar()
        self.victorias_consecutivas = 0

    def calcular_siguiente_apuesta(self, resultado):
        if resultado:  # Si ganamos
            self.victorias_consecutivas += 1

            # Después de 3 victorias consecutivas, volvemos a la apuesta base
            if self.victorias_consecutivas >= 3:
                self.apuesta_actual = self.apuesta_base
                self.victorias_consecutivas = 0
            else:
                self.apuesta_actual *= 2
        else:  # Si perdemos
            self.apuesta_actual = self.apuesta_base
            self.victorias_consecutivas = 0

        # Si tenemos capital finito, limitamos la apuesta al capital disponible
        if not self.capital_infinito and self.capital < self.apuesta_actual:
            self.apuesta_actual = min(self.apuesta_actual, self.capital)

def simular_estrategia(estrategia, ruleta, num_tiradas, capital_infinito=False):
    """Simula una estrategia de apuesta durante un número de tiradas"""
    estrategia.reiniciar()
    estrategia.capital_infinito = capital_infinito

    tiradas_realizadas = 0
    while tiradas_realizadas < num_tiradas:
        if not capital_infinito and estrategia.capital <= 0:
            break

        estrategia.realizar_apuesta(ruleta)
        tiradas_realizadas += 1

    return estrategia.historial_capital

def calcular_frsa(estrategia, ruleta, num_tiradas, repeticiones=100, capital_infinito=False):
    """Calcula la frecuencia relativa de obtener la apuesta favorable según n tiradas"""
    frsa = np.zeros(num_tiradas)
    repeticiones_reales = np.zeros(num_tiradas)

    for _ in range(repeticiones):
        estrategia.reiniciar()

        i = 0
        while i < num_tiradas:
            if estrategia.capital <= 0 and not capital_infinito:
                break

            resultado_ganador = estrategia.realizar_apuesta(ruleta)

            repeticiones_reales[i] += 1
            if resultado_ganador:
                frsa[i] += 1

            i += 1

    frsa = np.divide(frsa, repeticiones_reales, out=np.zeros_like(frsa), where=repeticiones_reales != 0)
    frsa_acumulada = np.zeros(num_tiradas)
    suma_acumulada = 0
    for i in range(num_tiradas):
        suma_acumulada += frsa[i]
        frsa_acumulada[i] = suma_acumulada / (i + 1)

    return frsa, frsa_acumulada


def main():
    parser = argparse.ArgumentParser(description='Simulador de estrategias de apuesta en ruleta')
    parser.add_argument('-c', type=int, default=5, help='Número de corridas')
    parser.add_argument('-n', type=int, default=2000, help='Número de tiradas')
    parser.add_argument('-s', choices=['m', 'd', 'f', 'o'], default='m', help='Estrategia: m (martingala), d (D\'Alembert), f (Fibonacci), o (Paroli)')
    parser.add_argument('-a', choices=['i', 'f'], default='f', help='Tipo de capital: i (infinito), f (finito)')

    args = parser.parse_args()

    # Configuración
    num_corridas = args.c
    num_tiradas = args.n
    capital_infinito = args.a == 'i'
    seleccion_apuesta = 'rojo'

    # Inicializar la ruleta (definimos como global para que esté disponible en los métodos de las estrategias)
    global ruleta
    ruleta = Ruleta()

    # Seleccionar la estrategia e inicializar con la selección de apuesta
    if args.s == 'm':
        nombre_estrategia = "Martingala"
        estrategia = Martingala(seleccion_apuesta=seleccion_apuesta)
    elif args.s == 'd':
        nombre_estrategia = "D'Alembert"
        estrategia = DAlembert(seleccion_apuesta=seleccion_apuesta)
    elif args.s == 'f':
        nombre_estrategia = "Fibonacci"
        estrategia = Fibonacci(seleccion_apuesta=seleccion_apuesta)
    else:
        nombre_estrategia = "Paroli"
        estrategia = Paroli(seleccion_apuesta=seleccion_apuesta)

    # Mostrar información de la apuesta seleccionada
    apuesta_str = str(seleccion_apuesta) if seleccion_apuesta is not None else "Ninguna"
    print(f"Selección de apuesta: {apuesta_str}")

    historiales_capital = []

    # Calcular FRSA y FRSA acumulada
    frsa, frsa_acumulada = calcular_frsa(estrategia, ruleta, num_tiradas, repeticiones=100, capital_infinito=capital_infinito)

    for _ in range(num_corridas):
        estrategia.reiniciar()
        historial = simular_estrategia(estrategia, ruleta, num_tiradas, capital_infinito=capital_infinito)
        historiales_capital.append(historial)

    # FRSA y FRSA acumulada
    if num_tiradas > 100:
        fig = plt.figure(figsize=(16, 8))
        gs = fig.add_gridspec(1, 2)
        ax1 = fig.add_subplot(gs[0, 0])
        ax1_line = fig.add_subplot(gs[0, 1])
    else:
        fig, (ax1, ax1_line) = plt.subplots(1, 2, figsize=(14, 6))

    # Frecuencia relativa (gráfico de barras)
    if num_tiradas > 100:
        num_bins = min(50, num_tiradas // 10)
        bin_size = num_tiradas // num_bins
        binned_frsa = np.zeros(num_bins)
        for i in range(num_bins):
            start_idx = i * bin_size
            end_idx = min((i + 1) * bin_size, num_tiradas)
            binned_frsa[i] = np.mean(frsa[start_idx:end_idx])

        bin_labels = [f"{i*bin_size+1}-{min((i+1)*bin_size, num_tiradas)}" for i in range(num_bins)]

        ax1.bar(range(num_bins), binned_frsa, color='red')
        ax1.set_xticks(range(0, num_bins, max(1, num_bins // 10)))
        ax1.set_xticklabels([bin_labels[i] for i in range(0, num_bins, max(1, num_bins // 10))], rotation=45)
        ax1.set_xlabel('Grupos de tiradas')
        ax1.set_ylabel('fr (frecuencia relativa promedio)')
        ax1.set_title('frsa agrupada (Frecuencia relativa promedio por grupos de tiradas)', fontsize=18)
    else:
        ax1.bar(range(1, num_tiradas + 1), frsa, color='red')
        ax1.set_xlabel('n (número de tiradas)')
        ax1.set_ylabel('fr (frecuencia relativa)')
        ax1.set_title('frsa (Frecuencia relativa de ganar la apuesta según n)', fontsize=18)

    # Frecuencia relativa acumulada (gráfico de línea)
    ax1_line.plot(range(1, num_tiradas + 1), frsa_acumulada, color='blue', linewidth=2, label='Frec. relativa')
    ax1_line.axhline(y=0.4865, color='green', linestyle='--', alpha=0.7, label='Frec. relativa esperada')
    ax1_line.set_xlabel('n (número de tiradas)')
    ax1_line.set_ylabel('fr acumulada')
    ax1_line.set_title('Frecuencia relativa acumulada', fontsize=18)
    ax1_line.legend()

    fig.suptitle(f'FRSA - Estrategia: {nombre_estrategia}', fontsize=20)
    plt.tight_layout()
    plt.savefig(f'./TP 1.2/frsa_{nombre_estrategia}.png')
    plt.clf()

    # Flujo de caja
    fig, ax2 = plt.subplots(1, 1, figsize=(10, 6))

    for i, historial in enumerate(historiales_capital, start=1):
        ax2.plot(range(len(historial)), historial, alpha=0.6, label=f'Flujo de caja - Corrida {i}')

    ax2.axhline(y=100, color='blue', linestyle='-', alpha=0.7, label='fci (flujo de caja inicial)')
    ax2.axhline(y=0, color='red', alpha=0.7, linestyle='--')
    ax2.set_xlabel('n (número de tiradas)')
    ax2.set_ylabel('cc (cantidad de capital)')
    ax2.set_title(f'Flujo de caja - Estrategia: {nombre_estrategia} - Capital {"Infinito" if capital_infinito else "Finito"}')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(f'./TP 1.2/flujo_caja_{nombre_estrategia}_{args.a}.png')
    plt.clf()

if __name__ == "__main__":
    main()
