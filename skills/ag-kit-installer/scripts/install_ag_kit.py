import os
import shutil
import subprocess
import sys
from pathlib import Path

def install_ag_kit():
    repo_url = "https://github.com/vudovn/antigravity-kit.git"
    home_dir = Path.home()
    dest_base = home_dir / ".gemini" / "antigravity"
    temp_clone_dir = Path("./temp_ag_kit_clone")

    print(f"[*] Iniciando instalação do Antigravity Kit...")
    print(f"[*] Destino Global: {dest_base}")

    # 1. Garantir que o diretório base existe
    dest_base.mkdir(parents=True, exist_ok=True)

    # 2. Clonar o repositório
    if temp_clone_dir.exists():
        shutil.rmtree(temp_clone_dir)

    try:
        print(f"[*] Clonando repositório de {repo_url}...")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, str(temp_clone_dir)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Erro ao clonar o repositório: {e}")
        return

    # 3. Pastas para copiar
    folders_to_copy = ["agents", "skills", "workflows", "rules"]

    for folder in folders_to_copy:
        src_folder = temp_clone_dir / folder
        dest_folder = dest_base / folder

        if src_folder.exists():
            print(f"[*] Copiando {folder} para {dest_folder}...")
            # Se a pasta já existir no destino, removemos para garantir limpeza (ou mesclamos se preferível)
            if dest_folder.exists():
                shutil.rmtree(dest_folder)
            shutil.copytree(src_folder, dest_folder)
        else:
            print(f"[!] Aviso: Pasta '{folder}' não encontrada no repositório.")

    # 4. Limpeza
    print(f"[*] Limpando arquivos temporários...")
    shutil.rmtree(temp_clone_dir)

    print("\n[✔] Instalação concluída com sucesso!")
    print(f"Agentes e Skills agora estão ativos em: {dest_base}")
    print("Você pode usar comandos como '/brainstorm' ou agentes como '@frontend-specialist' globalmente.")

if __name__ == "__main__":
    install_ag_kit()
