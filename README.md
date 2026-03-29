# Antigravity Skills & Kit - Guia do Projeto Solubiz

Este repositório contém as **Skills e Configurações** especializadas para o ecossistema Antigravity (IA), focadas principalmente no **Adianti Framework**, **FormDin v4** e **FormDin v5**.

Este projeto deve ser clonado dentro da pasta raiz do seu projeto Adianti ou FormDin para que a IA (Antigravity ou Claude Code) reconheça as instruções. Em conjunto será utilizao o Antigravity Kit e algumas skill do Awesome Skills.

# Instalação resumida
Abaixo um resumo de como instalar o Antigravity e as skills:

1. Tenha o Antigravity instalado
1. Clone o seu projeto Adianti/FormDin
1. Instale esse projeto skill-antigravity na pasta raiz do seu projeto Adianti/FormDin
1. Instalar o Antigravity Kit Globalmente
1. Instalar o Awesome Skills localmente, somentes as recomendadas ou que for pertinente para o seu projeto. ***🚫NÃO instale todas as skills do Awesome Skills, pois são milhares e vai deixar o Antigravity lento. 🐌***

# Instalação detalhada 


## 0. Seu projeto
1. Clone o seu projeto Adianti/FormDin
2. Abra o seu projeto no Antigravity
3. verifique que no .gitignore do seu projeto tem a linha .agent, se não tiver, adicione e commite a alteração
4. abra o terminal dentro do Antigravity e execute a próxima seção para instalar as skills


## 1. Instalação das Skills para Adianti/FormDin de forma local

Para garantir que a IA conheça as regras do Adianti/FormDin, as skills devem estar na pasta `.agent`.

**Como Clonar Localmente:**
Acesse a pasta raiz do seu projeto e execute:
```bash
git clone https://github.com/bjverde/skill-antigravity.git .agent
```

---

## 2. Instalação do Antigravity Kit (Global)

O **Antigravity Kit** fornece agentes especialistas (Frontend, Backend, etc.) e workflows estruturados para a IA.

**Instalação Global (NPM):**
Esse processo de instalar exige que você tenha o Node.js instalado. Não gosto desse metodo pois te obriga ter no NodeJs só para baixo arquivos arquivo. Se não tem ou não quer instalar, pule para a instalação manual (recomendo).

```bash
npm install -g @vudovn/ag-kit
```

**Instalação Globa Sem Node.js (Recomendado):**
Foi criada a skill `ag-kit-installer` para instalar o Antigravity kit globalmente no windows usando o script Python. Se não tiver python instalado a skill vai executar os comandos via PowerShell.

1. Abra o toogle de agents do Antigravity
1. De comando "Instalar Antigravity Kit globalmente" ou forma alternativa execute o comando python abaixo no terminal dentro da pasta do projeto no Antigravity:
   ```bash
   python .agent/skills/ag-kit-installer/scripts/install_ag_kit.py
   ```
   *O script irá baixar o repositório oficial e organizar as pastas `agents/`, `skills/`, `workflows/` e `rules/` automaticamente na sua pasta global `%USERPROFILE%\.gemini\antigravity\`.*
1. Vericando se a instalação foi bem sucedida, feche o Antigravity e abra novamente. Abra o toogle de agents do Antigravity e chame @documentation-specialist e veja se ele responde. Se sim, a instalação foi bem sucedida.

---

## 3. Integração com Awesome Skills

O repositório **Awesome Skills** contém milhares de utilitários genéricos. Você pode instalá-los junto com as skills do Adianti.

***🚫NÃO instale todas as skills do Awesome Skills, pois são milhares e vai deixar o Antigravity lento. 🐌***


**Como Instalar Skills Utilitárias (Ex: Security, Debug):**
```bash
npx antigravity-awesome-skills --path ./.agent/skills
```

---

## 4. Configuração do Git e Exclusão

Para evitar o versionamento de milhares de arquivos genéricos no seu repositório principal e no repositório de skills, siga estas regras:

1.  **Na Raiz do Projeto (`.gitignore`):** Deve conter a linha `.agent/` (isso já está configurado no projeto Solubiz).
2.  **Na Pasta `.agent/` (`.agent/.gitignore`):** Ignoramos as skills externas/genéricas instaladas via Awesome Skills para manter o foco apenas nas skills Adianti.

---

## 5. Dicas de Skills e Agentes

### 1. Stack Adianti (PHP/Web/DB)
Utilize estas skills genéricas (do Awesome Skills) para complementar as do projeto:
- `@debugging-strategies` (Estratégias de depuração PHP)
- `@api-design-principles` (Design de APIs RestService)
- `sql-injection-testing` (Segurança em consultas SQL)
- `@security-auditor` (Auditoria de segurança de código)

### 2. Meta-Skill: "Criar Skills com Facilidade"
Para criar novas automatizações rapidamente, utilize o playbook de documentação:
- **`@doc-coauthoring`**: Ajuda a converter notas de código em um arquivo `SKILL.md` estruturado.
- **Agente `Documentation Specialist`**: Use-o para gerar a estrutura YAML e as instruções de novas skills.

### 3. Recomendação de Configuração (Skill Factory)
Crie sua própria "fábrica de skills" para acelerar o desenvolvimento. Exemplo de uso:
*"Use a skill-factory para criar uma nova skill que automatize o padrão de [Alguma Função do Adianti]"*.

---

*Documentação atualizada por Antigravity em 29/03/2026.*
