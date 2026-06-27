---
name: adianti-form-field-style
description: >
  Padroniza o estilo de código na criação de campos de formulário no Adianti Framework.
  Garante que todas as configurações e atributos de um campo fiquem agrupados junto de sua instância.
---

# Skill: Estilo de Código para Campos de Formulário (Adianti)

Esta skill define o padrão de escrita e organização de código para a instanciação e configuração de campos de formulários (`TEntry`, `TCombo`, `TDate`, etc.) em classes `Form.php` e filtros de `List.php`.

## 📏 Regra de Ouro: Agrupamento por Objeto

Todas as chamadas de métodos que configuram um campo **devem ficar imediatamente abaixo de sua instanciação**.
Não separe a criação da variável de suas configurações (como validações, máscaras e tamanhos). Cada campo deve ser um bloco lógico contínuo. Separe blocos de campos diferentes com uma linha em branco.

### ❌ O que NÃO fazer (Incorreto)
Não defina todos os campos juntos para depois configurá-los em blocos separados.

```php
// Instanciação
$nome = new TEntry('nome');
$cpf = new TEntry('cpf');

// Configuração separada
$nome->addValidation("Nome", new TRequiredValidator()); 
$cpf->setMask('999.999.999-99');
$nome->setSize('100%');
$cpf->setSize('calc(100% - 140px)');
```

### ✅ O que FAZER (Correto)
Configure tudo relacionado ao objeto imediatamente após sua criação.

```php
$nome = new TEntry('nome');
$nome->addValidation("Nome", new TRequiredValidator());
$nome->setMaxLength(255);
$nome->setSize('100%');

$cpf = new TEntry('cpf');
$cpf->addValidation("Documento", new TRequiredValidator());
$cpf->setInnerIcon(new TImage('fas:smile #4CAF50'), 'right');
$cpf->setMask('999.999.999-99');
$cpf->setMaxLength(20);
$cpf->setSize('calc(100% - 140px)');
```

## 🔧 Ordem Sugerida de Configurações
Para manter a consistência em todo o projeto, ao configurar um campo, siga preferencialmente a ordem abaixo:
1. Instanciação (`new TEntry(...)`, `new TCombo(...)`)
2. Adição de Itens (para `TCombo`, `TRadioGroup`, etc. usando `addItems`)
3. Validações (`addValidation`)
4. Ícones (`setInnerIcon`)
5. Máscaras e Formatações (`setMask`, `setNumericMask`, `setDatabaseMask`)
6. Limites de Caracteres (`setMaxLength`)
7. Tamanho do Componente (`setSize`)
8. Eventos e Ações (`setChangeAction`, `setExitAction`, `enableSearch`, `setEditable`)
