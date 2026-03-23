---
name: PDF to Markdown
description: Extrator de texto de PDFs para formato Markdown usando pypdf.
---

# PDF to Markdown Extraction Skill

Esta skill permite extrair conteúdo de arquivos PDF e convertê-los para Markdown de forma estruturada.

## Dependências
- `pypdf`: Necessário para a extração (instale via `pip install pypdf`).

## Uso pelo Agente
Sempre que o usuário fornecer um PDF ou pedir para ler um manual de referência que esteja em PDF, use o script localizado em `scripts/pdf2md.py`.

### Comando de Execução
```bash
python .agent/skills/pdf_to_markdown/scripts/pdf2md.py --input <CAMINHO_PDF> --output <CAMINHO_MD> --start <PAGINA_INICIAL> --end <PAGINA_FINAL>
```

### Argumentos
- `--input`: Caminho absoluto ou relativo para o arquivo `.pdf`.
- `--output`: Caminho para salvar o arquivo `.md` resultante.
- `--start`: Página inicial (1-indexed). Padrão: 1.
- `--end`: Página final (1-indexed). Padrão: última página.

## Casos de Uso
1. **Leitura de Documentação**: Extrair capítulos de livros técnicos (ex: Adianti Framework).
2. **Análise de Requisitos**: Converter PDFs de especificação para markdown para facilitar a busca e análise.
3. **Migração de Dados**: Recuperar textos de documentos PDF para inserção em novos sistemas.

## Notas de Implementação
O script realiza uma limpeza básica e formata os cabeçalhos com o nome do arquivo e o intervalo de páginas extraído.
