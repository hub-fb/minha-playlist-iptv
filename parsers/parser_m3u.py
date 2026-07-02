import re
import xml.etree.ElementTree as ET
import urllib.request

# URLs de EPG fornecidas
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
    """Baixa e carrega todos os arquivos EPG em memória."""
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
                logo = canal.find("icon").get("src") if canal.find("icon") is not None else ""
                if tvg_id:
                    EPG_DATA[tvg_id.lower()] = {
                        "tvg-id": tvg_id,
                        "tvg-name": nome,
                        "tvg-logo": logo
                    }
        except Exception as e:
            print(f"Erro ao carregar EPG {url}: {e}")

def ler_playlist(conteudo):
    """
    Lê uma playlist M3U e retorna lista de dicionários:
    { "nome": ..., "url": ..., "grupo": ..., "tvg-id": ..., "tvg-name": ..., "tvg-logo": ... }
    """
    canais = []
    linhas = conteudo.splitlines()
    nome, grupo, url, tvg_id, tvg_name, tvg_logo = "", "", "", "", "", ""

    for linha in linhas:
        linha = linha.strip()
        if linha.startswith("#EXTINF"):
            grupo_match = re.search(r'group-title="([^"]+)"', linha)
            tvg_id_match = re.search(r'tvg-id="([^"]+)"', linha)
            tvg_name_match = re.search(r'tvg-name="([^"]+)"', linha)
            tvg_logo_match = re.search(r'tvg-logo="([^"]+)"', linha)

            grupo = grupo_match.group(1) if grupo_match else "Sem Categoria"
            tvg_id = tvg_id_match.group(1) if tvg_id_match else ""
            tvg_name = tvg_name_match.group(1) if tvg_name_match else ""
            tvg_logo = tvg_logo_match.group(1) if tvg_logo_match else ""

            partes = linha.split(",", 1)
            nome = partes[1].strip() if len(partes) > 1 else "Sem Nome"

        elif linha and not linha.startswith("#"):
            url = linha.strip()

            # Se já vier com metadados completos, apenas replicar
            if tvg_id or tvg_name or tvg_logo:
                canais.append({
                    "nome": nome,
                    "url": url,
                    "grupo": grupo,
                    "tvg-id": tvg_id,
                    "tvg-name": tvg_name or nome,
                    "tvg-logo": tvg_logo
                })
            else:
                # Caso contrário, tentar enriquecer com EPG externo
                epg_info = {}
                if nome and nome.lower() in EPG_DATA:
                    epg_info = EPG_DATA[nome.lower()]
                elif tvg_id and tvg_id.lower() in EPG_DATA:
                    epg_info = EPG_DATA[tvg_id.lower()]

                canais.append({
                    "nome": nome,
                    "url": url,
                    "grupo": grupo,
                    "tvg-id": epg_info.get("tvg-id", tvg_id),
                    "tvg-name": epg_info.get("tvg-name", tvg_name or nome),
                    "tvg-logo": epg_info.get("tvg-logo", tvg_logo)
                })

            nome, grupo, url, tvg_id, tvg_name, tvg_logo = "", "", "", "", "", ""

    return canais

# Carregar EPG ao importar
carregar_epg()
