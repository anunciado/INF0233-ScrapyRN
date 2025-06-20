import pandas as pd
import os
import re
import glob

class TransformadorReceitasRN:
    def __init__(self):
        self.DADOS_BRUTOS_DIR = os.path.join("dados_brutos", "receita")
        self.DADOS_LIMPOS_DIR = os.path.join("dados_limpos", "receita")
        os.makedirs(self.DADOS_LIMPOS_DIR, exist_ok=True)

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

    def transformar_dados(self):
        """
        Método principal para transformar os dados de receitas do RN.
        Lê os arquivos CSV da pasta dados_brutos/receita e gera um arquivo consolidado
        com os dados processados.
        """
        print("🔄 Iniciando transformação dos dados de receitas...")
        
        # Busca todos os arquivos CSV na pasta de dados brutos
        padrao_arquivo = os.path.join(self.DADOS_BRUTOS_DIR, "receita_*_raw.csv")
        arquivos = glob.glob(padrao_arquivo)
        
        if not arquivos:
            print("⚠️ Nenhum arquivo de receita encontrado para processar.")
            return

        # Processamento dos arquivos
        dataframes = []
        for arquivo in arquivos:
            try:
                print(f"🔄 Processando arquivo: {os.path.basename(arquivo)}")
                df = self._processar_arquivo_csv(arquivo)
                dataframes.append(df)
            except Exception as e:
                print(f"❌ Erro ao processar {arquivo}: {e}")

        # Gerar CSV processado
        if dataframes:
            df_total = pd.concat(dataframes, ignore_index=True)
            
            # Ordenar por ano e mês
            df_total = df_total.sort_values(['Ano', 'Mês'])
            
            # Salvar arquivo processado
            output_file = "receitas_rn_clean.csv"
            output_path = os.path.join(self.DADOS_LIMPOS_DIR, output_file)
            df_total.to_csv(output_path, index=False, encoding='utf-8')
            print(f"\n✅ Dados processados salvos em: {output_file}")
            
        else:
            print("⚠️ Nenhum dado foi processado.")