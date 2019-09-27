curl -X POST \
  http://localhost:5000/predict \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 0769c3a7-67a9-4427-a649-5f4c588f856d' \
  -H 'cache-control: no-cache' \
  -d '{
"input_number1": 10,
"input_number2": 5
}'
