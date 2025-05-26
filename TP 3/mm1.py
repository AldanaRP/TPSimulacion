"""
Sistema M/M/1/K
Llegadas y tiempo de servicio exponenciales
1 servidor
Cola finita de tamaño K, FIFO

Variar (al menos) las tasas de arribo: 25%, 50%, 75%, 100%, 125% con respecto a la tasa de servicio
"""

# Mínimo 10 corridas por cada experimento
# Quedaria poder especificar parametros de entrada por consola
# Variar tasas de arribo un 25%, 50%, 75%, 100%, 125% con respecto a la tasa de servicio
# Ver bien el sim_time, justificar valor

import simpy
import numpy as np
from collections import defaultdict

class MM1Queue:
  def __init__(self, env, arrival_rate, service_rate, queue_capacity=None, max_n_tracked=10):
    self.env = env
    self.server = simpy.Resource(env, capacity=1)
    self.arrival_rate = arrival_rate
    self.service_rate = service_rate
    self.queue_capacity = queue_capacity
    self.wait_times = []
    self.queue_times = []
    self.server_busy_time = 0

    # Métricas de estado del sistema
    self.num_in_system = 0
    self.area_num_in_system = 0.0
    self.area_num_in_queue = 0.0
    self.last_event_time = 0.0

    # Para probabilidad de n clientes en cola
    self.max_n_tracked = max_n_tracked
    self.queue_length_time = defaultdict(float)

    # Métricas de rechazo
    self.rejected_arrivals = 0
    self.total_arrivals = 0

  def update_areas(self):
    time_since_last = self.env.now - self.last_event_time
    queue_length = max(self.num_in_system - 1, 0)
    self.area_num_in_system += self.num_in_system * time_since_last
    self.area_num_in_queue += queue_length * time_since_last

    # Contar cuánto tiempo hay n clientes en cola
    if queue_length <= self.max_n_tracked:
      self.queue_length_time[queue_length] += time_since_last
    else:
      self.queue_length_time[self.max_n_tracked] += time_since_last  # agrupar los grandes

    self.last_event_time = self.env.now

  def arrival(self):
    while True:
      yield self.env.timeout(np.random.exponential(1 / self.arrival_rate))
      self.update_areas()
      self.total_arrivals += 1

      # Verificar capacidad si hay límite
      if self.queue_capacity is not None and self.num_in_system >= self.queue_capacity + 1:
        self.rejected_arrivals += 1
        continue  # llegada rechazada

      self.num_in_system += 1
      self.env.process(self.service())

  def service(self):
    arrival_time = self.env.now
    with self.server.request() as req:
      yield req
      self.update_areas()

      wait = self.env.now - arrival_time
      self.queue_times.append(wait)
      self.wait_times.append(wait)

      service_time = np.random.exponential(1 / self.service_rate)
      yield self.env.timeout(service_time)

      self.update_areas()
      self.num_in_system -= 1
      self.server_busy_time += service_time

      self.wait_times[-1] += service_time

  def run(self, sim_time):
    self.env.process(self.arrival())
    self.env.run(until=sim_time)
    self.update_areas()

    self.avg_num_in_system = self.area_num_in_system / sim_time
    self.avg_num_in_queue = self.area_num_in_queue / sim_time
    self.prob_n_in_queue = {
      n: self.queue_length_time[n] / sim_time for n in range(self.max_n_tracked + 1)
    }

    self.blocking_probability = (
      self.rejected_arrivals / self.total_arrivals if self.total_arrivals > 0 else 0
    )

# Parámetros
arrival_rate = 0.5  # 0.25, 0.5, 0.75, 1.0, 1.25
service_rate = 1.0
sim_time = 1000
queue_capacity = 50  # 0, 2, 5, 10, 50

env = simpy.Environment()
queue = MM1Queue(env, arrival_rate, service_rate, queue_capacity=queue_capacity, max_n_tracked=queue_capacity if queue_capacity != None else 1000)
queue.run(sim_time)

print(f"Capacidad de cola: {queue_capacity if queue_capacity != None else 'infinita'}")
print(f"Probabilidad de denegación de servicio: {queue.blocking_probability:.4f}")
print(f"Promedio de clientes en el sistema (L): {queue.avg_num_in_system:.4f}")
print(f"Promedio de clientes en la cola (Lq): {queue.avg_num_in_queue:.4f}")
print(f"Tiempo promedio en el sistema (W): {np.mean(queue.wait_times):.4f}")
print(f"Tiempo promedio en la cola (Wq): {np.mean(queue.queue_times):.4f}")
print(f"Utilización del servidor: {queue.server_busy_time / sim_time:.4f}")

print("\nProbabilidad de encontrar exactamente n clientes en cola:")
for n, prob in queue.prob_n_in_queue.items():
  if prob > 0:
    print(f" P(n={n}) = {prob:.4f}")
  if n != queue_capacity and prob == 0:
    print(f" P(n>={n}) = 0.0000")
    break
