from pathlib import Path
from datetime import date
import json
import re

import streamlit as st
from PIL import Image, ImageOps

from dados import carregar_caderno
from funcao import (
    selecionar_receita_do_dia,
    carregar_lista_compras,
    salvar_lista_compras,
    adicionar_ingredientes,
    localizar_imagem,
    obter_preparos_da_receita,
    obter_ingredientes_completos,
    obter_etapas_completas,
    receita_e_composta,
)
from padronizacao_ingredientes import (
    formatar_nome_ingrediente,
    ingrediente_generico,
    ingredientes_genericos,
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Meu Caderno de Receitas",
    page_icon="🍰",
    layout="wide",
    initial_sidebar_state="expanded",
)

PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_IMAGENS = PASTA_PROJETO / "imagens"
ARQUIVO_LISTA = PASTA_PROJETO / "lista_compras.json"

VINHO = "#5A1018"
VINHO_ESCURO = "#3D090E"
VINHO_CLARO = "#7A333B"
VERDE = "#859277"
VERDE_CLARO = "#DDE3D6"
MARROM = "#77563C"
MARROM_CLARO = "#B79B82"
CREME = "#F8F2E4"
CREME_ESCURO = "#EEE4D0"
BRANCO = "#FFFDF8"
TEXTO = "#493D35"
CINZA = "#8D8176"
BORDA = "#DCCEB9"


# ============================================================
# CSS / IDENTIDADE VISUAL
# ============================================================

