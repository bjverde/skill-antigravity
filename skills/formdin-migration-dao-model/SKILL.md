---
name: FormDin4 DAO/VO to Adianti Model Migration
description: Guia determinístico para migrar VOs, DAOs e Stored Procedures de FormDin4 para TRecord e transações PDO no Adianti Framework.
---

# 🗄️ Migração: DAO/VO para Adianti Model & Persistência

Esta skill guia o Agente de IA na migração da camada de persistência do FormDin4 para o Adianti Framework. Ela detalha como extinguir VOs, reescrever DAOs como `TRecord` e tratar consultas complexas ou stored procedures legadas.

---

## 📐 Diretrizes de Persistência

| Componente FormDin4 | Equivalente Adianti | Regra de Implementação |
| :--- | :--- | :--- |
| **DAO Simples (`X_catalogo_telefonesDAO.class.php`, `T_circunscricaoDAO.class.php`)** | **`TRecord` Model** (VO/DAO Originais **Extintos**) | Para tabelas simples com operações CRUD padrão. Cria-se apenas o Model (`TRecord`) em `app/model/<nome_modulo>/`. O VO e o DAO originais são extintos. |
| **DAO Complexo (`V_telefone_principal_pessoaDAO`, `V_telefone_pessoaDAO`, `V_telefone_orgaoDAO`)** | **Cópia do DAO e VO** | Para DAOs que consultam VIEWS complexas, subqueries aninhadas, ou lógica SQL pesada customizada. **Faz-se uma cópia direta do DAO e do VO** para manter a compatibilidade da lógica complexa sem tentar forçar em um `TRecord`. |
| **VO de DAO Simples (`SomeVO.class.php`)** | **Extinto** | Em DAOs simples, o VO é extinto e as propriedades são tratadas dinamicamente pelo `TRecord`. |
| **VO de DAO Complexo (`V_telefone_orgaoVO.class.php`)** | **Cópia do VO** (na pasta `dao`) | Copiado para manter a assinatura dos métodos do DAO complexo. **Deve ser salvo na mesma pasta do DAO** (`app/control/<nome_modulo>/dao/`). Não crie a pasta `vo`. |
| **Campos Virtuais/Joins** | **Métodos `get_`/`_to_string`** | Tabelas relacionadas em `$sqlFrom` são mapeadas via relacionamentos Lazy Load (N:1) ou Virtual Data (`_to_string`). |
| **Filtros (`processWhereGridParameters`)** | **`TCriteria` e `TFilter`** | Os filtros condicionais na Grid de busca são reescritos usando a API Fluent do Adianti. |
| **Stored Procedures (`EXEC ...`)** | **DAO Class** | Criada como classe de acesso a dados em `app/control/<nome_modulo>/dao/` (não é Model/TRecord). Executada via PDO de `TTransaction::get()`. |

---

## 1. Extinção do VO & Criação do Model (`TRecord`)

No FormDin4, toda tabela/objeto de dados exigia uma classe VO (`*VO.class.php`) com getters e setters. No Adianti, o modelo estende `TRecord` e expõe atributos dinamicamente, dispensando os getters/setters repetitivos, exceto para associações.

### 📝 Exemplo Prático de De / Para

#### 🔴 Antes (FormDin4 - `dao/T_circunscricaoVO.class.php`)
```php
class T_circunscricaoVO
{
    private $icodigo = null;
    private $snome = null;
    public function __construct( $icodigo=null, $snome=null ) {
        $this->setIcodigo( $icodigo );
        $this->setSnome( $snome );
    }
    public function setIcodigo( $strNewValue = null ) { $this->icodigo = $strNewValue; }
    public function getIcodigo() { return $this->icodigo; }
    public function setSnome( $strNewValue = null ) { $this->snome = $strNewValue; }
    public function getSnome() { return $this->snome; }
}
```

#### 🟢 Depois (Adianti - `app/model/<nome_modulo>/Circunscricao.php`)
```php
class Circunscricao extends TRecord
{
    const TABLENAME  = 'T_CIRCUNSCRICAO';
    const PRIMARYKEY = 'iCodigo'; // Mantém caixa legada se necessário
    const IDPOLICY   = 'serial';

    public function __construct($id = NULL, $callObjectLoad = TRUE)
    {
        parent::__construct($id, $callObjectLoad);
        parent::addAttribute('sNome');
    }
}
```

---

## 1.1 Diferenciação: DAO Simples vs. DAO Complexo

Ao analisar os arquivos do diretório `dao/` legado, o Agente de IA deve classificá-los em **DAO Simples** ou **DAO Complexo** e aplicar a estratégia correta de migração.

