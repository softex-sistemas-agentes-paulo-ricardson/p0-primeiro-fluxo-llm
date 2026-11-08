"""Cliente HTTP isolado: concentra a lógica de chamada ao LLM."""

import os
from dotenv import find_dotenv, load_dotenv

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
    """Envia o prompt ao LLM e devolve o texto da resposta.

    Esqueleto inicial: a chamada real à API REST será implementada
    no nível Básico.
    """
    raise NotImplementedError("Chamada ao LLM ainda não implementada.")