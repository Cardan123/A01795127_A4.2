"""
Programa para contar frecuencia de palabras en un archivo.
"""

import sys
import time
import logging
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO, format="%(message)s")

def process_file(file_path: str) -> Tuple[Dict[str, int], List[str]]:
    """
    Procesa un archivo y cuenta las palabras.

    Args:
        file_path (str): Ruta del archivo

    Returns:
        Tuple[Dict[str, int], List[str]]: (contador de palabras, errores)
    """
    word_count = {}
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                try:
                    stripped_line = line.strip()
                    if not stripped_line:
                        errors.append(f"Línea {line_num}: Línea vacía")
                        continue

                    words = stripped_line.split()
                    for word in words:
                        word_count[word] = word_count.get(word, 0) + 1

                except UnicodeDecodeError:
                    errors.append(f"Línea {line_num}: Caracteres inválidos")
    except FileNotFoundError:
        logging.error("Error: Archivo '%s' no encontrado", file_path)
        sys.exit(1)
    except OSError as os_error:
        logging.error("Error del sistema al leer el archivo: %s", os_error)
        sys.exit(1)

    return word_count, errors

def sort_words(word_count: Dict[str, int]) -> List[Tuple[str, int]]:
    """
    Ordena las palabras primero alfabéticamente y luego por frecuencia.

    Args:
        word_count (Dict[str, int]): Diccionario de palabras y conteos

    Returns:
        List[Tuple[str, int]]: Lista ordenada de tuplas (palabra, conteo)
    """
    return sorted(word_count.items(), key=lambda x: (-x[1], x[0]))

def main():
    """
    Función principal del programa.
    """
    if len(sys.argv) != 2:
        logging.error("Uso: python wordCount.py archivoConDatos.txt")
        sys.exit(1)

    start_time = time.time()
    file_path = sys.argv[1]

    word_count, errors = process_file(file_path)

    if not word_count:
        logging.error("No se encontraron palabras válidas")
        sys.exit(1)

    # Generar resultados
    sorted_words = sort_words(word_count)
    results = ["Palabra\tConteo", "================"]
    results += [f"{word}\t{count}" for word, count in sorted_words]

    execution_time = time.time() - start_time
    time_msg = f"\nTiempo de ejecución: {execution_time:.4f} segundos"

    # Mostrar en consola
    logging.info("\n".join(results))
    logging.info(time_msg)

    for error in errors:
        logging.warning(error)

    # Escribir archivo
    with open("WordCountResults.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))
        f.write(time_msg)
        if errors:
            f.write("\n\nErrores:\n" + "\n".join(errors))

if __name__ == "__main__":
    main()
