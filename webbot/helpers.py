import requests
from bs4 import BeautifulSoup
from lxml import etree
from datetime import datetime
import pandas as pd

def get_ano(vendas: list[dict]):
    data_inicio = 9999
    data_fim = 0

    for objeto in vendas:
        data = int(objeto['data_vencimento'].split("/")[1])
        
        if data < data_inicio:
            data_inicio = data

        if data > data_fim:
            data_fim = data
        
    return data_inicio, data_fim

def get_ano_mes(objeto:dict):
    string_data_vencimento = objeto['data_vencimento'].split('/')
    mes = string_data_vencimento[0]
    ano = string_data_vencimento[1]
    return mes, int(ano) 

def get_indices():
    url = f'https://aplicativos.tjes.jus.br/sistemaspublicos/corregedoria/tabelas_atm/AtualizMonetaria.cfm?DtInicio=1969&DtFinal=2024&Botao=Gerar+Relatório'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tabelas = soup.find_all('table', cellpadding="5", cellspacing="3")

    valores = {}

    tabela1 = tabelas[0]
    linhas1 = tabela1.find_all('tr')[1:]  

    for linha in linhas1:
        colunas = linha.find_all('td')
        if colunas:
            ano = colunas[0].text.strip()
            meses_jan_jun = {
                "01": colunas[1].text.strip(),
                "02": colunas[2].text.strip(),
                "03": colunas[3].text.strip(),
                "04": colunas[4].text.strip(),
                "05": colunas[5].text.strip(),
                "06": colunas[6].text.strip(),
            }
            valores[ano] = meses_jan_jun

    tabela2 = tabelas[1]
    linhas2 = tabela2.find_all('tr')[1:]  

    for linha in linhas2:
        colunas = linha.find_all('td')
        if colunas:
            ano = colunas[0].text.strip()
            meses_jul_dez = {
                "07": colunas[1].text.strip(),
                "08": colunas[2].text.strip(),
                "09": colunas[3].text.strip(),
                "10": colunas[4].text.strip(),
                "11": colunas[5].text.strip(),
                "12": colunas[6].text.strip(),
            }
            if ano in valores:
                valores[ano].update(meses_jul_dez)  
            else:
                valores[ano] = meses_jul_dez

    df = pd.DataFrame.from_dict(valores, orient='index')

    df.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Ano'}, inplace=True)
    df.to_csv('indices.csv', index=False)

    print("Arquivo CSV criado com sucesso: 'indices.csv'")

def calcular_valor_corrigido(valor:float, indice:float, indice_atual:float):
    valor_corrigido = (valor * indice) / indice_atual
    return valor_corrigido

def csv_populado(nome_arquivo):
    try:
        df = pd.read_csv(nome_arquivo)
        if df.empty:
            return False
        else:
            return True
        
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo {nome_arquivo} não foi encontrado.")
    
    except pd.errors.EmptyDataError:
        return False

def obter_valor(nome_arquivo:str, ano:int, mes:str):
    df = pd.read_csv(nome_arquivo)
    if ano in df['Ano'].values:
        valor = df.loc[df['Ano'] == ano, mes].values
        if valor.size > 0:
            return valor[0]
        else:
            return None
    else:
        return None

def reajuste(lista_objetos:list[dict], ano_atual, mes_atual):
    valores_corrigidos = []
    indice_atual = obter_valor('indices.csv', ano_atual, mes_atual)
    for venda in lista_objetos:
        mes, ano = get_ano_mes(venda)
        valor = venda['valor']
        indice = obter_valor('indices.csv', ano, mes)
        corrigido = calcular_valor_corrigido(valor, indice, indice_atual)

        valores_corrigidos.append({
            'id': venda['id'], 
            'data_vencimento': venda['data_vencimento'],
            'data_atual': f'{mes_atual}/{ano_atual}',
            'valor_antigo': venda['valor'], 
            'valor_corrigido': float(f'{corrigido:.2f}'),
            'indice_atual': float(indice_atual),
            'indice_data': float(indice)
        })

    return valores_corrigidos