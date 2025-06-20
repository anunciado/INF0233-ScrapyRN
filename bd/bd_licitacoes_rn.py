import sqlite3
import csv
from datetime import datetime


class BDLicitacoesRN:
    def __init__(self, db_name='dados_rn.db'):
        """Inicializa a classe e cria a conexão com o banco de dados"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabela()
        self.arquivo_entrada = "dados_limpos/licitacao/licitacoes_rn_clean.csv"

    def criar_tabela(self):
        """Cria a tabela no banco de dados se ela não existir"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS licitacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT,
                ano INTEGER,
                processo TEXT,
                modalidade TEXT,
                objeto TEXT,
                situacao TEXT,
                valor REAL,
                orgao TEXT,
                categoria TEXT,
                link_aviso TEXT,
                link_contrato TEXT,
                data_insercao TEXT
            )
        ''')
        self.conn.commit()

    def limpar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM licitacao;")
        self.conn.commit()

    def converter_valor(self, valor_str):
        """Converte o valor do formato brasileiro para float"""
        if not valor_str or valor_str == "0,00":
            return 0.0

        try:
            # Remove pontos e substitui vírgula por ponto
            cleaned = valor_str.replace('.', '').replace(',', '.')
            return float(cleaned)
        except ValueError:
            return 0.0

    def carregar_dados(self):
        """Insere os dados do arquivo CSV no banco de dados"""
        with open(self.arquivo_entrada, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Limpa a tabela antes de inserir novos dados
            self.limpar_tabela()

            for row in reader:
                # Prepara os dados para inserção
                data = (
                    row['Número'],
                    int(row['Ano']),
                    row['Processo'],
                    row['Modalidade'],
                    row['Objeto'],
                    row['Situação'],
                    self.converter_valor(row['Valor']),
                    row['Órgão'],
                    row['Categoria'],
                    row['Link Aviso'],
                    row['Link Contrato'],
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )

                # Insere no banco de dados
                self.cursor.execute('''
                    INSERT INTO licitacao (
                        numero, ano, processo, modalidade, objeto, 
                        situacao, valor, orgao, categoria, link_aviso, link_contrato, data_insercao
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', data)

        self.conn.commit()
        print(f"✅ Dados do arquivo {self.arquivo_entrada} inseridos com sucesso!")

    def close(self):
        """Fecha a conexão com o banco de dados"""
        self.conn.close()