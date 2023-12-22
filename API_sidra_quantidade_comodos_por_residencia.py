from flask import Flask, jsonify
import pandas as pd
import requests

#===Novo objeto do tipo RetornoSidra, objeto o qual armazena os dados retornados pela API Sidra
class RetornoSidra():
    def __init__(self,dados):
        self.dados = list(str(dados))
    
    def get_valores(self):
        dados = self.dados
        valores = []
        contador = 0

        for i in range(len(dados)):
            if contador < (len(dados) - 1):

                if dados[contador-1] == "'" and dados[contador] == 'V' and dados[contador+1] == "'":
                    valor = ''
                    contador += 5
                    while dados[contador] != "'":
                        valor += dados[contador]
                        contador += 1
                    if valor[0].isnumeric():
                        if '.' in valor:
                            valor = float(valor)
                        else:
                            valor = int(valor)
                    valores.append(valor)
            else:
                break
            contador += 1
        return valores

    
    def get_d4n(self):
        dados = self.dados
        d4n = []
        contador = 0

        for i in range(len(dados)):
            if contador < (len(dados) - 1):

                if dados[contador] == "D" and dados[contador+1] == "4" and dados[contador+2] == "N":
                    valor = ''
                    contador += 7
                    while dados[contador] != "'":
                        valor += dados[contador]
                        contador += 1
                    d4n.append(valor)
            else:
                break
            contador += 1
        return d4n

    
    def get_nn(self):
        dados = self.dados
        nn = []
        contador = 0

        for i in range(len(dados)):
            if contador < (len(dados) - 1):

                if dados[contador-1] == "'" and dados[contador] == "N" and dados[contador+1] == "N" and dados[contador+2] == "'":
                    valor = ''
                    contador += 6
                    while dados[contador] != "'":
                        valor += dados[contador]
                        contador += 1
                    nn.append(valor)
            else:
                break
            contador += 1
        return nn
    
    
    def get_mn(self):
        dados = self.dados
        mn = []
        contador = 0

        for i in range(len(dados)):
            if contador < (len(dados) - 1):

                if dados[contador-1] == "'" and dados[contador] == "M" and dados[contador+1] == "N" and dados[contador+2] == "'":
                    valor = ''
                    contador += 6
                    while dados[contador] != "'":
                        valor += dados[contador]
                        contador += 1
                    mn.append(valor)
            else:
                break
            contador += 1
        return mn

    
    def get_d1n(self):
        dados = self.dados
        d1n = []
        contador = 0

        for i in range(len(dados)):
            if contador < (len(dados) - 1):

                if dados[contador] == "D" and dados[contador+1] == "1" and dados[contador+2] == "N":
                    valor = ''
                    contador += 7
                    while dados[contador] != "'":
                        valor += dados[contador]
                        contador += 1
                    d1n.append(valor)
            else:
                break
            contador += 1
        return d1n

    
    def get_d3n(self):
        dados = self.dados
        d3n = []
        contador = 0

        for i in range(len(dados)):
            if contador < (len(dados) - 1):

                if dados[contador] == "D" and dados[contador+1] == "3" and dados[contador+2] == "N":
                    valor = ''
                    contador += 7
                    while dados[contador] != "'":
                        valor += dados[contador]
                        contador += 1
                    d3n.append(valor)
            else:
                break
            contador += 1
        return d3n
    
    def get_d2n(self):
        dados = self.dados
        d2n = []
        contador = 0

        for i in range(len(dados)):
            if contador < (len(dados) - 1):

                if dados[contador] == "D" and dados[contador+1] == "2" and dados[contador+2] == "N":
                    valor = ''
                    contador += 7
                    while dados[contador] != "'":
                        valor += dados[contador]
                        contador += 1
                    d2n.append(valor)
            else:
                break
            contador += 1
        return d2n

#===Função de construção de dataframe
def construir_dataframe(list_colunas):
    df = pd.DataFrame(columns=range(len(list_colunas)))
    
    nomes_colunas = []
    for i in range(len(list_colunas)):
        nomes_colunas.append(list_colunas[i].pop(0))
        
    for i in range(len(list_colunas)):
        df[i] = list_colunas[i]
    
    df.columns = nomes_colunas
    
    return df

#====API
app = Flask(__name__)

#===Adquirindo amostra dos dados
@app.route('/getAmostra/ibge/sidra/quantidade_comodos_por_residencia', methods=['GET'])
def getAmostra():

    url_api = 'https://apisidra.ibge.gov.br/values/T/206/P/1970,1980,1991,2000,2010/V/1000096/C1/1,2/C65/1059,1060,1061,1062,1063,1064,1065,1066,1067,2511/N1/1'
    response = requests.get(url_api)
    dados = response.json()

    dados_sidra = RetornoSidra(dados)
    list_colunas = [dados_sidra.get_nn(), dados_sidra.get_d1n(), dados_sidra.get_d3n(), dados_sidra.get_d4n(),dados_sidra.get_valores(),  dados_sidra.get_mn()]
    dataframe = construir_dataframe(list_colunas)

    dados_json = dataframe.to_json(orient='records')

    return jsonify(dados_json)

url_api = 'https://apisidra.ibge.gov.br/values/T/206/P/2010/V/1000096/C1/1,2/C65/1059,1060,1061,1062,1063,1064,1065,1066,1067,2511/N1/1'
response = requests.get(url_api)
dados = response.json()

dados_sidra = RetornoSidra(dados)
list_colunas = [dados_sidra.get_nn(), dados_sidra.get_d1n(), dados_sidra.get_d3n(), dados_sidra.get_d4n(),dados_sidra.get_valores(),  dados_sidra.get_mn()]
dataframe = construir_dataframe(list_colunas)
print(dataframe.to_json(orient='records'))

app.run(port=5000,host='localhost',debug=True)