---
name: FormDin4 ServidorConfig to Adianti Migration
description: Guia de migração e criação do arquivo ServidorConfig.class.php de FormDin4 para o Adianti.
---

# Skill: Migração de Configuração do Servidor (FormDin 4 para Adianti)

> [!NOTE]
> No FormDin 4, as configurações do servidor e do ambiente eram lidas e tratadas por controladores específicos da aplicação. No Adianti/FormDin 5, adotamos uma classe estruturada `ServidorConfig` sob a pasta `app/` para gerenciar a leitura e o parsing do arquivo `.ini` do sistema de forma limpa usando a classe utilitária `TFormDinIniFileHandler`.

---

## 📐 Padrões Técnicos e Diretrizes

Todos os arquivos `ServidorConfig.class.php` gerados na pasta de destino devem respeitar rigorosamente a estrutura demonstrada no exemplo [ServidorConfig.class.php](../../../app/control/ServidorConfig.class.php).

| Elemento / Regra | Detalhamento / Diretriz | Exemplo |
| :--- | :--- | :--- |
| **Localização do Destino** | Sempre deve ser gerado no caminho relativo `<pasta_de_destino>/app/ServidorConfig.class.php`. | `C:\destino\app\ServidorConfig.class.php` |
| **Constante da Configuração** | `const NOME_ARQUIVO_CONFIG` deve vir do valor definido no controller herdado do FormDin 4. | `const NOME_ARQUIVO_CONFIG = 'sisas.ini';` |
| **Leitor de INI** | Usar obrigatoriamente a classe utilitária `TFormDinIniFileHandler`. | `$this->formDinIniFile = new TFormDinIniFileHandler($this->ini_path);` |
| **Tratamento de Exceção de Chaves** | No método `getKeyInSection`, capturar `LogicException` para retornar `null` caso a chave não exista na seção. | Ver bloco `try-catch` no exemplo [ServidorConfig.class.php](../../../app/control/ServidorConfig.class.php#L51-L62) |
| **Mapeamento de Drivers PDO** | Método `getPdoDriverKeyInSection` deve mapear de forma uniforme bancos de dados para seus respectivos drivers PDO. | Ver mapeamento no exemplo [ServidorConfig.class.php](../../../app/control/ServidorConfig.class.php#L63-L85) |

---

## 🚀 Procedimento Passo a Passo para o Agente (IA)

Sempre que a fase de migração da configuração do servidor for acionada, siga rigorosamente os passos abaixo:

### Passo 1: Localizar o Arquivo Legado no FormDin 4
1. Localize o arquivo `controllers/ServidorConfig.class.php` na estrutura legada do FormDin 4.
2. Identifique o valor atribuído à constante `NOME_ARQUIVO_CONFIG` (geralmente contendo o nome do arquivo `.ini` da aplicação).

### Passo 2: Criar o Novo Arquivo de Destino
1. Crie o arquivo `<pasta_de_destino>/app/ServidorConfig.class.php`.
2. Escreva o cabeçalho PHP e a definição da classe `ServidorConfig` seguindo exatamente o design do arquivo exemplo:
   - Definição do separador de diretório (`DS`).
   - Mapeamento das propriedades privadas: `$formDinIniFile`, `$ini_path`, `$config`, `$perfilAcesso`, `$perfilAdm`.
   - Implementação do construtor que define o caminho absoluto em `$_SERVER['DOCUMENT_ROOT'] . DS . 'config' . DS . self::NOME_ARQUIVO_CONFIG`.
   - Inicialização das propriedades `$config`, `$perfilAcesso` e `$perfilAdm` mapeadas para as seções `'config'`, `'ds-acesso'` e `'ds-adm'`, respectivamente.

### Passo 3: Adicionar Lógica Robustecida de Chaves e Drivers
1. Garanta a presença dos métodos de consulta genérica: `getSection`, `getKeyInSection` e `getPdoDriverKeyInSection`.
2. Garanta a presença dos getters: `getConfig()`, `getPerfilAcesso()`, `getPerfilAdm()`.

---

## 🏁 Checklist de Conclusão para o Agente

- [ ] A constante `NOME_ARQUIVO_CONFIG` foi atualizada com o valor correto vindo do FormDin 4?
- [ ] O arquivo foi criado exatamente em `<pasta_de_destino>/app/ServidorConfig.class.php`?
- [ ] O construtor lê corretamente o arquivo `.ini` utilizando a classe `TFormDinIniFileHandler`?
- [ ] O método `getKeyInSection` trata corretamente chaves inexistentes retornando `null` sob `LogicException`?
- [ ] O método `getPdoDriverKeyInSection` foi integralmente replicado para suportar os drivers PDO necessários?
