# sysfiles
SysFiles

Existe uma estrutura base que vamos seguir para a construção de nossas aplicações em Flask: 

## 1. Virtual Environment

Vamos usar o esquema de [virtual environment](https://docs.python.org/3/library/venv.html)

```bash
python3 -m venv venv
```

Mais detalhes em [python venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)

### 1.1 Para ativar o venv (Linux e MacOS)

```bash
source venv/bin/activate
```

### 1.2 Para desativar o venv 

```bash
deactivate
```

## 2. Uma vez criado e ativado o venv precisamos instalar os módulos, pacotes e bibliotecas usadas pela aplicação

```bash
pip3 install -r requirements.txt
```

## 3. É preciso configurar as variáveis de ambiente da aplicação

```bash
export FLASK_APP=run.py && export FLASK_ENV=development
```

## 4. Para executar a aplicação principal

```bash
flask run --host=0.0.0.0 --port=5000
```

## 5. Segue a estrutura base dos diretorios no projeto da aplicacao myapp

*requirements.txt* - arquivo que contem os módulos, pacotes e bibliotecas que serão usados pela aplicação

*run.py* - script principal que carrega o banco de dados (db) e executa a aplicação principal (app)

*docs* - diretório que guarda a documentação do projeto como arquitetura, design, requisitos e demais documentos de apoio como esquemas de UI ou fluxos BPMN

*myapp* - diretorio que contem os módulos de implementação do projeto, a pasta static e a pasta template.

*myapp/__init__.py* - script principal que instancia e configura a aplicação (app). Também importa os demais módulos da aplicação.

*myapp/static* - guarda arquivos estáticos como css, javascripts e resources (imagens e demais arquivos públicos)

*myapp/templates* - templates (views) da aplicação

*myapp/templates/authenticate* - templates (views) .html da autenticação dos usuários (login, register, password recovery)

*myapp/templates/base.html* - view base dos templates

*myapp/authentication.py* - módulo de autenticação dos usuários da aplicação.

*myapp/dao.py* - definição das classes de manipulação do ORM (Object–relational mapping) para manipular o banco de dados.

*myapp/errors.py* - módulo que manipula as páginas de erros (4xx - client errors, 5xx - server errors) http (HTTP status codes) da aplicação

*myapp/forms.py* - módulo que define os formulários e suas validações

*myapp/main.py* - módulo principal que manipula as rotas de acesso geral da aplicação

*myapp/users.py* - módulo que manipula as rotas dos usuários que acessam a aplicação

*myapp/uploads.py* - módulo que manipula as rotas de uploads de arquivos

*myapp/utils.py* - módulo de utilidades genéricas da aplicação

## 6. Executar no Heroku

Acesse sua conta do Heroku via terminal
```bash
heroku login
```

Baixe a versão inicial disponível em [v.1.0.0](https://github.com/myplayareas/sysfiles/archive/refs/tags/v1.0.0.zip)

Descompacte em sysfiles
```bash
cd sysfiles
```

Inicialize o repositorio git
```bash
git init
```

Crie o arquivo bash de configuração (config.sh) da aplicação
```bash
#!/bin/sh
export FLASK_APP=run.py && export FLASK_ENV=development
```

Atribua a permissão de execução ao arquivo de configuração
```bash
chmod u+x config.sh
```

Crie o arquivo (Procfile) de deploy e execução da release 
```bash
release: bash config.sh
web: gunicorn run:app
```

Adicione todo o conteúdo da pasta sysfiles no repositório git
```bash
git add .
```

Faça o commit de todo o conteúdo 
```bash
git commit -m "make it better"
```

Crie o aplicativo sysfiles no Heroku usando o comando heroku apps: create [app name]
```bash
heroku apps:create sysfiles
```

Suba as modificações locais para o git do Heroku
```bash
git push heroku master
```

Caso o deploy aconteça com sucesso a aplicação estará disponível em [http://sysfiles.herokuapp.com](http://sysfiles.herokuapp.com)
