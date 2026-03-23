<?php

/**
 * Exemplo de Modelo Adianti com Relacionamentos e Campos Automáticos
 * Baseado em system/app/model/Pessoa.php
 */
class PessoaExample extends TRecord
{
    const TABLENAME  = 'pessoa';
    const PRIMARYKEY = 'id';
    const IDPOLICY   = 'uuid'; // UUID para chaves primárias (como em VendaCertificado)

    const DELETEDAT  = 'deleted_at';
    const CREATEDAT  = 'created_at';
    const UPDATEDAT  = 'update_at';
    
    // Campo personalizado para o vendedor/usuário que criou o registro
    const CREATED_BY_USER_ID = 'vendedor_id'; 

    private SystemUnit $system_unit;
    private TipoCliente $tipo_cliente;

    /**
     * Constructor method
     */
    public function __construct($id = NULL, $callObjectLoad = TRUE)
    {
        parent::__construct($id, $callObjectLoad);
        parent::addAttribute('system_unit_id');
        parent::addAttribute('tipo_cliente_id');
        parent::addAttribute('nome');
        parent::addAttribute('documento');
        parent::addAttribute('email');
        parent::addAttribute('vendedor_id');
        parent::addAttribute('created_at');
        parent::addAttribute('update_at');
        parent::addAttribute('deleted_at');
    }

    /**
     * RELACIONAMENTO N:1 (Associação) - Lazy Load
     */
    public function get_tipo_cliente()
    {
        if (empty($this->tipo_cliente)) {
            $this->tipo_cliente = new TipoCliente($this->tipo_cliente_id);
        }
        return $this->tipo_cliente;
    }

    /**
     * RELACIONAMENTO 1:N (Coleção)
     */
    public function getPessoaContatos()
    {
        $criteria = new TCriteria;
        $criteria->add(new TFilter('pessoa_id', '=', $this->id));
        return PessoaContato::getObjects($criteria);
    }

    /**
     * Método Auxiliar: Retorna lista de contatos em formato de String
     * Padrão comum em modelos complexos como VendaCertificado
     */
    public function get_contatos_to_string()
    {
        $values = PessoaContato::where('pessoa_id', '=', $this->id)->getIndexedArray('id', 'valor');
        return implode(', ', $values);
    }

    /**
     * HOOK: onBeforeDelete
     * Executado antes da exclusão. Usado para validação de integridade manual.
     */
    public function onBeforeDelete()
    {
        // Verifica se há endereços vinculados
        if (PessoaEndereco::where('pessoa_id', '=', $this->id)->first()) {
            throw new Exception("Não é possível excluir esta pessoa pois ela possui endereços cadastrados.");
        }

        // Verifica se há vendas vinculadas (como em VendaCertificado)
        if (VendaCertificado::where('pessoa_id', '=', $this->id)->first()) {
            throw new Exception("Não é possível excluir esta pessoa pois ela possui vendas vinculadas.");
        }
    }

    /**
     * Exemplo de busca filtrada usando Fluent API
     */
    public static function buscarPorDocumento($doc)
    {
        return self::where('documento', '=', $doc)->first();
    }
}
