#Criptografia de Júlio César
import requests
import hashlib
import json

alfabeto = 'abcdefghijklmnopqrstuvwxyz'

#INFORMAR O TOKEN FORNECIDO PELO CODENATION
TOKEN = input('Qual seu token?')

#IMPORTAR DADOS FORNECIDO PELO CODENATION
url_get = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={0}'.format(TOKEN)
response = requests.get(url_get)
response_json = response.json()
numero_casas = response_json['numero_casas']
cifrado = response_json['cifrado']
token = response_json['token']

#PROGRAMA DE DESCRIPTOGRAFIA
def decifrar():
    mensagem = ''
    for x in cifrado:
        if x in alfabeto:
            posicao_atual = alfabeto.index(x)
            mensagem += alfabeto[posicao_atual - numero_casas]
        else:
            mensagem += x
    return mensagem.lower()

decifrado = decifrar()

#CRIAR RESUMO CRIPTOGRÁFICO
resumo_criptografico = hashlib.sha1(str(decifrado).encode('utf-8')).hexdigest()

#RESULTADO FINAL COM TODOS OS DADOS
resultado = {
"numero_casas": numero_casas,
"token": token,
"cifrado": cifrado,
"decifrado": decifrado,
"resumo_criptografico": resumo_criptografico
}

#CRIAR ARQUIVO JSON
def criar_arquivo():
    arquivo = open('answer.json', 'w')
    json.dump(resultado, arquivo, indent=4, sort_keys=False)
    arquivo.close()

#POSTAR RESULTADO FINAL
def postar_resultado():
    url_post = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={0}'.format(TOKEN)
    file = {"answer": open("answer.json", "rb")}
    requests.post(url_post, files=file)
    #pra ver se deu tudo certo
    print(response.status_code)
    print(response.content)


if __name__ == '__main__':
    print(resultado)
    criar_arquivo()
    postar_resultado()
