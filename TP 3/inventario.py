import random
import heapq
import numpy as np
import argparse
import os
import csv

# faltaria hacer graficos, hacer en archivo aparte de resultados

"""
Politicas (s, S) a testear:
(20, 40)
(20, 60)
(20, 80)
(20, 100)
(40, 60)
(40, 80)
(40, 100)
(60, 80)
(60, 100)

Tiempos entre demandas:
0.1 parece ser ideal, a lo sumo 0.11 0.12
"""

runs = 10 # Corridas

inventory_over_time = []
sampling_interval = 0.1
next_sample_time = 0.0

parser = argparse.ArgumentParser(description='Modelo de Inventario (s, S)')
parser.add_argument('-s', '--s', type=int, required=True, help='Nivel de pedido')
parser.add_argument('-S', '--S', type=int, required=True, help='Nivel objetivo')
parser.add_argument('-t', '--mean_interdemand', type=float, required=True, help='Tiempo entre demandas')
args = parser.parse_args()

# Política de inventario (s, S)
# Se hace un pedido cuando el inventario cae debajo de s, se ordena hasta el nivel S
s = args.s
S = args.S

initial_inventory = S # Igualo el inventario inicial a S
n_months = 12
mean_interdemand = args.mean_interdemand

# Tiempo minimo y maximo de entrega
min_lag = 0.5            
max_lag = 1.0           

# Costos de orden, incremental, mantenimiento, faltante
setup_cost = 30.0
incremental_cost = 2.0
holding_cost = 1.0
shortage_cost = 5.0

# Distribución de tamaños de demanda
#demand_probabilities = [0.05, 0.10, 0.15, 0.20, 0.15, 0.10, 0.10, 0.05, 0.05, 0.05]
demand_probabilities = [0.10, 0.20, 0.40, 0.20, 0.10]
demand_sizes = list(range(1, 6))  # 1 al 5
#demand_sizes = list(range(1, 11))  # 1 al 10

# Estado inicial
sim_time = 0.0
inventory_level = initial_inventory
order_pending = False
pending_order_amount = 0

# Estadísticas
total_ordering_cost = 0.0
area_holding = 0.0
area_shortage = 0.0
last_event_time = 0.0

# Cola de eventos: (tiempo_evento, tipo_evento)
event_queue = []

# Tipos de eventos
#- Arrival of an order to the company from the supplier
#- Demand for the product from a customer
#- End of the simulation after n months
#- Inventory evaluation (and possible ordering) at the beginning of a month

ORDER_ARRIVAL = 1
DEMAND = 2
SIMULATION_END = 3
EVALUATE_INVENTORY = 4

def expon(mean):
  return np.random.exponential(mean)

def random_demand():
  return random.choices(demand_sizes, weights=demand_probabilities)[0]

def schedule_event(event_type, time_offset):
  """
  Programa un evento futuro
  
  Parámetros:
  - event_type: tipo de evento
  - time_offset: cuánto tiempo en el futuro ocurrirá el evento
  """
  heapq.heappush(event_queue, (sim_time + time_offset, event_type))

def order_arrival():
  """
  Evento de llegada de pedido
  Actualiza el inventario con la cantidad ordenada y marca que ya no hay un pedido pendiente
  """
  global inventory_level, order_pending, pending_order_amount
  inventory_level += pending_order_amount
  order_pending = False
  pending_order_amount = 0

def demand():
  """
  Evento de demanda
  Genera una demanda aleatoria y reduce el nivel de inventario según el tamaño
  """
  global inventory_level
  size = random_demand()
  inventory_level -= size

def evaluate_inventory():
  """
  Evento de evaluación mensual de inventario
  Si el nivel actual está por debajo del punto de reorden (s) y no hay pedido pendiente,
  se programa un nuevo pedido hasta el nivel S, con un tiempo de entrega aleatorio
  También se acumula el costo asociado al pedido
  """
  global total_ordering_cost, order_pending, pending_order_amount
  if inventory_level < s and not order_pending:
    pending_order_amount = S - inventory_level
    delay = random.uniform(min_lag, max_lag)
    schedule_event(ORDER_ARRIVAL, delay)
    total_ordering_cost += setup_cost + incremental_cost * pending_order_amount
    order_pending = True

