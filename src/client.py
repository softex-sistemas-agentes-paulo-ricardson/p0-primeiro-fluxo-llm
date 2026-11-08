"""Cliente HTTP isolado: concentra a lógica de chamada ao LLM."""

import os
from dotenv import find_dotenv, load_dotenv

import requests

INSTRUCAO_SISTEMA = (
    "Você reescreve mensagens em tom formal e profissional, em português do Brasil. "
    "Não acrescente nem remova informações e preserve o sentido original. "
    "Responda apenas com o texto reescrito, sem comentários, aspas ou explicações."
)

def carregar_configuracao() -> dict:
    """Lê as variáveis do .env e devolve a configuração do LLM"""
    load_dotenv(find_dotenv(usecwd=True), override=True)

    return {
        "base_url": os.getenv("LLM_API_BASE_URL"),
        "api_key": os.getenv("LLM_API_KEY"),
        "modelo": os.getenv("LLM_MODEL_NAME"),
        "temperatura": float(os.getenv("LLM_TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "1000"))
    }

def enviar_prompt_llm(prompt: str) -> str:
    """Envia o prompt ao LLM e devolve o texto da resposta."""

    config = carregar_configuracao()

    url = config["base_url"].rstrip("/") + "/chat/completions"
    cabecalhos = {"Authorization": f"Bearer {config['api_key']}"}
    corpo = {
        "model": config["modelo"],
        "messages": [
            {"role": "system", "content": INSTRUCAO_SISTEMA},
            {"role": "user", "content": prompt},
        ],
        "temperature": config["temperatura"],
        "max_tokens": config["max_tokens"],
    }

    resposta = requests.post(url, headers=cabecalhos, json=corpo, timeout=30)
    resposta.raise_for_status()

    dados = resposta.json()
    return dados["choices"][0]["message"]["content"]