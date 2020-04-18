* Run ``--with-threads`` to requests model endpoints from view endpoints

* In HTML [delete via POST] as there is [no Delete in HTML]

* Of the different [Strategies of API Versioning] I pick the simplest and insert ``v1`` in my API endpoint URLs.

* Declare custom CLI commands via the ``@click.command`` decorator (see [db.py](app/db.py))

* Follow [Flask Testing] for easy ``PyTest`` unit testing incl a Client Fixture

* Different routes for html and for json [preferable] over branching by request type). Split code into
_Views_ and _Models_ following this [Flask Project Structure Guidance]. Views respond
with ``html``, Models respond with ``json`` payloads. Models act as API for both the Views and command line interfaces (CLI)

* Refactoring according to the [Flask Blog Tutorial] incl. moving
persistence from file based json to ``SQlite`` works well.


[delete via POST]: https://dev.to/moz5691/method-override-for-put-and-delete-in-html-3fp2
[Strategies of API Versioning]: https://www.xmatters.com/blog/devops/blog-four-rest-api-versioning-strategies/
[Flask Testing]: https://flask.palletsprojects.com/en/1.1.x/testing/
[Flask Project Structure Guidance]: https://exploreflask.com/en/latest/organizing.html
[no Delete in HTML]: https://softwareengineering.stackexchange.com/a/211790 
[json-routing]: https://stackoverflow.com/questions/49631072/how-to-return-also-json-and-render-template-in-flask
[Flask Blog Tutorial]: https://flask.palletsprojects.com/en/1.1.x/tutorial/