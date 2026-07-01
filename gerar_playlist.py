import json
import urllib.request
from datetime import datetime

from parsers.parser_m3u import ler_playlist
from parsers.parser_json import ler_json

print("=" * 60)
print("Bassetti IPTV Hub")
print("=" * 60)

with open("fontes.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

playlist_final = []

urls_existentes = set()

playlist_final.append("#EXTM3U")

for fonte in sorted(
    dados["fontes"],
    key=lambda x: x.get("prioridade", 0),
    reverse=True
):

    if not fonte.get("ativa", True):
        continue

    print(f"\nBaixando: {fonte['nome']}")

    try:

        resposta = urllib.request.urlopen(
            fonte["url"],
            timeout=30
        )

        conteudo = resposta.read().decode(
            "utf-8",
            errors="ignore"
        )

        nome_arquivo = (
            fonte["nome"]
            .replace(" ", "_")
            .replace("/", "_")
        )

        extensao = "json" if fonte["tipo"] == "json" else "m3u"

        with open(
            f"cache/{nome_arquivo}.{extensao}",
            "w",
            encoding="utf-8"
        ) as destino:

            destino.write(conteudo)

        if fonte["tipo"] == "m3u":

            canais = ler_playlist(conteudo)

        elif fonte["tipo"] == "json":

            canais = ler_json(conteudo)

        else:

            canais = []

        print(f"{len(canais)} canais encontrados.")

        adicionados = 0

        for canal in canais:

            url = canal["url"].strip()

            if url in urls_existentes:
                continue

            urls_existentes.add(url)

            playlist_final.append(canal["info"])
            playlist_final.append(url)

            adicionados += 1

        print(f"{adicionados} canais adicionados.")

        print("OK")

    except Exception as erro:

        print(f"ERRO: {erro}")

with open(
    "ListaIPTV.m3u",
    "w",
    encoding="utf-8"
) as destino:

    destino.write("\n".join(playlist_final))

dados["ultimaAtualizacao"] = datetime.now().strftime(
    "%d/%m/%Y %H:%M:%S"
)

with open(
    "fontes.json",
    "w",
    encoding="utf-8"
) as arquivo:

    json.dump(
        dados,
        arquivo,
        indent=4,
        ensure_ascii=False
    )

print("\n" + "=" * 60)
print(f"TOTAL DE CANAIS: {len(urls_existentes)}")
print("=" * 60)
print("Playlist atualizada com sucesso.")
