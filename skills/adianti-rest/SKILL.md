---
name: Adianti REST Services
description: Guia de padrões para criação, configuração e consumo de serviços REST, RESTful e RESTful seguro com token JWT no Adianti Framework.
---

# 🌐 Adianti REST Services Skill

> [!NOTE]
> Este guia estabelece os padrões e práticas recomendadas para a implementação de Web Services no Adianti Framework (v8 e anteriores), detalhando as abordagens de serviços REST tradicionais, RESTful baseados em rotas e RESTful seguros utilizando tokens JWT.

---

## 📐 Padrões Técnicos

| Elemento | Regra | Detalhamento |
| :--- | :--- | :--- |
| **Classe Base** | Herdar de `AdiantiRecordService` | Garante os métodos automáticos CRUD: `load()`, `store()`, `delete()`, `loadAll()` e `deleteAll()`. |
| **Constantes da Classe** | `DATABASE`, `ACTIVE_RECORD` | Constantes obrigatórias indicando o arquivo `.ini` de banco de dados e a respectiva model (ex: `Contact`). |
| **Segurança por Classe** | `REST_KEY` (Opcional - v8+) | Define uma chave de acesso única para aquela classe de serviço específica, sem precisar usar a global. |
| **Rotas RESTful** | Padrão de 3 regras por recurso | Necessita de 3 regras de reescrita no [.htaccess](../../.htaccess) para mapear `/recurso/<id>`, `/recurso/<id>/action` e `/recurso`. |
| **Autenticação JWT** | Rota de autenticação dedicada | Rota `/auth/<user>/<senha>` mapeada para a classe `ApplicationAuthenticationRestService`. |
| **Transações** | Abrir/Fechar `TTransaction` explicitamente | Em métodos personalizados, abrir com `TTransaction::open('conexao')` e fechar com `TTransaction::close()`. |

---

## 🚀 Habilitação do Servidor

Para colocar o servidor REST ou RESTful no ar, o primeiro passo é renomear o arquivo do servidor no diretório raiz:

- **Para REST Comum (Sem segurança nativa)**:
  Renomear `rest.php.dist` para `rest.php`.
  > [!WARNING]
  > Este método expõe as classes do framework sem controle prévio. É fundamental implementar validações ou filtros dentro de `rest.php`.

- **Para RESTful Seguro (Com Basic/JWT)**:
  Renomear `rest-secure.php.dist` para `rest.php`.

---

## 🛠️ Como Criar uma Classe de Serviço

A classe de serviço atua como fachada, expondo dados da tabela representados por uma model.

### 1. Criar a Model (se já não existir)
Criar em `app/model/<Model>.php`:
```php
<?php
class Contact extends TRecord
{
    const TABLENAME = 'contact';
    const PRIMARYKEY= 'id';
    const IDPOLICY =  'max'; // {max, serial}
    
    public function __construct($id = NULL, $callObjectLoad = TRUE)
    {
        parent::__construct($id, $callObjectLoad);
        parent::addAttribute('name');
        parent::addAttribute('email');
        parent::addAttribute('number');
        parent::addAttribute('address');
        parent::addAttribute('notes');
    }
}
```

### 2. Criar a Service
Criar em `app/service/<Model>RestService.php`. Ela deve herdar de `AdiantiRecordService`:
```php
<?php
class ContactRestService extends AdiantiRecordService
{
    const DATABASE      = 'contacts'; // Refere-se a app/config/contacts.ini
    const ACTIVE_RECORD = 'Contact';   // Refere-se à model Contact
    
    // OPCIONAL (v8+): Chave de autorização específica para esta classe
    // const REST_KEY = 'minha_chave_secreta_super_forte_aqui';
}
```

### 3. Métodos Personalizados e Transações
Caso os métodos CRUD herdados não sejam suficientes, declare métodos estáticos ou dinâmicos que manipulem as transações manualmente.
```php
    public static function getBetween($request)
    {
        TTransaction::open(self::DATABASE); // Utiliza a conexão do banco configurada
        $response = array();
        
        // Exemplo de busca personalizada por intervalo
        $all = Contact::where('id', '>=', $request['from'])
                      ->where('id', '<=', $request['to'])
                      ->load();
                      
        foreach ($all as $contact)
        {
            $response[] = $contact->toArray();
        }
        
        TTransaction::close(); // SEMPRE feche a transação após o uso
        return $response;
    }
```

---

## 🔗 Configuração de Rotas (.htaccess)

Para expor o serviço como RESTful, adicione as regras de regravação no arquivo [.htaccess](../../.htaccess) da raiz. Substitua `contacts` pelo nome do recurso em minúsculas e `ContactRestService` pelo nome da classe de serviço:

