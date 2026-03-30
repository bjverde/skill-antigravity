---
name: adianti-menuxml
description: >
  Inclui novas entradas no arquivo system/menu.xml do Adianti Framework.
  Verifica se a tela já possui permissões registradas antes de adicionar ao menu.
---

# Skill: Gerador de Menu (Adianti Framework)

Esta skill é responsável por adicionar novas opções de navegação no arquivo central de interface `system/menu.xml`.

## 🛠️ Procedimento Interno para o Agente (IA)

Sempre que o usuário pedir para "adicionar ao menu":

### 1. Validação de Pré-Requisitos
Antes de editar o XML, verifique:
- Se a classe (Controller) existe.
- Se existe uma **Migration** de permissão para esta classe (conforme `adianti-migration`).
- Se não houver, avise ao usuário: *"Essa tela ainda não tem permissões no banco. Gostaria de criar a migration primeiro?"*.

### 2. Formatação do XML
O item deve ser inserido dentro do nó `<menu>` ou de um `<menugroup>` existente.

**Template de Item**:
```xml
<menuitem label="<Nome Amigável>">
    <icon>fas:chevron-right</icon>
    <action><NomeDaClasse></action>
</menuitem>
```

---

## 📐 Padrões de Interface
| Elemento | Regra | Exemplo |
| :--- | :--- | :--- |
| `label` | Use o nome amigável (Pascal Case com espaços). | "Lista de Preços" |
| `icon` | Sempre use o prefixo `fas:` (FontAwesome Solid). | `fas:barcode` |
| `action` | O nome EXATO da classe Controller. | `PrecoList` |

> [!TIP]
> **Hierarquia**: Se o usuário não especificar o grupo, procure por um grupo relacionado (ex: "Cadastros", "Relatórios") ou adicione na raiz do menu.

---
*Skill ativada por: "adicionar ao menu", "editar menu.xml", "nova entrada no menu".*
