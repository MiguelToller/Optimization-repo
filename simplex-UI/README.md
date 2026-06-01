# Resolutor de Programação Linear - Algoritmo Simplex com Interface Gráfica

Este projeto é uma aplicação desktop desenvolvida em Python para resolver problemas de Programação Linear (Otimização), utilizando uma implementação própria e nativa do método **Simplex Primal**. A ferramenta conta com uma interface gráfica de usuário (GUI) limpa e intuitiva, permitindo a inserção dinâmica de variáveis e restrições.

---

## 🚀 Funcionalidades

* **Implementação Própria do Simplex:** Motor de cálculo executado de forma pura através de operações de pivoteamento no Tableau Simplex.
* **Interface Moderna (UI):** Desenvolvida com a biblioteca `CustomTkinter`, oferecendo suporte nativo ao modo escuro ou claro (acompanhando o sistema operacional).
* **Estrutura Dinâmica:** Botões operacionais para adicionar ou remover linhas de restrições de forma ilimitada, conforme as dimensões do problema.
* **Tratamento Automático de Sinais:** Conversão matemática integrada quando o usuário seleciona restrições do tipo maior ou igual (`>=`).
* **Validação de Entradas:** Bloqueios internos no código que impedem o travamento do software caso o usuário insira valores vazios ou formatos de matriz incompatíveis.

---

## 🛠️ Tecnologias Utilizadas

* Python 3 - Linguagem de programação base.
* CustomTkinter - Construção da interface gráfica customizada.
* NumPy - Manipulação matemática da estrutura do Tableau, matrizes e vetores.

---

## 📦 Pré-requisitos e Instalação

Para rodar o projeto, você precisará ter o Python instalado em seu computador e as bibliotecas externas listadas acima.

### 1. Clonar o Repositório

Abra o seu terminal na pasta desejada e execute os comandos:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Instalar as Dependências

Você pode instalar as dependências utilizando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Nota:** Caso prefira não utilizar o arquivo `requirements.txt`, você pode instalar os pacotes diretamente executando o comando abaixo:

```bash
pip install customtkinter numpy
```

### 3. Executar a Aplicação

Após instalar as dependências, inicie o programa com o comando:

```bash
python main.py
```
