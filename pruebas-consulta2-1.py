import random
import time
from phe import paillier

def test_case(num_values):
    # Generar par de claves de 2048 bits
    public_key, private_key = paillier.generate_paillier_keypair(n_length=2048)
    
    # Generar lista de valores aleatorios (gastos)
    values = [random.randint(1, 1000) for _ in range(num_values)]
    plain_sum = sum(values)
    
    # Cifrar cada uno de los valores
    encrypted_values = [public_key.encrypt(v) for v in values]
    
    # Suma homomórfica: se suman los valores cifrados
    encrypted_sum = encrypted_values[0]
    for ev in encrypted_values[1:]:
        encrypted_sum += ev
    
    # Descifrar la suma
    decrypted_sum = private_key.decrypt(encrypted_sum)
    return values, plain_sum, decrypted_sum

def main():
    for num in [5, 100]:
        print(f"Prueba con {num} valores:")
        inicio = time.time()
        values, plain_sum, decrypted_sum = test_case(num)
        fin = time.time()
        
        print("Valores:", values)
        print("Suma en claro:", plain_sum)
        print("Suma cifrada descifrada:", decrypted_sum)
        print("Prueba exitosa:", plain_sum == decrypted_sum)
        print("Tiempo de ejecución: {:.4f} segundos".format(fin - inicio))
        print("-" * 50)

if __name__ == "__main__":
    main()
