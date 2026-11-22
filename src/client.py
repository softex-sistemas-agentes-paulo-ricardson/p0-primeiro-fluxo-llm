"""Cliente HTTP isolado: concentra a lógica de chamada ao LLM."""

import os
from dotenv import find_dotenv, load_dotenv

import requests

INSTRUCAO_SISTEMA = (
    "Você reescreve mensagens em tom formal e profissional, em português do Brasil. "
    "Não acrescente nem remova informações e preserve o sentido original. "
    "Responda apenas com o texto reescrito, sem comentários, aspas ou explicações."
)

class ErroConfiguracao(Exception):
    """A configuração do LLM está ausente ou é inválida"""

def ler_variavel(nome, padrao=None):
    """Le uma variável de ambiente; vazia ou só com espaços conta como ausente"""

    valor = os.getenv(nome, "").strip()
    return valor or padrao

class ErroConfiguracao(Exception):
    """A configuração do LLM está ausente ou é inválida."""


def ler_numero(nome, tipo, padrao):
    """Lê uma variável numérica e a converte com `tipo` (int ou float)."""
    texto = ler_variavel(nome)
    if texto is None:
        return padrao
    try:
        return tipo(texto)
    except ValueError:
        raise ErroConfiguracao(
            f"{nome} deve ser um número ({tipo.__name__}), mas o valor é {texto!r}."
        ) from None

def carregar_configuracao() -> dict:
    """Lê as variáveis do .env e devolve a configuração do LLM"""
    load_dotenv(find_dotenv(usecwd=True), override=True)

    return {
        "base_url": ler_variavel("LLM_API_BASE_URL"),
        "caminho": ler_variavel("LLM_API_PATH", "/chat/completions"),
        "api_key": ler_variavel("LLM_API_KEY"),
        "modelo": ler_variavel("LLM_MODEL_NAME"),
        "temperatura": ler_numero("LLM_TEMPERATURE", float, 0.7),
        "max_tokens": ler_numero("LLM_MAX_TOKENS", int, 1000),
        "timeout": ler_numero("LLM_TIMEOUT", float, 30.0),
    }

def enviar_prompt_llm(prompt: str) -> str:
    """Envia o prompt ao LLM e devolve o texto da resposta."""

    config = carregar_configuracao()

    url = config["base_url"].rstrip("/") + "/" + config["caminho"].lstrip("/")
    cabecalhos = {}
    if config["api_key"]:
        cabecalhos["Authorization"] = f"Bearer {config['api_key']}"
    corpo = {
        "model": config["modelo"],
        "messages": [
            {"role": "system", "content": INSTRUCAO_SISTEMA},
            {"role": "user", "content": prompt},
        ],
        "temperature": config["temperatura"],
        "max_tokens": config["max_tokens"],
    }

    resposta = requests.post(url, headers=cabecalhos, json=corpo, timeout=config["timeout"])
    resposta.raise_for_status()

    dados = resposta.json()
    return dados["choices"][0]["message"]["content"]