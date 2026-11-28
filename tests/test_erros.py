"""Testes offline do tratamento de erros da chamada ao LLM."""

import pytest
import requests

from src.client import ErroLLM, enviar_prompt_llm

URL = "https://api.exemplo.test/v1/chat/completions"

CONFIG = {
    "base_url": "https://api.exemplo.test/v1",
    "caminho": "/chat/completions",
    "api_key": "segredo-123",
    "modelo": "modelo-teste",
    "temperatura": 0.7,
    "max_tokens": 100,
    "timeout": 30,
    "instrucao": "instrucao-test",
}


@pytest.fixture
def api(monkeypatch, requests_mock):
    """Configuração falsa e rede falsa: o teste só escolhe o que a API responde."""
    monkeypatch.setattr("src.client.carregar_configuracao", lambda: CONFIG)
    return requests_mock


def resposta_com(conteudo, finish_reason="stop"):
    """Monta o JSON de uma resposta do LLM."""
    mensagem = {"role": "assistant"}
    if conteudo is not None:
        mensagem["content"] = conteudo
    return {"choices": [{"finish_reason": finish_reason, "message": mensagem}]}


@pytest.mark.parametrize(
    "status, trecho",
    [
        (401, "LLM_API_KEY"),
        (404, "LLM_MODEL_NAME"),
        (429, "429"),
        (503, "indisponível"),
        (400, "status 400"),
    ],
)
def test_status_http_vira_mensagem(api, status, trecho):
    api.post(URL, status_code=status)

    with pytest.raises(ErroLLM, match=trecho):
        enviar_prompt_llm("oi")


@pytest.mark.parametrize(
    "excecao, trecho",
    [
        (requests.exceptions.ReadTimeout, "não respondeu em 30 segundos"),
        (requests.exceptions.ConnectTimeout, "não respondeu"),
        (requests.exceptions.ConnectionError, "conectar"),
        (requests.exceptions.SSLError, "SSL"),
    ],
)
def test_falha_de_rede_vira_mensagem(api, excecao, trecho):
    api.post(URL, exc=excecao)

    with pytest.raises(ErroLLM, match=trecho):
        enviar_prompt_llm("oi")


@pytest.mark.parametrize(
    "corpo, trecho",
    [
        ({"json": {}}, "formato inesperado"),
        ({"json": {"choices": []}}, "formato inesperado"),
        ({"text": "<html>erro do proxy</html>"}, "JSON"),
    ],
)
def test_resposta_invalida(api, corpo, trecho):
    api.post(URL, **corpo)

    with pytest.raises(ErroLLM, match=trecho):
        enviar_prompt_llm("oi")


@pytest.mark.parametrize(
    "conteudo, finish_reason, trecho",
    [
        ("", "stop", "vazia"),
        (None, "stop", "vazia"),
        ("Olá, tudo", "length", "LLM_MAX_TOKENS"),
        (None, "length", "LLM_MAX_TOKENS"),
    ],
)
def test_resposta_vazia_ou_cortada(api, conteudo, finish_reason, trecho):
    api.post(URL, json=resposta_com(conteudo, finish_reason))

    with pytest.raises(ErroLLM, match=trecho):
        enviar_prompt_llm("oi")


def test_resposta_normal_continua_funcionando(api):
    api.post(URL, json=resposta_com("Resposta formal."))

    assert enviar_prompt_llm("oi") == "Resposta formal."


def test_mensagem_de_erro_nao_expoe_a_chave(api):
    api.post(URL, status_code=401)

    with pytest.raises(ErroLLM) as erro:
        enviar_prompt_llm("oi")

    assert "segredo-123" not in str(erro.value)