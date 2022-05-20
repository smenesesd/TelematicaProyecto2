import numpy as np
import random as rd

Filas  = rd.randint(2,10)
Columnas = rd.randint(2,10)

Matriz = np.zeros((Filas, Columnas))

for i in range(Filas):
    for j in range(Columnas):
        Digito = rd.randint(0,99)
        Matriz[i,j] = Digito

print(Matriz)
print("\n\n")

Num = rd.randint(0,101)
print("Numero es: ", Num)

diagonal  =0

for i in range(Filas):
    for j in range(Columnas):
        if j >= diagonal:
            Matriz[i,j] = Num
    diagonal +=1

print(Matriz)