# Wayne Enterprises Security System

Um sistema web de gerenciamento de inventário e controle de acesso desenvolvido para as Indústrias Wayne, permitindo o controle estratégico de equipamentos, armaduras, veículos e dispositivos de segurança. 
---
## Funcionalidades

* Autenticação Dinâmica:** Identificação automática do perfil e exibição do nome completo formatado.
* Gestão de Recursos (CRUD):** Cadastro, edição e acompanhamento de status de equipamentos Wayne Tech.
* Controle de Permissões em Tempo Real:** Ocultação e bloqueio de botões (Adicionar/Excluir) de acordo com o perfil logado.
* Persistência de Dados Local:** Utilização de `localStorage` para salvar o estado do inventário e das sessões ativas.
* Interface Temática:** Background e estilização visual ajustados dinamicamente para cada perfil.

---
## Tecnologias Utilizadas

* HTML5:** Estrutura semântica e acessível.
* CSS3:** Layouts em Flexbox, Grid e variáveis visuais com tema Dark/Wayne Enterprises.
* JavaScript (ES6+):** Manipulação de DOM, regras de negócios e gerenciamento de armazenamento local.
* Git & GitHub:** Controle de versão e hospedagem de código fonte.
* Vercel & Render:** Plataformas de hospedagem e deploy contínuo.

---

## Controle de Acesso (RBAC)

O sistema possui 3 níveis de acesso pré-cadastrados:

| Usuário               | E-mail            | Senha       | Perfil         | Permissões                                         |
| :---                  | :---              | :---        | :---           | :---                                               |
| **Bruce Wayne**       | `bruce@wayne.com` | `batman123` | **Admin**      | Acesso total: Visualizar, Criar e Excluir recursos |
| **Lucius Fox**        | `fox@wayne.com`   | `tech123`   | **Gerente**    | Visualizar e Criar novos recursos                  |
| **Alfred Pennyworth** | `alfred@wayne.com`| `tea123`    | **Funcionário**| Apenas visualização de recursos                    |

---
