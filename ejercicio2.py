"""
Programa para convertir números de un archivo a binario y hexadecimal.
"""

import sys
import time
import logging
from typing import Tuple, List

logging.basicConfig(level=logging.INFO, format="%(message)s")

def read_numbers(file_path: str) -> Tuple[List[int], List[str]]:
    """
    Lee un archivo y extrae números enteros válidos.

    Args:
        file_path (str): Ruta del archivo

    Returns:
        Tuple[List[int], List[str]]: (números válidos, errores)
    """
    numbers = []
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                value = line.strip()
                if not value:
                    errors.append(f"Línea {line_num}: Línea vacía")
                    continue

                try:
                    num = int(value)
                    numbers.append(num)
                except ValueError:
                    try:
                        float_num = float(value)
                        if float_num.is_integer():
                            numbers.append(int(float_num))
                        else:
                            errors.append(f"Línea {line_num}: '{value}' no es entero")
                    except ValueError:
                        errors.append(f"Línea {line_num}: '{value}' no es número válido")
    except FileNotFoundError:
        logging.error("Error: Archivo '%s' no encontrado", file_path)
        sys.exit(1)

    return numbers, errors

def to_binary(number: int) -> str:
    """
    Convierte un entero a binario sin usar prefijos.

    Args:
        number (int): Número a convertir

    Returns:
        str: Representación binaria sin prefijo.
    """
    if number == 0:
        return "0"

    binary = []
    while number > 0:
        binary.append(str(number % 2))
        number = number // 2

    return "".join(reversed(binary))

def to_hex(number: int) -> str:
    """
    Convierte un entero a hexadecimal sin usar prefijos.

    Args:
        number (int): Número a convertir

    Returns:
        str: Representación hexadecimal en mayúsculas sin prefijo.
    """
    if number == 0:
        return "0"

    hex_map = "0123456789ABCDEF"
    hex_digits = []

    while number > 0:
        remainder = number % 16
        hex_digits.append(hex_map[remainder])
        number = number // 16

    return "".join(reversed(hex_digits))

def calculate_decimal_equivalent(numbers: List[int]) -> List[int]:
    """
    Calcula un valor en el rango de 0 a 100 para cada número.

    Args:
        numbers (List[int]): Lista de números.

    Returns:
        List[int]: Lista de valores en el rango de 0 a 100.
    """
    if not numbers:
        return []

    min_num = min(numbers)
    max_num = max(numbers)
    if max_num == min_num:
        return [50] * len(numbers)  # Si todos los números son iguales, asignamos 50
    return [round(100 * (num - min_num) / (max_num - min_num)) for num in numbers]

def main():
    """
    Función principal del programa.
    """
    if len(sys.argv) != 2:
        logging.error("Uso: python convertNumbers.py archivoConDatos.txt")
        sys.exit(1)

    start_time = time.time()
    file_path = sys.argv[1]

    numbers, errors = read_numbers(file_path)

    if not numbers:
        logging.error("No se encontraron números válidos")
        sys.exit(1)

    # Calcular valores normalizados en decimal (0-100)
    decimal_values = calculate_decimal_equivalent(numbers)

    # Generar resultados
    results = ["Índice\tNúmero\tDecimal\tBinario\tHexadecimal", "=" * 50]
    for i, (num, dec) in enumerate(zip(numbers, decimal_values), start=1):
        results.append(f"{i}\t{num}\t{dec}\t{to_binary(num)}\t{to_hex(num)}")

    execution_time = time.time() - start_time
    time_msg = f"\nTiempo de ejecución: {execution_time:.4f} segundos"

    # Mostrar en consola
    logging.info("\n".join(results))
    logging.info(time_msg)
    for error in errors:
        logging.warning(error)

    # Escribir archivo
    with open("ConversionResults.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))
        f.write(time_msg)
        if errors:
            f.write("\n\nErrores:\n" + "\n".join(errors))

if __name__ == "__main__":
    main()
