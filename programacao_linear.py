import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
from fractions import Fraction


# ---------------- INTERSEÇÃO ----------------
def intersecao(r1, r2):
    a1, b1, c1 = r1
    a2, b2, c2 = r2

    det = a1*b2 - a2*b1
    if det == 0:
        return None

    x = Fraction(c1*b2 - c2*b1, det)
    y = Fraction(a1*c2 - a2*c1, det)

    return (x, y)


# ---------------- VERIFICAR RESTRIÇÕES ----------------
def satisfaz(p, inequacoes):
    x, y = p

    if x < 0 or y < 0:
        return False

    for a1, a2, op, vd in inequacoes:
        val = a1*x + a2*y

        if op == '<=' and val > vd: return False
        if op == '<' and val >= vd: return False
        if op == '>=' and val < vd: return False
        if op == '>' and val <= vd: return False

    return True


# ---------------- CALCULAR VÉRTICES ----------------
def calcular_vertices(inequacoes):
    retas = [(Fraction(a1), Fraction(a2), Fraction(vd)) for a1, a2, _, vd in inequacoes]

    pontos = []

    for r1, r2 in combinations(retas, 2):
        p = intersecao(r1, r2)
        if p:
            pontos.append(p)

    for a1, a2, vd in retas:
        if a1 != 0:
            pontos.append((Fraction(vd, a1), Fraction(0)))
        if a2 != 0:
            pontos.append((Fraction(0), Fraction(vd, a2)))

    pontos.append((Fraction(0), Fraction(0)))

    validos = [p for p in pontos if satisfaz(p, inequacoes)]
    validos = list(set(validos))

    return validos


# ---------------- MAIN ----------------
def resolver():
    sistema = []

    print("\n--- Sistema de Inequações ---\n")

    while True:
        print(f"Inequação #{len(sistema) + 1}:")
        a1 = float(input("a1 (x): "))
        a2 = float(input("a2 (y): "))
        op = input("Sinal (<, <=, >, >=): ")
        vd = float(input("Valor direito: "))

        sistema.append((a1, a2, op, vd))

        if input("Continuar? (s/n): ") != 's':
            break

    # ---------------- FUNÇÃO OBJETIVO ----------------
    print("\n--- Função Objetivo ---")
    a = float(input("Coeficiente de x: "))
    b = float(input("Coeficiente de y: "))

    func_obj = lambda x, y: a*x + b*y
    titulo = f"Max z = {a}x + {b}y"

    # ---------------- VÉRTICES ----------------
    vertices = calcular_vertices(sistema)

    print("\nVértices da região viável:")
    for p in vertices:
        print(p)

    # ---------------- TABELA ----------------
    print("\nTabela da função objetivo:")

    melhor_ponto = None
    melhor_valor = None

    for x, y in vertices:
        z = func_obj(x, y)

        if melhor_valor is None or z > melhor_valor:
            melhor_valor = z
            melhor_ponto = (x, y)

    for x, y in vertices:
        z = func_obj(x, y)

        if (x, y) == melhor_ponto:
            print(f"* ({x}, {y}) -> z = {z}  <-- MÁXIMO")
        else:
            print(f"  ({x}, {y}) -> z = {z}")

    print(f"\n>>> PONTO ÓTIMO: ({melhor_ponto[0]}, {melhor_ponto[1]}) -> z = {melhor_valor}")

    # ---------------- PLOT ----------------
    plt.figure(figsize=(10, 7))

    max_x = max(float(p[0]) for p in vertices)
    max_y = max(float(p[1]) for p in vertices)

    limite_x = max_x + 2
    limite_y = max_y + 2

    x = np.linspace(0, limite_x, 500)
    y = np.linspace(0, limite_y, 500)

    X, Y = np.meshgrid(x, y)
    regiao = np.ones_like(X, dtype=bool)

    # região viável
    for a1, a2, op, vd in sistema:
        expr = a1*X + a2*Y

        if op == '<=': regiao &= (expr <= vd)
        elif op == '<': regiao &= (expr < vd)
        elif op == '>=': regiao &= (expr >= vd)
        elif op == '>': regiao &= (expr > vd)

    plt.imshow(regiao, extent=(0, limite_x, 0, limite_y),
               origin='lower', alpha=0.3, cmap='Blues')

    # retas
    for a1, a2, op, vd in sistema:
        if a2 != 0:
            y_reta = (vd - a1*x) / a2
            plt.plot(x, y_reta, label=f'{a1}x + {a2}y {op} {vd}')
        else:
            plt.axvline(vd/a1, label=f'{a1}x {op} {vd}')

    # pontos pretos
    for px, py in vertices:
        plt.scatter(float(px), float(py), color='black')
        plt.text(float(px), float(py), f"({px},{py})", fontsize=9)

    # ponto ótimo vermelho
    px, py = melhor_ponto
    plt.scatter(float(px), float(py), color='red', s=120)

    # proporção correta
    plt.gca().set_aspect('equal', adjustable='box')

    plt.axhline(0, color='black')
    plt.axvline(0, color='black')

    plt.grid(True)
    plt.legend()
    plt.title(titulo)

    plt.show()


if __name__ == "__main__":
    resolver()