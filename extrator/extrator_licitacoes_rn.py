import os

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd

class ExtratorLicitacoesRN:
    def __init__(self):
        self.DOWNLOAD_DIR = "dados_brutos/licitacao"
        self.ANOS = {
            "27": "2025", "26": "2024", "25": "2023", "24": "2022",
            "23": "2021", "22": "2020", "21": "2019", "20": "2018",
            "18": "2017", "17": "2016", "16": "2015", "15": "2014",
            "14": "2013", "13": "2012", "12": "2011", "11": "2010",
            "10": "2009", "9": "2008", "8": "2007", "7": "2006",
            "6": "2005", "5": "2004", "4": "2003", "3": "2002",
            "2": "2001", "1": "2000",
        }
        self.BASE_URL = "http://servicos.searh.rn.gov.br"
        self.COLUNAS = [
            'Número', 'Processo', 'Modalidade', 'Objeto',
            'Situação', 'Valor', 'Órgão', 'Aviso', 'Contrato'
        ]
        os.makedirs(self.DOWNLOAD_DIR, exist_ok=True)

    async def extrair_dados(self):
        """Método principal para coletar dados de licitações."""
        dados = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            for value, ano in self.ANOS.items():
                print(f"🔄 Processando ano {ano}...")
                await page.goto(f"{self.BASE_URL}/searh/Licitacao")

                await page.select_option("select#Idanolicitacao", value)
                await page.click("button.btn.btn-primary:has-text('Consultar')")

                pagina = 1
                while True:
                    print(f"🔄 Página {pagina}")
                    html = await page.content()
                    soup = BeautifulSoup(html, 'html.parser')

                    if soup.find('h4', string='Nenhum resultado encontrado.'):
                        print(f"❌ Nenhum resultado encontrado na página {pagina}. Encerrando o ano {ano}.")
                        break

                    tabela = soup.find('table', class_='table')
                    if not tabela:
                        break

                    linhas = tabela.find_all('tr')[1:]  # Ignora cabeçalho
                    for linha in linhas:
                        colunas = linha.find_all('td')
                        if len(colunas) >= 9:
                            dados.append(colunas)

                    # Próxima página
                    proxima_url = f"{self.BASE_URL}/searh/Licitacao/Paginados?pagina={pagina + 1}"
                    await page.goto(proxima_url)
                    pagina += 1

            await browser.close()

        # Salvar CSV
        df = pd.DataFrame(dados, columns=self.COLUNAS)
        output_file = "licitacoes_rn_raw.csv"
        full_path = f"{self.DOWNLOAD_DIR}/{output_file}"
        df.to_csv(full_path, index=False, encoding='utf-8')
        print(f"\n✅ Arquivo final salvo como: {output_file}")
