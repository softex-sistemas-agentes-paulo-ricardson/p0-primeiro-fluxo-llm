# P0 — Primeiro Fluxo com LLM

Implementação do fluxo inicial com LLM, cobrindo evolução do básico ao avançado com agentes e prompts.

Projeto desenvolvido durante o **Bloco 0 (Nivelamento) do Programa TrendsIA**. O objetivo atual é configurar o ambiente de desenvolvimento isolado, padronizar o gerenciamento de dependências e estabelecer as configurações de exclusão e documentação do repositório.

---

## 📁 Estrutura do Projeto

Neste momento inicial, o repositório conta com os seguintes arquivos e diretórios configurados:

```text
p0-primeiro-fluxo-llm/
├── .venv/               # Ambiente virtual isolado gerenciado pelo Python venv (não versionado)
├── .gitignore           # Regras de exclusão de arquivos e pastas no controle de versão
├── requirements.txt     # Manifesto com a declaração das dependências do projeto
└── README.md            # Guia de configuração e instruções para reprodução do ambiente
```

## ⚙️ Pré-requisitos

- Python 3.10 ou superior instalado na máquina.
- Git instalado e configurado no terminal.

## 🚀 Como Configurar e Reproduzir o Ambiente

Para configurar o ambiente de desenvolvimento local em uma nova máquina, siga os passos abaixo:

### 1. Clonar o Repositório

```bash
git clone https://github.com/SEU_USUARIO/p0-primeiro-fluxo-llm.git
cd p0-primeiro-fluxo-llm
```

### 2. Criar e Ativar o Ambiente Virtual (`.venv`)

- **Windows (PowerShell):**

  ```powershell
  python -m venv .venv
  (Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; .venv\Scripts\Activate.ps1
  ```

- **Windows (Prompt de Comando - CMD):**

  ```bat
  python -m venv .venv
  .venv\Scripts\activate.bat
  ```

- **Linux / macOS (Bash):**

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

Verifique se o terminal exibe o prefixo `(.venv)` no início da linha de comando para confirmar que a ativação foi concluída com sucesso.

### 3. Instalar as Dependências

Com o ambiente virtual devidamente ativado, execute a instalação dos pacotes declarados no manifesto:

```bash
pip install -r requirements.txt
```

### 4. Validar o Isolamento das Bibliotecas

Para conferir se os pacotes foram instalados dentro do ambiente isolado, execute:

```bash
pip list
```

Os seguintes pacotes devem constar na listagem:

- `requests`
- `python-dotenv`
- `pytest`
- `requests-mock`
