curl -X PUT \
  http://localhost:5000/classify \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 0769c3a7-67a9-4427-a649-5f4c588f856d' \
  -H 'cache-control: no-cache' \
  -d '{
"field1": "some-value",
"field2": "some-other-value"
}'
