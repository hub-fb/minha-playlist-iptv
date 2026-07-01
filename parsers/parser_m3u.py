def ler_playlist(conteudo):
    canais = []

    linhas = conteudo.splitlines()

    info = None

    for linha in linhas:

        linha = linha.strip()

        if linha.startswith("#EXTINF"):
            info = linha

        elif linha.startswith("http://") or linha.startswith("https://"):

            canais.append({
                "info": info,
                "url": linha
            })

            info = None

    return canais
