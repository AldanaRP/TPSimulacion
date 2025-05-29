import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import defaultdict
import numpy as np
import os

# Lo que faltaria es mostrar la probabilidad de bloqueo (que es constante y no tiene sentido graficarla)
# Podria mostrarse en consola tambien todos los resultados promediados (menos prob_n_in_queue y queue_over_time)

os.makedirs('./TP 3/Imagenes', exist_ok=True)

df = pd.read_csv('./TP 3/resultados.csv')
arrival_rate = df['arrival_rate'].iloc[0]
queue_capacity = df['queue_capacity'].iloc[0]
queue_type = 'infinita' if queue_capacity == '' or pd.isna(queue_capacity) else f'K{int(queue_capacity)}'

metric_aliases = {
  "avg_num_in_system": "Clientes en sistema",
  "avg_num_in_queue": "Clientes en cola",
  "avg_wait_time": "Tiempo total en sistema",
  "avg_queue_time": "Tiempo en cola",
}

server_utilization = {"server_utilization": "Util. Servidor"}

metrics = list(metric_aliases.keys())
server_utilization_key = "server_utilization"


# Grafico de metricas por cada corrida
plt.figure(figsize=(10, 6))
for metric in metrics:
  plt.plot(df['run'], df[metric], marker='o', label=metric_aliases[metric], alpha=0.7)

plt.title('Métricas por corrida')
plt.xlabel('Corrida')
plt.ylabel('Valor')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f'./TP 3/Imagenes/metricas_{arrival_rate}_{queue_type}.png')

# Grafico de utilizacion del servidor por cada corrida

plt.figure(figsize=(10, 6))
plt.plot(df['run'], df[server_utilization_key], marker='o', label=server_utilization[server_utilization_key])

plt.title('Utilización del servidor por corrida')
plt.xlabel('Corrida')
plt.ylabel('Valor')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f'./TP 3/Imagenes/util_sv_{arrival_rate}_{queue_type}.png')

# Combinar distribuciones de todas las corridas
combined_probs = defaultdict(float)

for probs_json in df['prob_n_in_queue']:
  probs = json.loads(probs_json)
  for n, p in probs.items():
    combined_probs[int(n)] += p

# Promediar
for n in combined_probs:
  combined_probs[n] /= len(df)

# Grafico de prob promedio de n clientes en cola

plt.figure(figsize=(10, 6))
plt.bar(combined_probs.keys(), combined_probs.values())
plt.title('Probabilidad promedio de encontrar n clientes en cola')
plt.xlabel('n clientes en cola')
plt.ylabel('Probabilidad')
plt.grid(True, axis='y')
plt.tight_layout()
plt.savefig(f'./TP 3/Imagenes/prob_n_clientes_{arrival_rate}_{queue_type}.png')

# Grafico del tamaño de la cola a lo largo del tiempo

all_sizes = []
all_times = []

plt.figure(figsize=(10, 6))
for i, row in df.iterrows():
  queue_over_time = json.loads(row['queue_over_time'])  # parsear lista de pares [tiempo, tamaño]
  times, sizes = zip(*queue_over_time)              
  plt.plot(times, sizes, label=f'Corrida {i+1}', alpha=0.5)
  all_sizes.append(sizes)
  all_times.append(times)

avg_sizes = np.mean(all_sizes, axis=0)
avg_times = all_times[0]

plt.plot(avg_times, avg_sizes, color='black', linewidth=2.5, label='Promedio')

plt.title('Tamaño de la cola a lo largo del tiempo')
plt.xlabel('Tiempo')
plt.ylabel('Clientes en cola')
plt.legend(loc='upper right')
plt.grid(True)
plt.tight_layout()
plt.savefig(f'./TP 3/Imagenes/cola_vs_tiempo_{arrival_rate}_{queue_type}.png')
