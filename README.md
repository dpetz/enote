

Calling the ``flask`` script w/o arguments in the project folder reminds you of useful commands
```
export FLASK_APP=app
export FLASK_ENV=development
flask run
flask routes
flask init-db
```

``init-db`` is a custom command defined in ```db.py`` via the ``@click.command('init-db')`` decorator 

```
static            GET                /static/<path:filename>
v1.find           GET                /v1/find
v1.links          GET                /v1/note/<int:id>/links
v1.note           DELETE, GET        /v1/note/<int:id>
v1.notes          GET                /v1/notes
v1.toc            DELETE, GET, POST  /v1/toc
web.import_notes  GET, POST          /import
web.index         GET                /
web.note          DELETE, GET        /<int:id>
```

* [Endpoints](doc/Endpoints.md) for both a browser and a CLI
* [Insights](doc/Insights.md) for design decisions etc.
* [Todos](doc/Todos.md) such as unit tests

