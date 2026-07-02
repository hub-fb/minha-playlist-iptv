import json

def ler_json(conteudo, origem=None):
    canais = []

    try:
        dados = json.loads(conteudo)

        # O Famelack Brasil retorna uma lista de canais
        if not isinstance(dados, list):
            return canais

        for item in dados:

            nome = item.get("name", "Sem Nome")
            grupo = item.get("country", "INT").upper()

            fontes = item.get("sources", {})
            streams = fontes.get("streams", [])

            # Famelack Brasil
            if origem and "countries/br.json" in origem:
                grupo = "BRAZIL"
                tvg_logo = "https://www.gov.br/agricultura/pt-br/assuntos/relacoes-internacionais/agro-mais-investimentos/imagens/bandeira-do-brasil.png"
            else:
                tvg_logo = ""

            # Streams
            for url in streams:
                canais.append({
                    "nome": nome,
                    "url": url,
                    "grupo": grupo,
                    "tvg-id": "",
                    "tvg-name": nome,
                    "tvg-logo": tvg_logo
                })

            # YouTube
            if not streams and "youtube" in item:
                yt = item["youtube"]

                if isinstance(yt, list) and yt:
                    canais.append({
                        "nome": nome,
                        "url": yt[0],
                        "grupo": grupo,
                        "tvg-id": "",
                        "tvg-name": nome,
                        "tvg-logo": tvg_logo
                    })

    except Exception as erro:
        print(f"Erro JSON: {erro}")

    return canais
