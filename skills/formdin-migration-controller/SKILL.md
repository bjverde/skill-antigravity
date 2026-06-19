---
name: FormDin4 Controller to Adianti Controller Migration
description: Guia técnico para migração de Controllers e regras de negócio do FormDin4 para app/<nome_sistema>/control/controllers/ no Adianti.
---

# 🎮 Migração: Controller & Regras de Negócio

Esta skill guia o Agente de IA na migração das classes de controle do FormDin4 para o padrão adotado na migração para o Adianti Framework. O objetivo é manter as regras de negócio organizadas separadamente das telas de apresentação.

---

## 📐 Diretrizes de Organização

| Conceito | FormDin4 | Padrão Adianti (Neste Projeto) |
| :--- | :--- | :--- |
| **Localização** | Pasta raiz `controllers/` | Pasta `app/<nome_sistema>/control/controllers/` |
| **Instanciação** | Direta no arquivo de view (`new V_telefone_orgao()`) | Instanciada e chamada pelas classes de View (`app/<nome_sistema>/views/*`) |
| **Filtros Fixos** | Método `filtraConsulta()` injetando arrays | Embutidos na lógica de construção de `TCriteria` nas consultas do Controller |
| **Formatação UI** | Método `trataDados()` modificando o array bruto | Dividida: Lógica bruta fica no Controller, estilizações visuais (`<b>`, cores) migram para os *Transformers* do Datagrid na View |

---

## 1. Mapeamento de Classe de Controle

As controllers no FormDin4 atuavam como pontes diretas para o DAO, adicionando regras de filtro e pós-processamento. No Adianti, elas encapsulam as transações do banco de dados (`TTransaction`), coordenam carregamentos e retornam dados estruturados.

### 📝 Exemplo Prático de De / Para

#### 🔴 Antes (FormDin4 - `controllers/V_telefone_orgao.class.php`)
```php
class V_telefone_orgao
{
    private $dao = null;

    public function __construct() {
        $this->dao = new V_telefone_orgaoDAO();
    }
    
    private function filtraConsulta( $where=null ) {
        $where['CSTATUS']='A';
        $where['CAMBITO']='I';
        return $where;
    }
    
    private function trataDados( $listTelefoneOrgao ) {
        if( is_array($listTelefoneOrgao) && !empty($listTelefoneOrgao) ){
            foreach ($listTelefoneOrgao['TELEFONEPRINCIPAL'] as $key => $telefonePrincipal) {
                if($telefonePrincipal=='Sim'){
                    $listTelefoneOrgao['INUMEROTELEFONE'][$key]='<b>'.$listTelefoneOrgao['INUMEROTELEFONE'][$key].'</b>';
                }
            }
        }
        return $listTelefoneOrgao;
    }
    
    public function selectAll( $orderBy=null, $where=null ) {
        $where = $this->filtraConsulta($where);
        $result = $this->dao->selectAll( $orderBy, $where );
        $result = $this->trataDados( $result );
        return $result;
    }
}
```

#### 🟢 Depois (Adianti - `app/<nome_sistema>/control/controllers/TelefoneOrgaoController.php`)
```php
class TelefoneOrgaoController
{
    /**
     * Retorna a lista de telefones aplicando filtros de negócio obrigatórios.
     */
    public static function getTelefonesOrgao($orderBy = 'icodigo', $filters = [])
    {
        try {
            TTransaction::open(Constantes::DATABASE_MAIN);
            
            $criteria = new TCriteria;
            
            // 1. Aplicação das Regras de Negócio Fixas (Filtros Legados de filtraConsulta)
            $criteria->add(new TFilter('cstatus', '=', 'A'));
            $criteria->add(new TFilter('cambito', '=', 'I'));
            
            // 2. Aplicação de filtros dinâmicos de busca vindos da View
            if (!empty($filters['icodigo'])) {
                $criteria->add(new TFilter('icodigo', '=', $filters['icodigo']));
            }
            if (!empty($filters['snome'])) {
                $criteria->add(new TFilter('snome', 'like', "%{$filters['snome']}%"));
            }
            
            // Propriedade de ordenação
            if ($orderBy) {
                $criteria->setProperty('order', $orderBy);
            }
            
            $repository = new TRepository('TelefoneOrgao');
            $objects = $repository->load($criteria);
            
            TTransaction::close();
            
            return $objects;
            
        } catch (Exception $e) {
            TTransaction::rollback();
            throw $e;
        }
    }
}
```

---

## 2. Lidando com `trataDados()` (Estilização vs Lógica)

No legado, o controller embutia tags HTML (ex: `<b>`) nos dados brutos. No Adianti, separamos rigorosamente:
1. **Lógica de Dados**: Permanece no Controller (ex: identificar se o telefone é principal).
2. **Estilização de Apresentação**: Move-se para o *Transformer* da coluna do Datagrid na View (conforme detalhado na skill [**adianti-list-column**](skills/adianti-list-column/SKILL.md)).

### 🟢 Exemplo de Transformer da View para Substituir o `trataDados` Legado
```php
$column_telefone = new TDataGridColumn('inumerotelefone', "Telefone", 'center');
$column_telefone->setTransformer(function($value, $object, $row) {
    if ($object->telefoneprincipal === 'Sim') {
        return "<b>{$value}</b>";
    }
    return $value;
});
```

---

## 3. Controladores para Stored Procedures

> [!IMPORTANT]
> Para cada Stored Procedure legado (geralmente arquivos `controllers/Sp_...class.php`), **DEVE** ser criado um controlador correspondente sob a pasta `app/<nome_sistema>/control/controllers/`.
> 
> A controller da Procedure atuará como a camada de entrada para a View e delegará a chamada segura ao DAO da procedure (que fica em `app/<nome_sistema>/control/dao/`).

### 🟢 Exemplo Prático de Controller de Procedure
```php
class SpHierarquiaOrgaoController
{
    /**
     * Executa e retorna os dados da Stored Procedure Hierarquia Orgao
     */
    public static function execProcedure($icodigo, $itipo, $stipo)
    {
        try {
            // Delegação para o DAO da Procedure
            return SpHierarquiaOrgao::execProcedure($icodigo, $itipo, $stipo);
        } catch (Exception $e) {
            throw $e;
        }
    }
}
```

---

## 🏁 Checklist de Conversão de Controllers
- [ ] A classe de controle foi colocada sob o namespace do sistema (`app/<nome_sistema>/control/controllers/`)?
- [ ] Para Stored Procedures (ex: `Sp_...`), foi criada uma controller correspondente que delega a chamada para a DAO da SP?
- [ ] A abertura e fechamento de transações (`TTransaction::open` / `TTransaction::close`) e a captura de erros (`TTransaction::rollback`) foram implementados?
- [ ] Os filtros obrigatórios originais (como `CSTATUS='A'`) foram devidamente embutidos na criação do `TCriteria`?
- [ ] A estilização visual (ex: `<b>`) contida anteriormente no controller foi transferida para os *Transformers* do Datagrid na View?
- [ ] Não há vazamentos de conexão (TTransaction fechada com segurança em blocos `finally` ou `catch`)?
