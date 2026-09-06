"""
Multiplicacao de matrizes - versao com THREADS (paralelismo em uma unica maquina)

Uso:
  python3 multiplicacaoMatrizThread.py 300
"""

import random
import sys
import threading
import time

N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
THREADS = 4

random.seed(42)  # mesma semente das outras versoes
A = [[random.random() for _ in range(N)] for _ in range(N)]
B = [[random.random() for _ in range(N)] for _ in range(N)]
C = [[0] * N for _ in range(N)]


def calcular(ini, fim):
    for i in range(ini, fim):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k] * B[k][j]


inicio = time.time()

threads = []
linhas = N // THREADS
for t in range(THREADS):
    ini = t * linhas
    fim_bloco = N if t == THREADS - 1 else (t + 1) * linhas
    th = threading.Thread(target=calcular, args=(ini, fim_bloco))
    threads.append(th)
    th.start()

for th in threads:
    th.join()

fim = time.time()

print("N =", N, "| threads =", THREADS)
print("C[0][0] =", C[0][0])
print("Tempo com threads:", (fim - inicio) * 1000, "ms")
