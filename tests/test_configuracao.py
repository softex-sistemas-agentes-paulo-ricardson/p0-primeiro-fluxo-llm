"""Testes offline da leitura e da validação da configuração."""

import pytest

from src.client import ErroConfiguracao, carregar_configuracao

VARIAVEIS = [
    "LLM_API_BASE_URL",
    "LLM_API_PATH",
    "LLM_API_KEY",
    "LLM_MODEL_NAME",
    "LLM_TEMPERATURE",
    "LLM_MAX_TOKENS",
    "LLM_TIMEOUT",
]


@pytest.fixture
def ambiente(monkeypatch):
    """Isola o teste do .env real e define uma configuração mínima válida."""
    monkeypatch.setattr("src.client.load_dotenv", lambda *args, **kwargs: None)
    for nome in VARIAVEIS:
        monkeypatch.delenv(nome, raising=False)
    monkeypatch.setenv("LLM_API_BASE_URL", "https://api.exemplo.test/v1")
    monkeypatch.setenv("LLM_MODEL_NAME", "modelo-teste")
    return monkeypatch


def test_valores_padrao(ambiente):
    config = carregar_configuracao()

    assert config["caminho"] == "/chat/completions"
    assert config["api_key"] is None
    assert config["temperatura"] == 0.7
    assert config["max_tokens"] == 1000
    assert config["timeout"] == 30.0


def test_variaveis_vazias_usam_padrao(ambiente):
    ambiente.setenv("LLM_API_PATH", "")
    ambiente.setenv("LLM_TEMPERATURE", "")
    ambiente.setenv("LLM_MAX_TOKENS", "")
    ambiente.setenv("LLM_TIMEOUT", "")

    config = carregar_configuracao()

    assert config["caminho"] == "/chat/completions"
    assert config["temperatura"] == 0.7
    assert config["max_tokens"] == 1000
    assert config["timeout"] == 30.0


def test_valores_do_ambiente_sao_convertidos(ambiente):
    ambiente.setenv("LLM_TEMPERATURE", "0.2")
    ambiente.setenv("LLM_MAX_TOKENS", "2000")
    ambiente.setenv("LLM_TIMEOUT", "60")

    config = carregar_configuracao()

    assert config["temperatura"] == 0.2
    assert config["max_tokens"] == 2000
    assert config["timeout"] == 60.0


def test_espacos_nas_pontas_sao_removidos(ambiente):
    ambiente.setenv("LLM_MODEL_NAME", "  modelo-teste  ")

    config = carregar_configuracao()

    assert config["modelo"] == "modelo-teste"


def test_base_ausente(ambiente):
    ambiente.delenv("LLM_API_BASE_URL")

    with pytest.raises(ErroConfiguracao, match="LLM_API_BASE_URL"):
        carregar_configuracao()


def test_base_sem_esquema(ambiente):
    ambiente.setenv("LLM_API_BASE_URL", "api.exemplo.test/v1")

    with pytest.raises(ErroConfiguracao, match="http"):
        carregar_configuracao()


def test_modelo_ausente(ambiente):
    ambiente.delenv("LLM_MODEL_NAME")

    with pytest.raises(ErroConfiguracao, match="LLM_MODEL_NAME"):
        carregar_configuracao()


def test_caminho_com_jogo_da_velha(ambiente):
    ambiente.setenv("LLM_API_PATH", "#/chat/completions")

    with pytest.raises(ErroConfiguracao, match="#"):
        carregar_configuracao()


@pytest.mark.parametrize(
    "nome, valor",
    [
        ("LLM_TEMPERATURE", "abc"),
        ("LLM_MAX_TOKENS", "abc"),
        ("LLM_MAX_TOKENS", "1.5"),
        ("LLM_TIMEOUT", "dez"),
    ],
)
def test_numero_invalido_informa_a_variavel(ambiente, nome, valor):
    ambiente.setenv(nome, valor)

    with pytest.raises(ErroConfiguracao, match=nome):
        carregar_configuracao()


@pytest.mark.parametrize(
    "nome, valor",
    [
        ("LLM_TEMPERATURE", "-0.1"),
        ("LLM_MAX_TOKENS", "0"),
        ("LLM_TIMEOUT", "-5"),
    ],
)
def test_numero_fora_da_faixa(ambiente, nome, valor):
    ambiente.setenv(nome, valor)

    with pytest.raises(ErroConfiguracao, match=nome):
        carregar_configuracao()


def test_mensagem_de_erro_nao_expoe_a_chave(ambiente):
    ambiente.setenv("LLM_API_KEY", "segredo-123")
    ambiente.delenv("LLM_MODEL_NAME")

    with pytest.raises(ErroConfiguracao) as erro:
        carregar_configuracao()

    assert "segredo-123" not in str(erro.value)