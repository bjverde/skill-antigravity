---
name: adianti-migration
description: >
  Automatiza a criação de arquivos de Migration PHP para o Adianti Framework.
  Gera a classe V00x... e o template up/down para qualquer mudança de banco.
---

# Skill: Gerador de Migrations (Adianti Framework)

Esta skill é o motor para criar os arquivos de versão do banco de dados localizados em `system/app/database/migrations/`.

## 🛠️ Procedimento Interno para o Agente (IA)

Sempre que o usuário pedir para "criar uma migration":

### 1. Determinar Versão
- Liste os arquivos na pasta `system/app/database/migrations/`.
- Identifique o maior número `VXXX` (ex: `V015`).
- Defina o próximo número (ex: `V016`).

### 2. Gerar Arquivo
O arquivo deve ser nomeado `V<Versao><Assunto>.php`.

**Template Geral**:
```php
<?php

class V<PROXIMO_NUMERO><NomeDaAcao> extends Migration
{
    public function getVersion(): string { return 'V<PROXIMO_NUMERO>'; }

    public function getDescription(): string 
    { 
        return '<Descricao Amigável da Mudança>'; 
    }

    public function up(): void 
    {
        TTransaction::open('<DATABASE_NAME>');
        $conn = TTransaction::get();
        
        // Comandos SQL aqui
        $conn->exec("...");
        
        TTransaction::close();
    }

    public function down(): void 
    {
        TTransaction::open('<DATABASE_NAME>');
        $conn = TTransaction::get();
        
        // Rollback SQL aqui
        $conn->exec("...");
        
        TTransaction::close();
    }
}
```

---

## 📐 Padrões de Uso
1. **Banco Permission**: Se a migration for de permissões, consulte a skill `adianti-permission` para preencher os comandos SQL nos métodos `up()` e `down()`.
2. **Banco de Dados**: Se não for especificado, o default para novas tabelas é o banco principal definido na skill `adianti_persistence`.

> [!IMPORTANT]
> **Consistência**: O nome da classe PHP **deve** ser idêntico ao nome do arquivo (sem o `.php`).

---
*Skill ativada por: "criar migration", "nova versão de banco", "migration SQL".*
