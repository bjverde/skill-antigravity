---
name: adianti-list-daterange
description: Padroniza a criação de filtros de intervalo de data (De/Até) em telas de listagem do Adianti.
---

# Skill: Adianti List Date Range Filters

Esta skill automatiza a implementação de filtros de busca por período (intervalo de datas) em telas do tipo `List.php`, garantindo a cobertura total do dia (00:00:00 às 23:59:59).

## 📐 Padrões Técnicos

| Regra | Detalhamento |
| :--- | :--- |
| **Componente** | Usar `TDate` para os campos de filtro (mesmo que o banco seja DateTime). |
| **Nomenclatura** | Sufixos `_de` (início) e `_ate` (fim) baseados no nome da coluna. |
| **Máscaras** | Display: `dd/mm/yyyy` | DB: `yyyy-mm-dd`. |
| **Filtros (onSearch)** | Usar `>=` com `00:00:00` e `<=` com `23:59:59` para campos DateTime. |

## 🚀 Como Implementar

### 1. Definição dos Campos (`__construct`)
Para cada campo de data (ex: `dt_include`), criar dois objetos:

```php
$dt_include_de = new TDate('dt_include_de');
$dt_include_ate = new TDate('dt_include_ate');

$dt_include_de->setMask('dd/mm/yyyy');
$dt_include_de->setDatabaseMask('yyyy-mm-dd');
$dt_include_de->setSize('100%');

$dt_include_ate->setMask('dd/mm/yyyy');
$dt_include_ate->setDatabaseMask('yyyy-mm-dd');
$dt_include_ate->setSize('100%');
```

### 2. Layout do Formulário
Agrupar os campos de intervalo em linhas do `BootstrapFormBuilder`:

```php
$this->form->addFields(
    [new TLabel("Inclusão De:")], [$dt_include_de],
    [new TLabel("Inclusão Até:")], [$dt_include_ate]
);
```

### 3. Lógica de Busca (`onSearch`)
Adicionar os filtros condicionais garantindo a integridade do intervalo:

```php
if (!empty($data->dt_include_de))
{
    $filters[] = new TFilter('dt_include', '>=', $data->dt_include_de . ' 00:00:00');
}

if (!empty($data->dt_include_ate))
{
    $filters[] = new TFilter('dt_include', '<=', $data->dt_include_ate . ' 23:59:59');
}
```

> [!TIP]
> Se o campo no banco de dados for apenas `DATE` (sem hora), remova os sufixos de tempo (`00:00:00`).

## 🏁 Checklist de Conclusão
- [ ] Criou os campos com sufixos `_de` e `_ate`?
- [ ] Aplicou as máscaras de banco de dados corretamente?
- [ ] No `onSearch`, usou `>=` para o início e `<=` para o fim?
- [ ] Adicionou as horas `00:00:00` e `23:59:59` para campos do tipo DateTime?
