# --------------------------------------------------------------------------------------------------------------------- #
# Imports
# --------------------------------------------------------------------------------------------------------------------- #

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# --------------------------------------------------------------------------------------------------------------------- #
# Tratar tabela de empresas da B3 e respectivos setores
# --------------------------------------------------------------------------------------------------------------------- #

def tratar_setores_empresas_b3():
    lista_empresas_b3 = pd.read_excel('../data/raw/ClassifSetorial.xlsx', skiprows = 1).drop('Unnamed: 0', axis = 1)
    lista_empresas_b3.columns = ['setor', 'subsetor', 'segmento', 'nome_pregao', 'codigo', 'segmento_negociacao']
    lista_empresas_b3 = lista_empresas_b3[lista_empresas_b3['nome_pregao'] != 'NOME DE PREGÃO']
    lista_empresas_b3 = lista_empresas_b3[['codigo', 'nome_pregao', 'setor', 'subsetor', 'segmento']]

    for c in ['setor', 'subsetor', 'segmento']:
        lista_empresas_b3[c] = lista_empresas_b3[c].ffill()

    print(f"Quantidade de linhas da tabela: {lista_empresas_b3.shape[0]}")
    print(f"Quantidade de códigos únicos:   {lista_empresas_b3['codigo'].nunique()}")

    for c in ['setor', 'subsetor', 'segmento']:
        tmp = lista_empresas_b3[[c]].value_counts().reset_index()
        print(f"{c} | {tmp.shape[0]} categorias")
    
    return lista_empresas_b3

# --------------------------------------------------------------------------------------------------------------------- #
# Tratar tabela de ativos da carteira do Ibovespa
# --------------------------------------------------------------------------------------------------------------------- #

def tratar_ativos_ibovespa():
    # leitura da base
    ativos_ibov = pd.read_csv('../data/raw/IBOVDia_09-03-26.csv', encoding = 'latin1', sep = ';', skiprows = 1).drop('Part. (%)', axis = 1).reset_index()

    # correção do layout
    ativos_ibov.columns = ['ticker', 'empresa', 'tipo_acao', 'qtd_teorica', 'pct_part']
    ativos_ibov = ativos_ibov[ativos_ibov['empresa'].notna()]

    # criar coluna de código para join
    ativos_ibov['codigo'] = ativos_ibov['ticker'].apply(lambda x: x[:4])

    # separar tipo da ação
    ativos_ibov['segm_gov'] = ativos_ibov['tipo_acao'].apply(lambda x: x.split(' ')[-1])
    ativos_ibov['tipo_acao_2'] = ativos_ibov.apply(lambda row: row['tipo_acao'].replace(row['segm_gov'], '').strip(), axis = 1)
    ativos_ibov['tipo_acao'] = np.where(ativos_ibov['tipo_acao_2'] == '', ativos_ibov['segm_gov'], ativos_ibov['tipo_acao_2'])
    ativos_ibov['tipo_acao'] = ativos_ibov['tipo_acao'].str.replace('  ', ' ')
    ativos_ibov['segm_gov'] = np.where(ativos_ibov['tipo_acao_2'] == '', None, ativos_ibov['segm_gov'])
    ativos_ibov['complemento_tipo'] = ativos_ibov['tipo_acao'].apply(lambda x: x.split(' '))
    ativos_ibov['tipo_acao'] = ativos_ibov['complemento_tipo'].apply(lambda x: x[0])
    ativos_ibov['complemento_tipo'] = np.where(ativos_ibov['complemento_tipo'].apply(lambda x: len(x)) == 2, ativos_ibov['complemento_tipo'].apply(lambda x: x[-1]), None)
    ativos_ibov = ativos_ibov.drop('tipo_acao_2', axis = 1)

    # reorganizar colunas
    ativos_ibov = ativos_ibov[['ticker', 'codigo', 'empresa', 'tipo_acao', 'complemento_tipo', 'segm_gov', 'qtd_teorica', 'pct_part']]

    # transformar colunas float
    ativos_ibov['qtd_teorica'] = ativos_ibov['qtd_teorica'].str.replace('.', '').astype(float)
    ativos_ibov['pct_part'] = ativos_ibov['pct_part'].str.replace(',', '.').astype(float)

    return ativos_ibov

# --------------------------------------------------------------------------------------------------------------------- #
# Juntar bases e persistir
# --------------------------------------------------------------------------------------------------------------------- #

def juntar_bases(ativos_ibov, lista_empresas_b3):
    ativos_ibov_enriquecida = ativos_ibov.copy()

    # join com segmento
    ativos_ibov_enriquecida = ativos_ibov_enriquecida.merge(lista_empresas_b3.drop('nome_pregao', axis = 1), on = 'codigo', how = 'left')
    ativos_ibov_enriquecida = ativos_ibov_enriquecida.drop('codigo', axis = 1)

    return ativos_ibov_enriquecida

def persistir_tabela_dimensao(ativos_ibov_enriquecida):
    ativos_ibov_enriquecida.to_parquet('../data/refined/ativos_ibov.parquet', engine = 'pyarrow')

# --------------------------------------------------------------------------------------------------------------------- #
# Orquestração do pipeline
# --------------------------------------------------------------------------------------------------------------------- #

def pipeline_tabela_dimensao():
    print('Processando setores das empresas da B3\n ..........')
    lista_empresas_b3 = tratar_setores_empresas_b3()

    print('\nProcessando ativos do Ibovespa ..................')
    ativos_ibov = tratar_ativos_ibovespa()

    print('\nJuntando bases ..................................')
    ativos_ibov_enriquecida = juntar_bases(ativos_ibov, lista_empresas_b3)

    print('\nPersistindo bases ...............................')
    persistir_tabela_dimensao(ativos_ibov_enriquecida)

    print('\nFim do pipeline da tabela dimensão :)')

# --------------------------------------------------------------------------------------------------------------------- #
# Execução
# --------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    try:
        pipeline_tabela_dimensao()

    except Exception as e:
        print(e)
    