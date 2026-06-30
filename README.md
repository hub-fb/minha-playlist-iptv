# Bassetti IPTV Hub

Projeto para consolidação automática de playlists IPTV públicas.

## Objetivos

- Importar playlists M3U e M3U8
- Importar fontes JSON
- Remover canais duplicados
- Organizar por categoria
- Gerar uma playlist única
- Atualizar automaticamente via GitHub Actions

## Estrutura

- fontes.json → cadastro das fontes
- ListaIPTV.m3u → playlist consolidada
- cache/ → arquivos temporários
- logs/ → estatísticas e registros
- parsers/ → leitores de M3U e JSON
