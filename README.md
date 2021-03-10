# conference-python-shop-example

Ejemplo hecho con el [La documentación de Flask](https://flask.palletsprojects.com/en/1.1.x/) y la documentación de [Bootstrap 5.0](https://getbootstrap.com/docs/5.0)

## Activar el ambiente (opcional)

```
$ . venv/bin/activate
```

En Windows:
```
> venv\Scripts\activate
```

## Inicializar base de datos
```
flask init-db
```

## Ejecutar aplicación modo desarrollo
Linux y Mac:
```
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run
```

Windows cmd, usar 'set' en lugar de 'export':
```
> set FLASK_APP=flaskr
> set FLASK_ENV=development
> flask run
```

## Ejecutar aplicación modo producción
```
waitress-serve --call 'flaskr:create_app'
```