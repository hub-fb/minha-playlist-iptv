import json

def normalizar_grupo(grupo, nome):
    """Normaliza o grupo para o país correspondente."""
    grupo_lower = grupo.lower()
    nome_lower = nome.lower()

    if "brasil" in grupo_lower or "brazil" in grupo_lower or nome_lower.startswith("br:"):
        return "BRAZIL"
    elif "usa" in grupo_lower or "united states" in grupo_lower or "estados unidos" in grupo_lower or nome_lower.startswith("us:"):
        return "ESTADOS UNIDOS"
    elif "portugal" in grupo_lower or nome_lower.startswith("pt:"):
        return "PORTUGAL"
    elif "mexico" in grupo_lower or nome_lower.startswith("mx:"):
        return "MEXICO"
    elif "pluto" in grupo_lower:
        return "PLUTO TV"
    elif "plex" in grupo_lower:
        return "PLEX"
    elif "samsung" in grupo_lower:
        return "SAMSUNG TV PLUS"
    else:
        return grupo or "INTERNACIONAL"

def ler_json(conteudo):
    """
    Lê uma fonte JSON e retorna lista de dicionários no formato:
    { "nome": ..., "url": ..., "grupo": ..., "tvg-id": ..., "tvg-name": ..., "tvg-logo": ... }
    """
    canais = []
    try:
        dados = json.loads(conteudo)
        for item in dados.get("canais", []):
            nome = item.get("nome", "Sem Nome")
            url = item.get("url", "").strip()
            grupo = item.get("grupo", "Sem Categoria")
            tvg_id = item.get("tvg-id", "")
            tvg_name = item.get("tvg-name", nome)
            tvg_logo = item.get("tvg-logo", "")

            if url:
                grupo = normalizar_grupo(grupo, nome)
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