st.markdown(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Montserrat:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            color: {TEXTO};
        }}

        .stApp {{
            background: {CREME};
        }}

        [data-testid="stSidebar"] {{
            background: {VINHO_ESCURO};
            border-right: 1px solid rgba(255,253,248,.10);
        }}

        [data-testid="stSidebar"] * {{
            font-family: 'Montserrat', Arial, sans-serif;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            width: 100%;
            min-height: 42px;
            border: 1px solid rgba(255,255,255,.14);
            background: rgba(255,255,255,.035);
            color: {BRANCO} !important;
            border-radius: 12px;
            text-align: left;
            padding: .62rem .85rem;
            font-size: .86rem;
            font-weight: 500;
            transition: .2s ease;
        }}

        [data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(255,255,255,.10);
            border-color: rgba(255,255,255,.28);
            transform: translateX(2px);
        }}

        [data-testid="stSidebar"] .stButton > button:focus {{
            box-shadow: 0 0 0 2px rgba(255,253,248,.18);
        }}

        h1, h2, h3, h4 {{
            font-family: 'Cormorant Garamond', Georgia, serif !important;
            color: {VINHO_ESCURO} !important;
        }}

        p, label, .stMarkdown, .stTextInput, .stSelectbox, .stMultiSelect {{
            font-family: 'Montserrat', Arial, sans-serif;
        }}

        /* Seletor de ingredientes: mesma linguagem visual do restante do projeto. */
        .ingredient-selector-label {{
            color: {VINHO_ESCURO} !important;
            font-family: 'Montserrat', Arial, sans-serif;
            font-size: .86rem;
            font-weight: 700;
            margin: .2rem 0 .45rem;
        }}

        .stMultiSelect [data-baseweb="select"] > div {{
            background: {BRANCO} !important;
            border: 1px solid {BORDA} !important;
            border-radius: 14px !important;
            box-shadow: 0 4px 14px rgba(73,61,53,.04) !important;
            min-height: 48px !important;
        }}

        .stMultiSelect [data-baseweb="select"] input {{
            color: {TEXTO} !important;
            font-family: 'Montserrat', Arial, sans-serif !important;
        }}

        .stMultiSelect [data-baseweb="tag"] {{
            background: {VERDE_CLARO} !important;
            border: 1px solid {VERDE} !important;
            border-radius: 999px !important;
            padding: 2px 8px !important;
        }}

        .stMultiSelect [data-baseweb="tag"] span {{
            color: {VINHO_ESCURO} !important;
            font-family: 'Montserrat', Arial, sans-serif !important;
            font-size: .78rem !important;
            font-weight: 600 !important;
        }}

        div[data-baseweb="popover"],
        div[data-baseweb="menu"] {{
            background: {BRANCO} !important;
        }}

        [data-baseweb="option"] {{
            color: {TEXTO} !important;
            font-family: 'Montserrat', Arial, sans-serif !important;
        }}

        [data-baseweb="option"]:hover {{
            background: {CREME_ESCURO} !important;
        }}

        /* Dropdown do seletor de ingredientes: mesma paleta do aplicativo. */
        div[data-baseweb="popover"] > div,
        div[data-baseweb="popover"] [role="listbox"],
        div[data-baseweb="popover"] [data-baseweb="menu"],
        div[data-baseweb="menu"],
        ul[role="listbox"] {{
            background: {BRANCO} !important;
            color: {TEXTO} !important;
            border-color: {BORDA} !important;
            box-shadow: 0 10px 28px rgba(73,61,53,.12) !important;
        }}

        div[data-baseweb="popover"] [data-baseweb="option"],
        div[data-baseweb="popover"] li,
        ul[role="listbox"] li {{
            background: {BRANCO} !important;
            color: {TEXTO} !important;
        }}

        div[data-baseweb="popover"] [data-baseweb="option"]:hover,
        div[data-baseweb="popover"] li:hover,
        ul[role="listbox"] li:hover {{
            background: {CREME_ESCURO} !important;
            color: {VINHO_ESCURO} !important;
        }}

        .ingredient-pill {{
            display: inline-block;
            padding: .38rem .72rem;
            margin: .18rem .25rem .18rem 0;
            border-radius: 999px;
            font-family: 'Montserrat', Arial, sans-serif;
            font-size: .78rem;
            font-weight: 600;
        }}

        .ingredient-have {{
            background: {VERDE_CLARO};
            color: {VINHO_ESCURO} !important;
            border: 1px solid #C8D3BE;
        }}

        .ingredient-missing {{
            background: {CREME_ESCURO};
            color: {MARROM} !important;
            border: 1px solid {BORDA};
        }}

        .hero-title {{
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 3.15rem;
            line-height: .98;
            font-weight: 600;
            color: {VINHO_ESCURO};
            margin-bottom: .3rem;
        }}

        .hero-subtitle {{
            color: {MARROM};
            font-size: 1rem;
            letter-spacing: .01em;
            line-height: 1.5;
        }}

        .hero-description {{
            color: {TEXTO} !important;
            font-size: .92rem;
            line-height: 1.65;
            max-width: 680px;
            margin: .7rem 0 1.1rem;
        }}

        .section-title {{
            font-family: 'Cormorant Garamond', Georgia, serif;
            color: {VINHO_ESCURO};
            font-size: 2rem;
            font-weight: 600;
            margin: 1.4rem 0 .65rem;
        }}

        .eyebrow {{
            color: {VINHO};
            font-size: .72rem;
            letter-spacing: .16em;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: .3rem;
        }}

        .soft-card {{
            background: {BRANCO};
            border: 1px solid {BORDA};
            border-radius: 18px;
            padding: 1.2rem;
            box-shadow: 0 8px 22px rgba(73,61,53,.07);
        }}

        .stMarkdown, .stMarkdown p, .stMarkdown li,
        [data-testid="stText"], [data-testid="stCaptionContainer"] p {{
            color: {TEXTO} !important;
        }}

        .stMarkdown strong, .stMarkdown b {{
            color: {VINHO_ESCURO} !important;
        }}

        .recipe-intro {{
            background: {CREME_ESCURO};
            border: 1px solid {BORDA};
            border-left: 4px solid {VERDE};
            padding: 1rem 1.1rem;
            border-radius: 0 14px 14px 0;
            margin: .5rem 0 1.4rem;
            color: {TEXTO} !important;
            line-height: 1.55;
        }}

        .preparo-card {{
            background: {BRANCO};
            border: 1px solid {BORDA};
            border-radius: 18px;
            padding: 1.3rem 1.4rem;
            margin: 0 0 1.25rem;
            box-shadow: 0 7px 20px rgba(73,61,53,.06);
        }}

        .preparo-header {{
            display: flex;
            align-items: center;
            gap: .85rem;
            padding-bottom: .9rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid {BORDA};
        }}

        .preparo-numero {{
            width: 38px;
            height: 38px;
            min-width: 38px;
            border-radius: 50%;
            background: {VINHO};
            color: {BRANCO} !important;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Montserrat', Arial, sans-serif;
            font-size: .78rem;
            font-weight: 700;
        }}

        .preparo-titulo {{
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.75rem;
            line-height: 1.1;
            color: {VINHO_ESCURO} !important;
            font-weight: 600;
        }}

        .preparo-subtitulo {{
            color: {CINZA} !important;
            font-size: .72rem;
            text-transform: uppercase;
            letter-spacing: .12em;
            margin-top: .15rem;
        }}

        .preparo-label {{
            color: {VINHO} !important;
            font-family: 'Montserrat', Arial, sans-serif;
            font-size: .74rem;
            font-weight: 700;
            letter-spacing: .1em;
            text-transform: uppercase;
            margin: .8rem 0 .45rem;
        }}

        .preparo-ingrediente {{
            color: {TEXTO} !important;
            font-size: .9rem;
            line-height: 1.55;
            margin: .2rem 0;
        }}

        .preparo-passo {{
            color: {TEXTO} !important;
            font-size: .9rem;
            line-height: 1.65;
            padding: .25rem 0 .55rem;
            border-bottom: 1px solid rgba(220,206,185,.45);
        }}

        .preparo-passo:last-child {{
            border-bottom: none;
        }}

        .step-title {{
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.35rem;
            color: {VINHO};
            font-weight: 600;
            margin: 1rem 0 .4rem;
        }}

        .recipe-card-title {{
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.55rem;
            line-height: 1.1;
            color: {VINHO_ESCURO};
            margin-top: .8rem;
        }}

        .meta {{
            color: {CINZA};
            font-size: .78rem;
            margin-top: .3rem;
        }}

        .badge {{
            display: inline-block;
            background: {VERDE_CLARO};
            color: {VINHO_ESCURO};
            border-radius: 999px;
            padding: .3rem .65rem;
            margin: .15rem .15rem .15rem 0;
            font-size: .73rem;
            font-weight: 600;
        }}

        .empty-state {{
            background: {BRANCO};
            border: 1px dashed {BORDA};
            border-radius: 18px;
            padding: 2.5rem 1.5rem;
            text-align: center;
            color: {CINZA};
        }}

        .empty-icon {{
            color: {VINHO_CLARO};
            font-size: 2rem;
            margin-bottom: .5rem;
        }}

        .ingredient-item {{
            color: {TEXTO};
            padding: .35rem 0;
            line-height: 1.5;
        }}

        .missing-item {{
            color: {VINHO};
            padding: .3rem 0;
        }}

        .combo-result {{
            border-radius: 14px;
            padding: 1rem 1.2rem;
            margin: .9rem 0 1.2rem;
            border: 1px solid {{BORDA}};
            box-shadow: 0 4px 14px rgba(73,61,53,.04);
        }}

        .combo-result-ok {{
            background: #F1F4EC;
            border-left: 4px solid {{VERDE}};
        }}

        .combo-result-no {{
            background: #F7F1E8;
            border-left: 4px solid {{MARROM_CLARO}};
        }}

        .combo-result-title {{
            font-family: 'Montserrat', Arial, sans-serif;
            font-size: .72rem;
            font-weight: 700;
            letter-spacing: .09em;
            text-transform: uppercase;
            color: {{VINHO_ESCURO}} !important;
            margin-bottom: .45rem;
        }}

        .combo-result-text {{
            color: {{TEXTO}} !important;
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.3rem;
            font-weight: 600;
            line-height: 1.3;
        }}

        .combo-result-text span {{
            color: {{MARROM_CLARO}} !important;
            padding: 0 .3rem;
        }}

        .combo-result-help {{
            color: {{MARROM}} !important;
            font-family: 'Montserrat', Arial, sans-serif;
            font-size: .78rem;
            line-height: 1.45;
            margin-top: .5rem;
        }}

        .success-box {{
            background: {VERDE_CLARO};
            border: 1px solid #C7D1BE;
            color: {VINHO_ESCURO};
            padding: .8rem 1rem;
            border-radius: 12px;
            margin: .7rem 0;
        }}

        [data-baseweb="select"] *,
        [data-baseweb="input"] *,
        [data-baseweb="textarea"] * {{
            color: {TEXTO} !important;
        }}

        [data-baseweb="select"] > div,
        [data-baseweb="input"] > div {{
            background-color: {BRANCO} !important;
            border-color: {BORDA} !important;
        }}

        input::placeholder {{
            color: {CINZA} !important;
            opacity: 1 !important;
        }}

        [data-testid="stWidgetLabel"] p {{
            color: {TEXTO} !important;
            font-weight: 600 !important;
        }}

        .sidebar-brand {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            padding: .35rem .1rem .85rem;
        }}

        .sidebar-brand-inner {{
            width: 178px;
            min-height: 148px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem 1.15rem;
            background: rgba(255,253,248,.035);
            border: 1px solid rgba(255,253,248,.16);
            border-radius: 48% 48% 42% 42% / 38% 38% 52% 52%;
            box-shadow: inset 0 0 0 5px rgba(255,253,248,.018);
        }}

        .sidebar-brand img {{
            width: 100%;
            max-width: 154px;
            max-height: 128px;
            object-fit: contain;
            display: block;
        }}

        .sidebar-frase {{
            text-align: center;
            color: rgba(255,253,248,.82) !important;
            font-family: 'Montserrat', Arial, sans-serif;
            font-size: .78rem;
            line-height: 1.55;
            margin: .2rem 0 .95rem;
        }}

        .stButton > button {{
            border-radius: 10px;
            border: 1px solid {BORDA};
            background: {BRANCO};
            color: {VINHO_ESCURO};
            font-weight: 600;
            transition: .2s ease;
        }}

        .stButton > button:hover {{
            border-color: {VINHO};
            color: {VINHO};
            background: {CREME_ESCURO};
        }}

        .stCheckbox label p {{
            color: {TEXTO} !important;
        }}

        hr {{
            border-color: {BORDA};
        }}

        .section-divider {{
            height: 1px;
            background: {BORDA};
            margin: 1.7rem 0 1rem;
        }}

        .shortcut-card {{
            background: {BRANCO};
            border: 1px solid {BORDA};
            border-radius: 16px;
            padding: .95rem 1rem 1rem;
            min-height: 178px;
            box-shadow: 0 6px 18px rgba(73,61,53,.055);
        }}

        .shortcut-title {{
            font-family: 'Cormorant Garamond', Georgia, serif;
            color: {VINHO_ESCURO};
            font-size: 1.65rem;
            line-height: 1.05;
            font-weight: 600;
            margin: .05rem 0 .35rem;
        }}

        .shortcut-description {{
            color: {CINZA};
            font-family: 'Montserrat', Arial, sans-serif;
            font-size: .8rem;
            line-height: 1.55;
            min-height: 2.5rem;
            margin-bottom: .8rem;
        }}

        .combo-card {{
            background: {BRANCO};
            border: 1px solid {BORDA};
            border-radius: 14px;
            padding: .85rem 1rem;
            margin: .55rem 0;
        }}

        .combo-valid {{
            border-left: 4px solid {VERDE};
        }}

        .combo-missing {{
            border-left: 4px solid {MARROM_CLARO};
            background: {CREME_ESCURO};
        }}

        .combo-label {{
            color: {CINZA};
            font-family: 'Montserrat', Arial, sans-serif;
            font-size: .67rem;
            font-weight: 700;
            letter-spacing: .12em;
            margin-bottom: .25rem;
        }}

        .combo-nomes {{
            color: {VINHO_ESCURO};
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.25rem;
            line-height: 1.25;
        }}

        .combo-nomes span {{
            color: {MARROM_CLARO};
            padding: 0 .25rem;
        }}

        /* Sidebar clara: melhora o contraste com a logo escura. */
        [data-testid="stSidebar"] {{
            background: {CREME_ESCURO} !important;
            border-right: 1px solid {BORDA};
        }}

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
            color: {TEXTO} !important;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            background: rgba(255,253,248,.72) !important;
            color: {VINHO_ESCURO} !important;
            border: 1px solid {BORDA} !important;
            border-radius: 12px !important;
            box-shadow: none !important;
        }}

        [data-testid="stSidebar"] .stButton > button:hover {{
            background: {BRANCO} !important;
            color: {VINHO} !important;
            border-color: {MARROM_CLARO} !important;
        }}

        [data-testid="stSidebar"] .stButton > button:focus {{
            box-shadow: 0 0 0 2px rgba(90,16,24,.12) !important;
        }}

        .sidebar-brand-inner {{
            width: 182px;
            min-height: 142px;
            padding: .65rem 1rem;
            background: rgba(255,253,248,.55);
            border: 1px solid rgba(119,86,60,.22);
            border-radius: 34% 66% 57% 43% / 45% 40% 60% 55%;
            box-shadow: 0 8px 22px rgba(73,61,53,.06);
            transform: rotate(-1deg);
        }}

        .sidebar-brand img {{
            width: auto;
            max-width: 155px;
            max-height: 122px;
            object-fit: contain;
            display: block;
            transform: rotate(1deg);
        }}

        .sidebar-frase {{
            color: {MARROM} !important;
        }}

        .stCheckbox label p {{
            color: {TEXTO} !important;
            font-family: 'Montserrat', Arial, sans-serif !important;
            font-size: .92rem !important;
        }}

        [data-testid="stMetricValue"],
        [data-testid="stMetricLabel"] {{
            color: {VINHO_ESCURO} !important;
        }}

        /* Remove a barra/elementos de edição que poluem o canto superior. */
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        .stDeployButton {{
            display: none !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ESTADO
# ============================================================


def _carregar_caderno():
    return carregar_caderno()


if "caderno" not in st.session_state:
    st.session_state.caderno = _carregar_caderno()

if "lista_compras" not in st.session_state:
    st.session_state.lista_compras = carregar_lista_compras()

if "receita_do_dia" not in st.session_state:
    st.session_state.receita_do_dia = selecionar_receita_do_dia(
        st.session_state.caderno
    )

if "pagina" not in st.session_state:
    st.session_state.pagina = "Início"

if "receita_selecionada" not in st.session_state:
    st.session_state.receita_selecionada = None


# ============================================================
# FUNÇÕES DE ESTADO / NAVEGAÇÃO
# ============================================================

def navegar(pagina):
    st.session_state.pagina = pagina
    st.session_state.receita_selecionada = None


def abrir_receita(receita):
    st.session_state.receita_selecionada = receita.nome
    st.session_state.pagina = "Receitas"


def obter_receita_selecionada():
    nome = st.session_state.receita_selecionada

    if not nome:
        return None

    return st.session_state.caderno.buscar_receita(nome)


def obter_ingredientes_brutos_para_compra(receita):
    """
    Retorna somente ingredientes que precisam ser comprados.

    Em receitas compostas, referências como "2 discos de massa de cenoura"
    ou "2 receitas de brigadeiro tradicional" não entram na lista.
    Os ingredientes reais vêm dos preparos que compõem a receita.
    """
    caderno = st.session_state.caderno
    preparos = obter_preparos_da_receita(receita, caderno)

    if not preparos:
        return ingredientes_genericos(receita.ingredientes)

    ingredientes = []

    def adicionar_unico(item):
        normalizado = " ".join(str(item).lower().split())
        if not any(normalizado == " ".join(str(x).lower().split()) for x in ingredientes):
            ingredientes.append(item)

    nomes_preparos = [p.nome.lower() for p in preparos]

    for ingrediente in receita.ingredientes:
        texto = ingrediente.lower().strip()
        referencia_preparo = any(nome in texto for nome in nomes_preparos)
        referencia_generica = (
            "disco de" in texto
            or "discos de" in texto
            or "receita de" in texto
            or "receitas de" in texto
            or "confeitos e decorações" in texto
        )

        if not referencia_preparo and not referencia_generica:
            adicionar_unico(ingrediente)

    for preparo in preparos:
        for ingrediente in preparo.ingredientes:
            adicionar_unico(ingrediente)

    return ingredientes_genericos(ingredientes)


def adicionar_receita_a_lista(receita):
    ingredientes = obter_ingredientes_brutos_para_compra(receita)

    quantidade = adicionar_ingredientes(
        st.session_state.lista_compras,
        ingredientes
    )

    salvar_lista_compras(st.session_state.lista_compras)
    return quantidade


def alternar_compra(indice):
    item = st.session_state.lista_compras[indice]

    if isinstance(item, dict):
        item["comprado"] = not item.get("comprado", False)

    salvar_lista_compras(st.session_state.lista_compras)


def remover_item(indice):
    st.session_state.lista_compras.pop(indice)
    salvar_lista_compras(st.session_state.lista_compras)


# ============================================================
# COMPONENTES VISUAIS
# ============================================================

def mostrar_imagem(caminho, largura="100%", altura="240px", padronizar=False):
    imagem = localizar_imagem(caminho)

    if imagem:
        if padronizar:
            try:
                foto = Image.open(imagem).convert("RGB")
                foto = ImageOps.fit(
                    foto,
                    (1200, 850),
                    method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.5),
                )
                st.image(foto, use_container_width=True)
                return
            except Exception:
                pass

        st.image(str(imagem), use_container_width=True)
    else:
        st.markdown(
            f"""
            <div style="
                height:{altura};
                background:{CREME_ESCURO};
                border:1px solid {BORDA};
                border-radius:16px;
                display:flex;
                align-items:center;
                justify-content:center;
                color:{CINZA};
                font-family:Georgia,serif;
                font-size:1.1rem;
            ">
                Imagem indisponível
            </div>
            """,
            unsafe_allow_html=True,
        )


def titulo_pagina(titulo, subtitulo=""):
    st.markdown(
        f'<div class="eyebrow">Meu Caderno de Receitas</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="hero-title">{titulo}</div>',
        unsafe_allow_html=True,
    )

    if subtitulo:
        st.markdown(
            f'<div class="hero-subtitle">{subtitulo}</div>',
            unsafe_allow_html=True,
        )


def mostrar_ingredientes(ingredientes, titulo="Ingredientes"):
    st.markdown(
        f'<div class="section-title">{titulo}</div>',
        unsafe_allow_html=True,
    )

    if not ingredientes:
        st.caption("Não há ingredientes adicionais cadastrados nesta etapa.")
        return

    for ingrediente in ingredientes:
        st.markdown(
            f'<div class="ingredient-item">• {ingrediente}</div>',
            unsafe_allow_html=True,
        )


def mostrar_modo_preparo(texto):
    linhas = str(texto or "").splitlines()

    for linha in linhas:
        linha = linha.strip()
        if linha:
            st.markdown(f"• {linha}")


# ============================================================
# ETAPAS ESTRUTURADAS DE RECEITAS
# ============================================================


ROTULOS_ETAPAS = {
    "base": "Base",
    "creme": "Creme",
    "geleia": "Geleia",
    "montagem": "Montagem",
    "caramelo": "Caramelo",
    "pudim": "Pudim",
}


def _normalizar_rotulo_etapa(rotulo):
    rotulo = " ".join(str(rotulo).strip().lower().split())
    return ROTULOS_ETAPAS.get(rotulo)


def _quebrar_modo_em_etapas(texto):
    """Divide o modo de preparo quando há títulos como Base:, Creme: e Montagem:."""
    etapas = []
    etapa_atual = None

    for linha in str(texto or "").splitlines():
        linha = linha.strip()

        if not linha:
            continue

        rotulo = None
        if linha.endswith(":"):
            rotulo = _normalizar_rotulo_etapa(linha[:-1])

        if rotulo:
            etapa_atual = {"titulo": rotulo, "linhas": []}
            etapas.append(etapa_atual)
            continue

        if etapa_atual is None:
            etapa_atual = {"titulo": "Preparo", "linhas": []}
            etapas.append(etapa_atual)

        etapa_atual["linhas"].append(linha)

    return etapas


def _ingredientes_por_etapa(receita, titulos):
    """Separa ingredientes cadastrados com rótulos como 'Base:' e 'Creme:'."""
    grupos = {titulo: [] for titulo in titulos}
    mapeamento = {titulo.lower(): titulo for titulo in titulos}

    # No pudim, o livro chama o grupo de ingredientes de 'Creme',
    # mas a etapa do preparo é apresentada como 'Pudim'.
    if receita.nome.lower() == "pudim de leite condensado":
        mapeamento["creme"] = "Pudim"

    for ingrediente in receita.ingredientes:
        texto = str(ingrediente).strip()
        match = re.match(r"^\s*([^:]+):\s*(.*)$", texto)

        if match:
            rotulo = _normalizar_rotulo_etapa(match.group(1))
            restante = match.group(2).strip()

            if rotulo and rotulo.lower() in mapeamento:
                grupos[mapeamento[rotulo.lower()]].append(restante)
                continue

        if len(titulos) == 1:
            grupos[titulos[0]].append(texto)

    return grupos


def obter_etapas_estruturadas(receita):
    """
    Organiza receitas que possuem componentes independentes no livro original.

    Atualmente as receitas com divisões explícitas são:
    Cheesecake -> Base, Creme e Montagem.
    Pannacota de Cumaru -> Creme, Geleia e Montagem.
    Pudim de Leite Condensado -> Caramelo e Pudim.
    """
    nome = receita.nome.lower().strip()

    estruturas = {
        "cheesecake": ["Base", "Creme", "Montagem"],
        "pannacota de cumaru": ["Creme", "Geleia", "Montagem"],
        "pudim de leite condensado": ["Caramelo", "Pudim"],
    }

    titulos = estruturas.get(nome)

    if not titulos:
        return [{
            "titulo": "Preparo",
            "ingredientes": list(receita.ingredientes),
            "modo_preparo": receita.modo_preparo,
        }]

    grupos = _ingredientes_por_etapa(receita, titulos)
    etapas_modo = _quebrar_modo_em_etapas(receita.modo_preparo)
    por_titulo_modo = {
        etapa["titulo"].lower(): etapa["linhas"]
        for etapa in etapas_modo
    }

    etapas = []

    for titulo in titulos:
        ingredientes = grupos.get(titulo, [])
        linhas = por_titulo_modo.get(titulo.lower(), [])

        if ingredientes or linhas:
            etapas.append({
                "titulo": titulo,
                "ingredientes": ingredientes,
                "modo_preparo": "\n".join(linhas),
            })

    if not etapas:
        return [{
            "titulo": "Preparo",
            "ingredientes": list(receita.ingredientes),
            "modo_preparo": receita.modo_preparo,
        }]

    return etapas


def mostrar_etapas_estruturadas(etapas):
    """Exibe cada componente da receita em um cartão visual separado."""
    for numero, etapa in enumerate(etapas, start=1):
        st.markdown(
            f'''<div class="preparo-card">
                <div class="preparo-header">
                    <div class="preparo-numero">{numero:02d}</div>
                    <div>
                        <div class="preparo-titulo">{etapa["titulo"]}</div>
                        <div class="preparo-subtitulo">Etapa da receita</div>
                    </div>
                </div>''',
            unsafe_allow_html=True,
        )

        if etapa["ingredientes"]:
            st.markdown(
                '<div class="preparo-label">Ingredientes desta etapa</div>',
                unsafe_allow_html=True,
            )
            for ingrediente in etapa["ingredientes"]:
                st.markdown(
                    f'<div class="preparo-ingrediente">• {ingrediente}</div>',
                    unsafe_allow_html=True,
                )

        if etapa["modo_preparo"]:
            st.markdown(
                '<div class="preparo-label">Modo de preparo</div>',
                unsafe_allow_html=True,
            )

            linhas = str(etapa["modo_preparo"] or "").splitlines()
            passo = 0
            for linha in linhas:
                linha = linha.strip()
                if not linha:
                    continue

                linha = re.sub(r"^\s*\d+[.)]\s*", "", linha)
                passo += 1

                st.markdown(
                    f'<div class="preparo-passo"><strong>{passo}.</strong> {linha}</div>',
                    unsafe_allow_html=True,
                )

        st.markdown('</div>', unsafe_allow_html=True)


def mostrar_botao_adicionar(receita, chave):
    if st.button(
        "＋ Adicionar ingredientes à lista",
        key=chave,
        use_container_width=True,
    ):
        quantidade = adicionar_receita_a_lista(receita)

        if quantidade:
            st.success(
                f"{quantidade} ingrediente(s) adicionado(s) à sua lista de compras."
            )
        else:
            st.info(
                "Os ingredientes desta receita já estão na sua lista de compras."
            )


def mostrar_card_receita(receita, chave):
    with st.container(border=True):
        mostrar_imagem(receita.foto, altura="210px", padronizar=True)

        st.markdown(
            f'<div class="recipe-card-title">{receita.nome}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="meta">{receita.categoria} · {receita.tempo} · {receita.dificuldade}</div>',
            unsafe_allow_html=True,
        )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "Ver receita →",
                key=f"ver_{chave}",
                use_container_width=True,
            ):
                abrir_receita(receita)
                st.rerun()

        with col2:
            texto = "♥ Favorita" if receita.favorita else "♡ Favoritar"

            if st.button(
                texto,
                key=f"fav_{chave}",
                use_container_width=True,
            ):
                if receita.favorita:
                    receita.remover_dos_favoritos()
                else:
                    receita.adicionar_aos_favoritos()
                st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