```apache
# RESTFUL routes
RewriteRule ^contacts/([A-Za-z0-9]*)$ rest.php?class=ContactRestService&method=handle&id=$1&%{QUERY_STRING} [NC]
RewriteRule ^contacts/([A-Za-z-_0-9]*)/([A-Za-z-_0-9]*)$ rest.php?class=ContactRestService&method=$2&id=$1&%{QUERY_STRING} [NC]
RewriteRule ^contacts$ rest.php?class=ContactRestService&method=handle&%{QUERY_STRING} [NC]
```

---

## 🛡️ Camada de Segurança e Autenticação

O Adianti Framework fornece três formas principais de validação em serviços usando `rest-secure.php` (renomeado para `rest.php`):

### 1. Autorização Global (Basic Auth)
Configura-se uma chave global `rest_key` no arquivo de preferências gerais:
No arquivo `app/config/application.php`:
```php
return [
    'general' => [
        // Outros parâmetros...
        'rest_key' => 'sua_chave_global_aqui',
    ]
];
```
O consumo do serviço exigirá o cabeçalho HTTP:
`Authorization: Basic sua_chave_global_aqui`

### 2. Autorização por Classe (REST_KEY)
A partir da versão 8+, você pode isolar o acesso definindo uma constante `REST_KEY` dentro do Service correspondente (conforme visto na seção anterior). O consumo segue exigindo `Authorization: Basic sua_chave_da_classe`.

### 3. Autenticação Baseada em Token JWT
Ideal quando é necessário identificar o usuário logado para auditoria e logs (`TSession::getValue('login')`).

#### Configuração Pré-requisito
No arquivo `app/config/application.php`, defina uma `seed` de criptografia forte:
```php
return [
    'general' => [
        // Outros parâmetros...
        'rest_key' => 'sua_chave_global_aqui',
        'seed' => 'sdf76oasdif7a_sua_semente_aqui'
    ]
];
```

#### Rota de Autenticação no `.htaccess`
Adicione a rota para captura e geração de token no [.htaccess](../../.htaccess):
```apache
RewriteRule ^auth/([A-Za-z0-9]*)/([A-Za-z0-9]*)$ rest.php?class=ApplicationAuthenticationRestService&method=getToken&login=$1&password=$2&%{QUERY_STRING} [NC]
```

---

## 📲 Exemplos de Consumo da API

Abaixo, veja como realizar as requisições de consumo tanto de forma simples (Basic) quanto segura com JWT.

### Obtenção de Token e Consumo RESTful Seguro (JWT)

````carousel
```php
// Consumo em PHP (usando cURL ou função nativa request.php)
require_once 'request.php';

try {
    // 1. Solicita o Token JWT usando Basic Auth (Credenciais do Usuário)
    $location = 'http://localhost/contacts/auth/admin/admin';
    $token = request($location, 'GET', [], 'Basic 123'); // "123" é a rest_key global
    
    // 2. Consome o recurso RESTful passando o Token JWT como Bearer
    $location = 'http://localhost/contacts/contacts/1';
    $response = request($location, 'GET', [], 'Bearer ' . $token);
    
    print_r($response);
} catch (Exception $e) {
    echo 'Erro: ' . $e->getMessage();
}
```
<!-- slide -->
```javascript
// Consumo em Javascript/jQuery
// 1. Obtenção do Token JWT
$.ajax({
    type: 'GET',
    url: 'http://localhost/contacts/auth/admin/admin',
    headers: {
        'Authorization': 'Basic 123' // Chave Global rest_key
    },
    success: function(token) {
        // 2. Consumo com o Token recebido
        $.ajax({
            type: 'GET',
            url: 'http://localhost/contacts/contacts/1',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            success: function(response) {
                console.log('Dados do Contato:', response.data);
            }
        });
    }
});
```
<!-- slide -->
```bash
# Consumo via Terminal/cURL (Shell)
# 1. Geração do Token
token=$(curl -s -H 'Authorization: Basic 123' http://localhost/contacts/auth/admin/admin)

# 2. Chamada RESTful Bearer
curl -i -X GET \
  -H "Authorization: Bearer $token" \
  https://localhost/contacts/contacts/1
```
````

---

## 🏁 Checklist de Conclusão para o Agente

- [ ] O arquivo do servidor foi configurado? (`rest-secure.php.dist` -> `rest.php`)
- [ ] A chave `rest_key` e a `seed` de geração foram configuradas em `app/config/application.php`?
- [ ] A nova classe herdada de `AdiantiRecordService` foi criada dentro de `app/service/`?
- [ ] Foram definidas as constantes obrigatórias `DATABASE` e `ACTIVE_RECORD`?
- [ ] As 3 rotas do recurso foram mapeadas no arquivo `.htaccess`?
- [ ] Em caso de transação em métodos próprios, o bloco `TTransaction::open()` e `TTransaction::close()` foi devidamente encapsulado?
- [ ] O cabeçalho adequado (`Basic` ou `Bearer`) é enviado nos testes de integração?
