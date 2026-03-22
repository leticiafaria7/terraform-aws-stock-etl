# --------------------------------------------------------------------------------------------------------------------- #
# Imports
# --------------------------------------------------------------------------------------------------------------------- #

import pandas as pd
import datetime
from tqdm import tqdm
from os import walk
from typing import List

# --------------------------------------------------------------------------------------------------------------------- #
# Listar arquivos de uma pasta
# --------------------------------------------------------------------------------------------------------------------- #

def listar_arquivos_pasta(folder_path: str) -> List[str]:

    files = []
    for (dirpath, dirnames, filenames) in walk(folder_path):
        files.extend(filenames)

    return files

# --------------------------------------------------------------------------------------------------------------------- #
# Gerar lista de arquivos
# --------------------------------------------------------------------------------------------------------------------- #

def gerar_lista_arquivos_hoje(path_scraped, dia):

    arquivos = listar_arquivos_pasta(path_scraped)
    arquivos_hoje = [file for file in arquivos if file[5:15] == dia]

    return arquivos_hoje

# --------------------------------------------------------------------------------------------------------------------- #
# Gerar base concatenada
# --------------------------------------------------------------------------------------------------------------------- #

def gerar_tabela_hoje_concat(path_scraped, arquivos_hoje):

    df_hoje = pd.DataFrame()

    for arquivo in arquivos_hoje:
        tmp = pd.read_csv(f"{path_scraped}{arquivo}")
        df_hoje = pd.concat([df_hoje, tmp])

    df_hoje = df_hoje[['date', 'codigo', 'price']]

    return df_hoje

# --------------------------------------------------------------------------------------------------------------------- #
# Persistir tabela
# --------------------------------------------------------------------------------------------------------------------- #

def persistir_tabela_hoje(df_hoje, path_daily, dia):

    df_hoje.to_parquet(f"{path_daily}/valores-acoes-{dia}.parquet", engine = 'pyarrow')

# --------------------------------------------------------------------------------------------------------------------- #
# Orquestrar
# --------------------------------------------------------------------------------------------------------------------- #

def gerar_tabela_acoes_diaria(path_scraped, path_daily, dia):

    arquivos_hoje = gerar_lista_arquivos_hoje(path_scraped, dia)
    df_hoje = gerar_tabela_hoje_concat(path_scraped, arquivos_hoje)
    persistir_tabela_hoje(df_hoje, path_daily, dia)
    print(f"\nFim da geração da tabela de valores das ações de {dia}")

# --------------------------------------------------------------------------------------------------------------------- #
# Loop para processar os dias que ainda não foram processados
# --------------------------------------------------------------------------------------------------------------------- #

def persistir_tabelas_ainda_nao_processadas():

    path_scraped = '../data/scraped/'
    path_daily = '../data/daily/'

    dias_processados = listar_arquivos_pasta(path_daily)
    dias_processados = [file.replace('valores-acoes-', '').replace('.parquet', '') for file in dias_processados]
    
    arquivos = listar_arquivos_pasta(path_scraped)
    dias = list(set([file[5:15] for file in arquivos]))
    dias = [dia for dia in dias if dia not in dias_processados]

    print(f"Dias ainda não processados: {dias}")

    for dia in tqdm(dias):
        gerar_tabela_acoes_diaria(path_scraped, path_daily, dia)

# --------------------------------------------------------------------------------------------------------------------- #
# Executar
# --------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    persistir_tabelas_ainda_nao_processadas()

    
