import json
import urllib.request
from datetime import datetime

print("=" * 50)
print("Bassetti IPTV Hub")
print("=" * 50)

with open("fontes.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

playlist_final = []

for fonte in dados["fontes"]:

    if not fonte["ativa"]:
        continue

    print(f"Baixando: {fonte['nome']}")

    try:
        resposta = urllib.request.urlopen(fonte["url"], timeout=20)
        conteudo = resposta.read().decode("utf-8", errors="ignore")

        nome = fonte["nome"].replace(" ", "_")
        extensao = "json" if fonte["tipo"] == "json" else "m3u"

        with open(f"cache/{nome}.{extensao}", "w", encoding="utf-8") as destino:
            destino.write(conteudo)

        if fonte["tipo"] == "m3u":
            playlist_final.append(f"# ===== {fonte['nome']} =====")
            playlist_final.append(conteudo)

        print("OK")

    except Exception as erro:
        print(f"ERRO: {erro}")

with open("playlist_consolidada.m3u", "w", encoding="utf-8") as destino:
    destino.write("\n".join(playlist_final))

dados["ultimaAtualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

with open("fontes.json", "w", encoding="utf-8") as arquivo:
    json.dump(dados, arquivo, indent=4, ensure_ascii=False)

print("Playlist consolidada criada.")
