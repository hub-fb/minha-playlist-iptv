import json


def normalizar_grupo(grupo, nome, origem=None):

    grupo = grupo or ""

    nome = nome or ""

    grupo_lower = grupo.lower()

    nome_lower = nome.lower()

    if origem and "countries/br.json" in origem:
        return "BRAZIL"

    if "brasil" in grupo_lower or "brazil" in grupo_lower:
        return "BRAZIL"

    if "usa" in grupo_lower or "united states" in grupo_lower:
        return "ESTADOS UNIDOS"

    if "portugal" in grupo_lower:
        return "PORTUGAL"

    if "mexico" in grupo_lower:
        return "MEXICO"

    if nome_lower.startswith("br:"):
        return "BRAZIL"

    if grupo:
        return grupo.upper()

    return "INTERNACIONAL"


def ler_json(conteudo, origem=None):

    canais = []

    try:

        dados = json.loads(conteudo)

        if isinstance(dados, list):

            itens = dados

        elif isinstance(dados, dict):

            itens = dados.get("channels", dados.get("canais", []))

        else:

            itens = []

        for item in itens:

            nome = item.get("name") or item.get("nome") or "Sem Nome"

            grupo = item.get("group") or item.get("grupo") or "Sem Categoria"

            tvg_id = item.get("tvg-id", "")

            tvg_name = item.get("tvg-name", nome)

            tvg_logo = item.get("tvg-logo", "")

            url = ""

            if "url" in item:

                url = item["url"]

            elif "sources" in item:

                fontes = item["sources"]

                if isinstance(fontes, list):

                    for fonte in fontes:

                        if fonte.get("url"):

                            url = fonte["url"]

                            break

                elif isinstance(fontes, dict):

                    streams = fontes.get("streams", [])

                    if streams:

                        url = streams[0]

            elif "youtube" in item:

                yt = item["youtube"]

                if isinstance(yt, list) and yt:

                    url = yt[0]

            if not url:

                continue

            grupo = normalizar_grupo(grupo, nome, origem)

            canais.append({

                "nome": nome,

                "url": url,

                "grupo": grupo,

                "tvg-id": tvg_id,

                "tvg-name": tvg_name,

                "tvg-logo": tvg_logo

            })

    except Exception as erro:

        print(f"Erro ao ler JSON: {erro}")

    return canais
