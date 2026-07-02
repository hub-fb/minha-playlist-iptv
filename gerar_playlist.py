import json
import urllib.request
from datetime import datetime
from parsers.parser_m3u import ler_playlist
from parsers.parser_json import ler_json

def carregar_fontes():
    with open("fontes.json", "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def salvar_cache(nome, extensao, conteudo):
    caminho = f"cache/{nome}.{extensao}"
    with open(caminho, "w", encoding="utf-8") as destino:
        destino.write(conteudo)

def processar_fonte(fonte, urls_adicionadas):
    canais_adicionados = []
    try:
        resposta = urllib.request.urlopen(fonte["url"], timeout=30)
        conteudo = resposta.read().decode("utf-8", errors="ignore")

        nome = fonte["nome"].replace(" ", "_")
        extensao = "json" if fonte["tipo"] == "json" else "m3u"
        salvar_cache(nome, extensao, conteudo)

        if fonte["tipo"] == "m3u":
            canais = ler_playlist(conteudo)
        else:
            canais = ler_json(conteudo)

        for canal in canais:
            url = canal.get("url", "").strip()
            if not url or url in urls_adicionadas:
                continue

            urls_adicionadas.add(url)
            grupo = canal.get("grupo", fonte.get("categoria", "Sem Categoria"))
            nome_canal = canal.get("nome", "Sem Nome")

            canais_adicionados.append(
                f'#EXTINF:-1 group-title="{grupo}",{nome_canal}\n{url}'
            )

        print(f"{len(canais_adicionados)} canais adicionados de {fonte['nome']}.")
    except Exception as erro:
        print(f"Erro ao importar {fonte['nome']}: {erro}")

    return canais_adicionados

def gerar_playlist():
    print("=" * 50)
    print("Bassetti IPTV Hub")
    print("=" * 50)

    dados = carregar_fontes()
    playlist_final = ["#EXTM3U"]
    urls_adicionadas = set()

    for fonte in sorted(dados["fontes"], key=lambda x: x["prioridade"], reverse=True):
        if not fonte.get("ativa", True):
            continue
        print(f"\nImportando: {fonte['nome']}")
        canais = processar_fonte(fonte, urls_adicionadas)
        playlist_final.extend(canais)

    with open("ListaIPTV.m3u", "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(playlist_final))

    dados["ultimaAtualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("fontes.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    print("\nPlaylist criada com sucesso.")

if __name__ == "__main__":
    gerar_playlist()
