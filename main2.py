import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from time import sleep

BASE_URL = "http://www.transparencia.rn.gov.br"
FORM_URL = f"{BASE_URL}/receita"
CSV_URL_TEMPLATE = f"{BASE_URL}/receita-prevista/exportcsv/{{mes}}/{{ano}}/%3C=/{{classificacao}}"

DOWNLOAD_DIR = "receitas_rn_csv"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

anos = list(range(2025, 2018, -1))  # 2025 até 2019
meses = list(range(1, 7))           # Janeiro a Junho
classificacao = "receita"
posicao = "No mês"

session = requests.Session()

# 1. Obter o token CSRF da página inicial
resp = session.get(FORM_URL)
soup = BeautifulSoup(resp.text, "html.parser")
csrf_token = soup.find("input", {"name": "_token"})["value"]

arquivos = []

# 2. Iterar sobre todos os meses e anos
for ano in anos:
    for mes in meses:
        print(f"🔄 Processando {mes:02}/{ano}...")

        # Enviar o POST da consulta (simula clicar em "Consultar")
        consulta_data = {
            "_token": csrf_token,
            "posicao": posicao,
            "mes": mes,
            "ano": ano,
            "classificacao": classificacao
        }

        r = session.post(f"{BASE_URL}/receita-prevista", data=consulta_data)

        if r.status_code != 200:
            print(f"❌ Erro na consulta para {mes:02}/{ano}")
            continue

        # 3. Construir a URL e fazer POST para baixar o CSV
        csv_url = CSV_URL_TEMPLATE.format(mes=mes, ano=ano, classificacao=classificacao)
        csv_post_data = {
            "_token": csrf_token
        }

        csv_response = session.post(csv_url, data=csv_post_data)

        if csv_response.status_code == 200 and len(csv_response.content) > 100:
            filename = f"receita_{ano}_{mes:02}.csv"
            filepath = os.path.join(DOWNLOAD_DIR, filename)

            with open(filepath, "wb") as f:
                f.write(csv_response.content)

            print(f"✅ CSV salvo: {filepath}")
            arquivos.append(filepath)
        else:
            print(f"⚠️ CSV não disponível para {mes:02}/{ano}")

        sleep(1)

# 4. Unir os CSVs com pandas
dataframes = []
for arquivo in arquivos:
    try:
        filename = os.path.basename(arquivo)
        match = re.search(r"receita_(\d{4})_(\d{2})\.csv", filename)
        if match:
            ano = int(match.group(1))
            mes = int(match.group(2))
        else:
            ano, mes = None, None

        try:
            df = pd.read_csv(arquivo, sep=';', encoding='utf-8')
        except UnicodeDecodeError:
            print(f"⚠️ Arquivo {filename} não está em UTF-8. Tentando latin1...")
            df = pd.read_csv(arquivo, sep=';', encoding='latin1')

        df['ano'] = ano
        df['mes'] = mes
        df['arquivo_origem'] = filename
        dataframes.append(df)

    except Exception as e:
        print(f"Erro ao ler {arquivo}: {e}")

# 5. Gerar CSV final
if dataframes:
    df_total = pd.concat(dataframes, ignore_index=True)
    output_file = "receita_rn_2019_2025_jan_jun.csv"
    df_total.to_csv(output_file, index=False, sep=';', encoding='utf-8')
    print(f"\n✅ Arquivo final salvo como: {output_file}")
else:
    print("⚠️ Nenhum dado foi consolidado.")