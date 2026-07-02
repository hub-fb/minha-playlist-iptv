import json


def ler_json(conteudo):

    canais = []

    try:

        dados = json.loads(conteudo)

    except Exception:

        return canais

    if not isinstance(dados, list):
        return canais

    for item in dados:

        if not isinstance(item, dict):
            continue

        nome = (
            item.get("name")
            or item.get("title")
            or item.get("channel")
            or "Canal sem nome"
        )

        url = (
            item.get("url")
            or item.get("stream")
            or item.get("src")
            or ""
        )

        if not url.startswith("http"):
            continue

        grupo = (
            item.get("category")
            or item.get("group")
            or item.get("country")
            or "Outros"
        )

        canais.append({
            "nome": nome.strip(),
            "url": url.strip(),
            "grupo": grupo.strip()
        })

    return canais
