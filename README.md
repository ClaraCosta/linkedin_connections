# LinkedIn Connections RPA

Automacao em Python + Selenium para abrir o Google Chrome, entrar em `Minha rede` no LinkedIn e enviar ate 10 convites por execucao. A extracao de nome, cargo e link do perfil usa BeautifulSoup sobre o HTML renderizado do card.

## Como rodar

```bash
source env/bin/activate
cp .env.example .env
python main.py
```

O programa encerra instancias anteriores do Chrome, abre e controla uma nova janela automaticamente. A sessao do LinkedIn fica no perfil dedicado `~/.linkedin-selenium`, fora do projeto. Na primeira execucao, entre manualmente no LinkedIn nessa janela; os proximos usos reutilizam a sessao salva.

## Configuracoes

Edite `.env` para mudar limite, pausas e perfil do Chrome. Use `.env.example` como modelo; o arquivo `.env` nao entra no Git.

Principais campos:

- `DAILY_CONNECTION_LIMIT`: quantidade maxima de convites por execucao.
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
