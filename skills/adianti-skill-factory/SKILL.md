---
name: Adianti Skill Factory
description: >
  Fábrica de automação para criar novas IA skills seguindo rigidamente
  os padrões do Adianti Framework e FormDin.
---

# 🏭 Adianti Skill Factory (V2 - Pro)

Esta meta-skill guia o Agente na criação de novos módulos de inteligência para o projeto, utilizando diretrizes de alta performance em documentação e engenharia de prompts.

## 🎯 Objetivo
Transformar novos conhecimentos técnicos em playbooks determinísticos que a IA possa seguir sem ambiguidade.

---

## 🛠️ Procedimento Interno para o Agente (IA)

Ao iniciar uma "fabricação", você deve seguir rigorosamente estes passos, consultando sempre o **`@documentation-specialist`** para o acabamento final.

### 1. Entrevista de Requisitos
Solicite ao usuário:
- **`Nome da Skill`**: (Ex: `adianti-boletos`)
- **`Propósito`**: O que ela resolve?
- **`Gatilhos`**: Palavras-chave exclusivas para ativação.

### 2. Protótipo Genérico de `SKILL.md` (A seguir)
O novo arquivo deve seguir esta estrutura básica:

```markdown
---
name: <Nome Exibição>
description: <Breve resumo de 1 linha>
---
# Skill: <Nome Completo>

> [!NOTE]
> Breve introdução sobre o contexto da skill no Adianti/FormDin.

## 📐 Padrões Técnicos
| Regra | Detalhamento |
| :--- | :--- |
| Ex: DB | Usar sempre Constantes::DATABASE_MAIN |

## 🚀 Como Executar
Passos claros para o humano ou para a própria IA.

## 🏁 Checklist de Conclusão
- [ ] O código gerado segue os padrões X?
- [ ] Foram incluídos os registros de permissão?
```

### 3. Controle de Qualidade (Scannability)
Antes de finalizar, valide o conteúdo com estes princípios:
- **Tabelas primeiro**: Use tabelas para regras e configurações.
- **Alertas Úteis**: Use `> [!IMPORTANT]` para regras que não podem ser violadas e `> [!TIP]` para sugestões.
- **Paths Clicáveis**: SEMPRE use links no formato caminhos relativos para arquivos mencionados.

### 4. Ciclo de Polimento (Agent Chaining)
1.  **Geração**: Crie o rascunho técnico inicial.
2.  **Revisão Estética**: Peça ao `@documentation-specialist` para melhorar a clareza.
3.  **Validação de Sintaxe**: Peça ao `@doc-coauthoring` para validar o YAML e o Markdown.

---

## 💾 Integração Git (Repositório `skill-antigravity`)
Ao concluir uma nova skill, lembre-se:
1.  Criar a nova pasta em `.agent/skills/<nova-skill>/`.
2.  Adicionar a nova skill à tabela no principal [README.md](../../.agent/README.md).
3.  Sugerir ao usuário o **Commit** no repositório de skills.

> [!IMPORTANT]
> Nunca sobrescreva uma skill existente sem perguntar antes. Sempre crie a nova pasta separadamente.

---
## 🚀 Como Iniciar?
Diga apenas: *"Use a adianti-skill-factory para [Assunto]"*.
