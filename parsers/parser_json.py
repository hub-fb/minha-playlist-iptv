import json

def normalizar_grupo(grupo, nome, origem=None):
    grupo_lower = grupo.lower()
    nome_lower = nome.lower()

    if origem and "countries/br.json" in origem:
        return "BRAZIL"

    if "brasil" in grupo_lower or "brazil" in grupo_lower or nome_lower.startswith("br:"):
        return "BRAZIL"
    elif "usa" in grupo_lower or "united states" in grupo_lower or "estados unidos" in grupo_lower or nome_lower.startswith("us:"):
        return "ESTADOS UNIDOS"
    elif "portugal" in grupo_lower or nome_lower.startswith("pt:"):
        return "PORTUGAL"
    elif "mexico" in grupo_lower or nome_lower.startswith("mx:"):
        return "MEXICO"
    else:
        return grupo or "INTERNACIONAL"

def ler_json(conteudo, origem=None):
    canais = []
    try:
        dados = json.loads(conteudo)

        # O Famelack Brasil tem estrutura diferente
        if isinstance(dados, list):
            itens = dados
        else:
            itens = dados.get("canais", [])

        for item in itens:
            nome = item.get("name") or item.get("nome") or "Sem Nome"
            grupo = item.get("grupo", "Sem Categoria")
            tvg_id = item.get("tvg-id", "")
            tvg_name = item.get("tvg-name", nome)
            tvg_logo = item.get("tvg-logo", "")

            # Extrair URL de diferentes campos
            url = ""
            if "url" in item:
                url = item["url"]
            elif "sources" in item and "streams" in item["sources"]:
                streams = item["sources"]["streams"]
                if isinstance(streams, list) and streams:
                    url = streams[0]
            elif "youtube" in item:
                yt = item["youtube"]
                if isinstance(yt, list) and yt:
                    url = yt[0]

            if url:
                grupo = normalizar_grupo(grupo, nome, origem)

                # Regra especial para Famelack Brasil
                if origem and "countries/br.json" in origem:
                    tvg_logo = "https://upload.wikimedia.org/wikipedia/commons/0/05/Flag_of_Brazil.svg"

                canais.append({
                    "nome": nome,
                    "url": url,
                    "grupo": grupo,
                    "tvg-id": tvg_id,
                    "tvg-name": tvg_name,
                    "tvg-logo": tvg_logo
                })
    except Exception as e:
        print(f"Erro ao ler JSON: {e}")

    return canais
