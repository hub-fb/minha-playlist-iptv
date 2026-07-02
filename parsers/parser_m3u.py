import re
import xml.etree.ElementTree as ET
import urllib.request

EPG_URLS = [
    "https://www.bevy.be/bevyfiles/brazil.xml",
    "https://www.bevy.be/bevyfiles/portugal.xml",
    "https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/PlutoTV/all.xml",
    "https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/Plex/all.xml",
    "https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/SamsungTVPlus/all.xml",
    "https://raw.githubusercontent.com/helenfernanda/gratis/main/distrotv.xml",
    "https://www.bevy.be/bevyfiles/mexicopremium.xml",
    "https://iptv-epg.org/files/epg-br.xml"
]

EPG_DATA = {}


def carregar_epg():
    global EPG_DATA

    for url in EPG_URLS:

        try:
            print(f"Carregando EPG: {url}")

            resposta = urllib.request.urlopen(url, timeout=60)

            xml = resposta.read()

            root = ET.fromstring(xml)

            for canal in root.findall("channel"):

                tvg_id = canal.get("id", "").strip()

                nome = canal.findtext("display-name", "").strip()

                icone = canal.find("icon")

                logo = icone.get("src") if icone is not None else ""

                if tvg_id:

                    EPG_DATA[tvg_id.lower()] = {
                        "tvg-id": tvg_id,
                        "tvg-name": nome,
                        "tvg-logo": logo
                    }

                if nome:

                    EPG_DATA[nome.lower()] = {
                        "tvg-id": tvg_id,
                        "tvg-name": nome,
                        "tvg-logo": logo
                    }

        except Exception as erro:

            print(f"Erro ao carregar EPG: {erro}")


def normalizar_grupo(grupo, nome):

    grupo = grupo or ""

    nome = nome or ""

    grupo_lower = grupo.lower()

    nome_lower = nome.lower()

    if "brasil" in grupo_lower or "brazil" in grupo_lower or nome_lower.startswith("br:"):
        return "BRAZIL"

    if "usa" in grupo_lower or "united states" in grupo_lower or "estados unidos" in grupo_lower:
        return "ESTADOS UNIDOS"

    if "portugal" in grupo_lower:
        return "PORTUGAL"

    if "mexico" in grupo_lower:
        return "MEXICO"

    if "pluto" in grupo_lower:
        return "PLUTO TV"

    if "plex" in grupo_lower:
        return "PLEX"

    if "samsung" in grupo_lower:
        return "SAMSUNG TV PLUS"

    if grupo:
        return grupo.upper()

    return "INTERNACIONAL"


def ler_playlist(conteudo):

    canais = []

    linhas = conteudo.splitlines()

    nome = ""
    grupo = ""
    tvg_id = ""
    tvg_name = ""
    tvg_logo = ""

    for linha in linhas:

        linha = linha.strip()

        if linha.startswith("#EXTINF"):

            grupo_match = re.search(r'group-title="([^"]+)"', linha)
            id_match = re.search(r'tvg-id="([^"]+)"', linha)
            name_match = re.search(r'tvg-name="([^"]+)"', linha)
            logo_match = re.search(r'tvg-logo="([^"]+)"', linha)

            grupo = grupo_match.group(1) if grupo_match else ""
            tvg_id = id_match.group(1) if id_match else ""
            tvg_name = name_match.group(1) if name_match else ""
            tvg_logo = logo_match.group(1) if logo_match else ""

            partes = linha.split(",", 1)

            nome = partes[1].strip() if len(partes) > 1 else "Sem Nome"

        elif linha.startswith("http://") or linha.startswith("https://"):

            grupo = normalizar_grupo(grupo, nome)

            epg = {}

            if tvg_id.lower() in EPG_DATA:
                epg = EPG_DATA[tvg_id.lower()]
            elif nome.lower() in EPG_DATA:
                epg = EPG_DATA[nome.lower()]

            canais.append({

                "nome": nome,

                "url": linha,

                "grupo": grupo,

                "tvg-id": epg.get("tvg-id", tvg_id),

                "tvg-name": epg.get("tvg-name", tvg_name or nome),

                "tvg-logo": epg.get("tvg-logo", tvg_logo)

            })

            nome = ""
            grupo = ""
            tvg_id = ""
            tvg_name = ""
            tvg_logo = ""

    return canais


carregar_epg()
