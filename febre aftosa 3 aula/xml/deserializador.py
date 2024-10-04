import xml.etree.ElementTree as ET

class DeserializadorXml:
    def __init__(self, arquivo_xml):
        self.arquivo_xml = arquivo_xml
        self.elementos = []

    def deserializar(self):
        arvore = ET.parse(self.arquivo_xml)
        raiz = arvore.getroot()
        
        for secao in raiz:
            for item in secao:
                self.elementos.append((item.tag, item.text))
    
    def relatar(self):
        quantidade = len(self.elementos)
        
        primeiro_elemento = self.elementos[0] if self.elementos else None
        ultimo_elemento = self.elementos[-1] if self.elementos else None
        
        print(f"Quantidade de elementos: {quantidade}")
        if primeiro_elemento:
            print(f"Primeiro elemento: Tag = {primeiro_elemento[0]}, Valor = {primeiro_elemento[1]}")
        if ultimo_elemento:
            print(f"Último elemento: Tag = {ultimo_elemento[0]}, Valor = {ultimo_elemento[1]}")

caminho_output = '/home/eduardo/Documentos/aulas/aulas-leonardo/web-semantica/febre aftosa 3 aula/xml/output.xml'

deserializador = DeserializadorXml(caminho_output)
deserializador.deserializar()
deserializador.relatar()
