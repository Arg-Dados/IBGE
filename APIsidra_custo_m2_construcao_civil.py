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
        nomes_colunas.append(list_colunas[i].pop(0).replace(' ', '-'))
        
    for i in range(len(list_colunas)):
        df[i] = list_colunas[i]
    
    df.columns = nomes_colunas
    
    return df

#====API
app = Flask(__name__)

#===Adquirindo amostra dos dados
@app.route('/getAmostra/ibge/sidra/custo_m2_construcao_civil', methods=['GET'])
def getAmostra():

    url_api = 'https://apisidra.ibge.gov.br/values/T/2296/P/201209,201210,201211,201212,201301,201302,201303,201304,201305,201306,201307,201308,201309,201310,201311,201312,201401,201402,201403,201404,201405,201406,201407,201408,201409,201410,201411,201412,201501,201502,201503,201504,201505,201506,201507,201508,201509,201510,201511,201512,201601,201602,201603,201604,201605,201606,201607,201608,201609,201610,201611,201612,201701,201702,201703,201704,201705,201706,201707,201708,201709,201710,201711,201712,201801,201802,201803,201804,201805,201806,201807,201808,201809,201810,201811,201812,201901,201902,201903,201904,201905,201906,201907,201908,201909,201910,201911,201912,202001,202002,202003,202004,202005,202006,202007,202008,202009,202010,202011,202012,202101,202102,202103,202104,202105,202106,202107,202108,202109,202110,202111,202112,202201,202202,202203,202204,202205,202206,202207,202208,202209,202210,202211,202212,202301,202302,202303,202304,202305,202306,202307,202308,202309,202310,202311/V/48/N1/1'
    response = requests.get(url_api)
    dados = response.json()

    dados_sidra = RetornoSidra(dados)
    list_colunas = [dados_sidra.get_nn(), dados_sidra.get_d1n(), dados_sidra.get_d2n(), dados_sidra.get_valores(),  dados_sidra.get_mn()]
    dataframe = construir_dataframe(list_colunas)

    dados_json = dataframe.to_json(orient='records')

    return jsonify(dados_json)

#===Realizando print de uma amostra dos dados
url_api = 'https://apisidra.ibge.gov.br/values/T/2296/P/202210,202211,202212,202301,202302,202303,202304,202305,202306,202307,202308,202309,202310,202311/V/48/N1/1'
response = requests.get(url_api)
dados = response.json()

dados_sidra = RetornoSidra(dados)
list_colunas = [dados_sidra.get_nn(), dados_sidra.get_d1n(), dados_sidra.get_d2n(), dados_sidra.get_valores(),  dados_sidra.get_mn()]
dataframe = construir_dataframe(list_colunas)
print(dataframe.to_json(orient='records'))

app.run(port=5000,host='localhost',debug=True)