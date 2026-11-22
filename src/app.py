"""Interface de linha de comando: captura a entrada e exibe a resposta."""

from src.client import ErroConfiguracao, enviar_prompt_llm


def executar_cli() -> None:
    print("=" * 56)
    print("P0 - Primeiro Fluxo com LLM")
    print("=" * 56)
    print("Digite sua mensagem para o LLM (ou digite 'sair' para encerrar).\n")

    while True:
        entrada = input("Usuário > ").strip()

        if entrada.lower() == "sair":
            print("Encerrando.")
            break

        if not entrada:
            print("Sistema > Entrada vazia. Digite uma mensagem.\n")
            continue

        try:
            resposta = enviar_prompt_llm(entrada)
        except ErroConfiguracao as erro:
            print(f"Sistema > Erro de configuração: {erro}")
            print("Sistema > Corrija o arquivo .env e envie a mensagem de novo.\n")

            continue

        print(f"IA > {resposta}\n")


if __name__ == "__main__":
    executar_cli()