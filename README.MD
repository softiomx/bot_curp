## Ejemplo de solicitud POST usando cURL

Puedes realizar una solicitud POST a la ruta `/download-pdf` de tu servidor Flask utilizando el siguiente comando `curl`:

```bash
curl -X POST \
  'http://127.0.0.1:5000/download-pdf' \
  --header 'Accept: */*' \
  --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "curp": ""
}'
