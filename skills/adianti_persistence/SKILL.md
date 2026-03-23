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

### 2.1. Estrutura Completa de um Modelo

> [!IMPORTANT]
> Ao criar um modelo, **TODOS** os elementos abaixo devem ser incluídos quando aplicável. Nunca omita nenhum deles.

A estrutura de um modelo completo segue esta ordem obrigatória:

1. **Constantes de tabela** (`TABLENAME`, `PRIMARYKEY`, `IDPOLICY`)
2. **Constantes de timestamps** (`CREATEDAT`, `UPDATEDAT`, `DELETEDAT`)
3. **Constantes de auditoria de usuário** (`CREATEDBY`, `UPDATEDBY`, `USERBYATT`)
4. **Propriedades `private` tipadas** para cada FK/associação
5. **Construtor** com `addAttribute()` para **TODAS** as colunas da tabela
6. **Métodos `set_`/`get_`** para cada FK (associação N:1)
7. **Métodos de coleção** (`get<Entidade>s()`) para relações 1:N
8. **Métodos `_to_string`** para exibição de dados relacionados

### 2.2. Exemplo Completo de Modelo

```php
class Pessoa extends TRecord
{
    const TABLENAME  = 'pessoa';     // Nome da tabela
    const PRIMARYKEY = 'id';         // Chave primária
    const IDPOLICY   = 'serial';     // {max, serial, uuid}

    // Campos automáticos de timestamp
    const CREATEDAT  = 'created_at';
    const UPDATEDAT  = 'update_at';
    const DELETEDAT  = 'deleted_at'; // Habilita Soft Delete
    
    // Usuários automáticos (Template/Framework) - quando aplicável
    const CREATEDBY  = 'created_by';
    const UPDATEDBY  = 'updated_by';
    const USERBYATT  = 'userid';     // {userid, login, usercustomcode}

    // Propriedades tipadas para cada FK/associação
    private SystemUnit $system_unit;
    private TipoCliente $tipo_cliente;
    private SystemUsers $system_users;
    private CategoriaCliente $categoria_cliente;

    public function __construct($id = NULL, $callObjectLoad = TRUE)
    {
        parent::__construct($id, $callObjectLoad);
        // TODAS as colunas da tabela, incluindo FKs e timestamps
        parent::addAttribute('tipo_cliente_id');
        parent::addAttribute('categoria_cliente_id');
        parent::addAttribute('system_users_id');
        parent::addAttribute('system_unit_id');
        parent::addAttribute('nome');
        parent::addAttribute('documento');
        parent::addAttribute('cpf');
        parent::addAttribute('telefone');
        parent::addAttribute('email');
        parent::addAttribute('dt_nascimento');
        parent::addAttribute('aboservacao');
        parent::addAttribute('obs');
        parent::addAttribute('login');
        parent::addAttribute('senha');
        parent::addAttribute('created_at');
        parent::addAttribute('update_at');
        parent::addAttribute('updated_at');
        parent::addAttribute('deleted_at');
    }

    // --- Métodos set_/get_ para cada FK (seção 5.1) ---

    public function set_tipo_cliente(TipoCliente $object)
    {
        $this->tipo_cliente = $object;
        $this->tipo_cliente_id = $object->id;
    }

    public function get_tipo_cliente()
    {
        if (empty($this->tipo_cliente))
            $this->tipo_cliente = new TipoCliente($this->tipo_cliente_id);
        return $this->tipo_cliente;
    }

    public function set_system_unit(SystemUnit $object)
    {
        $this->system_unit = $object;
        $this->system_unit_id = $object->id;
    }

    public function get_system_unit()
    {
        if (empty($this->system_unit))
            $this->system_unit = new SystemUnit($this->system_unit_id);
        return $this->system_unit;
    }

    // --- Métodos de coleção 1:N (seção 5.2) ---

    public function getPessoaEnderecos()
    {
        $criteria = new TCriteria;
        $criteria->add(new TFilter('pessoa_id', '=', $this->id));
        return PessoaEndereco::getObjects( $criteria );
    }

    public function getPessoaContatos()
    {
        $criteria = new TCriteria;
        $criteria->add(new TFilter('pessoa_id', '=', $this->id));
        return PessoaContato::getObjects( $criteria );
    }

    // --- Métodos _to_string (seção 5.4) ---
    // Ver seção 5.4 para exemplos completos
}
```

> [!CAUTION]
> **Regras obrigatórias ao criar um modelo:**
> - Sempre incluir `CREATEDAT`, `UPDATEDAT` e `DELETEDAT` se a tabela possuir essas colunas.
> - Sempre declarar `private <Tipo> $propriedade` para cada FK.
> - Sempre criar métodos `set_<nome>()` e `get_<nome>()` para cada FK.
> - Sempre listar **TODAS** as colunas da tabela em `addAttribute()`, inclusive FKs (`*_id`) e timestamps (`created_at`, `updated_at`, `deleted_at`).
> - Sempre criar métodos de coleção (`get<Entidade>s()`) para relações 1:N.
> - Sempre criar métodos `_to_string` quando a model é exibida em listagens com colunas de tabelas relacionadas.

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

