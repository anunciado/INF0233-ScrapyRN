import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd

ANOS = {
    "27": "2025",
    "26": "2024",
    "25": "2023",
    "24": "2022",
    "23": "2021",
    "22": "2020",
    "21": "2019",
    "20": "2018",
    "18": "2017",
    "17": "2016",
    "16": "2015",
    "15": "2014",
    "14": "2013",
    "13": "2012",
    "12": "2011",
    "11": "2010",
    "10": "2009",
    "9": "2008",
    "8": "2007",
    "7": "2006",
    "6": "2005",
    "5": "2004",
    "4": "2003",
    "3": "2002",
    "2": "2001",
    "1": "2000",
}

BASE_URL = "http://servicos.searh.rn.gov.br"

async def coletar_dados():
    dados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for value, ano in ANOS.items():
            print(f"Coletando ano {ano} (value={value})...")
            await page.goto(f"{BASE_URL}/searh/Licitacao")

            await page.select_option("select#Idanolicitacao", value)
            await page.click("button.btn.btn-primary:has-text('Consultar')")

            pagina = 1
            while True:
                print(f"  → Página {pagina}")
                html = await page.content()
                soup = BeautifulSoup(html, 'html.parser')

                if soup.find('h4', string='Nenhum resultado encontrado.'):
                    print(f"    Nenhum resultado encontrado na página {pagina}. Encerrando o ano {ano}.")
                    break

                tabela = soup.find('table', class_='table')
                if not tabela:
                    break

                linhas = tabela.find_all('tr')[1:]  # Ignora cabeçalho
                for linha in linhas:
                    colunas = linha.find_all('td')
                    if len(colunas) >= 7:
                        numero_ano = colunas[0].get_text(strip=True)
                        if '/' in numero_ano:
                            numero, ano_extr = [x.strip() for x in numero_ano.split('/', 1)]
                        else:
                            numero = numero_ano
                            ano_extr = ano

                        dados.append([
                            numero,
                            ano_extr,
                            colunas[1].get_text(strip=True),  # Processo
                            colunas[2].get_text(strip=True),  # Modalidade
                            colunas[3].get_text(strip=True),  # Objeto
                            colunas[4].get_text(strip=True),  # Situação
                            colunas[5].get_text(strip=True),  # Valor
                            colunas[6].get_text(strip=True)   # Órgão
                        ])
                # Próxima página → /searh/Licitacao/Paginados?pagina=N
                proxima_url = f"{BASE_URL}/searh/Licitacao/Paginados?pagina={pagina + 1}"
                await page.goto(proxima_url)
                pagina += 1

        await browser.close()

    # Salvar CSV
    colunas = [
        'Número',
        'Ano',
        'Processo',
        'Modalidade',
        'Objeto',
        'Situação',
        'Valor',
        'Órgão'
    ]
    df = pd.DataFrame(dados, columns=colunas)
    df.to_csv("licitacoes_rn.csv", index=False, encoding='utf-8-sig')
    print("\nArquivo CSV salvo com sucesso!")


asyncio.run(coletar_dados())