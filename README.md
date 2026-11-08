# P0 — Primeiro Fluxo com LLM

Aplicação em Python, executada no terminal, que reescreve uma mensagem informal em **tom formal e profissional** usando um LLM por meio de uma API REST.

Projeto desenvolvido durante o **Bloco 0 (Nivelamento) do Programa TrendsIA**.

---

## 🎯 Sobre o projeto

**Problema:** uma pessoa que escreve mensagens do dia a dia precisa transformar um texto informal em uma versão em tom formal e profissional, porque tem dificuldade de ajustar o tom sem mudar o sentido.

- **Usuário ou público:** estudantes e profissionais que escrevem e-mails, avisos e pedidos a pessoas de outros níveis hierárquicos e querem uma versão em tom formal do que digitaram.
- **Entrada:** mensagem informal, digitada no terminal.
- **Saída:** a mesma mensagem reescrita em tom formal.

**Por que um LLM:** trocar palavras por uma tabela de substituições (por exemplo, "vc" por "você") não resolve, porque a formalidade depende do contexto, da gíria e da estrutura da frase. O LLM reescreve a frase inteira preservando o sentido.

### Exemplos de entrada e saída

| Entrada | Saída |
|---|---|
| `vc pode me mandar o relatório pra hj?` | Você poderia me enviar o relatório para hoje? |
| `oi, to atrasado, chego em 10 min, avisa o pessoal pfv` | Olá, estou atrasado e chegarei em 10 minutos. Por gentileza, avise a todos. |
| `mano, o sistema caiu de novo kkkk ja é a terceira vez essa semana, alguem precisa resolver isso urgente!!!` | O sistema apresentou indisponibilidade novamente, sendo esta a terceira ocorrência nesta semana. É necessária a resolução deste problema com urgência. |

A saída do LLM varia entre execuções; os exemplos acima são de execuções reais com `gemini-3.5-flash`.

## 📁 Estrutura do Projeto

```text
p0-primeiro-fluxo-llm/
├── .venv/               # Ambiente virtual isolado (não versionado)
├── src/
│   ├── app.py           # Interface de linha de comando (captura a entrada e exibe a resposta)
│   └── client.py        # Cliente HTTP isolado (configuração e chamada à API do LLM)
├── tests/
│   └── test_client.py   # Testes offline, com mock da API (sem chamada real)
├── .env.example         # Modelo de configuração, sem credenciais reais
├── .gitignore           # Arquivos e pastas fora do controle de versão
├── requirements.txt     # Dependências do projeto
└── README.md            # Este guia
```

## ⚙️ Pré-requisitos

- Python 3.10 ou superior (desenvolvido com Python 3.12).
- Git instalado e configurado no terminal.
- Acesso a um LLM por API compatível com OpenAI (ver "Configuração do LLM").

## 🚀 Como Configurar e Reproduzir o Ambiente

Para configurar o ambiente de desenvolvimento local em uma nova máquina, siga os passos abaixo:

### 1. Clonar o Repositório

```bash
git clone https://github.com/softex-sistemas-agentes-paulo-ricardson/p0-primeiro-fluxo-llm.git
cd p0-primeiro-fluxo-llm
```

### 2. Criar e Ativar o Ambiente Virtual (`.venv`)

> **Execute apenas o bloco do seu sistema operacional.** Os comandos do Windows (`python`, `Set-ExecutionPolicy`, `.venv\Scripts\...`) não funcionam no Linux/macOS, e os do Linux/macOS (`python3`, `source`) não funcionam no PowerShell.

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

  No Ubuntu/Debian, se aparecer "ensurepip is not available" ou "python3-venv is not installed", instale o módulo e repita os comandos:

  ```bash
  sudo apt update
  sudo apt install python3-venv
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

## 🔑 Configuração do LLM

Copie o arquivo de exemplo e preencha com os dados do seu provedor:

- **Windows (PowerShell):** `Copy-Item .env.example .env`
- **Linux / macOS:** `cp .env.example .env`

O programa usa qualquer API compatível com OpenAI (`POST /chat/completions`, com a resposta em `choices[0].message.content`). Provedor e modelo utilizados no desenvolvimento: **Gemini, `gemini-3.5-flash`**.

| Variável | Descrição |
|---|---|
| `LLM_API_BASE_URL` | Base da API, sem o caminho final |
| `LLM_API_PATH` | Caminho do endpoint (opcional; padrão `/chat/completions`) |
| `LLM_API_KEY` | Chave da API (pode ficar vazia em servidores sem autenticação) |
| `LLM_MODEL_NAME` | Nome do modelo, como o provedor o identifica |
| `LLM_TEMPERATURE` | Temperatura de geração (opcional; padrão `0.7`) |
| `LLM_MAX_TOKENS` | Limite de tokens da resposta (opcional; padrão `1000`) |
| `LLM_TIMEOUT` | Tempo máximo de espera, em segundos (opcional; padrão `30`) |

Exemplo com Gemini:

```
LLM_API_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_API_PATH=/chat/completions
LLM_API_KEY=<sua chave>
LLM_MODEL_NAME=gemini-3.5-flash
```

Exemplo com Ollama local:

```
LLM_API_BASE_URL=http://localhost:11434/v1
LLM_API_PATH=/chat/completions
LLM_API_KEY=
LLM_MODEL_NAME=<nome que aparece em "ollama list">
LLM_TIMEOUT=120
```

> Nunca versione o arquivo `.env`: ele contém a chave da API e está no `.gitignore`.

Modelos que raciocinam antes de responder gastam parte do limite de tokens nesse raciocínio. Se a resposta vier cortada, aumente `LLM_MAX_TOKENS` (por exemplo, para `2000`).

Os testes simulados (mock) não exigem chave nem acesso à rede; só a execução real do programa exige o `.env` preenchido.

## ▶️ Execução

Com o ambiente virtual ativado, na raiz do projeto:

```bash
python -m src.app
```

Digite a mensagem informal e pressione Enter. Para encerrar, digite `sair`.

## 🧪 Testes

```bash
python -m pytest
```

Os testes rodam offline, com `requests-mock`, e não gastam requisições da API.

## ⚠️ Limitações conhecidas

- Modelos pequenos ou locais podem ignorar a instrução de devolver apenas o texto reescrito.
- O modelo pode reescrever até um texto que já está formal.
- A saída do LLM varia entre execuções.
- Em casos raros, a resposta pode vir cortada se o limite de tokens for apertado (ver `LLM_MAX_TOKENS`).
- O cliente entende o formato de resposta compatível com OpenAI; a interface nativa do Ollama (`/api/chat`) não é suportada.
