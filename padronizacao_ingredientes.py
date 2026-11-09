import re


# ============================================================
# PADRONIZAÇÃO DE INGREDIENTES
# ============================================================

SUBSTITUICOES = {
    # Óleos
    "óleo de girassol": "óleo",
    "oleo de girassol": "óleo",
    "óleo vegetal": "óleo",
    "oleo vegetal": "óleo",
    "óleo de soja": "óleo",
    "oleo de soja": "óleo",
    "óleo de milho": "óleo",
    "oleo de milho": "óleo",

    # Açúcares
    "açúcar": "açúcar refinado",
    "acucar": "açúcar refinado",
    "açúcar refinado": "açúcar refinado",
    "acucar refinado": "açúcar refinado",
    "açúcar cristal": "açúcar cristal",
    "acucar cristal": "açúcar cristal",
    "açúcar de confeiteiro": "açúcar de confeiteiro",
    "acucar de confeiteiro": "açúcar de confeiteiro",
    "açúcar impalpável": "açúcar impalpável",
    "acucar impalpavel": "açúcar impalpável",
    "açúcar refinado (para uma geleia mais doce colocar 100 g)": "açúcar refinado",
    "acucar refinado (para uma geleia mais doce colocar 100 g)": "açúcar refinado",
    "açúcar refinado (para uma geleia mais doce colocar 100 g)": "açúcar refinado",
    "açúcar refinado (para uma geleia mais doce colocar 100 g)": "açúcar refinado",

    # Aromas e especiarias
    "fava de cumaru": "cumaru",
    "fava do cumaru": "cumaru",
    "cumaru em fava": "cumaru",

    "extrato de baunilha": "baunilha",
    "essência de baunilha": "baunilha",
    "essencia de baunilha": "baunilha",


    # Chocolate/cacau
    "cacau 50% em pó": "cacau 50%",
    "cacau 50% em po": "cacau 50%",
    "cacau em pó": "cacau",
    "cacau em po": "cacau",
    "chocolate em pó": "chocolate",
    "chocolate em po": "chocolate",
    "chocolate meio amargo": "chocolate meio amargo",
    "chocolate meio amargo em gotas": "chocolate meio amargo",
    "chocolate meio amargo em gotas (ou picado)": "chocolate meio amargo",
    "chocolate ao leite": "chocolate ao leite",
    "chocolate ao leite em gotas": "chocolate ao leite",
    "chocolate ao leite em gotas (ou picado)": "chocolate ao leite",
    "chocolate branco": "chocolate branco",
    "chocolate branco em gotas": "chocolate branco",
    "chocolate branco em gotas ou picado fino": "chocolate branco",


    # Frutas
    "morangos": "morango",
    "morangos cortados (200 g)": "morango",
    "framboesas": "framboesa",
    "limões": "limão",
    "limoes": "limão",

    # Outros plurais
    "ovos": "ovo",
    "açúcares": "açúcar",
    "acucares": "açúcar",

    #Outros
    "fermento químico em pó": "fermento químico",
    "fermento quimico em po": "fermento químico",
    "fermento" : "fermento químico",
    "leite" : "leite",
    "leite integral" : "leite",
    "manteiga sem sal" : "manteiga sem sal",
    "manteiga com sal" : "manteiga com sal",
    "manteiga sem sal (1)" : "manteiga sem sal",
    "manteiga sem sal (2)" : "manteiga sem sal",
    "ovo + leite para pincelar" : "ovo",
    "água" : "água",
    "água filtrada" : "água",
    "água mineral" : "água",
    "água para cobrir o açúcar" : "água",
    "suco de limão siciliano + raspas de 1 limão siciliano" : "limão siciliano",
    "suco de limão" : "limão",

}


ROTULOS_IGNORADOS = {
    "base",
    "ingrediente",
    "ingredientes",
    "caramelo",
    "creme",
    "cobertura",
    "recheio",
    "massa",
    "calda",
    "finalização",
    "finalizacao",
    "montagem",
    "decoração",
    "decoracao",
    "confeitos",
    "confeito",
    "decorações",
    "decoracoes",
}


# ============================================================
# FUNÇÕES
# ============================================================

def formatar_nome_ingrediente(nome):
    """
    Deixa o nome do ingrediente com uma apresentação mais limpa.

    Exemplo:
        "FARINHA DE TRIGO" -> "Farinha de trigo"
    """

    nome = " ".join(str(nome).strip().lower().split())

    if not nome:
        return ""

    return nome[:1].upper() + nome[1:]


