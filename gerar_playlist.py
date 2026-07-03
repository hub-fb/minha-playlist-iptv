import json
import urllib.request
from datetime import datetime

from parsers.parser_m3u import ler_playlist
from parsers.parser_json import ler_json

print("=" * 60)
print("Bassetti IPTV Hub")
print("=" * 60)

# Carrega fontes
with open("fontes.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

playlist = ["#EXTM3U"]

urls_vistas = set()
total = 0

for fonte in dados["fontes"]:

    if not fonte.get("ativa", True):
        continue

    print(f"\nImportando: {fonte['nome']}")

    try:

        resposta = urllib.request.urlopen(fonte["url"], timeout=60)
        conteudo = resposta.read().decode("utf-8", errors="ignore")

        nome_cache = fonte["nome"].replace(" ", "_")
        extensao = "json" if fonte["tipo"] == "json" else "m3u"

        with open(f"cache/{nome_cache}.{extensao}", "w", encoding="utf-8") as destino:
            destino.write(conteudo)

        # ---------- M3U ----------
        if fonte["tipo"] == "m3u":
            canais = ler_playlist(conteudo)

        # ---------- JSON ----------
        elif fonte["tipo"] == "json":
            canais = ler_json(conteudo, fonte["url"])

        else:
            canais = []

        print(f"{len(canais)} canais encontrados.")

        adicionados = 0

        for canal in canais:

            url = canal.get("url", "").strip()

            if not url:
                continue

            if url in urls_vistas:
                continue

            urls_vistas.add(url)

            grupo = canal.get("grupo", "OUTROS").upper()

            if grupo in ("BR", "BRAZIL", "PLUTO TV"):
                grupo = "BRAZIL"

            linha = (
                '#EXTINF:-1 '
                f'tvg-id="{canal.get("tvg-id","")}" '
                f'tvg-name="{canal.get("tvg-name","")}" '
                f'tvg-logo="{canal.get("tvg-logo","")}" '
                f'group-title="{grupo}",'
                f'{canal.get("nome","Sem Nome")}'
            )

            playlist.append(linha)
            playlist.append(url)

            adicionados += 1

        total += adicionados

        print(f"{adicionados} canais adicionados.")

    except Exception as erro:

        print(f"Erro em {fonte['nome']}: {erro}")

# Salva playlist
with open("ListaIPTV.m3u", "w", encoding="utf-8") as arquivo:
    arquivo.write("\n".join(playlist))

# Atualiza data
dados["ultimaAtualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

with open("fontes.json", "w", encoding="utf-8") as arquivo:
    json.dump(dados, arquivo, indent=4, ensure_ascii=False)

print("\n========================================")
print(f"TOTAL DE CANAIS: {total}")
print("Playlist criada com sucesso.")
print("========================================")
