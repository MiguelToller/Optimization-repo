import random
from fractions import Fraction

# Função para imprimir a matriz de forma organizada
def imprimir_matriz(matriz):
    for linha in matriz:
        print([str(num) for num in linha])
    print()  # Linha em branco para melhor visualização

# Função que aplica o método de Gauss (diagonalização)
def diagonalizar(matriz):
    n = len(matriz)  # Número de linhas

    for i in range(n):  # Percorre cada linha (cada pivo)
        # 1. Normalizar a linha do pivo (tornar o pivo = 1)
        pivo = matriz[i][i]  # Elemento da diagonal principal (pivo)
        
        # Divide toda a linha pelo pivo para que ele vire 1
        matriz[i] = [Fraction(x, pivo) for x in matriz[i]]

        print(f"Apos normalizar linha {i}:")
        imprimir_matriz(matriz)

        # 2. Zerar os outros elementos da coluna
        for j in range(n):  # Percorre todas as outras linhas
            if j != i:  # Ignora a própria linha do pivo
                fator = matriz[j][i]  # Elemento que queremos zerar
                
                # Atualiza a linha: linha_j = linha_j - fator * linha_i
                matriz[j] = [
                    matriz[j][k] - fator * matriz[i][k]
                    for k in range(n + 1)  # n + 1 porque é matriz aumentada
                ]

                print(f"Apos zerar coluna {i} na linha {j}:")
                imprimir_matriz(matriz)

    return matriz  # Retorna a matriz já diagonalizada


# -------- CONFIGURAÇÃO --------
n = 3  # numero de variaveis (define o tamanho do sistema)

# Gerar matriz aumentada (n x n+1)
# Cada linha terá n coeficientes + 1 termo independente
matriz = [
    [random.randint(1, 10) for _ in range(n + 1)]  # Números aleatórios de 1 a 10
    for _ in range(n)
]

print("Matriz original:")
imprimir_matriz(matriz)

# Aplica o método de diagonalização (Gauss)
matriz_diag = diagonalizar(matriz)

print("Matriz diagonalizada:")
imprimir_matriz(matriz_diag)