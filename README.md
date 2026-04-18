# LinkedIn Connections RPA

Automacao em Python + Selenium para abrir o Google Chrome, entrar em `Minha rede` no LinkedIn e enviar ate 10 convites por execucao. A extracao de nome, cargo e link do perfil usa BeautifulSoup sobre o HTML renderizado do card.

## Como rodar

```bash
chmod +x run.sh
./run.sh
```

O `run.sh` abre o Google Chrome com um perfil de automacao em `.chrome-profile` e anexa o Selenium pela porta de depuracao `9222`. Se o LinkedIn pedir login, entre manualmente nessa janela uma vez e rode o script novamente.
Ao iniciar, o script pergunta quantas conexoes devem ser feitas. Se nada for digitado em 10 segundos, usa 10 como padrao.

## Configuracoes

Edite `settings.py` para mudar limite, pausas e perfil do Chrome.

Principais campos:

- `DAILY_CONNECTION_LIMIT`: quantidade maxima de convites por execucao.
- `CHROME_BINARY`: caminho do Google Chrome.
- `CHROME_USER_DATA_DIR`: diretorio de dados do Chrome. O padrao e `.chrome-profile` dentro do projeto.
- `CHROME_PROFILE_DIRECTORY`: perfil usado pelo Chrome, normalmente `Default`.
- `CHROMEDRIVER_LOG_PATH`: arquivo de log do ChromeDriver.
- `OUTPUT_XLSX_PATH`: caminho da planilha gerada com nome, descricao e status dos convites.
- `DRY_RUN`: quando `True`, apenas encontra os botoes sem clicar.
- `KEEP_BROWSER_OPEN`: quando `True`, deixa o Chrome aberto ao final.

Tambem e possivel sobrescrever por variavel de ambiente:

```bash
DAILY_CONNECTION_LIMIT=3 DRY_RUN=true ./run.sh
```

## Planilha

O RPA salva as pessoas em `$HOME/Documentos/linkedin_connections.xlsx`.

Colunas geradas:

- `data_hora`
- `nome`
- `descricao`
- `status`
- `perfil_linkedin`

## Observacoes

O Chrome atual nao permite DevTools remote debugging com o diretorio padrao do usuario, como `$HOME/.config/google-chrome`. Quando isso acontece, ele mostra:

```text
DevTools remote debugging requires a non-default data directory.
```

Por isso o RPA usa um perfil separado. Continua sendo Google Chrome, mas o login do LinkedIn precisa ser feito uma vez nesse perfil de automacao.
