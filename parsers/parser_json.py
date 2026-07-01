import json

def ler_json(conteudo):

    canais = []

    try:
        dados = json.loads(conteudo)

        if isinstance(dados, list):
            for canal in dados:
                canais.append(canal)

    except:
        pass

    return canais
