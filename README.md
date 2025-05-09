<h1 align=center> 🏀 Sport Hub API </h1>

Este projeto é uma API RESTful desenvolvida com Django, projetada para gerenciar informações relacionadas a um clube esportivo fictício que disponibiliza espaços para atividades de seus associados.


## 🎯 Funcionalidades
- Cadastro e autenticação de usuários.

- Gerenciamento de quadras esportivas.

- Agendamento e gerenciamento de reservas.

## 🛡️ Autenticação
A autenticação é feita via JWT. Para acessar rotas protegidas, envie o token no header:
  ```
  Authorization: Bearer {token}
```

## 🚀 Como Executar
1. Crie e ative um ambiente virtual:​
   ```
   python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```
2. Instale as dependências:​
    ```
    pip install -r requirements.txt
    ```
3. Configure as variáveis de ambiente no arquivo .env.
