---
name: Adianti Skill Factory
description: >
  Fábrica de Skills para automatizar a criação de novos playbooks de IA
  seguindo os padrões do Adianti Framework e FormDin.
---

# 🏭 Adianti Skill Factory (Meta-Skill)

Esta skill guia o agente na criação de **novas skills** de forma padronizada, garantindo que todo novo conhecimento adicionado ao projeto seja consistente, determinístico e fácil de usar tanto por humanos quanto por outras IAs.

## 🛠️ Procedimento Interno para o Agente (IA)

Ao ser ativada (via gatilhos como "criar nova skill"), a IA **deve** seguir rigorosamente estes passos:

### 1. Entrevista de Requisitos
Solicite ao usuário:
- **Nome da Skill**: (Ex: `adianti-boleto`)
- **Objetivo Primário**: (Ex: `Gerar classes de boleto usando a biblioteca X`)
- **Gatilhos (Triggers)**: (Palavras-chave que ativam a skill)

### 2. Estrutura do `SKILL.md`
A IA deve propor um rascunho de `SKILL.md` contendo as seguintes seções obrigatórias:

*   **Frontmatter YAML**: 
    ```yaml
    ---
    name: <Nome Exibição>
    description: <Breve resumo de 1 linha>
    ---
    ```
*   **Título Principal**: (Ex: `# Skill: <Nome Completo>`)
*   **Seção "Padrões e Regras"**: Onde são documentados os "segredos" técnicos (ex: `DB Main`, `Not Null`, `Soft Delete`).
*   **Seção "Template / Exemplo"**: Blocos de código comentados seguindo o estilo do projeto.
*   **Seção "Fluxo de Uso"**: Passos 1, 2, 3 para o usuário ou agente.
*   **Alerta de Segurança/Importante**: Usar `> [!IMPORTANT]` ou `> [!CAUTION]`.

### 3. Hierarquia de Arquivos
A fábrica deve criar a seguinte estrutura na pasta `.agent/skills/<nome-da-skill>/`:
- `SKILL.md`: O arquivo mestre.
- `scripts/`: (Opcional) Pasta para scripts auxiliares (Python, PHP CLI).
- `examples/`: (Opcional) Pasta para arquivos de exemplo completos.

---

## 💡 Dicas de Fabricação

1. **Keep it Concise**: Evite descrições longas; prefira links para arquivos e tabelas.
2. **Context Aware**: Sempre vincule a nova skill ao ecossistema Adianti/FormDin.
3. **Trigger Words**: Certifique-se de que os gatilhos no YAML são específicos o suficiente para não causar falsos positivos.

## 🚀 Como Iniciar uma Fabricação?
Basta me pedir:
- *"Use a adianti-skill-factory para criar a skill [Nome]"*
- *"Quero criar um novo playbook para [Assunto]"*

> [!TIP]
> **Automação de Registro**: Após criar a skill, a fábrica deve sugerir a atualização do `README.md` principal para incluir a nova ferramenta na tabela de Skills Locais.