### 5.1. Associação (N:1) - Lazy Load com `set_`/`get_`

Para cada coluna FK (`*_id`), crie:
1. Uma propriedade `private` tipada no topo da classe
2. Um par de métodos `set_<nome>()` / `get_<nome>()`

```php
// Propriedade tipada
private TipoCliente $tipo_cliente;

// Setter - permite atribuir o objeto diretamente: $pessoa->tipo_cliente = $obj;
public function set_tipo_cliente(TipoCliente $object)
{
    $this->tipo_cliente = $object;
    $this->tipo_cliente_id = $object->id;
}

// Getter com lazy load - permite acessar: $pessoa->tipo_cliente->nome;
public function get_tipo_cliente()
{
    if (empty($this->tipo_cliente))
        $this->tipo_cliente = new TipoCliente($this->tipo_cliente_id);
    return $this->tipo_cliente;
}
```

### 5.2. Composição (1:N) - Métodos de Coleção

Para cada tabela filha que referencia esta tabela, crie um método `get<Entidade>s()`:

```php
public function getPessoaEnderecos()
{
    $criteria = new TCriteria;
    $criteria->add(new TFilter('pessoa_id', '=', $this->id));
    return PessoaEndereco::getObjects( $criteria );
}
```

O "todo" gerencia as "partes" no `store`, `load` e `delete` usando os métodos nativos `saveComposite`, `loadComposite` e `deleteComposite`.

### 5.3. Agregação (N:N)

Utiliza uma tabela associativa. Gerenciada por `saveAggregate`, `loadAggregate` e `deleteComposite`.

### 5.4. Métodos `_to_string` (Virtual Data)

Estes métodos são usados pelo Adianti Builder para exibir dados de tabelas relacionadas em listagens (DataGrids). Para cada tabela filha (1:N) e suas respectivas FKs, crie pares `set_`/`get_` de virtual data.

> [!IMPORTANT]
> Estes métodos são **OBRIGATÓRIOS** em modelos gerados para o sistema. Sem eles, as listagens com colunas de tabelas relacionadas não funcionam.

**Padrão de nomenclatura:** `<tabela_filha>_<fk_da_filha>_to_string`

**Exemplo completo** (para a relação `Pessoa -> PessoaEndereco -> Cidade`):

```php
// Setter: recebe array de IDs ou string direta
public function set_pessoa_endereco_cidade_to_string($pessoa_endereco_cidade_to_string)
{
    if(is_array($pessoa_endereco_cidade_to_string))
    {
        $values = Cidade::where('id', 'in', $pessoa_endereco_cidade_to_string)->getIndexedArray('nome', 'nome');
        $this->pessoa_endereco_cidade_to_string = implode(', ', $values);
    }
    else
    {
        $this->pessoa_endereco_cidade_to_string = $pessoa_endereco_cidade_to_string;
    }

    $this->vdata['pessoa_endereco_cidade_to_string'] = $this->pessoa_endereco_cidade_to_string;
}

// Getter: retorna os nomes concatenados da FK na tabela filha
public function get_pessoa_endereco_cidade_to_string()
{
    if(!empty($this->pessoa_endereco_cidade_to_string))
    {
        return $this->pessoa_endereco_cidade_to_string;
    }

    $values = PessoaEndereco::where('pessoa_id', '=', $this->id)->getIndexedArray('cidade_id','{cidade->nome}');
    return implode(', ', $values);
}
```

**Regra geral para `_to_string`:**
- No **setter**: `<ModelFK>::where('id', 'in', $param)->getIndexedArray('<campo_display>', '<campo_display>')`
- No **getter**: `<TabelaFilha>::where('<fk_para_pai>', '=', $this->id)->getIndexedArray('<fk_da_filha>','{<relacao>-><campo_display>}')`
- O setter sempre salva em `$this->vdata[...]` para virtual data.

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

## 8. Checklist para Criação de Modelo

Ao criar um novo modelo TRecord, garanta que **TODOS** os itens abaixo sejam atendidos:

- [ ] Constantes `TABLENAME`, `PRIMARYKEY`, `IDPOLICY` definidas
- [ ] Constantes `CREATEDAT`, `UPDATEDAT`, `DELETEDAT` definidas (se a tabela tiver essas colunas)
- [ ] Constantes `CREATEDBY`, `UPDATEDBY`, `USERBYATT` definidas (se aplicável)
- [ ] Propriedade `private <Tipo> $nome` para cada FK
- [ ] `addAttribute()` para **TODAS** as colunas da tabela (FKs `*_id`, timestamps, e campos normais)
- [ ] Métodos `set_<nome>()` e `get_<nome>()` para cada FK/associação
- [ ] Métodos `get<Entidade>s()` para cada relação 1:N
- [ ] Métodos `_to_string` (set/get) para virtual data de tabelas filhas e suas FKs
- [ ] Hook `onBeforeDelete()` para verificar dependências (se necessário)
