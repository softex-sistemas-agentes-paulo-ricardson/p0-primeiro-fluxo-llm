"""Testes offline da CLI, sem teclado e sem chamada ao LLM."""

import pytest

from src.app import executar_cli


@pytest.mark.parametrize("vazia", ["", "   ", "\n", "\t"])
def test_entrada_vazia_nao_chama_o_llm(monkeypatch, capsys, vazia):
    entradas = iter([vazia, "sair"])
    chamadas = []
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    monkeypatch.setattr("src.app.enviar_prompt_llm", chamadas.append)

    executar_cli()

    assert chamadas == []
    assert "Entrada vazia" in capsys.readouterr().out