"""Ponto de entrada do projeto Meu Caderno de Receitas."""

from pathlib import Path
import subprocess
import sys


PASTA_PROJETO = Path(__file__).resolve().parent
ARQUIVO_APP = PASTA_PROJETO / "app.py"


def main():
    """Inicializa a aplicação Streamlit do projeto."""
    if not ARQUIVO_APP.exists():
        raise FileNotFoundError(f"Arquivo principal não encontrado: {ARQUIVO_APP}")

    comando = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(ARQUIVO_APP),
        "--server.headless",
        "true",
        "--server.address",
        "0.0.0.0",
        "--server.port",
        "8501",
    ]

    try:
        subprocess.run(comando, cwd=str(PASTA_PROJETO), check=True)
    except KeyboardInterrupt:
        print("Aplicação encerrada pelo usuário.")


if __name__ == "__main__":
    main()
