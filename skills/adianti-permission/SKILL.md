---
name: adianti-permission
description: >
  Repositório de comandos SQL para registro de programas e permissões no Adianti Framework.
  Fornece as queries brutas para inserção em system_program e system_group_program.
---

# Skill: SQL de Permissões (Adianti Framework)

Esta skill é a base de dados de comandos SQL necessária para registrar novas funcionalidades no sistema de permissões do Adianti. Ela deve ser consultada pela skill `adianti-migration` para preencher os métodos `up()` e `down()`.

## 🛠️ Comandos SQL para Migrations

Ao registrar uma nova tela, utilize os moldes abaixo:

### 1. Inserir Programa (`system_program`)
```sql
INSERT INTO system_program (id, name, controller) 
VALUES ( (SELECT max(p.id) + 1 FROM system_program p), '<NomeAmigável>', '<NomeClasse>' );
```

### 2. Vincular ao Grupo Administrador (`system_group_program`)
```sql
INSERT INTO system_group_program (id, system_group_id, system_program_id)
VALUES ( (SELECT max(gp.id) + 1 FROM system_group_program gp)
       , 1 -- Grupo ADM
       , (SELECT p.id FROM system_program p WHERE p.controller = '<NomeClasse>')
       );
```

### 3. Remover Programa (Rollback / Down)
```sql
-- Primeiro remover o vínculo
DELETE FROM system_group_program WHERE system_program_id IN (SELECT id FROM system_program WHERE controller = '<NomeClasse>');

-- Depois remover o programa
DELETE FROM system_program WHERE controller = '<NomeClasse>';
```

---

## 📐 Padrões de Dados
| Campo | Descrição | Exemplo |
| :--- | :--- | :--- |
| `name` | Descrição amigável que aparecerá no menu/permissoes. | "Cadastro de Produtos" |
| `controller` | O nome EXATO da classe PHP (Case Sensitive). | "ProdutoForm" |

> [!CAUTION]
> **IDs Seqüenciais**: Sempre use a subquery `(SELECT max(...) + 1 ...)` para evitar conflitos de ID em diferentes ambientes de desenvolvimento, já que o Adianti não usa Auto-Increment por padrão em algumas tabelas de sistema.

---
*Esta skill é utilizada como fonte de dados para as automações de registro.*
