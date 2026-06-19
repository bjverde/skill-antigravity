---
name: FormDin 4 to Adianti Complete Migration Orchestrator
description: Orquestrador completo para migração sequencial e coordenada de um módulo inteiro do FormDin 4 para o Adianti.
---

# 🚀 Orquestrador de Migração Completa: FormDin 4 para Adianti

Esta meta-skill guia o Agente de IA na execução passo a passo e orquestrada de uma migração completa do FormDin 4 para o Adianti. Ela coordena as demais sub-skills especializadas em uma sequência lógica obrigatória para garantir integridade, qualidade de código e conformidade com a arquitetura final.

---

## 📐 Fluxo Sequencial de Execução

> [!IMPORTANT]
> **Fase de Setup Obrigatória**: Antes de planejar ou iniciar qualquer ação de migração, o Agente de IA **DEVE** perguntar ativamente e obter do usuário as seguintes informações:
> 1. **Pasta de Destino**: O caminho absoluto ou relativo no File System onde os arquivos gerados serão salvos.
> 2. **Nome do Módulo**: O nome do módulo que definirá a estrutura do diretório da aplicação, a ser criado em `<pasta_de_destino>/app/control/<nome_modulo>/` (e caminhos correspondentes).
>
> Não prossiga sem que o usuário informe estes dois parâmetros.

A migração de qualquer módulo ou sistema legado deve seguir rigorosamente a ordem abaixo. O Agente **NÃO** deve pular fases ou iniciar telas (Views) antes que as dependências de persistência (Models) e constantes estejam completamente prontas.

| Ordem | Fase da Migração | Skill Especializada | Caminho Destino Recomendado |
| :---: | :--- | :--- | :--- |
| **1** | Constantes Globais (Constantes) | [**formdin-migration-constantes**](../formdin-migration-constantes/SKILL.md) | `<pasta_de_destino>/app/control/Constantes.class.php` |
| **2** | Persistência (Models & DAOs) | [**formdin-migration-dao-model**](../formdin-migration-dao-model/SKILL.md) | `<pasta_de_destino>/app/model/` (Tabelas)<br>`<pasta_de_destino>/app/control/<nome_modulo>/dao/` (Procedures) |
| **3** | Regras de Negócio (Controllers) | [**formdin-migration-controller**](../formdin-migration-controller/SKILL.md) | `<pasta_de_destino>/app/control/<nome_modulo>/controllers/` |
| **4** | Apresentação (Views/Telas) | [**formdin-migration-view**](../formdin-migration-view/SKILL.md) | `<pasta_de_destino>/app/control/<nome_modulo>/views/` |
| **5** | Navegação (Menu Dinâmico) | [**formdin-migration-menu**](../formdin-migration-menu/SKILL.md) | `<pasta_de_destino>/menuBuilderMPDFT.php` |
| **6** | Configuração do Servidor | [**formdin-migration-servidorconfig**](../formdin-migration-servidorconfig/SKILL.md) | `<pasta_de_destino>/app/ServidorConfig.class.php` |

---

## 🛠️ Procedimento Interno Passo a Passo

### 🔑 Fase 1: Constantes Globais (Constantes)
1. Ative a skill [**formdin-migration-constantes**](../formdin-migration-constantes/SKILL.md).
2. Localize o arquivo `includes/constantes.php` legado no FormDin 4.
3. Se o arquivo `<pasta_de_destino>/app/control/Constantes.class.php` já existir, mescle as novas constantes preservando os métodos e constantes existentes. Caso contrário, crie-o do zero usando o template padrão.

### 🎬 Fase 2: Mapeamento de Persistência (Models & DAOs)
1. Ative a skill [**formdin-migration-dao-model**](../formdin-migration-dao-model/SKILL.md).
2. Localize todos os arquivos `*VO.class.php` (a serem extintos) e `*DAO.class.php` na pasta `dao/` legado do FormDin.
3. Para tabelas de dados:
   - Crie uma classe Model que estende `TRecord` sob a pasta `<pasta_de_destino>/app/model/`.
   - Adicione todas as colunas mapeadas utilizando `parent::addAttribute()` no construtor.
