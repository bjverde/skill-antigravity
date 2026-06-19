---
name: FormDin4 Constantes to Adianti Migration
description: Guia completo para migrar constantes legadas (includes/constantes.php) do FormDin4 para a classe centralizada Constantes.class.php no Adianti framework.
---

# 🗺️ Migração: Constantes (FormDin4 para Adianti)

> [!NOTE]
> No FormDin 4, constantes gerais e configurações globais eram comumente definidas em arquivos como `includes/constantes.php` usando a função global do PHP `define()`.
> No Adianti/FormDin 5 adotado pelo MPDFT, centralizamos todas as constantes de banco, models, grupos de acesso, layout e botões em uma única classe utilitária de controle chamada `Constantes.class.php`, localizada em `<pasta_de_destino>/app/control/Constantes.class.php`.

---

## 📐 Padrões Técnicos e Mapeamento

Ao migrar constantes de um sistema legado, o Agente de IA deve garantir que todas as definições globais sejam convertidas em constantes de classe (`const`) dentro da classe `Constantes`, respeitando a formatação e preservando a infraestrutura existente de métodos auxiliares e definições de layout/design system.

### 1. Tabela De / Para: Conversão e Estrutura

| Elemento / Regra | Padrão FormDin4 (Legado) | Padrão Adianti MPDFT (Destino) |
| :--- | :--- | :--- |
| **Localização do Arquivo** | `includes/constantes.php` | `<pasta_de_destino>/app/control/Constantes.class.php` |
| **Sintaxe de Definição** | `define('CONSTANT_NAME', 'value');` | `const CONSTANT_NAME = 'value';` (dentro da classe `Constantes`) |
| **Concatenação Dinâmica** | `define('A', B . '/C');` | `const A = self::B . '/C';` (se referenciar outra constante de classe) |
| **Infraestrutura e Helpers** | Não se aplicava | Preservar `__construct()`, `getObjTLabel()`, `novoRegistro()`, `getDataGridActionDetalhar()` e constantes visuais de botões. |

---

### 2. Template e Estrutura da Classe `Constantes`

O arquivo final em `<pasta_de_destino>/app/control/Constantes.class.php` deve manter e conter a seguinte estrutura básica:

```php
<?php
class Constantes
{
	// --- DATABASE -----
	const DATABASE_ACESSO      = 'mpdft_acesso';
	const DATABASE_MAINDATABASE= 'maindatabase';
	const DATABASE_PERMISSION  = 'permission';

	//--- MODEL MPDFT -----
	const MODEL_PESSOA    = 'Pessoa';
	const MODEL_REGISTRO  = 'RegistroAcesso';
	const MODEL_TREGIAOADM = 'TRegiaoAdministrativa';

	// --- GRUPO de Acesso -----
	const GRP_STI     = 'sisas-sti';
	const GRP_ADMIN   = 'sisas-admin';
	const GRP_PUBLICO = 'publico';

	//--- LAYOUT -----
	const LAYOUT_FONT_SIZE = '14px';
	const LAYOUT_COR_CAMPO_OBRIGATORIO = '#ff0000';
	const GRID_NUMERO_REGISTROS = 20;
	const GRID_HEIGHT = 320;
	const GRID_STYLE_WIDTH = 'width: 100%';

	//Padrão de icones e cores das ações mais comuns
	const BTN_FIND_COR   = 'blue';
	const BTN_SAVE_COR   = 'green';
	const BTN_UPDATE_COR = '#FFC107';
	const BTN_DELETE_COR = 'red';
	const BTN_CLEAR_COR  = '#dd5a43';

	const BTN_FIND_ICONE   = 'fa:search';
	const BTN_SAVE_ICONE   = 'fa:save';
	const BTN_UPDATE_ICONE = 'far:edit';
	const BTN_DELETE_ICONE = 'far:trash-alt';
	const BTN_CLEAR_ICONE  = 'fa:eraser';
	const BTN_DETAIL_ICONE = 'far:eye';

	const BTN_FIND   = self::BTN_FIND_ICONE . ' ' .self::BTN_FIND_COR;
	const BTN_SAVE   = self::BTN_SAVE_ICONE . ' ' .self::BTN_SAVE_COR;
	const BTN_UPDATE = self::BTN_UPDATE_ICONE . ' '.self::BTN_UPDATE_COR;
	const BTN_DELETE = self::BTN_DELETE_ICONE . ' '.self::BTN_DELETE_COR;
	const BTN_CLEAR  = self::BTN_CLEAR_ICONE . ' ' .self::BTN_CLEAR_COR;
	const BTN_DETAIL = self::BTN_DETAIL_ICONE . ' '.self::BTN_UPDATE_COR;

	// <--- CONSTANTES DE NEGÓCIO E MIGRADA AQUI --->

	public function __construct() {}

	/**
	 * Retorna um objeto TLabel com o label, fonte padrão e a cor
	 * padrão para campos obrigatórios ou não
	 * @param string $label  01 - texto do label
	 * @param bool $required 02 - DEFAULT = False, campo obrigatório ou não
	 * @return TLabel
	 */
	public static function getObjTLabel(string $label, bool $required = FALSE): TLabel
	{
		$objLabel = new TLabel($label, null, Constantes::LAYOUT_FONT_SIZE);
		if ($required) {
			$objLabel = new TLabel($label, Constantes::LAYOUT_COR_CAMPO_OBRIGATORIO, Constantes::LAYOUT_FONT_SIZE);
		}
		return $objLabel;
	}
}
```

