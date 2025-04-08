import hashlib, random

# Parámetro común: número primo grande y generador (escogidos estáticamente para demostración)
P = 0x7fffffffffffffffffffffffffffffffff  # primo grande (~2^127 - 1, usado aquí como ejemplo)
G = 5  # generador elegido (debe ser primitivo mod P)

def hash_id(identifier):
    """Aplica SHA-256 al identificador y devuelve un entero módulo P."""
    h = hashlib.sha256(identifier.encode('utf-8')).digest()
    return int.from_bytes(h, byteorder='big') % P

def buscaComunes(listaA, listaB):
    """
    Encuentra elementos comunes entre listaA (aerolínea) y listaB (autoridad) usando PSI (ECDH).
    - Precondición: los elementos de ambas listas son identificadores únicos (ej. pasaportes) en formato de texto.
    - Retorna un conjunto con los identificadores comunes, sin revelar elementos no comunes.
    """
    # Secretos aleatorios de cada parte
    a = random.randrange(1, P)  # secreto aerolínea
    b = random.randrange(1, P)  # secreto autoridad

    # Cifrar conjuntos
    A_enc = [pow(G, a * hash_id(x), P) for x in listaA]  # lista de g^(a*H(x)) mod P
    B_enc = [pow(G, b * hash_id(y), P) for y in listaB]  # lista de g^(b*H(y)) mod P

    # Computar claves compartidas
    A_shared = [pow(val, b, P) for val in A_enc]  # eleva cada A_i^b -> g^(a*b*H(x))
    B_shared = [pow(val, a, P) for val in B_enc]  # eleva cada B_j^a -> g^(a*b*H(y))

    # Identificar intersección mediante coincidencia de claves
    conjunto_B = set(B_shared)
    comunes = [listaA[i] for i, k in enumerate(A_shared) if k in conjunto_B]
    return set(comunes)

# Ejemplo de uso:
pasajeros = ["ID001", "ID002", "ID003", "ID004"]
sospechosos = ["ID003", "ID005", "ID001"]
print(buscaComunes(pasajeros, sospechosos))  # Salida esperada: {"ID001", "ID003"}
