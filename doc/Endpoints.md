To open in browser just call the port, typically ``http://127.0.0.1:5000/``

The remainder of this page shows how to use the RESTful API endpoints
from a command line interface (CLI).

Endpoints API Version ``V1``

List all notes:
```
curl http://127.0.0.1:5000/v1/notes | jq .
```

[jq][jq] can be installed via ``brew install jq``

Delete note by ID:
```
curl --request POST http://127.0.0.1:5000/note/api/3/delete
```

The API is app specific and assigned during import.

## Viewing and Finding Notes

Fetch by ``id``:

```
curl http://127.0.0.1:5000/v1/note/212
```

Find by guid:
```
curl http://127.0.0.1:5000/note/api/find?guid=634581d4-1c57-4299-9b7b-ad34b46c641c | jq .

```
Or by [pattern matching][like] the title:
```
curl http://127.0.0.1:5000/v1/find?title=%25Learning | jq
```

... or the content:
```
curl http://127.0.0.1:5000/v1/find?content=%25Learning%25 | jq '. | length'
```

## Table of Contents

Import a [Table of Content][toc] file from ``[PROJECT_FOLDER]/import/toc.enex``:
```
curl -d file=import/zelda_toc%2Eenex http://127.0.0.1:5000/v1/toc
```
Remember encode [URL special characters][url-encode] like above.

Get all ToC elements:
```
curl http://127.0.0.1:5000/v1/toc | jq '. | length'
```

Wipe out the ToC with delete:
```
curl -X DELETE http://127.0.0.1:5000/v1/toc
```

## Import Notes

Import notes from an ``.enex`` file:
```
curl -X POST http://127.0.0.1:5000/v1/notes/?path=import/Samples_3.enex
```

## Analytics

Extract Links:

Append ``links`` to the URL for viewing:

```
curl http://127.0.0.1:5000/v1/note/212/links
```

[jq]: https://stedolan.github.io/jq/
[toc]: https://help.evernote.com/hc/en-us/articles/209005667-How-to-create-a-table-of-contents-with-links-to-other-notes
[url-encode]: https://secure.n-able.com/webhelp/NC_9-1-0_SO_en/Content/SA_docs/API_Level_Integration/API_Integration_URLEncoding.html
[like]: https://www.sqlitetutorial.net/sqlite-like/