4. Para Stored Procedures (geralmente prefixadas com `Sp_` ou `sp_`):
   - Crie uma classe DAO dedicada em `<pasta_de_destino>/app/control/<nome_modulo>/dao/` executando a procedure com `PDO` obtido de `TTransaction::get()`.

### ⚡ Fase 3: Mapeamento dos Controladores (Controllers)
1. Ative a skill [**formdin-migration-controller**](../formdin-migration-controller/SKILL.md).
2. Localize todos os arquivos de controller legados sob a pasta `controllers/` legado.
3. Crie os novos controladores correspondentes estendendo a lógica na pasta `<pasta_de_destino>/app/control/<nome_modulo>/controllers/`.
4. Garanta a abertura e o fechamento correto das conexões PDO (`TTransaction::open`, `TTransaction::close`, `TTransaction::rollback`).
5. Transfira a lógica de tratamento de dados brutos (`trataDados`) que tenha caráter visual para os *Transformers* da Datagrid na View.

### 🖥️ Fase 4: Migração de Apresentação (Views)
1. Ative a skill [**formdin-migration-view**](../formdin-migration-view/SKILL.md).
2. Localize as telas legadas sob a pasta `modulos/` legado.
3. Crie as novas páginas Adianti que estendem `TPage` (ou `TWindow` se forem popups) na pasta `<pasta_de_destino>/app/control/<nome_modulo>/views/`.
4. Substitua os componentes do formulário FormDin pelos equivalentes Bootstrap do Adianti (`BootstrapFormBuilder`, `TEntry`, `TCombo`, etc.).
5. Redirecione os eventos (`switch($acao)`) usando o sistema de `TAction` nativo.
6. Use `BootstrapDatagridWrapper` para grids sofisticadas e aplique a formatação correta de colunas com a skill [**adianti-list-column**](../adianti-list-column/SKILL.md).

### 🗺️ Fase 5: Integração de Menus (Menu)
1. Ative a skill [**formdin-migration-menu**](../formdin-migration-menu/SKILL.md).
2. Mapeie o menu legado construído anteriormente com `TMenuDhtmlx`.
3. Registre as novas Views do Adianti dinamicamente usando a estrutura `TFormDinMenuBuilder` em `<pasta_de_destino>/menuBuilderMPDFT.php`.

### ⚙️ Fase 6: Configuração do Servidor (ServidorConfig)
1. Ative a skill [**formdin-migration-servidorconfig**](../formdin-migration-servidorconfig/SKILL.md).
2. Extraia o nome do arquivo de configuração (`NOME_ARQUIVO_CONFIG`) do arquivo `controllers/ServidorConfig.class.php` do FormDin 4.
3. Crie e estruture a nova classe em `<pasta_de_destino>/app/ServidorConfig.class.php` com base no exemplo fornecido.

---

## 🏁 Checklist de Conclusão do Orquestrador
- [ ] **Constantes Globais:** Todas as constantes de `includes/constantes.php` foram migradas e mescladas com sucesso para a classe `Constantes.class.php`?
- [ ] **Persistência Completa:** Todos os VOs/DAOs e Procedures correspondentes foram migrados para `models/` e `control/dao/`?
- [ ] **Lógica Isolada:** As controllers do Adianti encapsulam todas as buscas e transações com tratamento de erro?
- [ ] **Telas Reescritas:** As Views do Adianti estendem `TPage`, estão populadas via controllers e são responsivas?
- [ ] **Apresentação Premium:** As datagrids usam `BootstrapDatagridWrapper` e os transformers corretos para formatação de dados visuais?
- [ ] **Integração de Menu:** As novas páginas foram devidamente integradas ao menu com checagem de grupo e acessibilidade?
- [ ] **Configuração do Servidor:** A classe `ServidorConfig` foi migrada e implementada com a constante de arquivo `.ini` do FormDin 4?
