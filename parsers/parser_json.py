import json


def ler_json(conteudo):

    canais = []

    try:

        dados = json.loads(conteudo)

        if not isinstance(dados, list):
            return canais

        for canal in dados:

            nome = canal.get("nome", "Sem nome")

            fontes = canal.get("fontes", {})

            fluxos = fontes.get("fluxos", [])

            if not fluxos:
                continue

            url = fluxos[0]

            info = f'#EXTINF:-1 group-title="Brasil",{nome}'

            canais.append({
                "info": info,
                "url": url
            })

    except Exception as erro:

        print(f"Erro JSON: {erro}")

    return canais
