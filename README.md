# conference-python-shop-example

Ejemplo hecho con el [tutorial oficial de Flask](https://flask.palletsprojects.com/en/1.1.x/tutorial/) y la documentación de [Bootstrap 5.0](https://getbootstrap.com/docs/5.0)

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

'\xfe\xe2\xc9\x8f\x8f\nP+\x811\xc1Q\x13\x85qQ'