def update_time_avg_stats(current_time):
  """
  Actualiza las estadísticas promedio de inventario entre eventos
    
  Parámetro:
  - current_time: tiempo actual del evento
  
  Calcula el área bajo la curva para el inventario disponible o faltante,
  usando el tiempo transcurrido desde el último evento
  """
  global area_holding, area_shortage, last_event_time, next_sample_time
  time_passed = current_time - last_event_time
  last_event_time = current_time
  if inventory_level > 0:
    area_holding += inventory_level * time_passed
  else:
    area_shortage += abs(inventory_level) * time_passed

  while next_sample_time <= current_time:
    inventory_over_time.append((next_sample_time, inventory_level))
    next_sample_time += sampling_interval

def reset_values():
  """
  Resetea los valores de las variables de estado y estadísticas
  para una nueva corrida de simulación
  """
  global sim_time, inventory_level, order_pending, total_ordering_cost, pending_order_amount
  global area_holding, area_shortage, last_event_time, event_queue, next_sample_time

  sim_time = 0.0
  inventory_level = initial_inventory
  order_pending = False
  pending_order_amount = 0
  total_ordering_cost = 0.0
  area_holding = 0.0
  area_shortage = 0.0
  last_event_time = 0.0
  inventory_over_time.clear()
  event_queue.clear()

  inventory_over_time.append((0.0, inventory_level))
  next_sample_time = 0.0


output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resultados_inv.csv')

with open(output_path, "w", newline="") as f:
  writer = csv.DictWriter(f, fieldnames=[
    "run", "S", "s", "mean_interdemand", "total_ordering_cost",
    "avg_holding_cost", "avg_shortage_cost", "total_cost", "inventory_over_time"
  ])
  writer.writeheader()


  for run in range(1, runs + 1):

    reset_values()

    # Programa los eventos iniciales
    schedule_event(DEMAND, expon(mean_interdemand))
    schedule_event(EVALUATE_INVENTORY, 1.0)
    schedule_event(SIMULATION_END, n_months)

    while event_queue:
      # Consigue el proximo evento y actualiza el tiempo
      sim_time, event_type = heapq.heappop(event_queue)
      update_time_avg_stats(sim_time)

      if event_type == ORDER_ARRIVAL:
        order_arrival()
      elif event_type == DEMAND:
        demand()
        schedule_event(DEMAND, expon(mean_interdemand))
      elif event_type == EVALUATE_INVENTORY:
        evaluate_inventory()
        if sim_time + 1.0 <= n_months:
          schedule_event(EVALUATE_INVENTORY, 1.0)
      elif event_type == SIMULATION_END:
        break

    avg_holding_cost = holding_cost * area_holding / n_months
    avg_shortage_cost = shortage_cost * area_shortage / n_months

    total_cost = total_ordering_cost + avg_holding_cost + avg_shortage_cost

    print(f"\n--- Corrida {run} ---")
    print(f"Costo de orden:       ${total_ordering_cost:.2f}")
    print(f"Costo de mantenimiento: ${avg_holding_cost:.2f}")
    print(f"Costo de faltante:     ${avg_shortage_cost:.2f}")
    print(f"COSTO TOTAL:           ${total_cost:.2f}")

    writer.writerow({
      "run": run,
      "S": S,
      "s": s,
      "mean_interdemand": mean_interdemand,
      "total_ordering_cost": total_ordering_cost,
      "avg_holding_cost": round(avg_holding_cost, 2),
      "avg_shortage_cost": round(avg_shortage_cost, 2),
      "total_cost": round(total_cost, 2),
      "inventory_over_time": inventory_over_time
    })

print(f"\nResultados guardados en: {output_path}\n")

