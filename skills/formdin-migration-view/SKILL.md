---
name: FormDin4 Module to Adianti View Migration
description: Guia completo de migração de telas legadas (modulos/*) para Adianti Views (app/control/<nome_sistema>/views/), com mapeamento de componentes (de-para) e redirecionamento de eventos.
---

# 🖥️ Migração: View (Telas FormDin4 para Adianti)

Esta skill guia o Agente de IA na reescrita de telas legadas contidas na pasta `modulos/` do FormDin4 para o padrão de Views (`TPage`, `BootstrapFormBuilder`, `TDataGrid`) do Adianti Framework, mapeando precisamente cada controle e redirecionamento de evento.

---

## 📐 Tabela De / Para: Componentes de Tela

Ao migrar uma view legado, use a tabela abaixo para converter os componentes estruturais:

| Elemento FormDin4 | Equivalente Adianti | Exemplo de Implementação no Adianti |
| :--- | :--- | :--- |
| `$frm = new TForm('Titulo', larg);` | `BootstrapFormBuilder` | `$this->form = new BootstrapFormBuilder('form_name');` |
| `$frm->setShowCloseButton(false);` | *Nativo em TWindow/TFrame* | Não aplicável no construtor de formulários. |
| `$frm->setMaximize(true);` | `$this->form->setUseButton();` | Em diálogos, pode-se usar controle de tamanho. |
| `$frm->addHiddenField('CAMPO');` | `THidden` | `$campo = new THidden('campo');` |
| `$frm->addTextField('C', 'L', tm);` | `TEntry` | `$campo = new TEntry('campo');` |
| `$frm->addNumberField('C', 'L', tm);` | `TNumeric` ou `TEntry` | `$campo = new TNumeric('campo', 0, ',', '.');` |
| `$frm->addSelectField('C', 'L', req, $it);` | `TCombo` ou `TDBCombo` | `$campo = new TCombo('campo'); $campo->addItems($it);` |
| `$frm->addMemoField('C', 'L', max, req, c, r);` | `TText` | `$campo = new TText('campo');` |
| `$frm->addButton('Voltar', null, 'Acao');` | `form->addAction(...)` | `$this->form->addAction("Voltar", new TAction([$this, 'onVoltar']), 'fas:arrow-left');` |
| `$gride = new TGrid('gd', 'Tit', $dados);` | `BootstrapDatagridWrapper` | `$this->datagrid = new BootstrapDatagridWrapper(new TDataGrid);` |
| `$gride->addColumn('C', 'L');` | `TDataGridColumn` | `$col = new TDataGridColumn('c', 'L', 'left');` |
| `$frm->addHtmlField('gride', $gride);` | `TPanelGroup` ou `TVBox` | `$panel = new TPanelGroup; $panel->add($this->datagrid);` |

---

## 🔄 Fluxo de Eventos: De switch($acao) para TAction

No FormDin4, o fluxo de envio e clique de botões era concentrado em um bloco `switch($acao)` que manipulava posts e redirecionava via `$frm->redirect(...)`. No Adianti, o fluxo é totalmente orientado a objetos através de ações explícitas (`TAction`) vinculadas a métodos da classe.

### 🔴 Antes (FormDin4 - switch legado)
```php
$acao = isset($acao) ? $acao : null;
switch( $acao ) {
    case 'Voltar':
        $frm->redirect('v_telefone_orgao.php', null, true);
        break;
    case 'gd_pessoas':
        $arrayPost = array('ICODIGOORGAO' => PostHelper::getArray('ICODIGO'));
        $frm->redirect('v_telefone_pessoa.php', null, true, $arrayPost);
        break;
}
```

### 🟢 Depois (Adianti - Métodos de Ação em TPage)
```php
public function onVoltar($param = null)
{
    // Redireciona de forma limpa para outra página TPage
    TApplication::loadPage('TelefoneOrgaoList', 'onShow');
}

public function onIrParaPessoas($param = null)
{
    // Passa parâmetros chaves no vetor de persistência de tela do Adianti
    $target_params = [
        'ICODIGOORGAO' => $param['key'] // A chave primaria é enviada no clique do botão da grid
    ];
    TApplication::loadPage('TelefonePessoaList', 'onShow', $target_params);
}
```

---

## 📂 Caso de Estudo: Migrando `detalhar_orgao.php`

A view legado `detalhar_orgao.php` exibe o formulário de detalhes de um Órgão (bloqueado para edição/somente leitura) e possui **duas Grids** (uma de telefones associados e outra de vinculação administrativa). Veja como convertemos esse layout complexo.

### 🟢 Conversão Completa para Adianti (Exemplo de View)

Crie uma página do Adianti que carrega a controller, renderiza o formulário principal e acopla os dois Datagrids:

```php
class DetalharOrgaoView extends TPage
{
    private $form;
    private $gridTelefones;
    private $gridHierarquia;
    private static $database = Constantes::DATABASE_MAIN;

    public function __construct($param = null)
    {
        parent::__construct();

        // 1. Instancia o Form do Painel Principal
        $this->form = new BootstrapFormBuilder('form_DetalhesOrgao');
        $this->form->setFormTitle("Detalhes da Unidade");

        // Campos do Formulário (Somente Leitura) - Siga a skill adianti-form-field-style
        $icodigo = new THidden('ICODIGO');
        
        $ssigla = new TEntry('SSIGLA');
        $ssigla->setEditable(false);
        
        $snome = new TEntry('SNOME');
        $snome->setEditable(false);
        
        $semail = new TEntry('SEMAIL');
        $semail->setEditable(false);
        
        $sendereco = new TEntry('SENDERECO');
        $sendereco->setEditable(false);
        
        $tatribuicao = new TText('TATRIBUICAO');
        $tatribuicao->setEditable(false);

        // Adicionando ao formulário em linhas
        $this->form->addFields([$icodigo]);
        $this->form->addFields([new TLabel('Sigla:')], [$ssigla], [new TLabel('Nome:')], [$snome]);
        $this->form->addFields([new TLabel('E-mail:')], [$semail], [new TLabel('Endereço:')], [$sendereco]);
        $this->form->addFields([new TLabel('Atribuição:')], [$tatribuicao]);

        // Ações do Formulário
        $this->form->addAction("Voltar", new TAction([$this, 'onVoltar']), 'fas:arrow-left #000000');

        // 2. Grid 1: Lista de Telefones
        $this->gridTelefones = new BootstrapDatagridWrapper(new TDataGrid);
        $this->gridTelefones->setHeight(150);

        $col_andar = new TDataGridColumn('sandar', 'Andar', 'left');
        $col_sala  = new TDataGridColumn('ssala', 'Sala', 'left');
        
        // Exemplo de Ordenação e Transfomer (Conforme adianti-list-column)
        $col_tel   = new TDataGridColumn('inumerotelefone', 'Telefone', 'center');
        $col_tel->setTransformer(function($value, $object, $row) {
            if ($object->itelefoneprincipal === $value) {
                return "<b>{$value}</b>";
            }
            return $value;
        });

        $this->gridTelefones->addColumn($col_andar);
        $this->gridTelefones->addColumn($col_sala);
        $this->gridTelefones->addColumn($col_tel);

        // Ação na Grid 1 (Botão Pessoas)
        $act_pessoas = new TDataGridAction(['DetalharOrgaoView', 'onIrParaPessoas'], ['key' => '{icodigo}']);
        $act_pessoas->setImage('fas:users #478fca');
        $act_pessoas->setLabel('Pessoas');
        $this->gridTelefones->addAction($act_pessoas);
        $this->gridTelefones->createModel();

        // Painel para conter a Grid 1
        $panelTelefones = new TPanelGroup("Lista de Telefones");
        $panelTelefones->add($this->gridTelefones);

        // 3. Montagem do Layout Completo na Tela
        $container = new TVBox;
        $container->style = 'width: 100%';
        $container->add($this->form);
        $container->add($panelTelefones);

        parent::add($container);
    }

    public function onVoltar($param = null)
    {
        TApplication::loadPage('TelefoneOrgaoList', 'onShow');
    }

    public function onIrParaPessoas($param = null)
    {
        TApplication::loadPage('TelefonePessoaList', 'onShow', ['ICODIGOORGAO' => $param['key']]);
    }

    /**
     * Ciclo de Vida: Carrega os dados na tela a partir da Controller
     */
    public function onShow($param = null)
    {
        if (isset($param['key'])) {
            $id = $param['key'];
            
            // Busca dados da controller unificada (Business Rules)
            $orgao = OrgaoController::getOrgaoDetalhado($id);
            $telefones = OrgaoController::getTelefonesOrgao($id);
            
            // Popula os campos do Formulário
            $this->form->setData($orgao);

            // Popula as Grids com dados
            $this->gridTelefones->clear();
            if ($telefones) {
                foreach ($telefones as $telefone) {
                    $this->gridTelefones->add($telefone);
                }
            }
        }
    }
}
```

---

## 🏁 Checklist de Conversão de Views
- [ ] A view foi convertida em uma classe que estende `TPage` (ou `TWindow` se for popup)?
- [ ] Os campos legados foram remapeados conforme a tabela De/Para de inputs?
- [ ] Os novos campos do formulário foram declarados seguindo o estilo da skill **`adianti-form-field-style`**?
- [ ] Componentes de Datagrid estão usando `BootstrapDatagridWrapper` para renderização elegante?
- [ ] Todas as colunas visíveis possuem ordenação e transformers de formatação apropriados?
- [ ] A lógica de navegação foi removida de scripts legados e implementada via `TAction` e métodos da classe?
- [ ] A carga inicial de dados e grids está centralizada em métodos do ciclo de vida (ex: `onShow`/`onEdit`) consultando a Controller?
