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

* Endpoint *occurrences*

  * POST register new occurrence (required field: license_plate, optional fields: occurrence_type, occurrence_title, observation, location, created_at, anonymous, image )\
    ```/api/occurrences/```
    * Data response
    ```json
    {
    "Message": "Ocorrência registrada com sucesso",
    "id": 1,
    "license_plate": "abc1234",
    "occurrence_type": "batida",
    "occurrence_title": "acidente feio",
    "observation": "o cara me deu uma batida atrás",
    "anonymous": false,
    "image" : "https://img.freepik.com/fotos-gratis/gotas-de-oleo-na-imagem-abstrata-padrao-psicodelico-de-agua_23-2148290141.jpg?size=626&ext=jpg",
    "location": "maranhão novo",
    "created_at": "2020-11-12"
    }
    ```

  * GET list user occurrences (no required fields)\
    ```/api/occurrences/```
    * Data response
    ```json
    [
      {
      "id": 1,
      "license_plate": "abc1234",
      "occurrence_type": "batida",
      "occurrence_title": "acidente feio",
      "observation": "o cara me deu uma batida atrás"
      "location": "maranhão novo",
      "anonymous": false,
      "image": null,
      "created_at": "2020-11-11"
      },
      {
      "id": 2,
      "license_plate": "cas1234",
      "occurrence_type": "estacionamento indevido",
      "occurrence_title": "estacionamento",
      "location": "centro",
      "anonymous": false,
      "image" : "https://img.freepik.com/fotos-gratis/gotas-de-oleo-na-imagem-abstrata-padrao-psicodelico-de-agua_23-2148290141.jpg?size=626&ext=jpg",
      "created_at": "2020-11-12"
      }
    ]
    ```

  * GET list user selected occurrence (no required fields)\
    ```/api/occurrences/<occurrence_id>/```
    * Data response
    ```json
    {
    "id": 2,
    "license_plate": "cas1234",
    "occurrence_type": "estacionamento indevido",
    "occurrence_title": "estacionamento",
    "anonymous": false,
    "image" : "https://img.freepik.com/fotos-gratis/gotas-de-oleo-na-imagem-abstrata-padrao-psicodelico-de-agua_23-2148290141.jpg?size=626&ext=jpg",
    "location": "centro",
    "created_at": "2020-11-12"
    }
    ```

  * PUT update occurrence (no required fields. The can't update guard, user and status)\
    ```/api/occurrences/<occurrence_id>/```
    * Data response
    ```json
    {
    "id":1
	  "license_plate": "abc4321",
	  "occurrence_type": "batida feia",
	  "occurrence_title": "acidente sinistro",
	  "location": "maranhão novo",
    "anonymous": false,
    "image" : "https://img.freepik.com/fotos-gratis/gotas-de-oleo-na-imagem-abstrata-padrao-psicodelico-de-agua_23-2148290141.jpg?size=626&ext=jpg",
    "created_at": "2020-11-11"
    }

  * DELETE delete occurrence (no required fields)\
    ```/api/occurrences/<occurrence_id>/```
    * No data response
  