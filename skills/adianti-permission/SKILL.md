---
name: adianti-permission
description: >
  Repositório de comandos SQL para registro de programas e permissões no Adianti Framework.
  Fornece as queries brutas para inserção em system_program e system_group_program.
---

# Skill: SQL de Permissões (Adianti Framework)

Esta skill é a base de dados de comandos SQL necessária para registrar novas funcionalidades no sistema de permissões do Adianti. Ela deve ser consultada pela skill `adianti-migration` para preencher os métodos `up()` e `down()`.

## 📌 Tabela de Parâmetros
| Variável | Descrição | Exemplo |
| :--- | :--- | :--- |
| `<NomeAmigável>` | Nome legível que aparecerá no Menu. | "Cadastro de Produtos" |
| `<NomeClasse>` | Nome EXATO da classe PHP (`Case Sensitive`). | "ProdutoForm" |

---

## 🛠️ Blocos de Comandos SQL

Utilize estes moldes para garantir a integridade dos IDs nos sistemas Adianti que não usam auto-incremento nas tabelas de sistema.

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

### 3. Remover Registro (Rollback / Down)
```sql
-- Primeiro remover o vínculo
DELETE FROM system_group_program WHERE system_program_id IN (SELECT id FROM system_program WHERE controller = '<NomeClasse>');

-- Depois remover o programa
DELETE FROM system_program WHERE controller = '<NomeClasse>';
```

---

## ✅ Checklist de Validação (Obrigatório)
Antes de aplicar este SQL em uma Migration, a IA deve validar:
- [ ] O nome da classe (`controller`) existe no diretório `app/control/`.
- [ ] O arquivo `VXXX.php` usa o banco `'permission'` para estas queries.
- [ ] A subquery de `max(id) + 1` foi incluída para evitar conflitos.

> [!CAUTION]
> **IDs Seqüenciais**: NUNCA use IDs fixos (ex: `VALUES (151, ...)`) — isto quebrará o sistema em diferentes bases de dados. Sempre use as subqueries de `MAX(id)`.

---
*Este repositório é mantido pela [**Adianti Skill Factory**](file:../adianti-skill-factory/SKILL.md).*