def mostrar_sidebar():
    with st.sidebar:
        logo = localizar_imagem("logo.png")

        if logo:
            import base64
            with open(logo, "rb") as arquivo:
                logo_b64 = base64.b64encode(arquivo.read()).decode()
            st.markdown(
                f'<div class="sidebar-brand"><div class="sidebar-brand-inner"><img src="data:image/png;base64,{logo_b64}"></div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="sidebar-brand"><div class="sidebar-brand-inner"><span style="font-family:Georgia,serif;font-size:1.7rem;color:{BRANCO};text-align:center;">Meu Caderno de Receitas</span></div></div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            f'<p class="sidebar-frase">Receitas, combinações e ideias<br>para preparar.</p>',
            unsafe_allow_html=True,
        )

        st.divider()

        paginas = [
            ("⌂", "Início"),
            ("▣", "Receitas"),
            ("◇", "Ingredientes"),
            ("✦", "Combinar"),
            ("♡", "Favoritas"),
            ("🛒", "Compras"),
        ]

        for icone, nome in paginas:
            if st.button(
                f"{icone}  {nome}",
                key=f"nav_{nome}",
                use_container_width=True,
            ):
                navegar(nome)
                st.rerun()

        st.divider()

        total = len(st.session_state.lista_compras)
        comprados = sum(
            1
            for item in st.session_state.lista_compras
            if isinstance(item, dict) and item.get("comprado", False)
        )

        st.markdown(
            f"**Lista de compras**  \n{comprados}/{total} itens marcados",
            unsafe_allow_html=True,
        )


