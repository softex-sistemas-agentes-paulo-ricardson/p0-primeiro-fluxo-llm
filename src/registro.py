"""Configuração do registro de execução (log)."""

import logging
from pathlib import Path

FORMATO = "%(asctime)s %(levelname)s %(message)s"


def configurar_registro(caminho: str = "logs/app.log") -> logging.Handler:
    """Grava o log do projeto em arquivo e devolve o handler criado."""
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(destino, encoding="utf-8")
    handler.setFormatter(logging.Formatter(FORMATO))

    logger = logging.getLogger("p0")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return handler