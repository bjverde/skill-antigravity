# Skill: Gerador de Telas Adianti Framework (List & Form)

Esta skill fornece diretrizes e templates para a criação de telas de consulta (`List.php`) e cadastro (`Form.php`) utilizando o Adianti Framework, seguindo os padrões do projeto Solubiz/GContabil.

## Padrões Gerais

- **Herança**: Todas as classes de visualização estendem `TPage`.
- **Banco de Dados**: Usar sempre `Constantes::DATABASE_MAIN`.
- **Componentes de UI**: Utilizar `BootstrapFormBuilder` para formulários e `BootstrapDatagridWrapper` para listagens.
- **Tipos de Campo Padrão**:
    - **Texto/Geral**: `TEntry`
    - **Chaves Estrangeiras (FK)**: `TDBCombo`
    - **Datas**: `TDate` ou `TDateTime` (conforme o tipo no banco)
- **Validação de Obrigatoriedade**: Sempre verificar se o campo no banco de dados é `NOT NULL`. Se for, aplicar `$field->addValidation("Label", new TRequiredValidator());`.
- **Metadados de Registro**: Incluir obrigatoriamente os arquivos `include_info_registro_*.php` para manter a rastreabilidade (usuário de criação/alteração e datas).

---

## Template: `<Nome>List.php`

### Estrutura da Classe
```php
class <Nome>List extends TPage
{
    private $form;
    private $datagrid;
    private $pageNavigation;
    private $loaded;
    private $filter_criteria;
    private static $database = Constantes::DATABASE_MAIN;
    private static $activeRecord = '<ModelName>';
    private static $primaryKey = '<pk_field>';
    private static $formName = 'form_<Nome>List';
    private $showMethods = ['onReload', 'onSearch', 'onRefresh', 'onClearFilters', 'onGlobalSearch'];
    private $limit = 20;

    public function __construct($param = null)
    {
        parent::__construct();
        // Configurar adianti_target_container se presente em $param

        $this->form = new BootstrapFormBuilder(self::$formName);
        $this->form->setFormTitle("Listagem de <Nome>");

        // Adicionar campos de filtro (TEntry, TDBCombo, etc.)
        // Exemplo: $id = new TEntry('id');

        // Renderização de Campos
        // $this->form->addFields([new TLabel("ID:")], [$id]);

        // IMPORTANTE: Incluir busca de metadados
        require_once 'include_info_registro_form.php';

        $this->form->setData(TSession::getValue(__CLASS__.'_filter_data'));

        // Ações do Formulário
        $this->form->addAction("Buscar", new TAction([$this, 'onSearch']), 'fas:search #ffffff')->addStyleClass('btn-primary');
        $this->form->addAction("Cadastrar", new TAction(['<Nome>Form', 'onEdit']), 'fas:plus #69aa46');
        $this->form->addAction("Limpar", new TAction([$this, 'onClear']), Constantes::BTN_CLEAR);

        // Datagrid
        $this->datagrid = new BootstrapDatagridWrapper(new TDataGrid);
        $this->datagrid->setId(__CLASS__.'_datagrid');
        $this->datagrid->datatable = 'true';
        $this->datagrid->setHeight(Constantes::GRID_HEIGHT);

        // Colunas
        // $col = new TDataGridColumn('field', 'Label', 'left');
        // $this->datagrid->addColumn($col);

        require_once 'include_info_registro_grid.php';

        // Ações da Grid
        $action_edit = new TDataGridAction(['<Nome>Form', 'onEdit'], ['key' => '{' . self::$primaryKey . '}']);
        $action_edit->setImage('far:edit #478fca');
        $this->datagrid->addAction($action_edit);

        $action_del = new TDataGridAction([$this, 'onDelete'], ['key' => '{' . self::$primaryKey . '}']);
        $action_del->setImage('fas:trash-alt #dd5a43');
        $this->datagrid->addAction($action_del);

        $this->datagrid->createModel();

        // Navegação e Painel
        $this->pageNavigation = new TPageNavigation;
        $this->pageNavigation->setAction(new TAction([$this, 'onReload']));

        $panel = new TPanelGroup();
        $panel->add($this->datagrid);
        $panel->addFooter($this->pageNavigation);

        // Layout (TVBox / TBreadCrumb)
        $container = new TVBox;
        $container->style = 'width: 100%';
        $container->add($this->form);
        $container->add($panel);
        parent::add($container);
    }

    // Métodos obrigatórios: onSearch, onReload, onDelete, onClear, show, manageRow
    // Implementar lógica de filtros em onSearch mapeando os campos do form.
    // Incluir 'include_info_registro_search.php' dentro de onSearch.
}
```

---

## Template: `<Nome>Form.php`

### Estrutura da Classe
```php
class <Nome>Form extends TPage
{
    protected BootstrapFormBuilder $form;
    private static $database = Constantes::DATABASE_MAIN;
    private static $activeRecord = '<ModelName>';
    private static $primaryKey = '<pk_field>';
    private static $formName = 'form_<Nome>Form';

    public function __construct($param = null)
    {
        parent::__construct();
        $this->form = new BootstrapFormBuilder(self::$formName);
        $this->form->setFormTitle("Cadastro de <Nome>");

        $pk = new TEntry(self::$primaryKey);
        $pk->setEditable(false);

        // --- DEFINIÇÃO DOS CAMPOS ---
        // Texto: $nome = new TEntry('nome');
        // FK: $fk_id = new TDBCombo('fk_id', self::$database, 'TargetModel', 'id', '{name}');
        // Data: $data = new TDate('data');
        
        // --- VALIDAÇÃO ---
        // Se NOT NULL no banco: $nome->addValidation("Nome", new TRequiredValidator());

        // --- ADICIONAR AO FORM ---
        // $this->form->addFields([new TLabel("ID:")], [$pk]);

        // Ações
        $this->form->addAction("Salvar", new TAction([$this, 'onSave']), 'fas:save #ffffff')->addStyleClass('btn-primary');
        $this->form->addAction("Limpar", new TAction([$this, 'onClear']), 'fas:eraser #dd5a43');
        $this->form->addAction("Voltar", new TAction(['<Nome>List', 'onShow']), 'fas:arrow-left #000000');

        $container = new TVBox;
        $container->style = 'width: 100%';
        $container->add($this->form);
        parent::add($container);
    }

    public function onSave($param = null)
    {
        try {
            TTransaction::open(self::$database);
            $this->form->validate();
            $data = $this->form->getData();

            $object = new <ModelName>;
            $object->fromArray((array) $data);
            $object->store();

            $data->{self::$primaryKey} = $object->{self::$primaryKey};
            $this->form->setData($data);

            TTransaction::close();
            new TMessage('info', "Registro salvo", new TAction(['<Nome>List', 'onShow']));
        } catch (Exception $e) {
            new TMessage('error', $e->getMessage());
            TTransaction::rollback();
        }
    }

    // Métodos obrigatórios: onEdit, onClear
}
```
