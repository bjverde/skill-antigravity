---
name: FormDin4 Menu to Adianti Menu Migration
description: Guia completo para migração de menus legados (TMenuDhtmlx) do FormDin4 para o padrão de menu dinâmico no Adianti (MPDFT) usando TFormDinMenuBuilder.
-# 🗺️ Migração: Menu (FormDin4 para Adianti MPDFT)

Esta skill guia o Agente de IA na conversão estruturada de menus legados do FormDin4 (gerados por `TMenuDhtmlx`) para o formato de menu dinâmico no Adianti Framework adotado pelo MPDFT, que utiliza a classe `TFormDinMenuBuilder` dentro do arquivo `<pasta_de_destino>/menuBuilderMPDFT.php`.

---

## 📐 Padrões Técnicos e Mapeamento

No FormDin4, os menus eram adicionados via PHP usando a classe `TMenuDhtmlx`. No Adianti (MPDFT), a navegação é construída via código no arquivo `<pasta_de_destino>/menuBuilderMPDFT.php` através de chamadas estruturadas de `$builder->addMenuItem(...)` envelopadas em uma classe e método específicos.

### 1. Estrutura do Arquivo de Menu no Adianti MPDFT

Todo o arquivo `menuBuilderMPDFT.php` deve seguir estritamente o template abaixo:

```php
<?php
class menuBuilderMPDFT
{
    public static function parse($theme)
    {
        $builder = new TFormDinMenuBuilder();

        // <itens de menu adicionados aqui>

        return $builder; // ou finalização da renderização do menu
    }
}
```

### 2. Assinatura dos Métodos de Item de Menu

*   **Antes (FormDin4 - Legado)**:
    ```php
    $menu->add(string $id, ?string $parentId, string $label, ?string $action, ?string $target, ?string $icon);
    ```
*   **Depois (Adianti - MPDFT)**:
    ```php
    $builder->addMenuItem(string $id, ?string $parentId, string $label, ?string $action, string $icon);
    ```

---

### 3. Tabela De / Para: Conversão de Parâmetros

Ao converter cada entrada `$menu->add(...)`, mapeie os parâmetros da seguinte forma:

| Parâmetro FormDin4 | Equivalente Adianti MPDFT | Regras de Migração e Formatação |
| :--- | :--- | :--- |
| **`$id`** | **`$id`** | Preservar a hierarquia. Se o pai for `'1'`, os filhos devem ser `'1.1'`, `'1.2'`, etc. *(Nota: o FormDin4 às vezes usava `'1.0'`, prefira convertê-los para sequenciais iniciando de `.1` no Adianti para maior limpeza).* |
| **`$parentId`** | **`$parentId`** | Manter a referência ao ID do elemento pai (ou `null` para nós raiz). |
| **`$label`** | **`$label`** | Nome amigável em **Pascal Case com espaços**. Se no legado for usado uma constante/define (ex: `TITULO_CATALOGO_PESSOA`), mantenha-a ou substitua pelo texto resolvido caso necessário. |
| **`$action`** | **`$action`** | **Conversão Crítica**: Substitua o caminho do script legado (ex: `modulos/v_telefone_pessoa.php`) pelo nome exato da classe do Adianti em `<sistema>/app/control/<nome_sistema>/views/` (ex: `TelefonePessoaList`). Se for um grupo de menu (sem página direta), defina como `null`. |
| **`$target`** | *N/A* | O parâmetro target é descartado na estrutura do MPDFT. |
| **`$icon`** | **`$icon`** | **Modernização**: Substitua imagens estáticas `.gif`/`.png` por ícones FontAwesome elegantes usando o prefixo `fas:` ou `fab:` e a classe `fa-fw`. Você também pode especificar cores em formato hexadecimal. |

---

### 4. Tabela De / Para: Nomes de Classes View (Exemplos)

Sempre verifique se a classe da View existe sob `<sistema>/app/control/<nome_sistema>/views/` ou gere-a seguindo a convenção de nomes:

| Script Legado (`modulos/`) | Nome da Classe View no Adianti |
| :--- | :--- |
| `v_telefone_pessoa.php` | `TelefonePessoaList` |
| `v_telefone_orgao.php` | `TelefoneOrgaoList` |
| `sp_pesquisar_outrosservicos.php` | `PesquisarOutrosServicosList` ou `PesquisarOutrosServicosForm` |
| `catalogo_pessoa_membros.php` | `CatalogoPessoaMembrosReport` ou `CatalogoPessoaMembrosList` |

---

### 5. Tabela De / Para: Modernização de Ícones

Substitua imagens de baixa resolução por ícones modernos e dinâmicos:

| Ícone Legado | Ícone FontAwesome Sugerido | Exemplo de Código |
| :--- | :--- | :--- |
| `administrator16.gif`, `user.png` | `fas:users fa-fw` ou `fas:user-tie fa-fw` | `'fas:users fa-fw'` |
| `home16.gif`, `orgao.png` | `fas:home fa-fw` ou `fas:building fa-fw` | `'fas:building fa-fw'` |
| `view16.png`, `search.png` | `fas:search fa-fw` ou `fas:binoculars fa-fw` | `'fas:search fa-fw'` |
| `adobe-acrobat-pdf-file-512.png` | `fas:file-pdf fa-fw` | `'fas:file-pdf fa-fw #E53935'` (vermelho elegante) |
| *Imagens sem correspondente claro* | `fas:th-list fa-fw` (ícone padrão para menus gerais) | `'fas:th-list fa-fw'` |

---

## 🛠️ Procedimento de Migração Passo a Passo

Sempre que realizar a migração de um menu, execute o seguinte procedimento:

