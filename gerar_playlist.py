import json
import urllib.request
from datetime import datetime

print("=" * 50)
print("Bassetti IPTV Hub")
print("=" * 50)

with open("fontes.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

fontes = dados["fontes"]

print(f"Foram encontradas {len(fontes)} fontes.\n")

for fonte in fontes:

    if not fonte["ativa"]:
        continue

    print(f"Baixando: {fonte['nome']}")

    try:

        resposta = urllib.request.urlopen(fonte["url"], timeout=20)

        conteudo = resposta.read().decode("utf-8", errors="ignore")

        nome = fonte["nome"].replace(" ", "_")

        extensao = "json" if fonte["tipo"] == "json" else "m3u"

        with open(
            f"cache/{nome}.{extensao}",
            "w",
            encoding="utf-8"
        ) as destino:

            destino.write(conteudo)

        print("OK")

    except Exception as erro:

        print(f"ERRO -> {erro}")

print("\nConcluído.")

dados["ultimaAtualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

with open("fontes.json", "w", encoding="utf-8") as arquivo:
    json.dump(
        dados,
        arquivo,
        indent=4,
        ensure_ascii=False
    )
