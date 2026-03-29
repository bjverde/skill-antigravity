# Antigravity Skills & Kit - Guia do Projeto Solubiz

Este repositório contém as **Skills e Configurações** especializadas para o ecossistema Antigravity (IA), focadas principalmente no **Adianti Framework**, **FormDin v4** e **FormDin v5**.

Este projeto deve ser clonado dentro da pasta raiz do seu projeto Adianti ou FormDin para que a IA (Antigravity ou Claude Code) reconheça as instruções. Em conjunto será utilizao o Antigravity Kit e algumas skill do Awesome Skills.

# Instalação resumida
Abaixo um resumo de como instalar o Antigravity e as skills:

1. Tenha o Antigravity instalado
1. Clone o seu projeto Adianti/FormDin
1. Usando o Antigravity abra o seu projeto
1. No terminal dentro do Antigravity, clone esse projeto skill-antigravity
1. Instalar o Antigravity Kit Globalmente

# Instalação detalhada 
---

## 1. Instalação do Antigravity Kit (Global)

O **Antigravity Kit** fornece agentes especialistas (Frontend, Backend, etc.) e workflows estruturados para a IA.

**Instalação Global:**
```bash
npm install -g @vudovn/ag-kit
```

**Como Iniciar no Projeto:**
Acesse a pasta raiz do seu projeto e execute:
```bash
ag-kit init
```
*Isso irá configurar os agentes e regras básicas no seu ambiente.*

---

## 2. Instalação das Skills Locais (Adianti)

Para garantir que a IA conheça as regras do Adianti, as skills devem estar na pasta `.agent`.

**Como Clonar Localmente:**
Acesse a pasta raiz do seu projeto e execute:
```bash
git clone https://github.com/bjverde/skill-antigravity.git .agent
```

---

## 3. Integração com Awesome Skills

O repositório **Awesome Skills** contém milhares de utilitários genéricos. Você pode instalá-los junto com as skills do Adianti.

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