### Passo 1: Análise e Mapeamento
1. Abra o arquivo de menu do FormDin4 (geralmente `includes/menu.php` ou `menu.xml`).
2. Mapeie todas as entradas `$menu->add`.
3. Para cada script listado no parâmetro `$action` (ex: `modulos/x.php`), localize a correspondente classe de visualização criada sob `app/control/<nome_sistema>/views/` (conforme as diretrizes da `formdin-migration-view`).

### Passo 2: Definir Grupos de Acesso (Segurança MPDFT)
1. No ecossistema MPDFT, o menu é condicionado pelas permissões de grupo.
2. Identifique quais itens requerem privilégios restritos.
3. Insira as chamadas `$builder->addMenuItem` correspondentes no interior dos blocos `if (serviceAccessPermission::usuarioTemGrupo(Constantes::GRP_...))` adequados em `menuBuilderMPDFT.php`.

### Passo 3: Geração do Código
1. Formate as chamadas `$builder->addMenuItem` com os novos IDs higienizados, labels em Pascal Case, ícones FontAwesome modernos (`fas:`) e classes Adianti corretas.

---

## 📂 Caso de Estudo Prático: Migração de `includes/menu.php`

Veja a conversão completa do menu legado do sistema `sigaweb`.

### 🔴 Antes: Código Legado do FormDin4 (`includes/menu.php`)
```php
<?php
$menu = new TMenuDhtmlx();

$menu->add('1', null, 'Consulta', null, null, 'view16.png');
$menu->add('1.0','1','Pessoa','modulos/v_telefone_pessoa.php', null, 'administrator16.gif');
$menu->add('1.1','1','Unidade','modulos/v_telefone_orgao.php', null, 'home16.gif');
$menu->add('1.2','1','Localização de Outros Serviço','modulos/sp_pesquisar_outrosservicos.php', null, null);

$menu->add('2', null, 'Catalogo Telefônico', null, null, 'adobe-acrobat-pdf-file-512.png');
$menu->add('2.1','2',TITULO_CATALOGO_PESSOA_MEMBRO,'modulos/catalogo_pessoa_membros.php', null, 'adobe-acrobat-pdf-file-512.png');
$menu->add('2.2','2',TITULO_CATALOGO_PESSOA_SERVIDOR,'modulos/catalogo_pessoa_servidores.php', null, 'adobe-acrobat-pdf-file-512.png');
$menu->add('2.3','2',TITULO_CATALOGO_PESSOA_GERAL,'modulos/catalogo_pessoa_geral.php', null, 'adobe-acrobat-pdf-file-512.png');

$menu->getXml();
?>
```

### 🟢 Depois: Código Migrado para Adianti (`menuBuilderMPDFT.php` em `<pasta_de_destino>/menuBuilderMPDFT.php`)
```php
<?php
class menuBuilderMPDFT
{
    public static function parse($theme)
    {
        $builder = new TFormDinMenuBuilder();

        // 1. Grupo Raiz: Consulta (Público ou Geral)
        $builder->addMenuItem('1', null, 'Consulta', null, 'fas:search fa-fw');

        // Submenus de Consulta (Mapeados para as classes correspondentes em app/control/<nome_sistema>/views/)
        // Nota: os IDs foram higienizados de 1.0 para 1.1, 1.1 para 1.2, etc.
        $builder->addMenuItem('1.1', '1', 'Pessoa', 'TelefonePessoaList', 'fas:users fa-fw');
        $builder->addMenuItem('1.2', '1', 'Unidade', 'TelefoneOrgaoList', 'fas:building fa-fw');
        $builder->addMenuItem('1.3', '1', 'Localização de Outros Serviços', 'PesquisarOutrosServicosList', 'fas:map-marked-alt fa-fw');

        // 2. Grupo Raiz: Catálogo Telefônico
        $builder->addMenuItem('2', null, 'Catálogo Telefônico', null, 'fas:book fa-fw');

        // Submenus do Catálogo Telefônico (com constantes de título mantidas ou resolvidas)
        // Mapeados para classes de Relatório/Listagem em formato PDF/Visual
        $builder->addMenuItem('2.1', '2', TITULO_CATALOGO_PESSOA_MEMBRO, 'CatalogoPessoaMembrosReport', 'fas:file-pdf fa-fw #E53935');
        $builder->addMenuItem('2.2', '2', TITULO_CATALOGO_PESSOA_SERVIDOR, 'CatalogoPessoaServidoresReport', 'fas:file-pdf fa-fw #E53935');
        $builder->addMenuItem('2.3', '2', TITULO_CATALOGO_PESSOA_GERAL, 'CatalogoPessoaGeralReport', 'fas:file-pdf fa-fw #E53935');

        return $builder;
    }
}
```->addMenuItem('2.3', '2', TITULO_CATALOGO_PESSOA_GERAL, 'CatalogoPessoaGeralReport', 'fas:file-pdf fa-fw #E53935');
```

---

## 🏁 Checklist de Conclusão

- [ ] Todos os scripts legados (`modulos/*.php`) foram substituídos por suas respectivas classes View do Adianti (`TPage`)?
- [ ] A hierarquia de IDs foi normalizada, evitando IDs decimais inconsistentes (ex: usar `'1.1'` em vez de `'1.0'`)?
- [ ] Todas as imagens antigas (`.png`, `.gif`) foram modernizadas para ícones do FontAwesome utilizando o prefixo `fas:` ou `fab:` e acompanhadas de `fa-fw`?
- [ ] Os itens restritos foram colocados dentro das condicionais de grupos de acesso (`serviceAccessPermission::usuarioTemGrupo`)?
- [ ] Foi executado ou recomendado o SQL de registro de permissões (`system_program` / `system_group_program`) para todas as novas classes registradas no menu?
