

Refactoring from file based json data to SQlite like in the 
[Flask Blog Tutorial]
(https://flask.palletsprojects.com/en/1.1.x/tutorial/)


Design Decisions:
* [creating different routes for html and for json]
(https://stackoverflow.com/questions/49631072/how-to-return-also-json-and-render-template-in-flask
) (vs branching by request type): 


To pretty print json with [jq](https://stedolan.github.io/jq/) via
``brew install jq`` first and then:
```
curl http://127.0.0.1:5000/note/api/list | jq .
```

You can also delete a note via a ``POST``request:
```
curl --request POST http://127.0.0.1:5000/note/api/3/delete
```


[Mastering Markdown](https://guides.github.com/features/mastering-markdown/)