def limpar_descricao_extra(texto):
    """
    Remove descrições que não representam um ingrediente
    independente.

    Exemplos:
        "Confeitos e decorações: coloridos" -> ""
        "Caramelo: açúcar refinado" -> "açúcar refinado"
        "Chocolate (opcional)" -> "Chocolate"
    """

    texto = str(texto).strip()

    if not texto:
        return ""

    # Remove linhas exclusivamente relacionadas à decoração
    if re.match(
        r"^\s*(?:confeitos?|decorações?|decoracoes?|"
        r"confeitos\s+e\s+decorações?|confeitos\s+e\s+decoracoes?|"
        r"finalização|finalizacao|decoração|decoracao)"
        r"(?:\s*[:,\-]\s*|\s+).*$",
        texto,
        flags=re.IGNORECASE,
    ):
        return ""

    # Trata textos como:
    # "Base: 200 g de farinha"
    # "Caramelo: 100 g de açúcar"
    if ":" in texto:
        esquerda, direita = texto.split(":", 1)

        if esquerda.strip().lower() in ROTULOS_IGNORADOS:
            texto = direita.strip()

    # Remove observações que não precisam aparecer
    texto = re.sub(
        r"\s*\((?:a gosto|opcional|para decorar|para decoração|"
        r"para decoracao)\)\s*",
        " ",
        texto,
        flags=re.IGNORECASE,
    )

    return " ".join(texto.split()).strip(" .,:;-—")


def ingrediente_generico(texto):
    """
    Converte um ingrediente da receita para um nome adequado
    para busca e lista de compras.

    As quantidades continuam preservadas nas receitas originais.
    Aqui trabalhamos apenas com o nome do ingrediente.
    """

    texto = str(texto).strip()

    if not texto:
        return ""

    # Remove rótulos no início
    texto = re.sub(
        r"^\s*(?:base|ingrediente|ingredientes)\s*(?::|,|-|\s)\s*",
        "",
        texto,
        flags=re.IGNORECASE,
    )

    texto = limpar_descricao_extra(texto)

    if not texto:
        return ""

    # ========================================================
    # REMOVE QUANTIDADES
    # ========================================================

    texto = re.sub(
        r"^\s*\d+(?:[.,]\d+)?\s*"
        r"(?:g\b|grama(?:s)?\b|kg\b|quilo(?:s)?\b|mg\b|"
        r"miligrama(?:s)?\b|ml\b|mililitro(?:s)?\b|l\b|"
        r"litro(?:s)?\b|xícara(?:s)?\b|xicara(?:s)?\b|"
        r"colher(?:es)?(?:\s+de\s+(?:sopa|chá))?\b|"
        r"copo(?:s)?\b|unidade(?:s)?\b|unid\.?\b|"
        r"fava(?:s)?\b|disco(?:s)?\b|receita(?:s)?\b)"
        r"\s*(?:de|do|da)?\s*",
        "",
        texto,
        flags=re.IGNORECASE,
    )

    # Exemplo: "3 ovos"
    texto = re.sub(
        r"^\s*\d+(?:[.,]\d+)?\s*(?=ovos?\b)",
        "",
        texto,
        flags=re.IGNORECASE,
    )

    # Expressões como:
    # "uma pitada de sal"
    # "um fio de óleo"
    texto = re.sub(
        r"^\s*(?:uma\s+pitada\s+de|um\s+fio\s+de|"
        r"pitada\s+de|fio\s+de)\s+",
        "",
        texto,
        flags=re.IGNORECASE,
    )

    # "de chocolate" -> "chocolate"
    texto = re.sub(
        r"^\s*de\s+",
        "",
        texto,
        flags=re.IGNORECASE,
    )

    texto = re.sub(r"\s+", " ", texto).strip(" .,:;-—")

    if not texto:
        return ""

    # ========================================================
    # SUBSTITUIÇÕES PADRÃO
    # ========================================================

    chave = texto.lower().strip()

    nome = SUBSTITUICOES.get(chave, chave)

    # Quando houver vírgulas, transforma a informação secundária
    # em observação.
    if "," in nome:
        partes = [
            parte.strip()
            for parte in nome.split(",")
            if parte.strip()
        ]

        if partes:
            principal = partes[0]
            observacao = ", ".join(partes[1:])

            if observacao:
                nome = f"{principal} ({observacao})"
            else:
                nome = principal

    return formatar_nome_ingrediente(nome)


def ingredientes_genericos(ingredientes):
    """
    Recebe uma lista de ingredientes e devolve uma lista limpa,
    sem repetições.
    """

    resultado = []
    vistos = set()

    for ingrediente in ingredientes:
        nome = ingrediente_generico(ingrediente)

        chave = nome.lower().strip()

        if nome and chave not in vistos:
            vistos.add(chave)
            resultado.append(nome)

    return resultado