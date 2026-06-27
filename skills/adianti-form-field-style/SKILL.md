---
name: adianti-form-field-style
description: >
  Padroniza o estilo de código na criação de campos de formulário no Adianti Framework.
  Define dois padrões de organização: FormDin (Padrão/Default) e Adianti (Sob demanda).
---

# Skill: Estilo de Código para Campos de Formulário (Adianti)

Esta skill define o padrão de escrita e organização de código para a instanciação e configuração de campos de formulários (`TEntry`, `TCombo`, `TDate`, etc.) em classes `Form.php` e filtros de `List.php`.

Existem dois padrões aceitos neste projeto: **Padrão FormDin** e **Padrão Adianti**.

---

## 1. Padrão FormDin (🏆 PADRÃO / DEFAULT)

Se o usuário não especificar qual padrão utilizar, **utilize sempre o Padrão FormDin**.

Neste padrão, todas as chamadas de métodos que configuram um campo **devem ficar imediatamente abaixo de sua instanciação**. Cada campo deve ser um bloco lógico contínuo. Separe blocos de campos diferentes com uma linha em branco.

### ✅ O que FAZER no Padrão FormDin
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

### 🔧 Ordem Sugerida de Configurações (FormDin)
Para manter a consistência, ao configurar um campo, siga preferencialmente a ordem abaixo:
1. Instanciação (`new TEntry(...)`, `new TCombo(...)`)
2. Adição de Itens (para `TCombo`, `TRadioGroup`, etc. usando `addItems`)
3. Validações (`addValidation`)
4. Ícones (`setInnerIcon`)
5. Máscaras e Formatações (`setMask`, `setNumericMask`, `setDatabaseMask`)
6. Limites de Caracteres (`setMaxLength`)
7. Tamanho do Componente (`setSize`)
8. Eventos e Ações (`setChangeAction`, `setExitAction`, `enableSearch`, `setEditable`)

---

## 2. Padrão Adianti (⚠️ APENAS SOB DEMANDA EXPLÍCITA)

Este padrão só deve ser utilizado **se o usuário solicitar explicitamente** ("Crie no padrão Adianti", por exemplo).

Neste formato, a instanciação de todos os campos ocorre primeiro. Em seguida, os métodos de configuração são agrupados por tipo de configuração (todas as validações juntas, todos os max lengths juntos, todos os tamanhos juntos, etc).

### ✅ O que FAZER no Padrão Adianti
Agrupe as operações por tipo de configuração:

```php
        $id = new TEntry('id');
        $nome = new TEntry('nome');
        $sigla = new TEntry('sigla');
        $codigo_ibge = new TEntry('codigo_ibge');

        $nome->addValidation("Nome", new TRequiredValidator()); 
        $sigla->addValidation("Sigla", new TRequiredValidator()); 
        $codigo_ibge->addValidation("Código IBGE", new TRequiredValidator()); 

        $id->setEditable(false);
        $sigla->setMaxLength(2);
        $nome->setMaxLength(255);
        $codigo_ibge->setMaxLength(10);

        $id->setSize(100);
        $nome->setSize('100%');
        $sigla->setSize('100%');
        $codigo_ibge->setSize('100%');
```

---

**Resumo da regra de decisão:**
- **Padrão FormDin** = Agrupamento por objeto (DEFAULT - Use sempre, a menos que avisado do contrário).
- **Padrão Adianti** = Agrupamento por tipo de configuração (SOB DEMANDA - Use apenas quando solicitado).
