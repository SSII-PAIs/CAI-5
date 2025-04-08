import time
from phe import paillier

def consulta_pir(base_datos, idx_consulta, n_length=2048):

    # 1. El cliente genera sus claves Paillier
    public_key, private_key = paillier.generate_paillier_keypair(n_length=n_length)

    # 2. Se construye un vector de consulta cifrado:
    # Se cifra un 1 en la posición deseada y 0 en las demás.
    consulta_cifrada = []
    for j in range(len(base_datos)):
        bit = 1 if j == idx_consulta else 0
        consulta_cifrada.append(public_key.encrypt(bit))
    
    # 3. El servidor computa la respuesta cifrada:
    # Se inicia la suma homomórfica con el cifrado de 0.
    respuesta_cifrada = public_key.encrypt(0)
    for c_bit, precio in zip(consulta_cifrada, base_datos):
        # La operación c_bit * precio equivale a multiplicar el bit cifrado por el valor del precio;
        # luego se suma homomórficamente.
        respuesta_cifrada += c_bit * precio
    
    # 4. El cliente descifra la respuesta
    precio_recuperado = private_key.decrypt(respuesta_cifrada)
    return precio_recuperado

# ============================== PRUEBAS ==============================

def test_eficacia():

    print("Ejecutando pruebas de eficacia...\n")

    # Caso 1: Lista de precios de vuelos
    precios_vuelos = [120, 250, 300, 450, 500]
    indices_a_probar = [0, 2, 4]
    for idx in indices_a_probar:
        resultado = consulta_pir(precios_vuelos, idx)
        esperado = precios_vuelos[idx]
        print(f"Consulta en índice {idx}: esperado={esperado} vs resultado={resultado}")
        assert resultado == esperado, f"Error en consulta en índice {idx}"

    # Caso 2: Otra lista de datos simulados
    datos_simulados = [10, 20, 30, 40, 50, 60, 70]
    indices_a_probar = [1, 3, 6]
    for idx in indices_a_probar:
        resultado = consulta_pir(datos_simulados, idx)
        esperado = datos_simulados[idx]
        print(f"Consulta en índice {idx}: esperado={esperado} vs resultado={resultado}")
        assert resultado == esperado, f"Error en consulta en índice {idx}"
    
    print("\nPruebas de eficacia completadas exitosamente.\n")


def test_eficiencia():

    print("Ejecutando pruebas de eficiencia...\n")
    
    # Creamos una base de datos simulada de 100 elementos (por ejemplo, precios aleatorios)
    base_datos = list(range(100))  # Precios 0, 1, 2, ..., 99
    idx_consulta = 50  # Consultamos el valor en la posición 50
    
    # Medir tiempo de consulta PIR usando clave de 64 bits (solo para test de eficiencia)
    start_pir = time.time()
    resultado_pir = consulta_pir(base_datos, idx_consulta, n_length=64)
    end_pir = time.time()
    tiempo_pir = end_pir - start_pir
    
    # Medir tiempo de búsqueda directa
    start_dir = time.time()
    resultado_directo = base_datos[idx_consulta]
    end_dir = time.time()
    tiempo_directo = end_dir - start_dir

    print(f"Tiempo consulta PIR (clave 64 bits): {tiempo_pir:.6f} segundos")
    print(f"Tiempo búsqueda directa: {tiempo_directo:.6f} segundos")
    print(f"Resultado PIR: {resultado_pir}, Resultado directo: {resultado_directo}")
    
    assert resultado_pir == resultado_directo, "El resultado PIR no coincide con la búsqueda directa."
    print("\nPruebas de eficiencia completadas.\n")

if __name__ == '__main__':
    # Ejecutar pruebas de eficacia y eficiencia
    test_eficacia()
    test_eficiencia()
