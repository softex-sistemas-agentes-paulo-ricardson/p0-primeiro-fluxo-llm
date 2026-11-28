"""Testes do registro de execução."""

import logging

from src.client import enviar_prompt_llm
from src.registro import configurar_registro

CONFIG = {
    "base_url": "https://api.exemplo.test/v1",
    "caminho": "/chat/completions",
    "api_key": "segredo-123",
    "modelo": "modelo-teste",
    "temperatura": 0.7,
    "max_tokens": 100,
    "timeout": 30,
    "instrucao": "instrucao-teste",
}


def test_log_nao_guarda_dados_sensiveis(monkeypatch, requests_mock, caplog):
    caplog.set_level(logging.INFO, logger="p0")
    monkeypatch.setattr("src.client.carregar_configuracao", lambda: CONFIG)
    requests_mock.post(
        "https://api.exemplo.test/v1/chat/completions",
        json={"choices": [{"message": {"content": "texto-da-resposta"}}]},
    )

    enviar_prompt_llm("mensagem-pessoal")

    assert "modelo-teste" in caplog.text
    for proibido in ("segredo-123", "mensagem-pessoal", "texto-da-resposta"):
        assert proibido not in caplog.text


def test_configurar_registro_grava_em_arquivo(tmp_path):
    arquivo = tmp_path / "logs" / "app.log"
    handler = configurar_registro(str(arquivo))

    logging.getLogger("p0").info("linha de teste")
    logging.getLogger("p0").removeHandler(handler)
    handler.close()

    assert "linha de teste" in arquivo.read_text(encoding="utf-8")