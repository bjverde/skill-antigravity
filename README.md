# Antigravity Skills & Kit - Guia do Projeto

Este repositório contém as **Skills e Configurações** especializadas para o ecossistema Antigravity (IA), focadas principalmente no **Adianti Framework**, **FormDin v4** e **FormDin v5**.

Este projeto deve ser clonado dentro da pasta raiz do seu projeto Adianti/FormDin para que a IA (Antigravity ou Claude Code) reconheça as instruções facilitando o desenvolvimento. Em conjunto será utilizado o Antigravity Kit (Global), algumas skill do Awesome Skills (local) e GSD (Global).

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

## 3. Instalação do Awesome Skills (local)

O repositório **Awesome Skills** contém milhares de utilitários genéricos. Você pode instalá-los junto com as skills do Adianti.

***🚫NÃO instale todas as skills do Awesome Skills, pois são milhares e vai deixar o Antigravity lento. 🐌***


**Como Instalar Skills Utilitárias (Ex: Security, Debug):**
```bash
npx antigravity-awesome-skills --path ./.agent/skills
```

---

## 4. Configuração do Git e Exclusão

Para evitar o versionamento de milhares de arquivos genéricos no seu repositório principal e no repositório de skills, siga estas regras:

1.  **Na Raiz do Projeto (`.gitignore`):** Deve conter a linha `.agent/` (isso já está configurado no projeto).
2.  **Na Pasta `.agent/` (`.agent/.gitignore`):** Ignoramos as skills externas/genéricas instaladas via Awesome Skills para manter o foco apenas nas skills Adianti.

---

# Dicas de Agentes, Skills, Rules e Workflows de projetos externos

## Antigravity Kit
O Antigravity Kit transforma a IA em uma "equipe virtual" através de agentes especialistas. Aqui estão alguns dos principais incluídos no kit:

🛠️ Engenharia e Desenvolvimento
* @backend-specialist: Focado em lógica de servidor, APIs e arquitetura de sistemas.
* @frontend-specialist: Especialista em UI/UX, CSS moderno, JavaScript e frameworks web.
* @debugger: Um agente focado exclusivamente em análise sistemática de logs e correção de erros.
* @database-architect: Especialista em modelagem de dados relacional e otimização de queries SQL.

🛡️ Qualidade e Segurança
* @security-auditor: Analisa o código em busca de vulnerabilidades como SQL Injection e falhas de autenticação.
* @test-engineer: Ajuda a criar planos de teste, testes unitários e automação de QA.

📋 Planejamento e Documentação
* @product-planner: Auxilia no brainstorming de funcionalidades e na criação de MVPs (utiliza o comando /brainstorm).
* @documentation-specialist: Ideal para manter o README atualizado ou criar novas skills (utiliza o comando /doc).

🚀 Outras Especialidades
* @devops-engineer: Focado em deploys, CI/CD e configurações de servidor (como o Wamp64/Apache).
* @seo-growth: Especialista em otimização para motores de busca e estratégias de crescimento.

### Como utilizá-los?
Você não precisa chamar um por um manualmente na maioria das vezes. Quando você inicia um workflow (como o /create ou /debug), o Antigravity automaticamente seleciona o "especialista" mais adequado para aquela tarefa.

Dica para seu projeto: Como você trabalha muito com PHP e Adianti, o @backend-specialist e o @database-architect serão seus parceiros mais frequentes!


## 1. Stack Adianti (PHP/Web/DB)
Utilize estas skills genéricas (do Awesome Skills) para complementar as do projeto:
- `@debugging-strategies` (Estratégias de depuração PHP)
- `@api-design-principles` (Design de APIs RestService)
- `sql-injection-testing` (Segurança em consultas SQL)
- `@security-auditor` (Auditoria de segurança de código)

---

# 🛠️ Ferramentas Especializadas do Projeto

Estas são as ferramentas desenvolvidas especificamente para o workflow da Adianti/FormDin. Elas estão localizadas na pasta `.agent/`.

## 🧠 Skills Locais (`.agent/skills/`)

As skills definem o "conhecimento especializado" da IA sobre o projeto.

| Nome | Descrição | Quando usar |
| :--- | :--- | :--- |
| [**adianti-codegen**](skills/adianti-codegen/SKILL.md) | Gerador de telas List e Form seguindo o padrão. | Ao precisar criar uma nova tela de cadastro ou consulta. |
| [**adianti-permission**](skills/adianti-permission/SKILL.md) | Automação de Migrations de permissão e Menu.xml. | Após criar novas telas para registrar o acesso. |
| [**adianti_persistence**](skills/adianti_persistence/SKILL.md) | Guia mestre de TRecord e persistência Adianti. | Ao criar ou depurar Models e persistência de dados. |
| [**adianti-skill-factory**](skills/adianti-skill-factory/SKILL.md) | Fábrica de automação para criar novas IA skills. | Para criar novos playbooks ou diretrizes para a IA. |
| [**ag-kit-installer**](skills/ag-kit-installer/SKILL.md) | Instalador do Antigravity Kit (via Python/PowerShell). | Na configuração inicial de uma nova máquina. |
| [**pdf_to_markdown**](skills/pdf_to_markdown/SKILL.md) | Extrator de PDFs para formato Markdown. | Para ler manuais técnicos (ex: Adianti) e transformá-los em conhecimento. |

## 🔄 Workflows Locais (`.agent/workflows/`)

Workflows são sequências de passos que guiam a IA em tarefas complexas.

*   [**`/pdf2md`**](workflows/pdf2md.md): Converte um arquivo PDF (manual ou livro) em um documento Markdown legível pela IA.

> [!TIP]
> **Fluxo de Trabalho Sugerido:** 
> 1. Use `adianti-codegen` para criar a tela. 
> 2. Use `adianti-permission` para registrar a tela no sistema. 
> 3. Se precisar consultar o manual do Adianti, use o workflow `/pdf2md`.

---

*Documentação atualizada por Antigravity em 29/03/2026.*