# ============================================================
# INÍCIO
# ============================================================

def pagina_inicio():
    receita = st.session_state.receita_do_dia

    col1, col2 = st.columns([1.25, 1])

    with col1:
        st.markdown(
            '<div class="eyebrow">Bem-vinda à sua cozinha</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="hero-title">Meu Caderno de Receitas</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="hero-subtitle">Receitas, combinações e ideias para preparar.</div>',
            unsafe_allow_html=True,
        )

        st.write("")
        st.markdown(
            '<div class="hero-description">Um espaço para encontrar receitas, descobrir o que preparar com os ingredientes que você já tem e criar novas combinações.</div>',
            unsafe_allow_html=True,
        )

        st.write("")

        if receita:
            with st.container(border=True):
                st.markdown(
                    '<div class="eyebrow">Receita do dia</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="section-title" style="margin-top:0">{receita.nome}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<span class="badge">{receita.categoria}</span> '
                    f'<span class="badge">{receita.dificuldade}</span> '
                    f'<span class="badge">{receita.tempo}</span>',
                    unsafe_allow_html=True,
                )

                st.write("")

                c1, c2 = st.columns(2)

                with c1:
                    if st.button(
                        "Ver receita →",
                        key="home_ver_receita",
                        use_container_width=True,
                    ):
                        abrir_receita(receita)
                        st.rerun()

                with c2:
                    if st.button(
                        "＋ Lista de compras",
                        key="home_add_lista",
                        use_container_width=True,
                    ):
                        quantidade = adicionar_receita_a_lista(receita)
                        if quantidade:
                            st.success(f"{quantidade} ingrediente(s) adicionado(s).")
                        else:
                            st.info("Os ingredientes já estão na lista.")

    with col2:
        if receita:
            mostrar_imagem(receita.foto, altura="380px")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Explore o caderno</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-description" style="margin-top:-.25rem; margin-bottom:1rem;">'
        'Cada espaço do caderno tem uma função: encontrar receitas, aproveitar ingredientes, combinar preparos e organizar as compras.'
        '</div>',
        unsafe_allow_html=True,
    )

    atalhos = [
        ("01", "Receitas", "Encontre sua próxima receita e consulte cada preparo."),
        ("02", "Ingredientes", "Escolha o que já tem em casa e veja o que pode preparar."),
        ("03", "Combinar", "Monte combinações entre massas, cremes e complementos."),
        ("04", "Compras", "Reúna os ingredientes que faltam e acompanhe o que já comprou."),
    ]

    for inicio in range(0, len(atalhos), 2):
        colunas = st.columns(2)

        for coluna, (numero, titulo, descricao) in zip(colunas, atalhos[inicio:inicio + 2]):
            with coluna:
                with st.container(border=True):
                    st.markdown(
                        f'<div class="eyebrow">{numero}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="shortcut-title">{titulo}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="shortcut-description">{descricao}</div>',
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        "Explorar →",
                        key=f"atalho_{titulo}",
                        use_container_width=True,
                    ):
                        navegar(titulo)
                        st.rerun()


