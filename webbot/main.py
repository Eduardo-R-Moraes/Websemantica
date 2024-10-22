from helpers import *

vendas_em_atraso = [
    {"id": 1, "valor": 5000.00, "data_vencimento": "07/2024"},
    {"id": 2, "valor": 7500.00, "data_vencimento": "05/2023"},
    {"id": 3, "valor": 12000.00, "data_vencimento": "04/2019"},
    {"id": 4, "valor": 10000.00, "data_vencimento": "08/2023"},
    {"id": 5, "valor": 8000.00, "data_vencimento": "06/2018"},
]

if not csv_populado('indices.csv'):
    indices = get_indices()

valores_corrigidos = reajuste(vendas_em_atraso, 2024, '10')

print('Dados totais:')
for venda in valores_corrigidos:
    print(venda)

print()
print('Formatado:')
for venda in valores_corrigidos:
    print(f'ID: {venda["id"]} -> Valor corrigido: R${venda["valor_corrigido"]}')

