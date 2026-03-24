---
name: adianti-permission
description: >
  Registra permissões e menu para novas telas no Adianti Framework usando Migrations e menu.xml.
  Use quando o usuário pedir para registrar tela, adicionar permissão, configurar menu, ou após criar uma nova tela.
  TRIGGER: registrar tela, permissão, menu, menu.xml, migration de permissão, Adianti.
---

# Skill: Registro de Permissões e Menu (Adianti Framework)

Esta skill fornece os procedimentos para registrar uma nova tela nos sistemas baseados no Adianti Framework, utilizando o novo sistema de **Migrations** para o banco de dados e atualização manual do `menu.xml`.

---

## 1. Registro de Permissões (Migrations)

O projeto migrou para um sistema de classes PHP (`Migration`) para gerenciar mudanças no banco de dados. **Não use mais o arquivo `inserts-permission.sql`.**

### Procedimento:
1. Verifique o último número de versão em `system/app/database/migrations/` (ex: `V002...`).
2. Crie um novo arquivo seguindo o padrão `V<PróximoNúmero><NomeDaTela>.php`.
3. Implemente a classe estendendo `Migration`.

### Template de Migration para Permissão:
```php
<?php

class V<PROXIMO_NUMERO><NomeDaTela> extends Migration
{
    public function getVersion(): string { return 'V<PROXIMO_NUMERO>'; }

    public function getDescription(): string 
    { 
        return 'Adiciona permissões para a tela <NomeAmigável>'; 
    }

    public function up(): void 
    {
        TTransaction::open('permission');
        $conn = TTransaction::get();
        
        // 1. Inserir Programa
        $conn->exec("INSERT INTO system_program (id, name, controller) 
                     VALUES ( (SELECT max(p.id) + 1 FROM system_program p), '<NomeAmigável>', '<NomeClasse>' )");
        
        // 2. Vincular ao Grupo Administrador (ID 1)
        $conn->exec("INSERT INTO system_group_program (id, system_group_id, system_program_id)
                     VALUES ( (SELECT max(gp.id) + 1 FROM system_group_program gp)
                            , 1 -- adm
                            , (SELECT p.id FROM system_program p where p.controller = '<NomeClasse>')
                            )");
        
        TTransaction::close();
    }

    public function down(): void 
    {
        TTransaction::open('permission');
        $conn = TTransaction::get();
        
        // Remover vínculo e programa
        $conn->exec("DELETE FROM system_group_program WHERE system_program_id IN (SELECT id FROM system_program WHERE controller = '<NomeClasse>')");
        $conn->exec("DELETE FROM system_program WHERE controller = '<NomeClasse>'");
        
        TTransaction::close();
    }
}
```

---

## 2. Registro no Menu (`system/menu.xml`)

Adicione a entrada correspondente no arquivo `system/menu.xml` para tornar a tela acessível.

### Template de Menu:
```xml
<menuitem label="<Nome Amigável>">
    <icon>fas:circle-notch</icon>
    <action><NomeClasse></action>
</menuitem>
```

> [!TIP]
> Ao criar uma dupla (List e Form), geralmente apenas a `List` vai para o menu. A `Form` é acessada através da `List`. No entanto, ambas precisam de permissão no SQL.

---

## 3. Como integrar com outras Skills

Ao finalizar a geração de código (ex: após usar a skill `adianti-codegen`):
1. Liste os arquivos em `system/app/database/migrations/` para determinar a próxima versão.
2. Crie o arquivo de migration com os inserts necessários.
3. Atualize o `menu.xml`.
