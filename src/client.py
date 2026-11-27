"""Cliente HTTP isolado: concentra a lógica de chamada ao LLM."""

import os
from dotenv import find_dotenv, load_dotenv

import requests

INSTRUCAO_SISTEMA = (
    "Você reescreve mensagens em tom formal e profissional, em português do Brasil. "
    "Não acrescente nem remova informações e preserve o sentido original. "
    "Responda apenas com o texto reescrito, sem comentários, aspas ou explicações."
)

def ler_variavel(nome, padrao=None):
    """Le uma variável de ambiente; vazia ou só com espaços conta como ausente"""

    valor = os.getenv(nome, "").strip()
    return valor or padrao

class ErroConfiguracao(Exception):
    """A configuração do LLM está ausente ou é inválida."""

class ErroLLM(Exception):
    """A chamada ao LLM falhou ou a resposta não pôde ser usada."""

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

def validar_configuracoes(config: dict) -> None:
    """Levanta ErroConfiguracao se um valor obrigatório faltar ou for inválido."""
    if not config["base_url"]:
        raise ErroConfiguracao("LLM_API_BASE_URL não foi definida no .env.")
    if not config["base_url"].startswith(("http://", "https://")):
        raise ErroConfiguracao("LLM_API_BASE_URL deve começar com http:// ou https://.")
    if not config["modelo"]:
        raise ErroConfiguracao("LLM_MODEL_NAME não foi definido no .env.")
    if "#" in config["caminho"]:
        raise ErroConfiguracao(
            "LLM_API_PATH contém '#'. Para comentar uma linha do .env, "
            "coloque o # no começo da linha."
        )
    if config["temperatura"] < 0:
        raise ErroConfiguracao("LLM_TEMPERATURE não pode ser negativa.")
    if config["max_tokens"] <= 0:
        raise ErroConfiguracao("LLM_MAX_TOKENS deve ser maior que zero.")
    if config["timeout"] <= 0:
        raise ErroConfiguracao("LLM_TIMEOUT deve ser maior que zero.")

def carregar_configuracao() -> dict:
    """Lê as variáveis do .env e devolve a configuração do LLM"""
    load_dotenv(find_dotenv(usecwd=True), override=True)

    config = {
        "base_url": ler_variavel("LLM_API_BASE_URL"),
        "caminho": ler_variavel("LLM_API_PATH", "/chat/completions"),
        "api_key": ler_variavel("LLM_API_KEY"),
        "modelo": ler_variavel("LLM_MODEL_NAME"),
        "temperatura": ler_numero("LLM_TEMPERATURE", float, 0.7),
        "max_tokens": ler_numero("LLM_MAX_TOKENS", int, 1000),
        "timeout": ler_numero("LLM_TIMEOUT", float, 30.0),
    }
    validar_configuracoes(config)
    return config

MENSAGENS_HTTP = {
    401: "A chave de API está ausente ou foi recusada (401). Confira LLM_API_KEY no .env.",
    403: "Acesso negado (403). Verifique as permissões da sua chave.",
    404: "Modelo ou endereço não encontrado (404). Confira LLM_MODEL_NAME, LLM_API_BASE_URL e LLM_API_PATH.",
    429: "Limite de requisições atingido (429). Aguarde um pouco e tente de novo.",
}

def mensagem_para_status(status: int) -> str:
    """Traduz um status HTTP de erro em uma mensagem para o usuário."""
    if status in MENSAGENS_HTTP:
        return MENSAGENS_HTTP[status]
    if status >= 500:
        return f"O serviço do LLM está indisponível ou sobrecarregado ({status}). Tente de novo mais tarde."
    return f"O servidor recusou o pedido (status {status})."

def extrair_texto(dados) -> str:
    """Extrai o texto da resposta do LLM ou levanta ErroLLM se ela não servir."""
    try:
        escolha = dados["choices"][0]
    except (KeyError, IndexError, TypeError):
        raise ErroLLM("A resposta do LLM veio em um formato inesperado.") from None

    if escolha.get("finish_reason") == "length":
        raise ErroLLM(
            "A resposta foi cortada porque o limite de tokens acabou. "
            "Aumente LLM_MAX_TOKENS no .env."
        )

    texto = (escolha.get("message") or {}).get("content")
    if not texto or not texto.strip():
        raise ErroLLM("A resposta do LLM veio vazia. Tente de novo.")
    return texto

def montar_url(config: dict) -> str:
    """Junta a base da API e o caminho do endpoint."""
    return config["base_url"].rstrip("/") + "/" + config["caminho"].lstrip("/")


def montar_cabecalhos(config: dict) -> dict:
    """Monta os cabeçalhos; sem chave, não envia Authorization."""
    cabecalhos = {}
    if config["api_key"]:
        cabecalhos["Authorization"] = f"Bearer {config['api_key']}"
    return cabecalhos


def montar_corpo(config: dict, prompt: str) -> dict:
    """Monta o corpo do pedido no formato compatível com OpenAI."""
    return {
        "model": config["modelo"],
        "messages": [
            {"role": "system", "content": INSTRUCAO_SISTEMA},
            {"role": "user", "content": prompt},
        ],
        "temperature": config["temperatura"],
        "max_tokens": config["max_tokens"],
    }

def enviar_prompt_llm(prompt: str) -> str:
    """Envia o prompt ao LLM e devolve o texto da resposta."""

    config = carregar_configuracao()

    url = montar_url(config)
    cabecalhos = montar_cabecalhos(config)
    corpo = montar_corpo(config, prompt)

    try:
        resposta = requests.post(url, headers=cabecalhos, json=corpo, timeout=config["timeout"])
        resposta.raise_for_status()
    except requests.exceptions.Timeout as erro:
        raise ErroLLM(
            f"O LLM não respondeu em {config['timeout']:g} segundos. "
            "Tente de novo ou aumente LLM_TIMEOUT."
        ) from erro
    except requests.exceptions.SSLError as erro:
        raise ErroLLM(
            "Falha na verificação do certificado SSL do servidor. "
            "Confira o endereço em LLM_API_BASE_URL."
        ) from erro
    except requests.exceptions.ConnectionError as erro:
        raise ErroLLM(
            "Não foi possível conectar ao servidor do LLM. "
            "Verifique a internet e o LLM_API_BASE_URL."
        ) from erro
    except requests.exceptions.HTTPError as erro:
        raise ErroLLM(mensagem_para_status(erro.response.status_code)) from erro

    try:
        dados = resposta.json()
    except ValueError:
        raise ErroLLM("A resposta do LLM não está em formato JSON.") from None

    return extrair_texto(dados)