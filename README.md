# **Denúncia Fácil API e Web**

Projeto utiliza [django 3.0](https://docs.djangoproject.com/pt-br/3.0/) e [django rest framework](https://www.django-rest-framework.org)

## Clonar projeto para desenvolvimento
User o comando para clonar o projeto em seu computador
```
$ git clone https://gitlab.com/tertulia/app-denuncia-facil/api-e-web.git
```
## Instalar dependências
### Ambiente virtual
Vá para o diretório do projeto
```
$ cd api-e-web
```
Para instalar o ambiente virtual use os comandos
```
$ pip install virtualenv
$ virtualenv venv -p python
```
Para ativar o ambiente virtual use o comando
- linux `source venv/bin/activate`
- windows `venv\Scripts\activate`
### Instalação das dependências
Para instalar as dependências use o comando
```
$ pip install -r environments/requirements-local.txt
```

### API

*BASE_URL* = https://api-denuncia-facil.herokuapp.com/

* Endpoint *accounts*

  * POST register new user (required fields: email, password)\
    ```/api/accounts/register/```
    * Data response
    ```json
    {
    "name": "user name",
    "email": "user@email.com",
    "cellphone": "9898989898",
    "token": "user_token"
    }
    ```
    
  * POST login user (required fields: email, password)\
    ```/api/accounts/login/```
    * Data response
    ```json
    {
    "name": "user name",
    "email": "user@email.com",
    "token": "user_token"
    }
    ```

  * PUT update user (no required fields. The user can only update 'name' and 'cellphone')\
    ```/api/accounts/updateprofile/```
    * Data response
    ```json
    {
    "name": "user name 2",
    "cellphone" : "9999999999"
    }  
