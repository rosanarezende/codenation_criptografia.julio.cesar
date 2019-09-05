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

def decifrar():
    """Realiza a descriptografia do texto informado
    INPUT:
    Recebe a mensagem criptografada e, com base na posição de cada letra no alfabeto,
    encontra a letra correta para montar a mensagem descriptografada.
    OUTPUT:
    Retorna a mensagem descriptografada, em letras minúsculas
    """
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

def criar_arquivo():
    """ Cria arquivo no formato json com os dados do resultado """
    arquivo = open('answer.json', 'w')
    json.dump(resultado, arquivo, indent=4, sort_keys=False)
    arquivo.close()

def postar_resultado():
    """ Envia o arquivo criado para o endereço informado pela Codenation """
    url_post = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={0}'.format(TOKEN)
    file = {"answer": open("answer.json", "rb")}
    requests.post(url_post, files=file)
    print(response.status_code) #pra ver se deu tudo certo
    print(response.content) #pra verificar o conteúdo postado


if __name__ == '__main__':
    print(resultado)
    criar_arquivo()
    postar_resultado()
