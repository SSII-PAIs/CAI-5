#!/usr/bin/env python3
import hashlib
import random
import time

# Parámetros criptográficos (para fines de demostración)
P = 0x7fffffffffffffffffffffffffffffffff  # Número primo grande (~2^127 - 1)
G = 5  # Generador elegido

def hash_id(identifier):
    """
    Aplica SHA-256 al identificador y devuelve un entero módulo P.
    """
    h = hashlib.sha256(identifier.encode('utf-8')).digest()
    return int.from_bytes(h, byteorder='big') % P

def buscaComunes(listaA, listaB):
    """
    Encuentra elementos comunes entre listaA (aerolínea) y listaB (autoridad) usando PSI (ECDH).
    
    Precondición:
      - Los elementos de ambas listas son identificadores únicos (ej. pasaportes) en formato de texto.
      
    Retorna:
      - Un conjunto con los identificadores comunes, sin revelar elementos no comunes.
    """
    # Generar secretos aleatorios para cada parte (aerolínea y autoridad)
    a = random.randrange(1, P)
    b = random.randrange(1, P)

    # "Cifrar" cada elemento de la lista
    A_enc = [pow(G, a * hash_id(x), P) for x in listaA]  # Para la aerolínea
    B_enc = [pow(G, b * hash_id(y), P) for y in listaB]  # Para la autoridad

    # Computar claves compartidas
    A_shared = [pow(val, b, P) for val in A_enc]  # g^(a*b*H(x)) para cada x en listaA
    B_shared = [pow(val, a, P) for val in B_enc]  # g^(a*b*H(y)) para cada y en listaB

    # Hallar la intersección mediante coincidencias en las claves
    conjunto_B = set(B_shared)
    comunes = [listaA[i] for i, k in enumerate(A_shared) if k in conjunto_B]
    return set(comunes)

# --- PRUEBAS ---

def test_pequena():
    """
    Prueba con listas pequeñas (3-4 elementos), similar al ejemplo dado.
    """
    print("Test con listas pequeñas de ejemplo:")
    pasajeros = ["ID001", "ID002", "ID003", "ID004"]
    sospechosos = ["ID003", "ID005", "ID001"]
    expected = {"ID001", "ID003"}
    
    result = buscaComunes(pasajeros, sospechosos)
    print("Pasajeros:", pasajeros)
    print("Sospechosos:", sospechosos)
    print("Esperado:", expected)
    print("Resultado:", result)
    print("Test " + ("OK" if result == expected else "FALLÓ"))
    print("-" * 40)

def test_listas_generadas():
    """
    Prueba con listas generadas aleatoriamente: 
    Se crea una listaA de 50 identificadores y una listaB de 50 identificadores donde se incorporan exactamente 20 elementos comunes.
    """
    print("Test con listas generadas aleatoriamente (50 elementos, 20 comunes):")
    # ListaA de 50 identificadores únicos
    listaA = [f"ID_{i:03d}" for i in range(50)]
    
    # Seleccionar 20 de listaA para que sean comunes en listaB
    comunes = random.sample(listaA, 20)
    # Generar 30 identificadores nuevos para listaB
    exclusivos = [f"ID_{50+i:03d}" for i in range(30)]
    
    # ListaB se forma uniendo los 20 comunes con los 30 exclusivos
    listaB = comunes + exclusivos
    random.shuffle(listaB)
    
    expected = set(comunes)
    result = buscaComunes(listaA, listaB)
    print("ListaA (50 elementos):", listaA)
    print("ListaB (50 elementos, 20 comunes):", listaB)
    print("Esperado:", expected)
    print("Resultado:", result)
    print("Test " + ("OK" if result == expected else "FALLÓ"))
    print("-" * 40)

def test_rendimiento():
    """
    Prueba de rendimiento para distintos tamaños de entrada.
    
    Se miden los tiempos de ejecución para listas de:
      - 100 elementos en cada lista (~0.03 segundos esperado)
      - 500 elementos (~0.15 segundos)
      - 1000 elementos (~0.35 segundos)
    """
    print("Pruebas de rendimiento:")
    sizes = [100, 500, 1000]
    
    for size in sizes:
        # Generar listaA con "size" identificadores únicos
        listaA = [f"ID_A_{i}" for i in range(size)]
        # Para listaB, incluir un 10% de elementos comunes y el resto nuevos
        comunes = random.sample(listaA, max(1, size // 10))  # garantizar al menos 1 común
        exclusivos = [f"ID_B_{i}" for i in range(size - len(comunes))]
        listaB = comunes + exclusivos
        random.shuffle(listaB)

        start = time.time()
        result = buscaComunes(listaA, listaB)
        end = time.time()
        duration = end - start

        print(f"Tamaño: {size} elementos en cada lista")
        print(f"Identificadores comunes esperados: {set(comunes)}")
        print(f"Identificadores comunes encontrados: {result}")
        print(f"Tiempo de cómputo: {duration:.4f} segundos")
        print("-" * 40)

def main():
    print("Iniciando pruebas de la función buscaComunes")
    test_pequena()
    test_listas_generadas()
    test_rendimiento()
    print("Pruebas completadas.")

if __name__ == '__main__':
    main()
