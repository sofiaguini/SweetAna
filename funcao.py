from datetime import date
from pathlib import Path
import json
import base64


# ============================================================
# CAMINHOS
# ============================================================

PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_IMAGENS = PASTA_PROJETO / "imagens"
ARQUIVO_LISTA_COMPRAS = PASTA_PROJETO / "lista_compras.json"


# ============================================================
# RECEITA DO DIA
# ============================================================

def selecionar_receita_do_dia(caderno):
    """
    Escolhe uma receita de forma determinística.
    A receita muda de acordo com o dia, mas permanece a mesma
    durante todo o dia.
    """

    if not caderno.receitas:
        return None

    indice = date.today().toordinal() % len(caderno.receitas)

    return caderno.receitas[indice]


# ============================================================
# LISTA DE COMPRAS
# ============================================================

def normalizar_texto(texto):
    """Padroniza um texto para facilitar comparações."""

    return " ".join(str(texto).lower().strip().split())


def carregar_lista_compras():
    """Carrega a lista de compras salva em JSON."""

    if not ARQUIVO_LISTA_COMPRAS.exists():
        return []

    try:
        with open(
            ARQUIVO_LISTA_COMPRAS,
            "r",
            encoding="utf-8"
        ) as arquivo:
            dados = json.load(arquivo)

        if isinstance(dados, list):
            return dados

    except (OSError, json.JSONDecodeError):
        pass

    return []


def salvar_lista_compras(lista):
    """Salva a lista de compras em JSON."""

    with open(
        ARQUIVO_LISTA_COMPRAS,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            lista,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def ingrediente_ja_na_lista(lista, ingrediente):
    """Verifica se um ingrediente já está na lista."""

    ingrediente_normalizado = normalizar_texto(ingrediente)

    for item in lista:
        if isinstance(item, dict):
            nome = item.get("nome", "")
        else:
            nome = str(item)

        if normalizar_texto(nome) == ingrediente_normalizado:
            return True

    return False


def adicionar_ingredientes(lista, ingredientes):
    """
    Adiciona ingredientes sem criar duplicações exatas.

    Retorna a quantidade de novos itens adicionados.
    """

    adicionados = 0

    for ingrediente in ingredientes:

        if not ingrediente_ja_na_lista(lista, ingrediente):

            lista.append({
                "nome": ingrediente,
                "comprado": False
            })

            adicionados += 1

    return adicionados


# ============================================================
# IMAGENS
# ============================================================

def localizar_imagem(nome_arquivo):
    """
    Procura uma imagem na pasta imagens.
    """

    if not nome_arquivo:
        return None

    nome = Path(nome_arquivo).name

    caminhos = [
        PASTA_IMAGENS / nome,
        PASTA_PROJETO / nome,
    ]

    for caminho in caminhos:
        if caminho.exists():
            return caminho

    return None


def imagem_para_base64(caminho):
    """
    Converte uma imagem em Base64 para uso no HTML/CSS.
    """

    if not caminho or not Path(caminho).exists():
        return None

    caminho = Path(caminho)

    extensao = caminho.suffix.lower()

    tipos = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp"
    }

    tipo = tipos.get(extensao, "image/png")

    with open(caminho, "rb") as arquivo:
        dados = base64.b64encode(arquivo.read()).decode()

    return f"data:{tipo};base64,{dados}"


# ============================================================
# PREPAROS DAS RECEITAS COMPOSTAS
# ============================================================

RELACAO_PREPAROS = {

    "Bolo de Cenoura": [
        "Massa Cenoura",
        "Brigadeiro Tradicional"
    ],

    "Bolo de Chocolate com Framboesa": [
        "Massa Chocolate",
        "Brigadeiro Tradicional",
        "Geleia de Frutas Vermelhas"
    ],

    "Bolo de Morango": [
        "Massa Branca",
        "Brigadeiro de Leite Ninho",
        "Creme de Baunilha"
    ],

    "Bolo Red Velvet": [
        "Massa Red Velvet",
        "Creme de Limão Siciliano"
    ],
}


def buscar_preparo_por_nome(caderno, nome):
    """
    Procura um preparo pelo nome.
    """

    for preparo in caderno.preparos:

        if normalizar_texto(preparo.nome) == normalizar_texto(nome):
            return preparo

    return None


def obter_preparos_da_receita(receita, caderno):
    """
    Retorna os preparos que fazem parte de uma receita composta.

    Exemplo:

    Bolo de Cenoura
        ↓
    Massa Cenoura
        ↓
    Brigadeiro Tradicional
    """

    nomes = RELACAO_PREPAROS.get(receita.nome, [])

    preparos = []

    for nome in nomes:

        preparo = buscar_preparo_por_nome(
            caderno,
            nome
        )

        if preparo is not None:
            preparos.append(preparo)

    return preparos


def receita_e_composta(receita):
    """
    Verifica se a receita possui preparos internos.
    """

    return receita.nome in RELACAO_PREPAROS


# ============================================================
# INGREDIENTES DE UMA RECEITA COMPLETA
# ============================================================

def obter_ingredientes_completos(receita, caderno):
    """
    Junta os ingredientes da receita final com os ingredientes
    dos preparos que fazem parte dela.

    Evita repetir exatamente o mesmo ingrediente.
    """

    ingredientes = []

    def adicionar(ingrediente):
        if normalizar_texto(ingrediente) not in [
            normalizar_texto(item)
            for item in ingredientes
        ]:
            ingredientes.append(ingrediente)

    # Ingredientes próprios da receita final
    for ingrediente in receita.ingredientes:
        adicionar(ingrediente)

    # Ingredientes dos preparos
    for preparo in obter_preparos_da_receita(
        receita,
        caderno
    ):

        for ingrediente in preparo.ingredientes:
            adicionar(ingrediente)

    return ingredientes


# ============================================================
# MODO DE PREPARO DA RECEITA COMPLETA
# ============================================================

def obter_etapas_completas(receita, caderno):
    """
    Monta todas as etapas necessárias para executar uma
    receita composta.

    Retorna uma lista de blocos contendo:

    - nome da etapa
    - ingredientes
    - modo de preparo
    """

    etapas = []

    preparos = obter_preparos_da_receita(
        receita,
        caderno
    )

    # --------------------------------------------------------
    # PREPAROS BASE
    # --------------------------------------------------------

    for preparo in preparos:

        etapas.append({
            "titulo": preparo.nome,
            "tipo": "preparo",
            "ingredientes": preparo.ingredientes,
            "modo_preparo": preparo.modo_preparo
        })

    # --------------------------------------------------------
    # MONTAGEM DA RECEITA FINAL
    # --------------------------------------------------------

    etapas.append({
        "titulo": "Montagem e finalização",
        "tipo": "montagem",
        "ingredientes": [],
        "modo_preparo": receita.modo_preparo
    })

    return etapas