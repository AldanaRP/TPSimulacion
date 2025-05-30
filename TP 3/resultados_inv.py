import pandas as pd
import matplotlib.pyplot as plt
import ast
import os

df = pd.read_csv("./TP 3/resultados_inv.csv")

output_dir = "./TP 3/Inventario"
os.makedirs(output_dir, exist_ok=True)

plt.figure(figsize=(12, 6))

s_line = df["s"].min()
S_line = df["S"].max()

# Iterar por cada corrida
for _, row in df.iterrows():
    run = row["run"]
    inventory_data_str = row["inventory_over_time"]

    try:
        # Convertir el string a lista de tuplas reales
        inventory_data = ast.literal_eval(inventory_data_str)
        times, inventories = zip(*inventory_data)  # Separar tiempos y niveles

        plt.plot(times, inventories, label=f'Corrida {run}', linewidth=1)
    except Exception as e:
        print(f"Error al procesar la corrida {run}: {e}")

plt.axhline(y=0, color='black', linestyle='-', linewidth=1.5, label='Nivel 0')
plt.axhline(y=s_line, color='red', linestyle='-', linewidth=1.5, label=f's = {s_line}')
plt.axhline(y=S_line, color='blue', linestyle='-', linewidth=1.5, label=f'S = {S_line}')

plt.title(f"Nivel de Inventario a lo Largo del Tiempo - Política ({s_line}, {S_line})")
plt.xlabel("Tiempo")
plt.ylabel("Nivel de Inventario")
plt.legend(loc="lower left", fontsize="small", ncol=2)
plt.grid(True)
plt.tight_layout()

filename = f"inventario_vs_tiempo_{s_line}_{S_line}.png"
filepath = os.path.join(output_dir, filename)
plt.savefig(filepath, bbox_inches="tight")
plt.close()

grouped = df.groupby(["s", "S", "mean_interdemand"])

for (s, S, mean_interdemand), group in grouped:
    # Calcular promedios y renombrar columnas
    summary = group[[
        "total_ordering_cost", "avg_holding_cost",
        "avg_shortage_cost", "total_cost"
    ]].mean().to_frame().T.round(2)

    summary.columns = [
        "Costo de orden",
        "Costo mantenimiento",
        "Costo faltante",
        "Costo total"
    ]

    fig, ax = plt.subplots(figsize=(8, 2))
    ax.axis('tight')
    ax.axis('off')

    table = ax.table(
        cellText=summary.values,
        colLabels=summary.columns,
        cellLoc='center',
        loc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    plt.title(
        f"Promedios política ({s}, {S})",
        fontsize=12, pad=5
    )

    filename = f"promedios_{s}_{S}.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, bbox_inches="tight")
    plt.close()