# ============================================================
# RECEITAS
# ============================================================

def pagina_receitas():
    receita_selecionada = obter_receita_selecionada()

    if receita_selecionada:
        pagina_detalhes_receita(receita_selecionada)
        return

    titulo_pagina(
        "Receitas",
        "Encontre uma receita, salve suas favoritas e consulte cada preparo.",
    )

    st.write("")

    col_busca, col_categoria = st.columns([2, 1])

    with col_busca:
        busca = st.text_input(
            "Buscar receita",
            placeholder="Ex.: chocolate, morango, brioche...",
            key="busca_receitas",
        )

    categorias = sorted(
        set(receita.categoria for receita in st.session_state.caderno.receitas)
    )

    with col_categoria:
        categoria = st.selectbox(
            "Categoria",
            ["Todas"] + categorias,
            key="categoria_receitas",
        )

    receitas = st.session_state.caderno.receitas

    if busca:
        termo = busca.lower().strip()
        receitas = [
            receita
            for receita in receitas
            if termo in receita.nome.lower()
            or termo in receita.categoria.lower()
            or any(termo in ingrediente.lower() for ingrediente in receita.ingredientes)
        ]

    if categoria != "Todas":
        receitas = [
            receita
            for receita in receitas
            if receita.categoria.lower() == categoria.lower()
        ]

    st.write("")

    if not receitas:
        st.markdown(
            '<div class="empty-state"><div class="empty-icon">♡</div><h3>Nenhuma receita encontrada</h3><p>Tente outro termo ou escolha outra categoria.</p></div>',
            unsafe_allow_html=True,
        )
        return

    st.caption(f"{len(receitas)} receita(s) encontrada(s)")

    for inicio in range(0, len(receitas), 3):
        colunas = st.columns(3)

        for coluna, receita in zip(colunas, receitas[inicio:inicio + 3]):
            with coluna:
                mostrar_card_receita(
                    receita,
                    f"{inicio}_{receita.nome}",
                )


