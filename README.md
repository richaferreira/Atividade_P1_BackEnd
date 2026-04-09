# Aplicação Backend Acadêmica (CRUD) - FastAPI & MongoDB

Esta é uma aplicação backend acadêmica humanizada, desenvolvida com **FastAPI** e **MongoDB**, projetada para ser executada em um ambiente containerizado com **Docker**.

## 🚀 Tecnologias Utilizadas

- **FastAPI**: Framework moderno e de alto desempenho para construir APIs com Python.
- **MongoDB**: Banco de dados NoSQL orientado a documentos para armazenamento flexível.
- **Docker & Docker Compose**: Para containerização e orquestração da aplicação e do banco de dados.
- **Motor & umongo**: Driver assíncrono e ODM (Object Document Mapper) para MongoDB.

## 📋 Funcionalidades (CRUD de Livros)

O sistema gerencia um catálogo de livros acadêmicos com os seguintes atributos:
1. **Título**: O nome da obra acadêmica.
2. **Autor**: O autor ou pesquisador responsável.
3. **Ano de Publicação**: O ano em que a obra foi publicada.
4. **Gênero**: A categoria ou área de estudo do livro.

### Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/livros/` | Cria um novo livro acadêmico. |
| GET | `/livros/` | Lista todos os livros cadastrados. |
| GET | `/livros/{id}` | Obtém detalhes de um livro específico pelo ID. |
| PUT | `/livros/{id}` | Atualiza as informações de um livro existente. |
| DELETE | `/livros/{id}` | Remove um livro do catálogo. |

## 🛠️ Como Executar o Projeto

### Pré-requisitos
- Docker e Docker Compose instalados em sua máquina.

### Passos para Execução
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/academic-crud-app.git
   cd academic-crud-app
   ```

2. Execute o Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Acesse a documentação interativa da API (Swagger UI):
   - [http://localhost:8000/docs](http://localhost:8000/docs)

## 🐳 Estrutura do Docker

O projeto utiliza dois serviços principais:
- **app**: O container da aplicação FastAPI, rodando na porta 8000.
- **mongodb**: O container do banco de dados MongoDB, rodando na porta 27017.

---
Desenvolvido com foco em simplicidade e boas práticas acadêmicas.
