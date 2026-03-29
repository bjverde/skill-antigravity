---
name: Ag-Kit Installer
description: Instalação global determinística do Antigravity Kit (Sem Node.js) via Python.
---
# Ag-Kit Installer

Esta skill automatiza a instalação global das definições do Antigravity Kit no Windows, sem a necessidade de Node.js ou NPM.

## O que esta skill faz?
1. Clona o repositório oficial `vudovn/antigravity-kit`.
2. Move as pastas `agents`, `skills`, `workflows` e `rules` para a pasta global `%USERPROFILE%\.gemini\antigravity`.
3. Garante que os Agentes e Comandos de Barra estejam disponíveis em todos os seus projetos.

## Como usar?
Basta solicitar no chat:
*"Use a skill ag-kit-installer para instalar o kit globalmente"*

Ou execute manualmente o script Python:
```bash
python .agent/skills/ag-kit-installer/scripts/install_ag_kit.py
```

## Requisitos
- **Git** instalado e no PATH.
- **Python 3** instalado e no PATH.
