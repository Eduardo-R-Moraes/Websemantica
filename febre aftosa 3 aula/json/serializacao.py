from bs4 import BeautifulSoup
import json

class HtmlToJsonSerializer:
    def __init__(self, html_file, json_file):
        self.html_file = html_file
        self.json_file = json_file

    def serialize(self):
        with open(self.html_file, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')
        data = {}

        for section in soup.find_all('section'):
            section_name = section['class'][0]
            section_data = {}

            for paragraph in section.find_all('p'):
                if 'class' in paragraph.attrs:
                    tag_name = paragraph['class'][0]
                    value = paragraph.get_text().strip()  # Remove espaços e quebras de linha
                    section_data[tag_name] = value

            data[section_name] = section_data

        with open(self.json_file, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Arquivo JSON gerado com sucesso: {self.json_file}")

    def deserialize(self):
        with open(self.json_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        print(f"Quantidade de elementos: {len(data)}")
        keys = list(data.keys())
        if keys:
            print(f"Primeiro elemento: {keys[0]}")
            print(f"Último elemento: {keys[-1]}")
        else:
            print("Nenhum elemento encontrado.")            

caminho_arquivo = '/home/eduardo/Documentos/aulas/aulas-leonardo/web-semantica/febre aftosa 3 aula/json/febre-aftosa.html'

caminho_output = '/home/eduardo/Documentos/aulas/aulas-leonardo/web-semantica/febre aftosa 3 aula/json/output.json'

serializer = HtmlToJsonSerializer(caminho_arquivo, caminho_output)
serializer.serialize()
serializer.deserialize()
