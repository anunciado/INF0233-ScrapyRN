import os
import pandas as pd
import re
from bs4 import BeautifulSoup

class TransformadorLicitacoesRN:
    def __init__(self):
        self.BASE_URL = "http://servicos.searh.rn.gov.br"
        self.DADOS_LIMPOS_DIR = os.path.join("dados_limpos", "licitacao")
        self.ARQUIVO_ENTRADA = "dados_brutos/licitacao/licitacoes_rn_raw.csv"
        os.makedirs(self.DADOS_LIMPOS_DIR, exist_ok=True)

    def limpar_td(self, texto):
        if pd.isna(texto):
            return ''
        return BeautifulSoup(texto, "html.parser").get_text(strip=True)

    def extrair_numero_ano(self, texto):
        texto_limpo = self.limpar_td(texto)
        match = re.search(r'(\d+)\s*/\s*(\d+)', texto_limpo)
        if match:
            return match.group(1), match.group(2)
        return '', ''

    def extrair_processo(self, texto):
        texto_limpo = self.limpar_td(texto)
        texto_limpo = texto_limpo.replace('em', '').strip()

        # Remove após o primeiro hífen
        if '-' in texto_limpo:
            texto_limpo = texto_limpo.split('-')[0].strip()

        # Remove barras e espaços excedentes
        texto_limpo = texto_limpo.replace('/', '').replace(' ', '')

        # Remove pontos
        texto_limpo = texto_limpo.replace('.', '')

        return texto_limpo

    def extrair_link(self, texto):
        if pd.isna(texto):
            return ''
        soup = BeautifulSoup(texto, "html.parser")
        link = soup.find('a')
        if link and 'href' in link.attrs:
            href = link['href']
            # Adiciona prefixo se o link for relativo (começa com "/")
            if href.startswith('/'):
                href = self.BASE_URL + href
            return href
        return ''

    def transformar_dados(self):
        """Método para transformar os dados das licitações."""
        # Lê o arquivo CSV
        df = pd.read_csv(self.ARQUIVO_ENTRADA)

        df['Número'], df['Ano'] = zip(*df['Número'].map(self.extrair_numero_ano))
        df['Processo'] = df['Processo'].map(self.extrair_processo)
        df['Modalidade'] = df['Modalidade'].map(self.limpar_td)
        df['Objeto'] = df['Objeto'].map(self.limpar_td)
        df['Situação'] = df['Situação'].map(self.limpar_td)
        df['Valor'] = df['Valor'].map(self.limpar_td)
        df['Órgão'] = df['Órgão'].map(self.limpar_td)
        df['Link Aviso'] = df['Aviso'].map(self.extrair_link)
        df['Link Contrato'] = df['Contrato'].map(self.extrair_link)

        # Filtrar: mantém apenas linhas com Processo numérico e Ano não vazio
        df = df[df['Processo'].str.match(r'^\d+$')]
        df = df[df['Ano'].str.match(r'^\d+$')]

        # Remove colunas antigas e reorganiza
        df = df[
            ['Número', 'Ano', 'Processo', 'Modalidade', 'Objeto', 'Situação', 'Valor', 'Órgão', 'Link Aviso',
             'Link Contrato']]
        
        # Salva o arquivo transformado
        df.to_csv('dados_limpos/licitacao/licitacoes_rn_clean.csv', index=False, encoding='utf-8')
        print("✅ Arquivo transformado salvo com sucesso!")