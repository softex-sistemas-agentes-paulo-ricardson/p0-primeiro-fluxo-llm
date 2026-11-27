"""Interface de linha de comando: captura a entrada e exibe a resposta."""

from src.client import ErroConfiguracao, ErroLLM, enviar_prompt_llm


def exibir_cabecalho() -> None:
    """Mostra o título e a instrução inicial."""
    print("=" * 56)
    print("P0 - Primeiro Fluxo com LLM")
    print("=" * 56)
    print("Digite sua mensagem para o LLM (ou digite 'sair' para encerrar).\n")


def ler_entrada() -> str:
    """Captura a mensagem do usuário, sem espaços nas pontas."""
    return input("Usuário > ").strip()


def processar_mensagem(mensagem: str) -> None:
    """Envia a mensagem ao LLM e mostra a resposta ou o erro."""
    try:
        resposta = enviar_prompt_llm(mensagem)
    except ErroConfiguracao as erro:
        print(f"Sistema > Erro de configuração: {erro}")
        print("Sistema > Corrija o arquivo .env e envie a mensagem de novo.\n")
        return
    except ErroLLM as erro:
        print(f"Sistema > Erro ao consultar o LLM: {erro}\n")
        return

    print(f"IA > {resposta}\n")


def executar_cli() -> None:
    """Laço principal: lê a entrada até o usuário digitar 'sair'."""
    exibir_cabecalho()

    while True:
        entrada = ler_entrada()

        if entrada.lower() == "sair":
            print("Encerrando.")
            break

        if not entrada:
            print("Sistema > Entrada vazia. Digite uma mensagem.\n")
            continue

        processar_mensagem(entrada)


if __name__ == "__main__":
    executar_cli()