> [!IMPORTANT]
> Se o arquivo de destino `<pasta_de_destino>/app/control/Constantes.class.php` já existir, **NUNCA** o sobrescreva completamente de forma cega.
> Você deve ler o arquivo existente e **mesclar** as novas constantes importadas de `includes/constantes.php`, mantendo as constantes de banco de dados, models, grupos de acesso, layout e métodos utilitários existentes intactos.

---

## 🛠️ Procedimento de Migração Passo a Passo

Sempre que realizar a migração de constantes do sistema legado, execute o seguinte procedimento:

### Passo 1: Análise e Extração das Constantes Legadas
1. Localize o arquivo `includes/constantes.php` na estrutura legada do FormDin4.
2. Leia o arquivo e identifique todas as declarações de constantes via `define('NOME', 'valor')` ou `const NOME = 'valor'`.
3. Separe as constantes específicas de negócio (como labels de tabelas, caminhos de arquivo, tipos ou chaves de negócio) das configurações de ambiente que devem ir para o arquivo `.ini` (conforme a skill `formdin-migration-servidorconfig`).

### Passo 2: Conversão de Sintaxe e Concatenação
1. Converta a sintaxe global para a sintaxe de classe:
   - *Antes*: `define('LABEL_SITUACAO_ATIVO', 'Ativo');`
   - *Depois*: `const LABEL_SITUACAO_ATIVO = 'Ativo';`
2. Corrija concatenações dinâmicas que façam referência a outras constantes. Use o prefixo `self::`:
   - *Antes*: `define('SUB_DIRETORIO', DIRETORIO_RAIZ . '/modulo');`
   - *Depois*: `const SUB_DIRETORIO = self::DIRETORIO_RAIZ . '/modulo';`

### Passo 3: Mesclagem no Arquivo Destino
1. Localize ou crie o arquivo `<pasta_de_destino>/app/control/Constantes.class.php`.
2. Se o arquivo já existir:
   - Localize o final do bloco de declaração de constantes (antes do método `__construct()`).
   - Insira as novas constantes de negócio de forma organizada, utilizando comentários descritivos (ex: `//--- CONSTANTES DE NEGOCIO MIGRADA ---`).
3. Se o arquivo não existir:
   - Crie-o utilizando o template padrão listado acima e inclua as novas constantes.

---

## 🏁 Checklist de Conclusão

- [ ] Todas as constantes globais do `includes/constantes.php` foram mapeadas e migradas para `Constantes.class.php`?
- [ ] A sintaxe `define()` foi convertida com sucesso para `const` dentro do escopo da classe `Constantes`?
- [ ] Concatenações dinâmicas que referenciam outras constantes foram convertidas para usar o operador de escopo `self::`?
- [ ] Os métodos utilitários como `getObjTLabel()` e `novoRegistro()` (se existentes) foram rigorosamente preservados sem alterações funcionais?
- [ ] A formatação do arquivo PHP segue o padrão do framework (tabulações, chaves, alinhamento de atribuições)?
