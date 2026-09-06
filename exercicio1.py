"""
Exercicio 1 - Multiplicacao de matrizes distribuida com MPI (mpi4py)

Regras atendidas:
  1. rank 0 gera as matrizes A e B
  2. A e B sao enviadas a todos os processos via broadcast (bcast)
  3. cada processo calcula apenas um bloco de linhas de C
  4. os blocos sao reunidos no rank 0 via gather
  5. rank 0 monta a matriz final
  6. o tempo de execucao e exibido em milissegundos

Uso:
  mpirun --hostfile hosts -np 4 python3 exercicio1.py 300
"""

from mpi4py import MPI
import random
import sys
import time

# N pode vir pela linha de comando: python3 exercicio1.py 600
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ---------------------------------------------------------------
# 1) Somente o rank 0 gera as matrizes
# ---------------------------------------------------------------
A = None
B = None

if rank == 0:
    random.seed(42)  # semente fixa: todos os testes usam as mesmas matrizes
    A = [[random.random() for _ in range(N)] for _ in range(N)]
    B = [[random.random() for _ in range(N)] for _ in range(N)]

# sincroniza todos antes de comecar a medir o tempo
comm.Barrier()
inicio = time.time()

# ---------------------------------------------------------------
# 2) Broadcast das matrizes para todos os processos
# ---------------------------------------------------------------
A = comm.bcast(A, root=0)
B = comm.bcast(B, root=0)

# ---------------------------------------------------------------
# 3) Divisao das linhas entre os processos
#    (funciona mesmo quando N nao e divisivel por size)
# ---------------------------------------------------------------
base = N // size
resto = N % size
linha_ini = rank * base + min(rank, resto)
linha_fim = linha_ini + base + (1 if rank < resto else 0)

# cada processo calcula apenas as suas linhas: C[i][j] = soma A[i][k]*B[k][j]
bloco_local = []
for i in range(linha_ini, linha_fim):
    linha = [0.0] * N
    for j in range(N):
        soma = 0.0
        for k in range(N):
            soma += A[i][k] * B[k][j]
        linha[j] = soma
    bloco_local.append(linha)

# ---------------------------------------------------------------
# 4) Gather: todos enviam seu bloco para o rank 0
# ---------------------------------------------------------------
blocos = comm.gather(bloco_local, root=0)

# ---------------------------------------------------------------
# 5) rank 0 monta a matriz final e mostra o tempo
# ---------------------------------------------------------------
if rank == 0:
    C = []
    for bloco in blocos:  # gather preserva a ordem dos ranks
        C.extend(bloco)

    fim = time.time()

    print("N =", N, "| processos =", size)
    print("Linhas montadas em C:", len(C))
    print("C[0][0] =", C[0][0])
    print("Tempo distribuido:", (fim - inicio) * 1000, "ms")