def pagina_detalhes_receita(receita):
    if st.button("← Voltar para receitas", key="voltar_receitas"):
        st.session_state.receita_selecionada = None
        st.rerun()

    st.write("")

    esquerda, direita = st.columns([1, 1.15])

    with esquerda:
        mostrar_imagem(receita.foto, altura="470px")

    with direita:
        st.markdown(
            f'<div class="eyebrow">{receita.categoria}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="hero-title">{receita.nome}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<span class="badge">{receita.tempo}</span> '
            f'<span class="badge">{receita.dificuldade}</span> '
            f'<span class="badge">Rendimento: {receita.rendimento}</span>',
            unsafe_allow_html=True,
        )

        st.write("")

        c1, c2 = st.columns(2)

        with c1:
            texto = "♥ Remover dos favoritos" if receita.favorita else "♡ Adicionar aos favoritos"

            if st.button(
                texto,
                key="detalhe_favorito",
                use_container_width=True,
            ):
                if receita.favorita:
                    receita.remover_dos_favoritos()
                else:
                    receita.adicionar_aos_favoritos()
                st.rerun()

        with c2:
            mostrar_botao_adicionar(
                receita,
                "detalhe_lista",
            )

    st.divider()

    ingredientes_completos = obter_ingredientes_completos(
        receita,
        st.session_state.caderno,
    )

    mostrar_ingredientes(
        ingredientes_completos,
        "Ingredientes da receita completa",
    )

    st.divider()

    st.markdown(
        '<div class="section-title">Modo de preparo</div>',
        unsafe_allow_html=True,
    )

    if receita_e_composta(receita):
        st.markdown(
            '<div class="recipe-intro"><strong>Esta receita é composta por diferentes preparos.</strong><br>Prepare cada componente na ordem indicada e, ao final, faça a montagem da receita.</div>',
            unsafe_allow_html=True,
        )

        etapas = obter_etapas_completas(
            receita,
            st.session_state.caderno,
        )

        for numero, etapa in enumerate(etapas, start=1):
            tipo = "Preparo" if etapa["tipo"] == "preparo" else "Finalização"

            st.markdown(
                f'''<div class="preparo-card">
                    <div class="preparo-header">
                        <div class="preparo-numero">{numero:02d}</div>
                        <div>
                            <div class="preparo-titulo">{etapa["titulo"]}</div>
                            <div class="preparo-subtitulo">{tipo}</div>
                        </div>
                    </div>''',
                unsafe_allow_html=True,
            )

            if etapa["ingredientes"]:
                st.markdown(
                    '<div class="preparo-label">Ingredientes desta etapa</div>',
                    unsafe_allow_html=True,
                )

                for ingrediente in etapa["ingredientes"]:
                    st.markdown(
                        f'<div class="preparo-ingrediente">• {ingrediente}</div>',
                        unsafe_allow_html=True,
                    )

            st.markdown(
                '<div class="preparo-label">Modo de preparo</div>',
                unsafe_allow_html=True,
            )

            linhas = str(etapa["modo_preparo"] or "").splitlines()

            for passo, linha in enumerate(linhas, start=1):
                linha = linha.strip()
                if linha:
                    st.markdown(
                        f'<div class="preparo-passo"><strong>{passo}.</strong> {linha}</div>',
                        unsafe_allow_html=True,
                    )

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        etapas_estruturadas = obter_etapas_estruturadas(receita)

        if len(etapas_estruturadas) > 1:
            st.markdown(
                '<div class="recipe-intro"><strong>Esta receita foi organizada por etapas.</strong><br>Cada componente possui seus próprios ingredientes e modo de preparo para facilitar a execução.</div>',
                unsafe_allow_html=True,
            )
            mostrar_etapas_estruturadas(etapas_estruturadas)
        else:
            st.markdown(
                '<div class="preparo-card">',
                unsafe_allow_html=True,
            )

            mostrar_modo_preparo(receita.modo_preparo)

            st.markdown('</div>', unsafe_allow_html=True)



