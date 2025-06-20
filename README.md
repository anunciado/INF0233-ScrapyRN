# INF0233-ScrapyRN
Uma ferramenta para extrair informações de licitações e receitas do estado do Rio Grande do Norte para a disciplina INF0243: Extração Automática de Dados da UFG.

## Funcionalidades

- Automação da extração, transformação e carregamento (ETL) de dados públicos do Rio Grande do Norte, sendo eles: licitações e receitas.        
- Persistência dos dados num banco de dados local.

## Tecnologias

 - Python 3, uma linguagem de programação de alto nível e de propósito geral;
 - Beautiful Soup, uma biblioteca para extrair dados de arquivos HTML e XML;
 - NumPy, uma biblioteca para cálculos númericos;
 - Pandas, uma biblioteca de análise e manipulação de dados;
 - Playwright, um framework para testes e automação na Web.

## Configuração do ambiente de desenvolvimento

1. Instale o python, na versão 3.10, através do [link](https://www.python.org/downloads/);
2. Instale o navegador do chrome através do [link](https://www.google.com/chrome/);
3. Clone este repositório https://github.com/anunciado/INF0233-ScrapyRN.git em sua máquina local;
4. Abra o projeto em sua IDE de preferência, como sugestão utilize o Visual Studio Code ou PyCharm;
5. Crie um ambiente virtual com o comando:
```
. python -m venv venv
```
6. Ative o ambiente virtual com o comando:
* No windows:
```
venv\Scripts\activate
```
* No linux:
```
source venv/bin/activate
```
7. Instale as bibliotecas no seu ambiente virtual a partir do arquivo _requirements.txt_ com o comando:
```
pip install -r requirements.txt
```
8. Instale o playwright com o comando:
```
playwright install
```
9. Execute o projeto com o comando:
```
python main.py
```

## Contribuição:

1. `Mova` a issue a ser resolvida para a coluna _In Progress_ no [board do projeto].  
2. `Clone` este repositório https://github.com/anunciado/INF0233-ScrapyRN.git.
3. `Crie` um branch a partir da branch _dev_.
4. `Commit` suas alterações.
5. `Realize` o push das alterações.
6. `Crie` a solicitação PR para branch _dev_.
7. `Mova` a _issue_ da coluna _In Progress_ para a coluna _Code Review_ do [board do projeto].

## Desenvolvedores

- [Luís Eduardo](https://github.com/anunciado)