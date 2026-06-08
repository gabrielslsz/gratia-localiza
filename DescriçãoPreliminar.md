# Sistema de Atendimento - Gratia Localiza

Este projeto é um sistema de atendimento desenvolvido para gerenciar solicitações entre clientes, atendentes e administradores.

## Arquitetura

O sistema segue o padrão MVC (Model-View-Controller) adaptado para o ecossistema Flask:
- Models: Utiliza SQLAlchemy para mapeamento objeto-relacional com SQLite.
- Views (Templates): Renderizadas com Jinja2 e estilizadas com Bootstrap 5.
- Controllers (Routes): Organizados via Flask Blueprints para separar as responsabilidades de Clientes, Atendentes e Administradores.

## Plataforma Tecnológica

- Linguagem: Python 3.12+
- Framework Web: Flask
- Motor de Template: Jinja 2
- Frontend: Bootstrap 5 (via CDN ou local)
- Banco de Dados: SQLite (para desenvolvimento e simplicidade)
- Containerização: Docker & Docker Compose
- Controle de Versão: Git/GitHub

## Estrutura de Diretórios

```text
gratia-localiza/
├── app/
│   ├── __init__.py          # Factory do Flask e configuração
│   ├── models.py            # Definição das tabelas (User, Ticket, Comment)
│   ├── routes/              # Blueprints por perfil
│   │   ├── auth.py          # Login, Logout e Autocadastro
│   │   ├── customer.py      # Painel do Cliente (Enviar/Consultar)
│   │   ├── attendant.py     # Painel do Atendente (Responder)
│   │   └── admin.py         # Painel do Admin (CRUD Atendentes, Relatórios)
│   ├── templates/           # Arquivos HTML (Jinja2)
│   ├── static/              # CSS, JS e Imagens
│   └── utils/               # Decorators de permissão e auxiliares
├── migrations/              # Controle de versões do banco (Flask-Migrate)
├── tests/                   # Testes unitários e de integração
├── .env.example             # Modelo de variáveis de ambiente
├── Dockerfile               # Configuração da imagem Docker
├── docker-compose.yml       # Orquestração dos serviços
├── requirements.txt         # Dependências do projeto
├── GEMINI.md                # Instruções técnicas (esta documentação)
└── README.md                # Visão geral do projeto
```

## Convenções

- Nomenclatura:
  - Variáveis e funções: snake_case
  - Classes: PascalCase
  - Arquivos: snake_case.py
- Commits: Seguir o padrão Conventional Commits.
- Idioma: Código e documentação técnica em Português.

## Serviços

- Web App: O core do sistema rodando Flask.
- Banco de Dados: SQLite persistido em volume Docker.
- Proxy/Servidor WSGI: Gunicorn (para produção dentro do Docker).

## Variáveis de Ambiente

As seguintes variáveis devem ser definidas no arquivo .env:

```bash
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_aqui
DATABASE_URL=sqlite:///atendimento.db
ADMIN_INITIAL_EMAIL=admin@sistema.com
ADMIN_INITIAL_PASSWORD=admin_root
```

## Definição de Usuários

1. Cliente:
   - Funcionalidade: Autocadastro via formulário público.
   - Permissões: Enviar novas solicitações e consultar suas próprias solicitações.
2. Atendente:
   - Funcionalidade: Cadastrado exclusivamente por um Administrador.
   - Permissões: Visualizar solicitações pendentes e respondê-las.
3. Administrador:
   - Funcionalidade: Existe um administrador inicial configurado via variáveis de ambiente/seed.
   - Permissões: CRUD completo de Atendentes e acesso a relatórios gerenciais (estatísticas de atendimento).

---
*Este documento serve como a fonte da verdade para a arquitetura e padrões do projeto.*
