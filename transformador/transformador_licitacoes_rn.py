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
        
        self.orgao_categoria = {
            # ADMINISTRAÇÃO
            'SEARH': 'ADMINISTRAÇÃO',  # Secretaria de Administração e RH
            'SET': 'ADMINISTRAÇÃO',     # Secretaria de Tributação
            'GAC': 'ADMINISTRAÇÃO',     # Gabinete Civil
            'SEPLAN': 'ADMINISTRAÇÃO',  # Secretaria de Planejamento
            'CONTROL': 'ADMINISTRAÇÃO', # Controladoria Geral
            'GVG': 'ADMINISTRAÇÃO',     # Governadoria
            'ASSECOM': 'ADMINISTRAÇÃO', # Assessoria de Comunicação
            
            # AGRICULTURA
            'SEARA': 'AGRICULTURA',     # Secretaria de Agricultura
            'EMATER': 'AGRICULTURA',    # Empresa de Assistência Técnica Rural
            'IDIARN': 'AGRICULTURA',    # Instituto de Irrigação
            'CEASA': 'AGRICULTURA',     # Central de Abastecimento
            
            # ASSISTÊNCIA SOCIAL
            'SETHAS': 'ASSISTÊNCIA SOCIAL',  # Secretaria do Trabalho, Habitação e Assistência Social
            'FUNDASE': 'ASSISTÊNCIA SOCIAL', # Fundação Socioeducativa
            
            # CIÊNCIA E TECNOLOGIA
            'ITEP': 'CIÊNCIA E TECNOLOGIA',  # Instituto Técnico-Científico de Perícia
            'FAPERN': 'CIÊNCIA E TECNOLOGIA', # Fundação de Apoio à Pesquisa
            'IPERN': 'CIÊNCIA E TECNOLOGIA',  # Instituto de Perícia
            'DATANORTE': 'CIÊNCIA E TECNOLOGIA', # Empresa de Tecnologia da Informação
            'DEI': 'CIÊNCIA E TECNOLOGIA',    # Departamento de Estatísticas
            
            # COMÉRCIO E SERVIÇOS
            'SETUR': 'COMÉRCIO E SERVIÇOS',  # Secretaria de Turismo
            'EMPROTUR': 'COMÉRCIO E SERVIÇOS', # Empresa de Turismo
            'JUCERN': 'COMÉRCIO E SERVIÇOS',  # Junta Comercial
            'IPEM': 'COMÉRCIO E SERVIÇOS',    # Instituto de Pesos e Medidas
            'DETRAN': 'COMÉRCIO E SERVIÇOS',  # Departamento de Trânsito
            
            # CULTURA
            'FJA': 'CULTURA',             # Fundação José Augusto (Cultura)
            'SEEL': 'CULTURA',            # Secretaria de Esporte e Lazer
            
            # DIREITOS DA CIDADANIA
            'SESED': 'DIREITOS DA CIDADANIA', # Secretaria de Segurança Pública
            'CORPO BOMBEIRO': 'DIREITOS DA CIDADANIA', # Corpo de Bombeiros
            'PM-DS': 'DIREITOS DA CIDADANIA', # Polícia Militar
            'PM-QCG': 'DIREITOS DA CIDADANIA', # Polícia Militar
            'PCRN': 'DIREITOS DA CIDADANIA',  # Polícia Civil
            'SAPE': 'DIREITOS DA CIDADANIA',  # Secretaria de Administração Penitenciária
            'SEDEC': 'DIREITOS DA CIDADANIA', # Defesa Civil
            
            # ENCARGOS ESPECIAIS
            'ARSEP': 'ENCARGOS ESPECIAIS',  # Agência Reguladora de Serviços
            'CAERN': 'ENCARGOS ESPECIAIS',  # Companhia de Águas e Esgotos
            'AGNRN': 'ENCARGOS ESPECIAIS',  # Agência Reguladora
            
            # ENERGIA
            'POTIGÁS': 'ENERGIA',  # Companhia de Gás
            
            # EDUCAÇÃO
            'SEEC': 'EDUCAÇÃO',  # Secretaria de Educação
            
            # GESTÃO AMBIENTAL
            'IDEMA': 'GESTÃO AMBIENTAL',  # Instituto de Desenvolvimento Sustentável
            'SEMARH': 'GESTÃO AMBIENTAL', # Secretaria de Meio Ambiente
            
            # JUDICIÁRIA
            'PGE': 'JUDICIÁRIA',          # Procuradoria Geral do Estado
            'SEJUC': 'JUDICIÁRIA',        # Secretaria de Justiça e Cidadania
            'DEFENSORIA': 'JUDICIÁRIA',   # Defensoria Pública
            
            # SAÚDE
            'SESAP': 'SAÚDE',        # Secretaria de Saúde
            'HMAF': 'SAÚDE',         # Hospital Militar
            'HGT': 'SAÚDE',          # Hospital Giselda Trigueiro
            'LACEN': 'SAÚDE',        # Laboratório Central
            'HDBC': 'SAÚDE',         # Hospital Dr. João Machado
            'HMWG': 'SAÚDE',         # Hospital Monsenhor Walfredo Gurgel
            'HRDML': 'SAÚDE',        # Hospital Regional Deoclécio Marques
            'HJM': 'SAÚDE',          # Hospital Juvino Barreto
            'HJPB': 'SAÚDE',         # Hospital João Pessoa
            'HCCA': 'SAÚDE',         # Hospital da Criança
            'HRF': 'SAÚDE',          # Hospital Regional de Fruturos
            'HRTVM': 'SAÚDE',        # Hospital Regional Tarcísio Maia
            'HRCNOVOS': 'SAÚDE',     # Hospital Regional de Nova Cruz
            'HRA': 'SAÚDE',          # Hospital Regional do Assú
            'HRHMM': 'SAÚDE',        # Hospital Regional de Mossoró
            'HMPMC': 'SAÚDE',        # Hospital de Pediatria
            'HEMORM': 'SAÚDE',       # Hemocentro
            'HROGS': 'SAÚDE',        # Hospital de Ortopedia
            'HRSPP': 'SAÚDE',        # Hospital Regional de Pau dos Ferros
            'HRPGOS': 'SAÚDE',       # Hospital Regional de Goianinha
            'II URSAP': 'SAÚDE',     # Unidade Regional de Saúde
            'HPVS': 'SAÚDE',         # Hospital de Pau dos Ferros
        }

    def obter_categoria(self, orgao):
        """Retorna a categoria do órgão com base no mapeamento."""
        return self.orgao_categoria.get(orgao, 'NÃO CLASSIFICADO')

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
        
        # Adiciona a nova coluna Categoria
        df['Categoria'] = df['Órgão'].map(self.obter_categoria)

        # Filtrar: mantém apenas linhas com Processo numérico e Ano não vazio
        df = df[df['Processo'].str.match(r'^\d+$')]
        df = df[df['Ano'].str.match(r'^\d+$')]

        # Remove colunas antigas e reorganiza
        df = df[
            ['Número', 'Ano', 'Processo', 'Modalidade', 'Objeto', 'Situação', 'Valor', 'Órgão', 'Categoria', 'Link Aviso',
             'Link Contrato']]
        
        # Salva o arquivo transformado
        df.to_csv('dados_limpos/licitacao/licitacoes_rn_clean.csv', index=False, encoding='utf-8')
        print("✅ Arquivo transformado salvo com sucesso!")