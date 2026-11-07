"""Testes unitários offline do cliente HTTP."""

import pytest

from src.client import enviar_prompt_llm


def test_cliente_ainda_nao_implementado():
    with pytest.raises(NotImplementedError):
        enviar_prompt_llm("Olá, IA!")