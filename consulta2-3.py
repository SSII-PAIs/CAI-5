from phe import paillier

def consulta_pir(base_datos, idx_consulta):
    # 1. El cliente genera sus claves Paillier con 2048 bits
    public_key, private_key = paillier.generate_paillier_keypair(n_length=2048)

    # 2. Construir vector de consulta cifrado
    consulta_cifrada = []
    for j in range(len(base_datos)):
        bit = 1 if j == idx_consulta else 0
        consulta_cifrada.append(public_key.encrypt(bit))  # ciframos 1 en la posición deseada, 0 en las demás

    # 3. El servidor computa la respuesta cifrada usando la base de datos
    # Aquí se hace la suma ponderada homomórfica: bit * valor
    respuesta_cifrada = public_key.encrypt(0)  # comenzamos con 0 cifrado
    for c_bit, precio in zip(consulta_cifrada, base_datos):
        respuesta_cifrada += c_bit * precio  # multiplicación escalar y suma homomórfica

    # 4. El cliente descifra la respuesta
    precio_recuperado = private_key.decrypt(respuesta_cifrada)
    return precio_recuperado

# Ejemplo de uso:
precios_vuelos = [120, 250, 300, 450, 500]  # base de datos simulada
consulta_index = 4  # queremos el precio del vuelo en índice 2 (300)
resultado = consulta_pir(precios_vuelos, consulta_index)
print("Precio recuperado:", resultado)
