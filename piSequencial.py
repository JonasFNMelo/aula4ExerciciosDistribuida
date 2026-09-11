"""
Estimativa de PI por Monte Carlo - versao SEQUENCIAL (sem threads, sem MPI)

Uso:
  python3 piSequencial.py 10000000
"""

import random
import sys
import time

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10000000

random.seed(1234)
dentro = 0

inicio = time.time()

for _ in range(N):
    x = random.random()
    y = random.random()
    if x * x + y * y <= 1:
        dentro += 1

pi = 4 * dentro / N
fim = time.time()

print("Pontos totais gerados:", N)
print("Pontos dentro do circulo:", dentro)
print("PI aproximado:", pi)
print("Erro absoluto:", abs(pi - 3.141592653589793))
print("Tempo sequencial:", (fim - inicio) * 1000, "ms")
