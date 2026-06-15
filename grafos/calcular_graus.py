import csv
import os
import networkx as nx

# Descobre a pasta onde este script está salvo para ler o dados.csv correto
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(diretorio_atual, "dados.csv")

# 1. CRIAÇÃO DOS GRAFOS (Direcionado e Não-Direcionado)
G_direcionado = nx.DiGraph()
G_nao_direcionado = nx.Graph()

# Carrega os dados do teu arquivo CSV
with open(caminho_csv, encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)
    for linha in leitor:
        origem = linha["origem"].strip()
        destino = linha["destino"].strip()
        
        # Adiciona no grafo direcionado (respeita a seta)
        G_direcionado.add_edge(origem, destino)
        # Adiciona no grafo não-direcionado (ignora a seta / mão dupla)
        G_nao_direcionado.add_edge(origem, destino)

print("=" * 50)
print("     ANÁLISE COMPLETA DOS GRAUS DE SEPARAÇÃO     ")
print("=" * 50)


# =============================================================================
# SCENARIO 1: SEGUINDO AS RETAS (Grafo Direcionado)
# =============================================================================
print("\n>>> 1. CONSIDERANDO O SENTIDO DAS SETAS (Direcionado) <<<")

caminhos_dir = []
maior_grau_dir = 0
par_maior_dir = None

for nodo_origem in G_direcionado.nodes():
    for nodo_destino in G_direcionado.nodes():
        if nodo_origem != nodo_destino and nx.has_path(G_direcionado, nodo_origem, nodo_destino):
            distancia = nx.shortest_path_length(G_direcionado, nodo_origem, nodo_destino)
            caminhos_dir.append(distancia)
            
            if distancia > maior_grau_dir:
                maior_grau_dir = distancia
                par_maior_dir = (nodo_origem, nodo_destino)

if caminhos_dir:
    media_dir = sum(caminhos_dir) / len(caminhos_dir)
    print(f"• Menor grau de separação ativo: 1 (Conexões diretas)")
    print(f"• Grau de separação médio (quando há conexão): {media_dir:.2f}")
    print(f"• Maior grau de separação encontrado (Diâmetro): {maior_grau_dir}")
    if par_maior_dir:
        caminho_exemplo = nx.shortest_path(G_direcionado, par_maior_dir[0], par_maior_dir[1])
        print(f"  Exemplo de caminho máximo: {' -> '.join(caminho_exemplo)}")
else:
    print("• Nenhuma conexão direcionada encontrada.")


# =============================================================================
# SCENARIO 2: SEM SEGUIR AS RETAS (Grafo Não-Direcionado)
# =============================================================================
print("\n>>> 2. IGNORANDO O SENTIDO DAS SETAS (Não-Direcionado) <<<")

caminhos_ndir = []
maior_grau_ndir = 0
par_maior_ndir = None

for nodo_origem in G_nao_direcionado.nodes():
    for nodo_destino in G_nao_direcionado.nodes():
        if nodo_origem != nodo_destino and nx.has_path(G_nao_direcionado, nodo_origem, nodo_destino):
            distancia = nx.shortest_path_length(G_nao_direcionado, nodo_origem, nodo_destino)
            caminhos_ndir.append(distancia)
            
            if distancia > maior_grau_ndir:
                maior_grau_ndir = distancia
                par_maior_ndir = (nodo_origem, nodo_destino)

if caminhos_ndir:
    media_ndir = sum(caminhos_ndir) / len(caminhos_ndir)
    print(f"• Grau de separação médio: {media_ndir:.2f}")
    print(f"• Maior grau de separação encontrado (Sem restrição de retas): {maior_grau_ndir}")
    if par_maior_ndir:
        caminho_exemplo_ndir = nx.shortest_path(G_nao_direcionado, par_maior_ndir[0], par_maior_ndir[1])
        print(f"  Exemplo de caminho máximo: {' <-> '.join(caminho_exemplo_ndir)}")
else:
    print("• Nenhuma conexão encontrada no modo não-direcionado.")

print("\n" + "=" * 50)