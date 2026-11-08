"""Testes unitários offline do cliente HTTP."""

from src.client import enviar_prompt_llm


def test_enviar_prompt_llm_sucesso(monkeypatch, requests_mock):
    monkeypatch.setattr(
        "src.client.carregar_configuracao",
        lambda: {
            "base_url": "https://api.exemplo.test/v1",
            "caminho": "/chat/completions",
            "api_key": "chave-de-teste",
            "modelo": "modelo-teste",
            "temperatura": 0.7,
            "max_tokens": 100,
        },
    )
    requests_mock.post(
        "https://api.exemplo.test/v1/chat/completions",
        json={"choices": [{"message": {"role": "assistant", "content": "Resposta formal."}}]},
        status_code=200,
    )

    resultado = enviar_prompt_llm("vc pode me mandar o relatório?")

    assert resultado == "Resposta formal."
    assert requests_mock.call_count == 1

    corpo = requests_mock.last_request.json()
    assert corpo["messages"][0]["role"] == "system"
    assert corpo["messages"][1] == {"role": "user", "content": "vc pode me mandar o relatório?"}
    assert requests_mock.last_request.headers["Authorization"] == "Bearer chave-de-teste"

def test_sem_chave_nao_envia_authorization(monkeypatch, requests_mock):
    monkeypatch.setattr(
        "src.client.carregar_configuracao",
        lambda: {
            "base_url": "https://api.exemplo.test/v1",
            "caminho": "/chat/completions",
            "api_key": "",
            "modelo": "modelo-teste",
            "temperatura": 0.7,
            "max_tokens": 100,
        },
    )
    requests_mock.post(
        "https://api.exemplo.test/v1/chat/completions",
        json={"choices": [{"message": {"content": "Ok."}}]},
    )

    enviar_prompt_llm("teste")

    assert "Authorization" not in requests_mock.last_request.headers