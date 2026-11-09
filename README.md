# Meu Caderno de Receitas

Aplicação web em Python para organizar receitas, listar ingredientes disponíveis, montar combinações de massas e cremes, salvar receitas favoritas e manter uma lista de compras.

## Visão geral

O projeto foi desenvolvido em Python com Streamlit e tem como objetivo funcionar como um caderno digital de receitas, com foco em:

- consulta e busca de receitas;
- organização por categoria e dificuldade;
- identificação de receitas a partir dos ingredientes disponíveis;
- combinação de massas, cremes e complementos;
- marcação de receitas favoritas;
- geração e persistência de lista de compras em JSON.

## Tecnologias utilizadas

- Python
- Streamlit
- Pillow

## Estrutura de pastas

- `app.py`: interface e navegação principal
- `main.py`: ponto de entrada da aplicação
- `modelos.py`: classes `Receita`, `Preparo` e `CadernoReceitas`
- `dados.py`: dados das receitas e preparos
- `funcao.py`: funções auxiliares e lógica de negócio
- `padronizacao_ingredientes.py`: normalização de nomes dos ingredientes
- `imagens/`: imagens das receitas e preparos
- `lista_compras.json`: armazenamento da lista de compras
- `requirements.txt`: dependências do projeto
- `render.yaml`: configuração de publicação no Render
- `documentacao/artigo/`: artigo e relatório acadêmico
- `documentacao/defesa/`: guia pessoal para estudo e apresentação
- `documentacao/apresentacao/`: poster final e template da mostra
- `documentacao/requisitos/`: enunciado da atividade A3
- `documentacao/referencias/`: modelo de artigo usado como referência
- `materiais_originais/`: arquivos de origem preservados, como o ZIP inicial de imagens
- `para_descartar_revisar/`: arquivos antigos/cache mantidos localmente para revisão; não são enviados ao Git

Os módulos Python e a pasta `imagens/` permanecem na raiz porque a aplicação usa esses caminhos diretamente.

## Como executar localmente

1. Acesse a pasta do projeto:

   ```bash
   cd meu_caderno_de_receitas
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie a aplicação:

   ```bash
   python main.py
   ```

   ou diretamente:

   ```bash
   streamlit run app.py
   ```

A aplicação estará disponível em:

- http://localhost:8501

## Como publicar no Render

1. Crie uma conta no [Render](https://render.com/) e faça login.
2. Clique em "New" e depois em "Web Service".
3. Conecte o repositório do GitHub que contém este projeto.
4. Use as configurações abaixo:
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
5. Clique em "Create Web Service".

O arquivo `render.yaml` já foi incluído no projeto para facilitar o deploy.

## Observações

- A aplicação usa persistência local em arquivo JSON para a lista de compras.
- A estrutura foi organizada em módulos para facilitar manutenção, extensão e apresentação em sala.
- O projeto foi pensado como uma solução prática de organização de receitas, mas também como demonstração de conceitos de programação em Python.

## Licença

Este projeto foi desenvolvido para fins acadêmicos como parte da A3.