# ============================================================
# INGREDIENTES
# ============================================================

def pagina_ingredientes():
    titulo_pagina(
        "Ingredientes",
        "Escolha o que você já tem em casa e descubra o que pode preparar.",
    )

    todos = []
    vistos = set()

    for receita in st.session_state.caderno.receitas:
        ingredientes_receita = obter_ingredientes_brutos_para_compra(receita)
        for ingrediente in ingredientes_receita:
            chave = ingrediente.lower().strip()
            if chave not in vistos:
                vistos.add(chave)
                todos.append(ingrediente)

    todos = sorted(todos, key=lambda item: item.lower())

    st.markdown(
        '<div class="ingredient-selector-label">Ingredientes disponíveis</div>',
        unsafe_allow_html=True,
    )

    selecionados = st.multiselect(
        "Ingredientes disponíveis",
        todos,
        placeholder="Clique aqui para escolher os ingredientes que você tem...",
        key="ingredientes_disponiveis",
        label_visibility="collapsed",
    )

    if not selecionados:
        st.markdown(
            '<div class="empty-state"><div class="empty-icon">◇</div><h3>Escolha alguns ingredientes</h3><p>Depois eu mostro quais receitas aproveitam melhor o que você já tem.</p></div>',
            unsafe_allow_html=True,
        )
        return

    resultados = []

    selecionados_normalizados = [
        " ".join(item.lower().strip().split())
        for item in selecionados
    ]

    for receita in st.session_state.caderno.receitas:
        ingredientes_receita = obter_ingredientes_brutos_para_compra(receita)
        encontrados = []
        faltantes = []

        for ingrediente in ingredientes_receita:
            texto = " ".join(ingrediente.lower().strip().split())
            encontrado = texto in selecionados_normalizados

            if encontrado:
                encontrados.append(ingrediente)
            else:
                faltantes.append(ingrediente)

        resultados.append({
            "receita": receita,
            "encontrados": encontrados,
            "faltantes": faltantes,
        })

    resultados.sort(
        key=lambda item: (len(item["faltantes"]), -len(item["encontrados"]))
    )

    st.write("")
    st.markdown(
        f'<div class="success-box">Você selecionou <strong>{len(selecionados)}</strong> ingrediente(s). As receitas abaixo estão organizadas pelas que exigem menos ingredientes adicionais.</div>',
        unsafe_allow_html=True,
    )

    for resultado in resultados:
        receita = resultado["receita"]
        encontrados = resultado["encontrados"]
        faltantes = resultado["faltantes"]

        with st.container(border=True):
            col1, col2 = st.columns([1, 1.45])

            with col1:
                mostrar_imagem(receita.foto, altura="220px")

            with col2:
                st.markdown(
                    f'<div class="recipe-card-title">{receita.nome}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="meta">{len(encontrados)} encontrados · {len(faltantes)} faltantes</div>',
                    unsafe_allow_html=True,
                )

                if encontrados:
                    st.markdown("**Você já tem:**")
                    for ingrediente in encontrados:
                        st.markdown(
                            f'<span class="ingredient-pill ingredient-have">✓ {ingrediente}</span>',
                            unsafe_allow_html=True,
                        )

                if faltantes:
                    st.markdown("**Ainda falta:**")
                    for ingrediente in faltantes:
                        st.markdown(
                            f'<span class="ingredient-pill ingredient-missing">• {ingrediente}</span>',
                            unsafe_allow_html=True,
                        )
                else:
                    st.success("Você já tem todos os ingredientes cadastrados!")

                c1, c2 = st.columns(2)

                with c1:
                    if st.button(
                        "Ver receita →",
                        key=f"ingrediente_ver_{receita.nome}",
                        use_container_width=True,
                    ):
                        abrir_receita(receita)
                        st.rerun()

                with c2:
                    if faltantes:
                        if st.button(
                            "＋ Adicionar faltantes",
                            key=f"faltantes_{receita.nome}",
                            use_container_width=True,
                        ):
                            quantidade = adicionar_ingredientes(
                                st.session_state.lista_compras,
                                faltantes,
                            )
                            salvar_lista_compras(st.session_state.lista_compras)
                            st.success(f"{quantidade} item(ns) adicionado(s).")
                    else:
                        if st.button(
                            "＋ Adicionar à lista",
                            key=f"todos_{receita.nome}",
                            use_container_width=True,
                        ):
                            quantidade = adicionar_receita_a_lista(receita)
                            st.success(f"{quantidade} item(ns) adicionado(s).")


# ============================================================
# COMBINAR
# ============================================================

