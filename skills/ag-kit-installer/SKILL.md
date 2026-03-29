---
name: Ag-Kit Installer
description: Instalação global determinística do Antigravity Kit via Python ou PowerShell.
---
# Ag-Kit Installer

Esta skill automatiza a instalação global das definições do Antigravity Kit no Windows, com foco total em persistência e inteligência global.

## O que esta skill faz?
1.  **Detecta o Ambiente**: Verifica se o Python está presente na máquina.
2.  **Instalação**: Clona o repositório oficial `vudovn/antigravity-kit`.
3.  **Deploy Global**: Move as pastas `agents`, `skills`, `workflows` e `rules` para `%USERPROFILE%\.gemini\antigravity`.

## Procedimento para o Agente (IA)

Ao ser invocada, a IA deve seguir este fluxo lógico:

1.  **ETAPA 1: Verificação de Python**
    - Executar `python --version`.
    - Se o comando for bem sucedido, prosseguir para a **ETAPA 2 (Python)**.
    - Se falhar, prosseguir para a **ETAPA 3 (PowerShell)**.

2.  **ETAPA 2: Instalação via Python (Preferencial)**
    - Executar o script: `python .agent/skills/ag-kit-installer/scripts/install_ag_kit.py`
    - Monitorar a saída por erro ou sucesso.

3.  **ETAPA 3: Instalação via PowerShell (Fallback)**
    - Caso o Python falhe, execute a seguinte sequência de comandos no Windows (PowerShell):
    ```powershell
    if (Test-Path "./temp_ag_kit_clone") { Remove-Item -Path "./temp_ag_kit_clone" -Recurse -Force }
    git clone --depth 1 https://github.com/vudovn/antigravity-kit.git ./temp_ag_kit_clone
    $source = "./temp_ag_kit_clone/.agent"
    $dest = "$HOME\.gemini\antigravity"
    New-Item -ItemType Directory -Force -Path $dest
    foreach ($folder in "agents", "skills", "workflows", "rules") {
        if (Test-Path "$source\$folder") {
            if (Test-Path "$dest\$folder") { Remove-Item -Path "$dest\$folder" -Recurse -Force }
            Copy-Item -Path "$source\$folder" -Destination $dest -Recurse -Force
        }
    }
    Remove-Item -Path "./temp_ag_kit_clone" -Recurse -Force
    ```

## Como usar?
Basta solicitar no chat:
*"Use a skill ag-kit-installer para instalar o kit globalmente"*

## Requisitos
- **Git** instalado e no PATH.
- **Python 3** (Opcional, mas preferido) ou **PowerShell**.
