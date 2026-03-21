# --------------------------------------------------------------------------------------------------------------------- #
# Imports
# --------------------------------------------------------------------------------------------------------------------- #

import pandas as pd
import datetime
import requests
import time
from tqdm import tqdm
from bs4 import BeautifulSoup

# --------------------------------------------------------------------------------------------------------------------- #
# Obter lista de ativos
# --------------------------------------------------------------------------------------------------------------------- #

ativos_ibov = pd.read_excel('refined/ativos_ibov.xlsx')
lista_ativos = list(ativos_ibov['ticker'].unique())

# --------------------------------------------------------------------------------------------------------------------- #
# Scraping
# --------------------------------------------------------------------------------------------------------------------- #

def get_stock_value(stock):
    url = f'https://www.google.com/finance/quote/{stock}:BVMF?hl=pt'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    date = datetime.datetime.now()
    price = soup.find('div', {'class':'YMlKec fxKbKc'}).text.encode('utf-8').decode('utf-8').replace('\xa0', ' ').strip()
    # print(price)

    df = pd.DataFrame(data = {'date':[date], 
                              'codigo':[stock],
                              'price':[price]})
    
    df['date'] = pd.to_datetime(df['date']).dt.round('min')
    df['price'] = df['price'].apply(lambda x: x.replace('R$ ', '').replace(',', '.')).astype(float)
    return df

# --------------------------------------------------------------------------------------------------------------------- #
# Concatenar tabelas
# --------------------------------------------------------------------------------------------------------------------- #

def get_table_stocks(lista_ativos):

    df_precos = pd.DataFrame()

    for ativo in tqdm(lista_ativos):
        try:
            tmp = get_stock_value(ativo)
            df_precos = pd.concat([df_precos, tmp])
        except Exception as e:
            print(e)

    df_precos = df_precos.reset_index(drop = True)

    filename = str(datetime.datetime.now())[:16].replace(' ', '-').replace(':', '-')
    df_precos.to_csv(f'scraped/file-{filename}.csv')

# --------------------------------------------------------------------------------------------------------------------- #
# Execução
# --------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':

    while True:
        print(f"Início da execução: {str(datetime.datetime.now())[:16]}")
        get_table_stocks(lista_ativos)
        print(f"Salvando arquivo: {str(datetime.datetime.now())[:16]}")
        print()
        time.sleep(60*60)
    