def pagina_combinar():
    titulo_pagina(
        "Combinar",
        "Veja o que já está combinado e quais possibilidades ainda faltam cadastrar.",
    )

    massas = st.session_state.caderno.filtrar_preparos_por_tipo("massa")
    recheios = st.session_state.caderno.filtrar_preparos_por_tipo("creme")
    complementos = st.session_state.caderno.filtrar_preparos_por_tipo("complemento")

    if not massas:
        massas = st.session_state.caderno.filtrar_preparos_por_tipo("base")
    if not complementos:
        complementos = st.session_state.caderno.filtrar_preparos_por_tipo("fruta")

    if not massas or not recheios or not complementos:
        st.warning("Os dados de massas, recheios ou complementos ainda não estão completos.")
        return

    combinacoes_validas = []
    combinacoes_faltantes = []

    for massa in massas:
        for recheio in recheios:
            for complemento in complementos:
                combinacao = (massa.nome, recheio.nome, complemento.nome)
                if st.session_state.caderno.verificar_combinacao_completa(*combinacao):
                    combinacoes_validas.append(combinacao)
                else:
                    combinacoes_faltantes.append(combinacao)

    st.markdown('<div class="section-title">Combinações já cadastradas</div>', unsafe_allow_html=True)

    if combinacoes_validas:
        for base, recheio, complemento in combinacoes_validas:
            st.markdown(
                f"""<div class="combo-card combo-valid">
                    <div class="combo-label">COMBINAÇÃO COMPATÍVEL</div>
                    <div class="combo-nomes">{base} <span>+</span> {recheio} <span>+</span> {complemento}</div>
                </div>""",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="empty-state"><h3>Nenhuma combinação cadastrada</h3><p>Ainda não há uma combinação completa registrada.</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Possibilidades ainda não cadastradas</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="recipe-intro">Aqui aparecem as combinações que o sistema ainda não considera completas. Elas ajudam a identificar quais possibilidades poderiam ser adicionadas às regras de compatibilidade.</div>',
        unsafe_allow_html=True,
    )

    if combinacoes_faltantes:
        st.caption(f"{len(combinacoes_faltantes)} possibilidade(s) ainda não cadastrada(s).")

        for base, recheio, complemento in combinacoes_faltantes:
            st.markdown(
                f"""<div class="combo-card combo-missing">
                    <div class="combo-label">AINDA NÃO CADASTRADA</div>
                    <div class="combo-nomes">{base} <span>+</span> {recheio} <span>+</span> {complemento}</div>
                </div>""",
                unsafe_allow_html=True,
            )
    else:
        st.success("Todas as combinações possíveis já estão cadastradas.")

    st.markdown('<div class="section-title">Testar uma combinação</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        base = st.selectbox(
            "1. Massa",
            [preparo.nome for preparo in massas],
            key="combinar_base",
        )

    with col2:
        recheio = st.selectbox(
            "2. Recheio",
            [preparo.nome for preparo in recheios],
            key="combinar_recheio",
        )

    with col3:
        complemento = st.selectbox(
            "3. Complemento",
            [preparo.nome for preparo in complementos],
            key="combinar_complemento",
        )

    if st.button("Verificar combinação", type="primary", use_container_width=True):
        valida = st.session_state.caderno.verificar_combinacao_completa(
            base, recheio, complemento
        )

        if valida:
            st.markdown(
                f"""<div class="combo-result combo-result-ok">
                    <div class="combo-result-title">✓ Combinação compatível</div>
                    <div class="combo-result-text">{base} <span>+</span> {recheio} <span>+</span> {complemento}</div>
                </div>""",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""<div class="combo-result combo-result-no">
                    <div class="combo-result-title">× Combinação ainda não cadastrada</div>
                    <div class="combo-result-text">{base} <span>+</span> {recheio} <span>+</span> {complemento}</div>
                    <div class="combo-result-help">Você pode considerar esta combinação como uma nova possibilidade.</div>
                </div>""",
                unsafe_allow_html=True,
            )


# ============================================================
# FAVORITAS
# ============================================================

def pagina_favoritas():
    titulo_pagina(
        "Favoritas",
        "Suas receitas salvas em um só lugar.",
    )

    favoritas = st.session_state.caderno.listar_favoritas()

    if not favoritas:
        st.markdown(
            '<div class="empty-state"><div class="empty-icon">♡</div><h3>Você ainda não salvou nenhuma favorita</h3><p>Abra uma receita e toque em “Adicionar aos favoritos”.</p></div>',
            unsafe_allow_html=True,
        )
        return

    st.caption(f"{len(favoritas)} receita(s) favorita(s)")

    for inicio in range(0, len(favoritas), 3):
        colunas = st.columns(3)

        for coluna, receita in zip(colunas, favoritas[inicio:inicio + 3]):
            with coluna:
                mostrar_card_receita(
                    receita,
                    f"fav_{inicio}_{receita.nome}",
                )


# ============================================================
# LISTA DE COMPRAS
# ============================================================

def pagina_compras():
    titulo_pagina(
        "Lista de compras",
        "Os ingredientes que você escolheu levar para a cozinha.",
    )

    lista = st.session_state.lista_compras
    total = len(lista)
    comprados = sum(
        1
        for item in lista
        if isinstance(item, dict) and item.get("comprado", False)
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Itens", total)

    with col2:
        st.metric("Comprados", comprados)

    with col3:
        st.metric("Faltam", max(total - comprados, 0))

    st.write("")

    if total == 0:
        st.markdown(
            '<div class="empty-state"><div class="empty-icon">♡</div><h3>Sua lista ainda está vazia</h3><p>Adicione ingredientes a partir de uma receita ou da busca por ingredientes.</p></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Explorar receitas →",
            use_container_width=True,
        ):
            navegar("Receitas")
            st.rerun()

        return

    if st.button(
        "Limpar lista",
        key="limpar_lista",
    ):
        st.session_state.lista_compras = []
        salvar_lista_compras([])
        st.rerun()

    st.write("")

    for indice, item in enumerate(lista):
        if isinstance(item, dict):
            nome = item.get("ingrediente", item.get("nome", "Ingrediente"))
            comprado = item.get("comprado", False)
        else:
            nome = str(item)
            comprado = False

        col_check, col_remove = st.columns([8, 1])

        with col_check:
            novo_estado = st.checkbox(
                nome,
                value=comprado,
                key=f"compra_{indice}_{nome}",
            )

            if novo_estado != comprado:
                alternar_compra(indice)
                st.rerun()

        with col_remove:
            if st.button(
                "×",
                key=f"remover_{indice}_{nome}",
            ):
                remover_item(indice)
                st.rerun()

        st.divider()

    st.caption(
        "Dica: você pode adicionar ingredientes de várias receitas e montar sua compra aos poucos."
    )


# ============================================================
# ROTEAMENTO PRINCIPAL
# ============================================================

mostrar_sidebar()

pagina = st.session_state.pagina

if pagina == "Início":
    pagina_inicio()
elif pagina == "Receitas":
    pagina_receitas()
elif pagina == "Ingredientes":
    pagina_ingredientes()
elif pagina == "Combinar":
    pagina_combinar()
elif pagina == "Favoritas":
    pagina_favoritas()
elif pagina == "Compras":
    pagina_compras()
else:
    pagina_inicio()
