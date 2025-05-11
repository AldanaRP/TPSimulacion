import requests
import time
import csv

def descargar_numeros_random_org(
    cantidad_total=50000,
    por_solicitud=10000,
    decimales=5,
    archivo_csv="random_org_numeros.csv"
  ):

  url = "https://www.random.org/decimal-fractions/"
  total_descargados = 0
  numeros = []

  while total_descargados < cantidad_total:
    cantidad_a_pedir = min(por_solicitud, cantidad_total - total_descargados)
    params = {
      "num": cantidad_a_pedir,
      "dec": decimales,
      "col": 1,
      "format": "plain",
      "rnd": "new"
    }

    print(f"Descargando {cantidad_a_pedir} números... ({total_descargados + cantidad_a_pedir}/{cantidad_total})")
    response = requests.get(url, params=params)
    if response.status_code == 200:
      texto = response.text.strip()
      numeros.extend(map(float, texto.splitlines()))
      total_descargados += cantidad_a_pedir
      time.sleep(1)
    else:
      raise Exception(f"Error al obtener datos: {response.status_code} - {response.text}")

  with open(archivo_csv, "w", newline="") as f_csv:
    writer = csv.writer(f_csv)
    for num in numeros:
      writer.writerow([num])

  print(f"Se guardaron {cantidad_total} números en:\n- {archivo_csv}")

if __name__ == "__main__":
  descargar_numeros_random_org()
