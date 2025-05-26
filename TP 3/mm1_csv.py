import simpy
import numpy as np
from collections import defaultdict
import argparse
import json
import csv
import os

"""
Hace 10 corridas y guarda los resultados en .csv
"""

parser = argparse.ArgumentParser(description='Simulación M/M/1/K')
parser.add_argument('-a', '--arrival_rate', type=float, required=True, help='Tasa de llegada')
parser.add_argument('-s', '--service_rate', type=float, required=True, help='Tasa de servicio')
parser.add_argument('-k', '--queue_capacity', type=int, default=None, help='Capacidad de la cola, usar None para infinita')
parser.add_argument('-t', '--sim_time', type=float, default=1000, help='Tiempo total de simulación')
args = parser.parse_args()

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
    self.queue_over_time = []

    self.num_in_system = 0
    self.area_num_in_system = 0.0
    self.area_num_in_queue = 0.0
    self.last_event_time = 0.0

    self.max_n_tracked = max_n_tracked
    self.queue_length_time = defaultdict(float)

    self.rejected_arrivals = 0
    self.total_arrivals = 0

  def update_areas(self):
    time_since_last = self.env.now - self.last_event_time
    queue_length = max(self.num_in_system - 1, 0)
    self.area_num_in_system += self.num_in_system * time_since_last
    self.area_num_in_queue += queue_length * time_since_last

    self.queue_over_time.append((self.env.now, queue_length))

    if queue_length <= self.max_n_tracked:
      self.queue_length_time[queue_length] += time_since_last
    else:
      self.queue_length_time[self.max_n_tracked] += time_since_last

    self.last_event_time = self.env.now

  def arrival(self):
    while True:
      yield self.env.timeout(np.random.exponential(1 / self.arrival_rate))
      self.update_areas()
      self.total_arrivals += 1

      if self.queue_capacity is not None and self.num_in_system >= self.queue_capacity + 1:
        self.rejected_arrivals += 1
        continue

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

# --- Simulación con múltiples corridas ---
num_runs = 10
max_n = args.queue_capacity if args.queue_capacity is not None else 100

# Crear archivo CSV y escribir encabezado

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resultados.csv')

with open(output_path, "w", newline="") as f:
  writer = csv.DictWriter(f, fieldnames=[
    "run", "arrival_rate", "service_rate", "queue_capacity", "sim_time",
    "blocking_probability", "avg_num_in_system", "avg_num_in_queue",
    "avg_wait_time", "avg_queue_time", "server_utilization", "prob_n_in_queue"
  ])
  writer.writeheader()

  for run_id in range(1, num_runs + 1):
    env = simpy.Environment()
    queue = MM1Queue(env, args.arrival_rate, args.service_rate, queue_capacity=args.queue_capacity, max_n_tracked=max_n)
    queue.run(args.sim_time)

    print(f"\n--- Corrida {run_id} ---")
    print(f"Probabilidad de denegación de servicio: {queue.blocking_probability:.4f}")
    print(f"Promedio de clientes en el sistema (L): {queue.avg_num_in_system:.4f}")
    print(f"Promedio de clientes en la cola (Lq): {queue.avg_num_in_queue:.4f}")
    print(f"Tiempo promedio en el sistema (W): {np.mean(queue.wait_times):.4f}")
    print(f"Tiempo promedio en la cola (Wq): {np.mean(queue.queue_times):.4f}")
    print(f"Utilización del servidor: {queue.server_busy_time / args.sim_time:.4f}")

    writer.writerow({
      "run": run_id,
      "arrival_rate": args.arrival_rate,
      "service_rate": args.service_rate,
      "queue_capacity": args.queue_capacity,
      "sim_time": args.sim_time,
      "blocking_probability": queue.blocking_probability,
      "avg_num_in_system": queue.avg_num_in_system,
      "avg_num_in_queue": queue.avg_num_in_queue,
      "avg_wait_time": np.mean(queue.wait_times),
      "avg_queue_time": np.mean(queue.queue_times),
      "server_utilization": queue.server_busy_time / args.sim_time,
      "prob_n_in_queue": json.dumps(queue.prob_n_in_queue)
    })
