# image-service
Serve to serve images

## Run app
add .env file (see .env.example)

```bash
poetry install
poetry run python run.py
```

## API
docs available on ```http://0.0.0.0:8080/docs```

### Add Image
* **POST /api/v1/images**
```curl
curl -X 'POST' \
  'http://0.0.0.0:8080/api/v1/images' \
  -F 'file=@file.png;type=image/png'
```

### Get image
* **GET /api/v1/images/{image_id}**
```curl
curl -X 'GET' \
  'http://0.0.0.0:8080/api/v1/images/bc1794c9-2be2-4d46-98ef-fa6841f0b337' \
   -o file.jpg
```

### Get resized image
* **GET /api/v1/images/{width}x{height}/{image_id}**
```curl
curl -X 'GET' \
  'http://0.0.0.0:8080/api/v1/images/500x500/bc1794c9-2be2-4d46-98ef-fa6841f0b337' \
   -o file.jpg
```
