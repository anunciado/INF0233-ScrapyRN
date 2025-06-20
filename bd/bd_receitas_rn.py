import sqlite3
import csv
from datetime import datetime


class BDReceitasRN:
    def __init__(self, db_name='dados_rn.db'):
        """Inicializa a classe e cria a conexão com o banco de dados"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabela()
        self.arquivo_entrada = "dados_limpos/receita/receitas_rn_clean.csv"

    def criar_tabela(self):
        """Cria a tabela no banco de dados se ela não existir"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS receita (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT,
                categoria TEXT,
                origem TEXT,
                especie TEXT,
                rubrica TEXT,
                alinea TEXT,
                detalhamento TEXT,
                receita_prevista REAL,
                receita_arrecadada REAL,
                ano TEXT,
                mes TEXT,
                data_insercao TEXT
            )
        ''')
        self.conn.commit()

    def limpar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM receita;")
        self.conn.commit()

    def carregar_dados(self):
        """Insere os dados do arquivo CSV no banco de dados"""
        with open(self.arquivo_entrada, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Limpa a tabela antes de inserir novos dados
            self.limpar_tabela()

            for row in reader:
                # Prepara os dados para inserção
                data = (
                    row['Código'],
                    row['Categoria'],
                    row['Origem'],
                    row['Espécie'],
                    row['Rúbrica'],
                    row['Alínea'],
                    row['Detalhamento'],
                    float(row['Receita Prevista (Bruta)']),
                    float(row['Receita Arrecadada (Bruta)']),
                    row['Ano'],
                    row['Mês'],
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )

                # Insere no banco de dados
                self.cursor.execute('''
                    INSERT INTO receita (
                        codigo, categoria, origem, especie, rubrica, alinea, detalhamento,
                        receita_prevista, receita_arrecadada, ano, mes, data_insercao
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', data)

        self.conn.commit()
        print(f"✅ Dados do arquivo {self.arquivo_entrada} inseridos com sucesso!")

    def close(self):
        """Fecha a conexão com o banco de dados"""
        self.conn.close()