# curso_backend_py_fastapi
Aprende todo lo que necesitas saber para crear APIs de forma rápida con FastAPI, en Python.

# El curso esta orientado a creacion de APIs de manera rapida utilizando Fastapi
Fastapi utiliza pydantic(para validacion de datos), swagger(para docuemntacion), *instale scalar(```pip install scalar-fastapi```) que es similar pero mejor*, y ademas utiliza de manera nativa asyncronia(asynco).  


### Primeros comandos

```uvirorn main:app --reload``` Este comando nos ayuda a crear un endpoint local con "--reload" que es un flag que nos ayuda a ver cambios en tiempo real. con "--port 4000" nos ayuda a elegir el port donde va a estar nuestro endpoint

### Metodos HTTP
1. POST: crear un recurso nuevo
2. PUT: modificar un recurso existente
3. GET: consultar informacion de un recurso
4. DELETE: eliminar un recurso

### Query parameters

Es un conjunto de parametros opcionales los cuales son añadidos al final la ruta con el objetivo de definir objetivos en la URL
Ponemos el ? para definir valores y & para concatenar varios parametros
Por ejemplo => http://127.0.0.1:4000/movies/?category=crimen

### Pydantic

Es una libreria para Validacion de datos y se utiliza en conjunto con fastapi. La estructura y tipo de datos y se pueden hacer validaciones automaticas.
Se puede hacer declarativo y basado en modelos. Podemos crear clases de python que actuan como modelo para validacion de nuestros datos. Podemos manipular datos y nos ayuda a hacer el cambio y las validaciones y tambien nos genera la documentacion automatica como fastapi


### JWT(JSON Web Token)

Header + Payload + Signature(header, payload, secret Key)
pip install pyjwt  

### SQLAlchemy
pip install sqlalchemy  
