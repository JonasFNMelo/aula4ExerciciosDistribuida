"""
Exercicio 2 - Estimativa de PI pelo metodo de Monte Carlo com MPI (mpi4py)

Ideia: em um quadrado de lado 1 que contem um quarto de circulo de raio 1,
a proporcao de pontos aleatorios que caem dentro do circulo tende a PI/4.
Logo:  PI ~= 4 * (pontos_dentro / pontos_totais)

Passos atendidos:
  - cada processo gera sua parte dos pontos aleatorios (x, y)
  - conta localmente quantos satisfazem x*x + y*y <= 1
  - as contagens locais sao somadas no rank 0 com reduce(op=MPI.SUM)
  - o rank 0 calcula PI e exibe o tempo em milissegundos

Uso:
  mpirun --hostfile hosts -np 4 python3 exercicio2.py 10000000
"""

from mpi4py import MPI
import random
import sys
import time

# total de pontos considerando TODOS os processos somados
# (assim a comparacao com a versao sequencial fica justa)
TOTAL = int(sys.argv[1]) if len(sys.argv) > 1 else 10000000

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ---------------------------------------------------------------
# 1) Divisao do trabalho: cada processo fica com uma fatia do total
#    (o resto e distribuido entre os primeiros ranks)
# ---------------------------------------------------------------
pontos_locais = TOTAL // size
if rank < TOTAL % size:
    pontos_locais += 1

# semente DIFERENTE por processo: se todos usassem a mesma, gerariam
# exatamente os mesmos pontos e a amostragem deixaria de ser independente
random.seed(1234 + rank)

comm.Barrier()
inicio = time.time()

# ---------------------------------------------------------------
# 2) Contagem local de pontos dentro do quarto de circulo
# ---------------------------------------------------------------
dentro_local = 0
for _ in range(pontos_locais):
    x = random.random()
    y = random.random()
    if x * x + y * y <= 1:
        dentro_local += 1

# ---------------------------------------------------------------
# 3) Agregacao: soma das contagens locais no rank 0
# ---------------------------------------------------------------
dentro_total = comm.reduce(dentro_local, op=MPI.SUM, root=0)
pontos_total = comm.reduce(pontos_locais, op=MPI.SUM, root=0)

# ---------------------------------------------------------------
# 4) Calculo final apenas no rank 0
# ---------------------------------------------------------------
if rank == 0:
    pi = 4 * dentro_total / pontos_total
    fim = time.time()

    print("Processos:", size)
    print("Pontos totais gerados:", pontos_total)
    print("Pontos dentro do circulo:", dentro_total)
    print("PI aproximado:", pi)
    print("Erro absoluto:", abs(pi - 3.141592653589793))
    print("Tempo distribuido:", (fim - inicio) * 1000, "ms")

# 5) Finalizacao do ambiente MPI: o mpi4py chama MPI.Finalize()
#    automaticamente ao encerrar o programa.
