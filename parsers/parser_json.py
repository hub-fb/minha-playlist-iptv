import json

def ler_json(conteudo, origem=None):

    canais = []

    try:

        dados = json.loads(conteudo)

        if not isinstance(dados, list):
            return canais

        for item in dados:

            nome = item.get("name", "Sem Nome")

            grupo = item.get("country", "INT").upper()

            fontes = item.get("sources", {})

            streams = fontes.get("streams", [])

            for url in streams:

                canais.append({

                    "nome": nome,

                    "url": url,

                    "grupo": grupo,

                    "tvg-id": "",

                    "tvg-name": nome,

                    "tvg-logo": ""

                })

    except Exception as erro:

        print(f"Erro JSON: {erro}")

    return canais