### 🟢 DAO Simples
* **O que é**: DAOs criados para tabelas físicas padrão que realizam operações CRUD simples (exemplo: [X_catalogo_telefonesDAO](file:///c:/wamp64/www/formDinApp/sigaweb/dao/X_catalogo_telefonesDAO.class.php), [T_circunscricaoDAO](file:///c:/wamp64/www/formDinApp/sigaweb/dao/T_circunscricaoDAO.class.php)).
* **Características**:
  - Mapeia diretamente uma única tabela física sem subqueries complexas ou joins estruturais em `$sqlFrom`.
  - Contém métodos CRUD padrão (`selectById`, `selectCount`, `selectAllPagination`, `insert`, `update`, `delete`).
* **Ação de Migração**:
  - **Crie apenas o Model do Adianti (`TRecord`)** sob a pasta `<pasta_de_destino>/app/model/<nome_modulo>/`.
  - **Extinga por completo** o arquivo `*DAO.class.php` e `*VO.class.php` originais.
  - A manipulação e filtragem desses dados deverão ser feitas de forma nativa na View/Controller usando as APIs do Adianti (`TRepository`, `TCriteria`, etc.).

### 🟡 DAO Complexo (Classes complexas)
* **O que é**: DAOs baseados em Views de banco de dados, subconsultas aninhadas com expressões (como `CASE WHEN`), ou lógica SQL de joins excessivamente personalizada que seria impraticável reescrever como `TRecord` direto (exemplos: [V_telefone_principal_pessoaDAO](file:///c:/wamp64/www/formDinApp/sigaweb/dao/V_telefone_principal_pessoaDAO.class.php), [V_telefone_pessoaDAO](file:///c:/wamp64/www/formDinApp/sigaweb/dao/V_telefone_pessoaDAO.class.php), [V_telefone_orgaoDAO](file:///c:/wamp64/www/formDinApp/sigaweb/dao/V_telefone_orgaoDAO.class.php)).
* **Características**:
  - Lógica complexa em `$sqlFrom` contendo cláusulas `from (select ... ) as res`, `left join` cruzados, ou comandos customizados (`CASE WHEN ...`).
  - Métodos extras de negócio/específicos da aplicação (por exemplo, `selectAndar()`).
  - Forte dependência da passagem de VOs como contêineres de parâmetros para os métodos.
* **Ação de Migração**:
  - **Faça uma cópia direta da classe DAO e da classe VO correspondente** para manter a compatibilidade total e evitar quebras de lógica!
  - **Caminho de Destino da Cópia**:
    - **Tanto a classe DAO quanto a classe VO** devem ser gravadas na **mesma pasta** de DAOs do módulo: `<pasta_de_destino>/app/control/<nome_modulo>/dao/`.
    - > [!WARNING]
    - > **NÃO** crie nem utilize uma pasta `vo/` para colocar o VO. Ambos (DAO e VO) devem ficar juntos no diretório `/dao/`.
    - **DAO**: salve em `<pasta_de_destino>/app/control/<nome_modulo>/dao/<Nome>DAO.class.php` (ou `.php`).
    - **VO**: salve em `<pasta_de_destino>/app/control/<nome_modulo>/dao/<Nome>VO.class.php` (ou `.php`).
  - **Adaptação Necessária**: Ajuste as referências a classes de suporte do FormDin4 legado no código copiado (como instanciar a conexão usando `TTransaction::get()` ou mantê-las envelopadas na transação aberta).

---

## 2. Migração de Consultas de DAO para Model/TRecord

As consultas padrões em DAOs (`selectAll`, `selectCount`, `selectById`) são mapeadas nativamente pelas funções do Adianti (`TRepository`, `TCriteria`, `TFilter` ou Fluent API).

### 🔍 Substituição de Filtros Dinâmicos
No FormDin4, o método `processWhereGridParameters()` montava a query baseando-se no tipo do campo. No Adianti, fazemos isso montando um `TCriteria`:

#### 🔴 Antes (FormDin4 - `dao/V_telefone_orgaoDAO.class.php`)
```php
private function processWhereGridParameters( $whereGrid )
{
    $result = $whereGrid;
    if ( is_array($whereGrid) ){
        $where = ' 1=1 ';
        $where = SqlHelper::getAtributeWhereGridParameters($where, $whereGrid, 'ICODIGO', SqlHelper::SQL_TYPE_NUMERIC);
        $where = SqlHelper::getAtributeWhereGridParameters($where, $whereGrid, 'SNOME', SqlHelper::SQL_TYPE_TEXT_LIKE);
        $result = $where;
    }
    return $result;
}
```

#### 🟢 Depois (Adianti - Método de Busca na Listagem ou View)
```php
$criteria = new TCriteria;

if (!empty($filter_data->icodigo)) {
    $criteria->add(new TFilter('icodigo', '=', $filter_data->icodigo));
}
if (!empty($filter_data->snome)) {
    $criteria->add(new TFilter('snome', 'like', "%{$filter_data->snome}%"));
}

$repository = new TRepository('TelefoneOrgao');
$objects = $repository->load($criteria);
```

---

## 3. Consultas Complexas & Stored Procedures

> [!IMPORTANT]
> Consultas extremamente complexas (que envolvem múltiplos sub-selects ou chamadas de Stored Procedures do banco de dados) **NÃO** devem ser mapeadas como `TRecord` puro. Elas devem ser resolvidas executando queries brutas através da conexão PDO do Adianti.
> > Quando for uma **Stored Procedure** (geralmente identificada pelo prefixo `Sp_` ou `sp_`), **NÃO** deve ser criado um Model (`app/model/<nome_modulo>/`). Em vez disso, crie uma classe DAO dedicada dentro da pasta `app/control/<nome_modulo>/dao/`.

### ⚙️ Execução de Stored Procedures no Adianti
Sempre encapsule a execução da stored procedure dentro de uma transação aberta na base de dados apropriada, usando prepared statements para evitar injeção de SQL. A classe DAO conterá a lógica de execução via conexão PDO obtida de `TTransaction::get()`.

#### 🔴 Antes (FormDin4 - `dao/Sp_detalhes_outroservicoDAO.class.php`)
```php
public function execProcedure( Sp_detalhes_outroservicoVO $objVo )
{
    $parameters = null;
    $icodigo = $objVo->getIcodigo();
    $icodigo = SqlHelper::attributeIsset($icodigo,' @icodigo ='.$icodigo,'');
    $parameters = $parameters.$icodigo;

    $icodlocalidade = $objVo->getIcodlocalidade();
    $icodlocalidade = SqlHelper::attributeIsset($icodlocalidade,' , @icodlocalidade ='.$icodlocalidade,'');
    $parameters = $parameters.$icodlocalidade;

    $sql = 'EXEC dbo.sp_detalhes_outroservico '.$parameters;
    $result = $this->tpdo->executeSql($sql);
    return $result[0];
}
```

#### 🟢 Depois (Adianti - DAO Class em `app/control/<nome_modulo>/dao/SpDetalhesOutroServico.php`)
```php
class SpDetalhesOutroServico
{
    /**
     * Executa a procedure sp_detalhes_outroservico
     */
    public static function execProcedure($icodigo, $icodlocalidade)
    {
        TTransaction::open(Constantes::DATABASE_MAIN);
        
        // Recupera a conexão PDO gerenciada pelo framework
        $conn = TTransaction::get();
        
        // Prepara a instrução SQL robusta
        $stmt = $conn->prepare("EXEC dbo.sp_detalhes_outroservico @icodigo = :icodigo, @icodlocalidade = :icodlocalidade");
        
        $stmt->execute([
            ':icodigo' => $icodigo,
            ':icodlocalidade' => $icodlocalidade
        ]);
        
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        TTransaction::close();
        
        return $result;
    }
}
```

> [!TIP]
> - Sempre use `PDO::FETCH_ASSOC` para receber as linhas como arrays associativos simples, o que facilita o consumo em TGrids dinâmicas.
> - Se a stored procedure retornar dados de uma listagem paginada, faça o cálculo de `OFFSET` e `LIMIT` antes de passar à procedure.

---

## 🏁 Checklist de Conversão de Dados
- [ ] Foi feita a classificação correta de cada DAO legado como **Simples** ou **Complexo**?
- [ ] Para **DAOs Simples**, o arquivo `*VO.class.php` e `*DAO.class.php` foram extintos e criados apenas como `TRecord` Model em `<pasta_de_destino>/app/model/<nome_modulo>/`?
- [ ] Para **DAOs Complexos** (ex: `V_telefone_orgaoDAO`), tanto o DAO quanto o VO foram copiados integralmente para a mesma pasta `<pasta_de_destino>/app/control/<nome_modulo>/dao/` (sem criar pasta `vo`)?
- [ ] Para Stored Procedures (ex: `Sp_...`), foi criada uma classe DAO em `<pasta_de_destino>/app/control/<nome_modulo>/dao/` executando prepared statements?
- [ ] Toda coluna do banco (incluindo FKs e metadados) nos novos models `TRecord` foi registrada via `parent::addAttribute()` no construtor do modelo?
- [ ] Chave primária (`PRIMARYKEY`) e a política de ID (`IDPOLICY`) foram devidamente configuradas nos models?
- [ ] Conexões dinâmicas foram migradas para `TTransaction::open(Constantes::DATABASE_MAIN)`?
- [ ] Stored procedures e DAOs copiados estão devidamente envelopados/adaptados para usar conexões via PDO `TTransaction::get()` onde aplicável?
