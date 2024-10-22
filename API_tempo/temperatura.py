import requests

def geraData(data: str):
    vetor = data.split('/')
    nova_data = f'{vetor[2]}-{vetor[1]}-{vetor[0]}'
    return nova_data

data_inicial = '28/10/2024'  # input('Digite data de início dd/mm/aaaa: ')
data_final = '29/10/2024'  # input('Digite data final dd/mm/aaaa: ')
latitude = -22.06  # float(input('Digite latitude: '))
longitude = -50.20  # float(input('Digite longitude: '))

data_inicial = geraData(data_inicial)
data_final = geraData(data_final)

# URL sem velocidade do vento e índice UV
url = (f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}'
       f'&daily=temperature_2m_max,temperature_2m_min,precipitation_sum'
       f'&start_date={data_inicial}&end_date={data_final}&timezone=America/Sao_Paulo')

requisição = requests.get(url)

# Exibir URL para debug
print(f"URL requisitada: {url}\n")

# Verificar a resposta
dados = requisição.json()  # Converte a resposta em JSON

# Imprimir a resposta completa para diagnóstico
print("Resposta da API:")
print(dados)

# Verificando se a chave 'daily' existe na resposta
if 'daily' in dados:
    # Formatando a resposta para uma exibição mais amigável
    print(f"\nPrevisão do tempo de {data_inicial} até {data_final}:\n")
    for i, data in enumerate(dados['daily']['time']):
        temp_max = dados['daily']['temperature_2m_max'][i]
        temp_min = dados['daily']['temperature_2m_min'][i]
        precipitation = dados['daily']['precipitation_sum'][i]
        
        print(f"Data: {data}")
        print(f"  - Temperatura Máxima: {temp_max}°C")
        print(f"  - Temperatura Mínima: {temp_min}°C")
        print(f"  - Precipitação: {precipitation} mm")
        print()
else:
    print("Erro: A chave 'daily' não foi encontrada na resposta.")
