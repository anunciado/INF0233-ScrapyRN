import asyncio

from bd.bd_licitacoes_rn import BDLicitacoesRN
from bd.bd_receitas_rn import BDReceitasRN
from extrator.extrator_receitas_rn import ExtratorReceitasRN
from extrator.extrator_licitacoes_rn import ExtratorLicitacoesRN
from transformador.transformador_licitacoes_rn import TransformadorLicitacoesRN
from transformador.transformador_receitas_rn import TransformadorReceitasRN

async def executar_extracao(extrator, nome_processo):
    """
    Executa o processo de extração de dados.
    
    Args:
        extrator: Instância do extrator a ser executado
        nome_processo: Nome do processo de extração para logging
    """
    print(f"\n📊 Iniciando extração de {nome_processo}...")
    try:
        await extrator.extrair_dados()
        print(f"✅ Coleta de {nome_processo} finalizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro na extração de {nome_processo}: {str(e)}")


def executar_transformacao(transformador, nome_processo):
    """
    Executa o processo de transformação dos dados.

    Args:
        extrator: Instância do extrator que contém os dados a serem transformados
        nome_processo: Nome do processo para logging
    """
    print(f"\n🔄 Iniciando transformação dos dados de {nome_processo}...")
    try:
        transformador.transformar_dados()
        print(f"✅ Transformação de {nome_processo} finalizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro na transformação de {nome_processo}: {str(e)}")


def executar_carregamento(carregador, nome_processo):
    """
    Executa o processo de carregamento dos dados.

    Args:
        carregador: Instância do bd que contém os dados a serem carregados
        nome_processo: Nome do processo para logging
    """
    print(f"\n🔄 Iniciando carregamento dos dados de {nome_processo}...")
    try:
        carregador.carregar_dados()
        print(f"✅ Carregamento de {nome_processo} finalizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro no carregamento de {nome_processo}: {str(e)}")

async def main():
    """
    Função principal que coordena a extração, transformação e bd dos dados de licitações e receitas do RN.
    """
    print("🚀 Iniciando extração de dados...")
    
    # Extração de receitas
    extrator_receitas = ExtratorReceitasRN()
    await executar_extracao(extrator_receitas, "receitas")

    # Extração de licitações
    extrator_licitacoes = ExtratorLicitacoesRN()
    await executar_extracao(extrator_licitacoes, "licitações")

    print("\n✨ Processo de extração finalizado!")
    print("🚀 Iniciando transformação dos dados...")

    # Transformação de receitas
    transformador_receitas = TransformadorReceitasRN()
    executar_transformacao(transformador_receitas, "receitas")

    # Transformação de licitações
    transformador_licitacoes = TransformadorLicitacoesRN()
    executar_transformacao(transformador_licitacoes, "licitações")

    print("\n✨ Processo de transformação finalizado!")
    print("🚀 Iniciando carregamento de dados...")

    # Carregamento de receitas
    bd_receitas = BDReceitasRN()
    try:
        executar_carregamento(bd_receitas, "receitas")
    finally:
        bd_receitas.close()

    # Carregamento de licitações
    bd_licitacoes = BDLicitacoesRN()
    try:
        executar_carregamento(bd_licitacoes, "licitações")
    finally:
        bd_licitacoes.close()

    print("\n✨ Processo de carregamento finalizado!")
if __name__ == "__main__":
    asyncio.run(main())  # Executando o loop de eventos assíncrono