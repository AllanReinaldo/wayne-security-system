# Wayne Enterprises Security System

Sistema Full Stack de gerenciamento de recursos e controle de acesso desenvolvido para as Indústrias Wayne. 
O sistema conta com autenticação segura via JWT, controle de acesso baseado em funções (RBAC), painel de 
métricas e CRUD completo de recursos.

---

## Tecnologias Utilizadas

### **Backend**
* **Python 3**
* **Flask**              (Microframework web)
* **Flask-JWT-Extended** (Autenticação via tokens JWT)
* **Flask-CORS**         (Integração segura com o Frontend)
* **Werkzeug**           (Criptografia de senhas com HASH)

### **Frontend**
* **HTML5**             (Estrutura semântica)
* **CSS3**              (Estilização em modo escuro com CSS Grid e Flexbox)
* **JavaScript (ES6+)** (Consumo da API REST via Fetch API)

---

## Controle de Acesso (RBAC)

O sistema possui 3 níveis de acesso pré-cadastrados:

| Usuário               | E-mail            | Senha       | Perfil         | Permissões                                         |
| :---                  | :---              | :---        | :---           | :---                                               |
| **Bruce Wayne**       | `bruce@wayne.com` | `batman123` | **Admin**      | Acesso total: Visualizar, Criar e Excluir recursos |
| **Lucius Fox**        | `fox@wayne.com`   | `tech123`   | **Gerente**    | Visualizar e Criar novos recursos                  |
| **Alfred Pennyworth** | `alfred@wayne.com`| `tea123`    | **Funcionário**| Apenas visualização de recursos                                                   |

---

## Como Executar o Projeto

### **1. Executando o Backend**

1. Abra o terminal na pasta `backend`:
   ```bash
   cd backend
