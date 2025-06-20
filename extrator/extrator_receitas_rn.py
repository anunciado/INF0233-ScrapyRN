import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from time import sleep

class ExtratorReceitasRN:
    def __init__(self):
        self.BASE_URL = "http://www.transparencia.rn.gov.br"
        self.FORM_URL = f"{self.BASE_URL}/receita"
        self.CSV_URL_TEMPLATE = f"{self.BASE_URL}/receita-prevista/exportcsv/{{mes}}/{{ano}}/%3C=/{{classificacao}}"
        self.DOWNLOAD_DIR = "dados_brutos/receita"
        self.session = requests.Session()
        os.makedirs(self.DOWNLOAD_DIR, exist_ok=True)

    def _obter_csrf_token(self):
        resp = self.session.get(self.FORM_URL)
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup.find("input", {"name": "_token"})["value"]

    def _baixar_csv(self, mes, ano, classificacao, csrf_token):
        csv_url = self.CSV_URL_TEMPLATE.format(mes=mes, ano=ano, classificacao=classificacao)
        csv_post_data = {"_token": csrf_token}
        return self.session.post(csv_url, data=csv_post_data)

    def _processar_arquivo_csv(self, arquivo):
        filename = os.path.basename(arquivo)
        match = re.search(r"receita_(\d{4})_(\d{2})_raw\.csv", filename)
        if match:
            ano, mes = int(match.group(1)), int(match.group(2))
        else:
            ano, mes = None, None

        df = pd.read_csv(arquivo, sep=',', encoding='utf-8')
        df['Ano'] = ano
        df['Mês'] = mes
        return df

    def extrair_dados(self, ano_inicio=2019, ano_fim=2025, mes_fim=6):
        """
        Método principal para coletar dados de receitas do RN.
        Para anos anteriores ao ano_fim, coleta todos os meses (1-12).
        Para o ano_fim, coleta do mês 1 até mes_fim.
        
        Args:
            ano_inicio (int): Ano inicial da coleta
            ano_fim (int): Ano final da coleta
            mes_fim (int): Mês final da coleta (aplicado apenas ao ano_fim)
        """
        anos = list(range(ano_fim, ano_inicio - 1, -1))
        classificacao = "receita"
        posicao = "No mês"
        arquivos = []

        csrf_token = self._obter_csrf_token()

        for ano in anos:
            # Define o intervalo de meses baseado no ano atual
            if ano == ano_fim:
                meses = list(range(1, mes_fim + 1))
            else:
                meses = list(range(1, 13))  # Janeiro a Dezembro

            for mes in meses:
                print(f"🔄 Processando {mes:02}/{ano}...")

                consulta_data = {
                    "_token": csrf_token,
                    "posicao": posicao,
                    "mes": mes,
                    "ano": ano,
                    "classificacao": classificacao
                }

                r = self.session.post(f"{self.BASE_URL}/receita-prevista", data=consulta_data)

                if r.status_code != 200:
                    print(f"❌ Erro na consulta para {mes:02}/{ano}")
                    continue

                csv_response = self._baixar_csv(mes, ano, classificacao, csrf_token)

                if csv_response.status_code == 200 and len(csv_response.content) > 100:
                    filename = f"receita_{ano}_{mes:02}_raw.csv"
                    filepath = os.path.join(self.DOWNLOAD_DIR, filename)

                    with open(filepath, "wb") as f:
                        f.write(csv_response.content)

                    print(f"\n✅ Arquivo final salvo como: {filename}")
                    arquivos.append(filepath)
                else:
                    print(f"⚠️ CSV não disponível para {mes:02}/{ano}")

                sleep(1)