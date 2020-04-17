* HTML does not support DELETE or PUT for [unclear reasons][html-delete]

* Declare custom CLI commands via the ``@click.command`` decorator (see [db.py](app/db.py))

* Follow [Flask Testing] for easy ``PyTest`` unit testing incl a Client Fixture

* Different routes for html and for json [preferable] over branching by request type). Split code into
_Views_ and _Models_ following this [Flask Project Structure Guidance]. Views respond
with ``html``, Models respond with ``json`` payloads. Models act as API for both the Views and command line interfaces (CLI)

* Refactoring according to the [Flask Blog Tutorial] incl. moving
persistence from file based json to ``SQlite`` works well.


[Flask Testing]: https://flask.palletsprojects.com/en/1.1.x/testing/
[Flask Project Structure Guidance]: https://exploreflask.com/en/latest/organizing.html
[html-delete]: https://softwareengineering.stackexchange.com/a/211790 
[json-routing]: https://stackoverflow.com/questions/49631072/how-to-return-also-json-and-render-template-in-flask
[Flask Blog Tutorial]: https://flask.palletsprojects.com/en/1.1.x/tutorial/