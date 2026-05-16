---
name: adianti-list-column
description: >
  Padroniza a criação de colunas em datagrids do Adianti Framework.
  Garante que todas as colunas sejam ordenáveis e que campos de data/hora sejam formatados corretamente.
---

# Skill: Padronização de Colunas Datagrid Adianti

Esta skill define as regras para a criação de colunas (`TDataGridColumn`) em telas de listagem (`List.php`), garantindo consistência na ordenação e formatação.

## Regras de Implementação

### 1. Ordenação Obrigatória (Sorting)
Todas as colunas visíveis devem permitir ordenação. Para isso, deve-se configurar uma `TAction` vinculada ao método `onReload` da página, passando o parâmetro `order` com o nome do campo.

**Padrão:**
```php
$column_<field> = new TDataGridColumn('<field>', "<Label>", 'left');
$order_<field> = new TAction([$this, 'onReload']);
$order_<field>->setParameter('order', '<field>');
$column_<field>->setAction($order_<field>);
```

### 2. Formatação de Datas e Data/Hora
Campos que representam datas ou carimbos de data/hora (ex: `dt_include`, `created_at`, `updated_at`, `data_nascimento`) devem ser formatados para o padrão brasileiro usando `setTransformer`.

- **Data e Hora**: Usar `Constantes::formatDateTimeBr($value)`
- **Apenas Data**: Usar `Constantes::formatDateBr($value)`

**Exemplo (Data e Hora):**
```php
$column_dt_include = new TDataGridColumn('dt_include', "Inclusão", 'left');
$column_dt_include->setTransformer(function($value, $object, $row) {
    return Constantes::formatDateTimeBr($value);
});
```

### 3. Alinhamento e Largura
- **IDs e Códigos**: Alinhamento `center`. Largura sugerida: `70px` ou `100px`.
- **Textos e Nomes**: Alinhamento `left`.
- **Valores Monetários**: Alinhamento `right`.

### 4. Exemplos Combinados
```php
// Coluna ID (Ordenável)
$column_id = new TDataGridColumn('id', "ID", 'center', '70px');
$order_id = new TAction([$this, 'onReload']);
$order_id->setParameter('order', 'id');
$column_id->setAction($order_id);

// Coluna Nome (Ordenável)
$column_name = new TDataGridColumn('name', "Nome", 'left');
$order_name = new TAction([$this, 'onReload']);
$order_name->setParameter('order', 'name');
$column_name->setAction($order_name);

// Coluna Data (Ordenável + Formatada)
$column_created_at = new TDataGridColumn('created_at', "Criado em", 'left');
$column_created_at->setTransformer(function($value, $object, $row) {
    return Constantes::formatDateTimeBr($value);
});
$order_created_at = new TAction([$this, 'onReload']);
$order_created_at->setParameter('order', 'created_at');
$column_created_at->setAction($order_created_at);
```
