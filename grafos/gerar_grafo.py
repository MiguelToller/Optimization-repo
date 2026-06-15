import csv
import os
from pyvis.network import Network

# Descobre a pasta onde este script está salvo para não errar o caminho
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(diretorio_atual, "dados.csv")
caminho_html = os.path.join(diretorio_atual, "grafo.html")


def extrair_casa(nome):
    if "Stark" in nome:
        return "#7F8C8D"  # Cinza
    elif "Lannister" in nome:
        return "#F1C40F"  # Dourado
    elif "Targaryen" in nome:
        return "#E74C3C"  # Vermelho
    elif "Baratheon" in nome:
        return "#D35400"  # Laranja
    elif "Tully" in nome:
        return "#3498DB"  # Azul
    else:
        return "#1ABC9C"  # Turquesa


# Inicializa a rede
net = Network(
    height="750px",
    width="100%",
    bgcolor="#222222",
    font_color="white",
    directed=True,
)
net.toggle_physics(True)

# Variável de controle (Corrigida!)
linhas_concluidas = 0

# Abre o arquivo usando o caminho absoluto
with open(caminho_csv, encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        origem = linha["origem"].strip()
        destino = linha["destino"].strip()
        relacao = linha["relacao"].strip()

        cor_origem = extrair_casa(origem)
        cor_destino = extrair_casa(destino)

        net.add_node(origem, label=origem, color=cor_origem, title=f"Casa de {origem}")
        net.add_node(
            destino, label=destino, color=cor_destino, title=f"Casa de {destino}"
        )
        net.add_edge(origem, destino, title=relacao, color="#95A5A6", width=2)
        linhas_concluidas += 1

# Configurações de layout/física
net.set_options(
    """
var options = {
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -8000,
      "centralGravity": 0.3,
      "springLength": 95,
      "springConstant": 0.04
    },
    "minVelocity": 0.75
  }
}
"""
)

# Validação e salvamento (Corrigido para usar a mesma variável!)
if linhas_concluidas > 0:
    net.show(caminho_html, notebook=False)
    print(f"\nSucesso! {linhas_concluidas} conexões geradas.")
    print(f"Abra o arquivo direto daqui: {caminho_html}")
else:
    print(
        "\nErro: Nenhuma linha foi lida do CSV. Verifique o conteúdo do seu dados.csv!"
    )