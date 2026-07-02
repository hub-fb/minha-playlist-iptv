import json

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
