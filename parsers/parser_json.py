import json


def ler_json(conteudo):

    canais = []

    try:

        dados = json.loads(conteudo)

        if not isinstance(dados, list):
            return canais

        for canal in dados:

            nome = canal.get("nome", "Sem nome")

            grupo = canal.get("categoria", "Brasil")

            fontes = canal.get("fontes", {})

            fluxos = fontes.get("fluxos", [])

            contador = 1

            for url in fluxos:

                if not url:
                    continue

                if contador == 1:
                    titulo = nome
                else:
                    titulo = f"{nome} ({contador})"

                canais.append({

                    "info": f'#EXTINF:-1 group-title="{grupo}",{titulo}',

                    "url": url.strip()

                })

                contador += 1

    except Exception as erro:

        print(f"Erro JSON: {erro}")

    return canais
