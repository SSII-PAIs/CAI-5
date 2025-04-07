from phe import paillier

# Generación de claves Paillier con 2048 bits
public_key, private_key = paillier.generate_paillier_keypair(n_length=2048)

# Recibir los valores de los gastos desde la consola
gasto1 = int(input("Introduce el primer gasto: "))
gasto2 = int(input("Introduce el segundo gasto: "))

# Cifrado de los valores
c1 = public_key.encrypt(gasto1)
c2 = public_key.encrypt(gasto2)

# Suma homomórfica: se pueden sumar directamente los objetos cifrados
c_suma = c1 + c2

# Descifrado de la suma
resultado = private_key.decrypt(c_suma)
print("Suma cifrada descifrada:", resultado)
