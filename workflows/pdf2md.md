---
description: Como extrair texto de um PDF para Markdown
---

# Extração de PDF para Markdown

Use este workflow para converter um arquivo PDF existente em um documento Markdown que possa ser lido e analisado pelo agente ou por humanos.

## Passos

1. Identifique o caminho completo do arquivo PDF que deseja extrair.
2. Decida o intervalo de páginas (Ex: páginas 34 a 97).
3. Execute o script de extração através do terminal:

// turbo
```powershell
python .agent/skills/pdf_to_markdown/scripts/pdf2md.py --input "document/livro_adianti.pdf" --output "document/extracao.md" --start 34 --end 97
```

> [!TIP]
> Você pode omitir o parâmetro `--end` para extrair da página inicial até o fim do documento.
> Você pode omitir o parâmetro `--start` para começar da página 1.

4. Informe o agente sobre o arquivo Markdown gerado para que ele possa analisá-lo.
