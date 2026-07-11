# LinkedIn Connections RPA

Automacao em Python + Selenium para abrir o Google Chrome, entrar em `Minha rede` no LinkedIn e enviar ate 10 convites por execucao. A extracao de nome, cargo e link do perfil usa BeautifulSoup sobre o HTML renderizado do card.

## Como rodar

```bash
source env/bin/activate
cp .env.example .env
python main.py
```

Para executar em segundo plano, apos instalar o atalho local, use:

```bash
linkedinbot start
linkedinbot status
linkedinbot stop
```

O programa encerra instancias anteriores do Chrome, abre e controla uma nova janela automaticamente. A sessao do LinkedIn fica no perfil dedicado `~/.linkedin-selenium`, fora do projeto. Na primeira execucao, entre manualmente no LinkedIn nessa janela; os proximos usos reutilizam a sessao salva.

## Configuracoes

Edite `.env` para mudar limite, pausas e perfil do Chrome. Use `.env.example` como modelo; o arquivo `.env` nao entra no Git.

Principais campos:

- `DAILY_CONNECTION_LIMIT`: quantidade maxima de convites por execucao.
- `MIN_INVITATION_PAUSE_SECONDS` e `MAX_INVITATION_PAUSE_SECONDS`: intervalo aleatorio entre convites.
- `BATCH_SIZE`, `MIN_BATCH_PAUSE_SECONDS` e `MAX_BATCH_PAUSE_SECONDS`: tamanho do lote e pausa aleatoria apos cada lote.
- `MAX_PAGE_REFRESHES_WITHOUT_SUGGESTIONS`: quantidade de recargas apos esgotar as sugestoes; o padrao e `1`.
- `CHROME_BINARY`: caminho do Google Chrome.
- `CHROME_USER_DATA_DIR`: perfil persistente do Chrome; o padrao e `~/.linkedin-selenium`.
- `CHROMEDRIVER_LOG_PATH`: arquivo de log do ChromeDriver.
- `OUTPUT_XLSX_PATH`: caminho da planilha gerada com nome, descricao e status dos convites.
- `DRY_RUN`: quando `True`, apenas encontra os botoes sem clicar.
- `KEEP_BROWSER_OPEN`: quando `True`, deixa o Chrome aberto ao final.

Tambem e possivel sobrescrever por variavel de ambiente:

```bash
DAILY_CONNECTION_LIMIT=3 DRY_RUN=true python main.py
```

## Planilha

O RPA salva as pessoas em `$HOME/Documentos/linkedin_connections.xlsx`.

Colunas geradas:

- `data_hora`
- `nome`
- `descricao`
- `status`
- `perfil_linkedin`

## Estrutura do projeto

```text
main.py                 # Ponto de entrada
config/
├── constants.py        # Valores fixos e regras estaveis
└── settings.py         # Leitura e conversao do .env
src/
├── bot.py              # Fluxo principal de convites
├── browser.py          # Inicializacao e controle do Chrome
├── linkedin.py         # Navegacao, leitura de cards e convites
├── logging_config.py   # Log no terminal e por arquivo de execucao
├── models.py           # Modelos de dados
└── storage.py          # Persistencia da planilha XLSX
```

Os logs de cada execucao sao criados em `logs/`, com data e hora no nome do arquivo. Configure `LOG_DIR` e `LOG_LEVEL` no `.env` se necessario.
