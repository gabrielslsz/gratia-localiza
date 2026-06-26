## Gratia Localiza

### Acesse em:


[https://gratialocaliza.com.br](https://gratia-localiza.onrender.com/login)

### Stack

- Python
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Migrate
- Gunicorn
- Bootstrap

### Executar

```bash
git clone https://github.com/gabrielslsz/gratia-localiza.git
cd gratia-localiza

python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
gunicorn "app:create_app()"
```

Este projeto foi desenvolvido para disciplina de desenvolvimento mobile 
do curso de pós-graduação em desenvolvimento de sistemas computacionais 
do IFTO.
