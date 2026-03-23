---
name: Adianti Persistence
description: Guia sobre o modelo de persistência (Active Record, TRecord, TRepository) do Adianti Framework.
---

# Adianti Framework Persistence Model

Este guia cobre a camada de persistência orientada a objetos do Adianti Framework, baseada nos padrões Active Record e Repository.

## 1. Configuração de Conexão (`app/config`)

As conexões são definidas em arquivos PHP que retornam um array de configuração.
Exemplo (`erpcertificadodigital.php`):
```php
return [
    'host' => "127.0.0.1",
    'name' => "gestaocd",
    'user' => "gestaocd",
    'pass' => "TJ@123456@bd",
    'type' => "mysql",
    'prep' => "1" // Prepared Statements
];
```

## 2. Definindo um Modelo (`TRecord`)

Toda classe de modelo deve estender `TRecord`.

```php
class Pessoa extends TRecord
{
    const TABLENAME  = 'pessoa';     // Nome da tabela
    const PRIMARYKEY = 'id';         // Chave primária
    const IDPOLICY   = 'uuid';       // {max, serial, uuid}

    // Campos automáticos
    const CREATEDAT  = 'created_at';
    const UPDATEDAT  = 'update_at';
    const DELETEDAT  = 'deleted_at'; // Habilita Soft Delete
    
    // Usuários automáticos (Template/Framework)
    const CREATEDBY  = 'created_by';
    const UPDATEDBY  = 'updated_by';
    const USERBYATT  = 'userid';     // {userid, login, usercustomcode}

    // Caso precise de nomes de campos personalizados para auditoria
    const CREATED_BY_USER_ID = 'vendedor_id'; 

    public function __construct($id = NULL, $callObjectLoad = TRUE)
    {
        parent::__construct($id, $callObjectLoad);
        parent::addAttribute('nome');
        parent::addAttribute('documento');
        // ... outros atributos
    }
}
```

## 3. Operações CRUD Básicas

As operações são executadas dentro de uma transação (`TTransaction`).

```php
TTransaction::open('erpcertificadodigital');

// Create
$p = new Pessoa;
$p->nome = 'João Silva';
$p->store();

// Load / Find
$p = new Pessoa(1); // Lança exceção se não encontrar
$p = Pessoa::find(1); // Retorna FALSE se não encontrar

// Update
$p = Pessoa::find(1);
if ($p) {
    $p->nome = 'João Alterado';
    $p->store();
}

// Delete
$p->delete(); // Exclusão física ou lógica (se DELETEDAT estiver definido)
Pessoa::delete(1); // Exclusão direta por ID

TTransaction::close();
```

## 4. Filtragem e Coleções (`TCriteria` e `TRepository`)

Para manipular conjuntos de objetos.

```php
$criteria = new TCriteria;
$criteria->add(new TFilter('tipo_cliente_id', '=', 1));
$criteria->setProperty('order', 'nome');

$repository = new TRepository('Pessoa');
$pessoas = $repository->load($criteria);

// Atalhos estáticos (Fluent API)
$pessoas = Pessoa::where('tipo_cliente_id', '=', 1)
                 ->orderBy('nome')
                 ->load();

$count = Pessoa::where('cidade_id', '=', 4)->count();
```

## 5. Relacionamentos

### Associação (1:1 / N:1) - Lazy Load
```php
public function get_cidade()
{
    if (empty($this->cidade))
        $this->cidade = new Cidade($this->cidade_id);
    return $this->cidade;
}
```

### Composição (1:N)
O "todo" gerencia as "partes" no `store`, `load` e `delete` usando os métodos nativos `saveComposite`, `loadComposite` e `deleteComposite`.

### Agregação (N:N)
Utiliza uma tabela associativa. Gerenciada por `saveAggregate`, `loadAggregate` e `deleteComposite`.

### Métodos Auxiliares ("To String")
Comumente usados para exibir listas de itens relacionados em formato de texto.
```php
public function get_itens_to_string()
{
    $values = Item::where('parent_id', '=', $this->id)->getIndexedArray('id','{descricao}');
    return implode(', ', $values);
}
```

## 6. Hook Methods (Ganchos)

Os ganchos permitem interceptar o ciclo de vida da persistência para validações ou ações automáticas.

- `onBeforeStore($object)`: Antes de salvar.
- `onAfterStore($object)`: Após salvar.
- `onBeforeDelete($object)`: Antes de excluir. Útil para verificar dependências manuais.
- `onAfterDelete($object)`: Após excluir.
- `onBeforeLoad($id)`: Antes de carregar.
- `onAfterLoad($object)`: Após carregar.

### Exemplo: Verificação de Dependência (`onBeforeDelete`)
```php
public function onBeforeDelete()
{
    // Verifica se há registros dependentes antes de permitir a exclusão
    if (ItemRelacionado::where('parent_id', '=', $this->id)->first()) {
        throw new Exception("Não é possível deletar este registro pois ele possui itens relacionados.");
    }
}
```

## 7. Logs e Transações
- `TTransaction::setLogger(new TLoggerTXT('log.txt'))`: Habilita log.
- `TTransaction::dump()`: Exibe SQL em tela.
- `TTransaction::rollback()`: Cancela operações em caso de erro.
