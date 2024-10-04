from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

class HtmlToXmlSerializer:
    def __init__(self, html_file, xml_file):
        self.html_file = html_file
        self.xml_file = xml_file

    def serialize(self):
        try:
            with open(self.html_file, 'r', encoding='utf-8') as file:
                content = file.read()

            soup = BeautifulSoup(content, 'html.parser')
            root = ET.Element('FebreAftosa')

            for section in soup.find_all('section'):
                section_element = ET.SubElement(root, section['class'][0])
                for paragraph in section.find_all('p'):
                    if 'class' in paragraph.attrs:
                        tag_name = paragraph['class'][0]
                        value = paragraph.get_text()
                        ET.SubElement(section_element, tag_name).text = value

            tree = ET.ElementTree(root)
            tree.write(self.xml_file, encoding='utf-8', xml_declaration=True)
            print(f"Arquivo XML gerado com sucesso: {self.xml_file}")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

caminho_arquivo = '/home/eduardo/Documentos/aulas/aulas-leonardo/web-semantica/febre aftosa 3 aula/xml/febre-aftosa.html'

caminho_output = '/home/eduardo/Documentos/aulas/aulas-leonardo/web-semantica/febre aftosa 3 aula/xml/output.xml'

serializer = HtmlToXmlSerializer(caminho_arquivo, caminho_output)
serializer.serialize()
