"""
Programa para calcular estadísticas descriptivas de un archivo de números.
"""

import sys
import statistics
import logging
from typing import List, Tuple
from collections import Counter

logging.basicConfig(level=logging.INFO, format="%(message)s")

def read_data(file_path: str) -> Tuple[List[float], List[str]]:
    """
    Lee un archivo y extrae los números válidos.

    Args:
        file_path (str): Ruta del archivo a procesar

    Returns:
        Tuple[List[float], List[str]]: (números válidos, errores encontrados)
    """
    numbers = []
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                value = line.strip()
                if value:
                    try:
                        numbers.append(float(value))
                    except ValueError:
                        errors.append(f"Línea {line_num}: '{value}' no es un número válido")
    except FileNotFoundError:
        logging.error("Error: Archivo '%s' no encontrado", file_path)
        sys.exit(1)

    return numbers, errors

def calculate_statistics(numbers: List[float]) -> dict:
    """
    Calcula estadísticas descriptivas a partir de una lista de números.

    Args:
        numbers (List[float]): Lista de números válidos

    Returns:
        dict: Diccionario con las estadísticas calculadas
    """
    count = len(numbers)
    mean = statistics.mean(numbers) if numbers else 0.0
    median = statistics.median(numbers) if numbers else 0.0
    variance = statistics.variance(numbers) if len(numbers) > 1 else 0.0
    std_dev = statistics.stdev(numbers) if len(numbers) > 1 else 0.0

    # Cálculo de la moda
    counter = Counter(numbers)
    max_freq = max(counter.values(), default=0)
    mode = [k for k, v in counter.items() if v == max_freq] if max_freq > 1 else ["Ninguna"]
    mode_value = mode[0] if isinstance(mode[0], (int, float)) else "Ninguna"

    return {
        "COUNT": count,
        "MEAN": mean,
        "MEDIAN": median,
        "MODE": mode_value,
        "VARIANCE": variance,
        "SD": std_dev
    }

def main():
    """
    Función principal del programa.
    """
    if len(sys.argv) != 2:
        logging.error("Uso: python computeStatistics.py archivoConDatos.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    numbers, errors = read_data(file_path)

    if not numbers:
        logging.error("No se encontraron números válidos en el archivo")
        sys.exit(1)

    # Calcular estadísticas
    stats = calculate_statistics(numbers)

    # Resultados con el formato correcto
    results = f"""
COUNT\t{stats['COUNT']}
MEAN\t{stats['MEAN']:.2f}
MEDIAN\t{stats['MEDIAN']:.1f}
MODE\t{stats['MODE']}
SD\t{stats['SD']:.7f}
VARIANCE\t{stats['VARIANCE']:.4f}
"""

    # Mostrar en consola
    logging.info(results)
    for error in errors:
        logging.warning(error)

    # Escribir en archivo
    with open("StatisticsResults.txt", 'w', encoding='utf-8') as result_file:
        result_file.write(results)
        if errors:
            result_file.write("\nErrores encontrados:\n" + "\n".join(errors))

if __name__ == "__main__":
    main()
