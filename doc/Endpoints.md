Browser entry page:
```
http://127.0.0.1:5000/note/web/list
```

The reminder of this page describes the RESTful API endpoints
for a command line interface (CLI).

List all notes:
```
curl http://127.0.0.1:5000/note/api/list | jq .
```

[jq][jq] can be installed via ``brew install jq``

Delete note with ID 3:
```
curl --request POST http://127.0.0.1:5000/note/api/3/delete
```


Find a note by guid:
```
curl http://127.0.0.1:5000/note/api/find?guid=634581d4-1c57-4299-9b7b-ad34b46c641c | jq .

```

## Table of Conents

Import a [Table of Content][toc] file from ``[PROJECT_FOLDER]/import/toc.enex`:
```
curl -d file=import%2Ftoc%2Eenex http://127.0.0.1:5000/note/api/toc
```
Remember encode [URL special characters][url-encode] like above.

To wipe out the table post w/o data:
```
curl -X POST http://127.0.0.1:5000/note/api/toc
```

Get all elements:
```
curl http://127.0.0.1:5000/note/api/toc | jq '. | length'```
```

[jq]: https://stedolan.github.io/jq/
[toc]: https://help.evernote.com/hc/en-us/articles/209005667-How-to-create-a-table-of-contents-with-links-to-other-notes
[url-encode]: https://secure.n-able.com/webhelp/NC_9-1-0_SO_en/Content/SA_docs/API_Level_Integration/API_Integration_URLEncoding.html