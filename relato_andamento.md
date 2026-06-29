# Relatório de Andamento do Trabalho — Gratia Localiza

Este documento apresenta o estado atual do desenvolvimento do **Sistema de Atendimento Gratia Localiza**, detalhando as escolhas de stack tecnológica, a preparação do ambiente, a inicialização do projeto e as dificuldades encontradas durante o processo.

---

## 1. Plataforma Tecnológica Utilizada

A arquitetura do sistema foi desenvolvida utilizando o padrão MVC (Model-View-Controller) adaptado ao ecossistema do Flask:

* **Linguagem & Framework**: Python 3.12+ com o microframework Flask.
* **Mapeamento Objeto-Relacional (ORM)**: SQLAlchemy por meio da extensão Flask-SQLAlchemy.
* **Autenticação e Sessões**: Flask-Login.
* **Controle de Banco**: Flask-Migrate (Alembic) para gerenciar o versionamento e migrações do banco de dados.
* **Banco de Dados**: SQLite para o desenvolvimento local (com arquivo persistido em [instance/atendimento.db](file:///home/gabriel-sousa/Documentos/gratia-localiza/instance/atendimento.db)).
* **Frontend**: Templates HTML integrados com Jinja2, utilizando Bootstrap 5 para responsividade e estilos personalizados declarados em [app/static/style.css](file:///home/gabriel-sousa/Documentos/gratia-localiza/app/static/style.css).
* **WSGI / Produção**: Gunicorn (especificado no [Procfile](file:///home/gabriel-sousa/Documentos/gratia-localiza/Procfile) para a execução em produção).
* **Containerização**: Docker e Docker Compose através do [Dockerfile](file:///home/gabriel-sousa/Documentos/gratia-localiza/Dockerfile) e do [docker-compose.yml](file:///home/gabriel-sousa/Documentos/gratia-localiza/docker-compose.yml).

---

## 2. Instalação do Ambiente de Desenvolvimento

* **Status**: Concluído com sucesso.
* Foi criado um ambiente virtual Python isolado (`.venv`) no diretório raiz do projeto.
* Todas as dependências declaradas em [requirements.txt](file:///home/gabriel-sousa/Documentos/gratia-localiza/requirements.txt) foram instaladas com êxito. 
* O ambiente foi testado e validado importando com sucesso os pacotes essenciais (`flask`, `flask_sqlalchemy`, `flask_login`, `flask_migrate`).

---

## 3. Inicialização do Projeto

* **Status**: Concluído com sucesso.
* A fábrica da aplicação ([app/__init__.py](file:///home/gabriel-sousa/Documentos/gratia-localiza/app/__init__.py)) foi estruturada para inicializar extensões e registrar os Blueprints que gerenciam cada perfil de usuário:
  - **Autenticação**: [app/routes/auth.py](file:///home/gabriel-sousa/Documentos/gratia-localiza/app/routes/auth.py) (login, logout e cadastro público de clientes).
  - **Cliente**: [app/routes/customer.py](file:///home/gabriel-sousa/Documentos/gratia-localiza/app/routes/customer.py) (abertura e acompanhamento de chamados).
  - **Atendente**: [app/routes/attendant.py](file:///home/gabriel-sousa/Documentos/gratia-localiza/app/routes/attendant.py) (visualização e respostas a chamados).
  - **Administrador**: [app/routes/admin.py](file:///home/gabriel-sousa/Documentos/gratia-localiza/app/routes/admin.py) (CRUD de atendentes e relatórios gerenciais).
* Os modelos de dados ([User](file:///home/gabriel-sousa/Documentos/gratia-localiza/app/models.py#L6), [Ticket](file:///home/gabriel-sousa/Documentos/gratia-localiza/app/models.py#L28) e [Comment](file:///home/gabriel-sousa/Documentos/gratia-localiza/app/models.py#L43)) foram criados no banco local através de `db.create_all()` executado automaticamente no contexto da aplicação.
* O sistema cria de forma automática o usuário administrador padrão (`admin@sistema.com`) no primeiro início da aplicação.

---

## 4. Dificuldades Encontradas

* **Reorganização Estrutural do Repositório**: Inicialmente o código fonte ficava isolado em uma subpasta `/backend`. Para simplificar os processos de deploy e orquestração do Docker, a estrutura foi movida para a raiz do repositório, o que demandou ajustes nas importações do Python e nos arquivos do Docker.
* **Ausência Física de Arquivos de Testes**: Embora o plano de testes detalhado (TDD First) esteja consolidado em [testing.md](file:///home/gabriel-sousa/Documentos/gratia-localiza/testing.md), a pasta `/tests` com as implementações de teste do pytest ainda precisa ser fisicamente gerada no projeto. Esta será a próxima tarefa de desenvolvimento.
* **Ajuste de Variáveis de Ambiente**: Sincronizar corretamente os segredos do `.env` local com as especificações exigidas na hora de rodar a imagem com Docker e preparar para o ambiente de staging.
