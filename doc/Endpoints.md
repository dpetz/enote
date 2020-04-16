
# Useful endpoints

Main page in browser:
```
http://127.0.0.1:5000/note/
```

To pretty print json with [jq](https://stedolan.github.io/jq/) via
``brew install jq`` first and then:
```
curl http://127.0.0.1:5000/note/api/list | jq .
```

You can also delete a note via a ``POST``request:
```
curl --request POST http://127.0.0.1:5000/note/api/3/delete
```
