import json
import urllib.request
from datetime import datetime

from parsers.parser_m3u import ler_playlist
from parsers.parser_json import ler_json

print("=" * 50)
print("Bassetti IPTV Hub")
print("=" * 50)

with open("fontes.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

playlist_final = ["#EXTM3U"]

urls_adicionadas = set()

for fonte in sorted(dados["fontes"], key=lambda x: x["prioridade"], reverse=True):

    if not fonte["ativa"]:
        continue

    print(f"\nImportando: {fonte['nome']}")

    try:

        resposta = urllib.request.urlopen(fonte["url"], timeout=30)
        conteudo = resposta.read().decode("utf-8", errors="ignore")

        nome = fonte["nome"].replace(" ", "_")
        extensao = "json" if fonte["tipo"] == "json" else "m3u"

        with open(f"cache/{nome}.{extensao}", "w", encoding="utf-8") as destino:
            destino.write(conteudo)

        if fonte["tipo"] == "m3u":

            canais = ler_playlist(conteudo)

        else:

            canais = ler_json(conteudo)

        total = 0

        for canal in canais:

            url = canal["url"].strip()

            if url in urls_adicionadas:
                continue

            urls_adicionadas.add(url)

            grupo = canal.get("grupo", fonte["categoria"])
            nome_canal = canal["nome"]

            playlist_final.append(
                f'#EXTINF:-1 group-title="{grupo}",{nome_canal}'
            )

            playlist_final.append(url)

            total += 1

        print(f"{total} canais adicionados.")

    except Exception as erro:

        print(f"Erro: {erro}")

with open("ListaIPTV.m3u", "w", encoding="utf-8") as arquivo:

    arquivo.write("\n".join(playlist_final))

dados["ultimaAtualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

with open("fontes.json", "w", encoding="utf-8") as arquivo:

    json.dump(dados, arquivo, indent=4, ensure_ascii=False)

print("\nPlaylist criada com sucesso.")
